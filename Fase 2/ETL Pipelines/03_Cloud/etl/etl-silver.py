import sys
import logging
from datetime import datetime, timezone

from awsglue.utils import getResolvedOptions
from awsglue.context import GlueContext
from awsglue.job import Job
from pyspark.context import SparkContext
from pyspark.sql import functions as F
from pyspark.sql.types import IntegerType, DoubleType, BooleanType

# ============================================================
# LOGGING
# ============================================================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(message)s",
    datefmt="%Y-%m-%dT%H:%M:%SZ",
)
log = logging.getLogger(__name__)

# ============================================================
# PARÂMETROS DO JOB
# ============================================================
# Job details -> Advanced properties -> Job parameters
#
#   --ENTIDADE    users
#   --BUCKET_SOR  420411424817-data-sor
#   --BUCKET_SOT  420411424817-data-sot

## @params: [JOB_NAME, ENTIDADE, BUCKET_SOR, BUCKET_SOT]
args = getResolvedOptions(sys.argv, [
    'JOB_NAME',
    'ENTIDADE',
    'BUCKET_SOR',
    'BUCKET_SOT',
])

# ============================================================
# CONTEXTO GLUE E SPARK
# ============================================================

sc          = SparkContext()
glueContext = GlueContext(sc)
spark       = glueContext.spark_session
job         = Job(glueContext)
job.init(args['JOB_NAME'], args)

spark.conf.set("spark.sql.sources.partitionOverwriteMode", "dynamic")
spark.sparkContext.setLogLevel("WARN")

# ============================================================
# VARIÁVEIS
# ============================================================

JOB_NAME       = args['JOB_NAME']
ENTIDADE       = args['ENTIDADE']
BUCKET_SOR     = args['BUCKET_SOR']
BUCKET_SOT     = args['BUCKET_SOT']
INGESTION_DATE = datetime.now(timezone.utc).strftime("%Y-%m-%d")
ano, mes, dia  = INGESTION_DATE.split("-")

# Lê a partição do dia atual gerada pelo job Bronze
BRONZE_PATH = f"s3://{BUCKET_SOR}/bronze/{ENTIDADE}/ano={ano}/mes={mes}/dia={dia}/"

log.info("=" * 60)
log.info(f"JOB       : {JOB_NAME}")
log.info(f"ENTIDADE  : {ENTIDADE}")
log.info(f"LENDO DE  : {BRONZE_PATH}")
log.info(f"CAMADA    : SILVER -> s3://{BUCKET_SOT}/silver/{ENTIDADE}")
log.info("=" * 60)

# ============================================================
# FUNÇÕES — TRANSFORMAÇÕES POR ENTIDADE
# ============================================================

def transformar_users(df):
    log.info("[SILVER] Aplicando regras: users")
    renomear = {
        "address.city":    "addr_city",
        "address.zipcode": "addr_zipcode",
        "address.geo.lat": "geo_lat",
        "address.geo.lng": "geo_lng",
        "company.name":    "company_name",
    }
    for original, novo in renomear.items():
        if original in df.columns:
            df = df.withColumnRenamed(original, novo)
    return (df
        .withColumn("id",       F.col("id").cast(IntegerType()))
        .withColumn("email",    F.trim(F.lower(F.col("email"))))
        .withColumn("username", F.trim(F.lower(F.col("username"))))
        .withColumn("name",     F.initcap(F.trim(F.col("name"))))
        .withColumn("geo_lat",  F.col("geo_lat").cast(DoubleType()))
        .withColumn("geo_lng",  F.col("geo_lng").cast(DoubleType()))
    )

def transformar_posts(df):
    log.info("[SILVER] Aplicando regras: posts")
    return (df
        .withColumnRenamed("id",     "post_id")
        .withColumnRenamed("userId", "user_id")
        .withColumn("post_id",          F.col("post_id").cast(IntegerType()))
        .withColumn("user_id",          F.col("user_id").cast(IntegerType()))
        .withColumn("title",            F.initcap(F.trim(F.col("title"))))
        .withColumn("body",             F.trim(F.regexp_replace(F.col("body"), "\n", " ")))
        .withColumn("title_word_count", F.size(F.split(F.col("title"), " ")))
        .withColumn("body_length",      F.length(F.col("body")))
    )

def transformar_todos(df):
    log.info("[SILVER] Aplicando regras: todos")
    return (df
        .withColumnRenamed("id",     "todo_id")
        .withColumnRenamed("userId", "user_id")
        .withColumn("todo_id",   F.col("todo_id").cast(IntegerType()))
        .withColumn("user_id",   F.col("user_id").cast(IntegerType()))
        .withColumn("completed", F.col("completed").cast(BooleanType()))
        .withColumn("status",    F.when(F.col("completed"), "COMPLETED").otherwise("PENDING"))
    )

TRANSFORMACOES = {
    "users": transformar_users,
    "posts": transformar_posts,
    "todos": transformar_todos,
}

def construir_silver(df_bronze):
    log.info("[SILVER] Iniciando transformacao")

    df          = df_bronze.drop("ano", "mes", "dia")
    transformar = TRANSFORMACOES.get(ENTIDADE, lambda d: d)
    df          = transformar(df)

    id_col = next((c for c in df.columns if c in ["id","post_id","todo_id","user_id"]), None)
    if id_col:
        antes = df.count()
        df    = df.dropDuplicates([id_col])
        log.info(f"[SILVER] Deduplicacao: {antes - df.count()} removidos (chave={id_col})")
    else:
        log.warning("[SILVER] Coluna de ID nao encontrada — deduplicacao ignorada")

    return (df
        .withColumn("_silver_processed_at", F.lit(datetime.now(timezone.utc).isoformat()))
        .withColumn("ano", F.lit(ano))
        .withColumn("mes", F.lit(mes))
        .withColumn("dia", F.lit(dia))
    )

def checar_qualidade(df, checks):
    log.info(f"[DQ:SILVER] Iniciando verificacoes | checks={len(checks)}")
    passou = falhou = criticos = 0

    for check in checks:
        tipo    = check["tipo"]
        coluna  = check.get("coluna")
        valor   = check.get("valor")
        critico = check.get("critico", True)
        ok      = False
        detalhe = ""

        try:
            if tipo == "not_null":
                nulos   = df.filter(F.col(coluna).isNull()).count()
                ok      = nulos == 0
                detalhe = f"{nulos} nulos encontrados"
            elif tipo == "min_count":
                contagem = df.count()
                ok       = contagem >= valor
                detalhe  = f"contagem={contagem} | minimo={valor}"
            elif tipo == "unique":
                dups    = df.count() - df.select(coluna).distinct().count()
                ok      = dups == 0
                detalhe = f"{dups} duplicatas encontradas"
            elif tipo == "regex":
                invalidos = df.filter(
                    F.col(coluna).isNotNull() & ~F.col(coluna).rlike(valor)
                ).count()
                ok      = invalidos == 0
                detalhe = f"{invalidos} com formato invalido"
            elif tipo == "range":
                mn, mx = valor
                fora   = df.filter((F.col(coluna) < mn) | (F.col(coluna) > mx)).count()
                ok      = fora == 0
                detalhe = f"{fora} fora do intervalo [{mn},{mx}]"
        except Exception as e:
            ok      = False
            detalhe = f"Erro: {e}"

        status = "PASS" if ok else ("FAIL" if critico else "WARN")
        if ok:
            passou += 1
            log.info(f"[DQ:SILVER] {status} | {tipo} | coluna={coluna} | {detalhe}")
        else:
            falhou += 1
            if critico:
                criticos += 1
                log.error(f"[DQ:SILVER] {status} | {tipo} | coluna={coluna} | {detalhe}")
            else:
                log.warning(f"[DQ:SILVER] {status} | {tipo} | coluna={coluna} | {detalhe}")

    score = round(passou / len(checks) * 100, 1)
    log.info(f"[DQ:SILVER] Score={score}% | PASS={passou} FAIL={falhou}")

    if criticos > 0:
        raise Exception(f"[DQ:SILVER] {criticos} check(s) critico(s) falharam. Job interrompido.")

def salvar_silver(df):
    path = f"s3://{BUCKET_SOT}/silver/{ENTIDADE}"
    log.info(f"[SILVER] Salvando em: {path}")
    df.write.partitionBy("ano", "mes", "dia").mode("overwrite").parquet(path)
    log.info(f"[SILVER] {df.count()} registros salvos")
    return path

# ============================================================
# REGRAS DE QUALIDADE
# ============================================================

CHECKS = {
    "users": [
        {"tipo": "min_count", "valor": 1,                                              "critico": True},
        {"tipo": "not_null",  "coluna": "id",                                          "critico": True},
        {"tipo": "not_null",  "coluna": "email",                                       "critico": True},
        {"tipo": "unique",    "coluna": "id",                                          "critico": True},
        {"tipo": "regex",     "coluna": "email", "valor": r"^[\w\.\-]+@[\w\.\-]+\.\w+$", "critico": False},
        {"tipo": "range",     "coluna": "geo_lat", "valor": (-90, 90),                 "critico": False},
        {"tipo": "range",     "coluna": "geo_lng", "valor": (-180, 180),               "critico": False},
    ],
    "posts": [
        {"tipo": "min_count", "valor": 1,              "critico": True},
        {"tipo": "not_null",  "coluna": "post_id",     "critico": True},
        {"tipo": "not_null",  "coluna": "user_id",     "critico": True},
        {"tipo": "unique",    "coluna": "post_id",     "critico": True},
        {"tipo": "range",     "coluna": "body_length", "valor": (1, 10000), "critico": False},
    ],
    "todos": [
        {"tipo": "min_count", "valor": 1,           "critico": True},
        {"tipo": "not_null",  "coluna": "todo_id",  "critico": True},
        {"tipo": "not_null",  "coluna": "user_id",  "critico": True},
        {"tipo": "unique",    "coluna": "todo_id",  "critico": True},
        {"tipo": "not_null",  "coluna": "status",   "critico": False},
    ],
}

# ============================================================
# EXECUÇÃO
# ============================================================

log.info(f"[SILVER] Lendo Bronze de: {BRONZE_PATH}")
df_bronze = spark.read.parquet(BRONZE_PATH)
log.info(f"[SILVER] {df_bronze.count()} registros lidos da Bronze")

df_silver   = construir_silver(df_bronze)
checks      = CHECKS.get(ENTIDADE, [])
if checks:
    checar_qualidade(df_silver, checks)
else:
    log.warning(f"[DQ:SILVER] Nenhuma regra definida para '{ENTIDADE}' — pulando verificacao")

silver_path = salvar_silver(df_silver)

log.info("=" * 60)
log.info("SUMARIO SILVER")
log.info(f"  Lido de  : {BRONZE_PATH}")
log.info(f"  Destino  : {silver_path}/ano={ano}/mes={mes}/dia={dia}/")
log.info(f"  Proxima etapa: executar job etl-gold com BUCKET_SOT={BUCKET_SOT}")
log.info("=" * 60)

job.commit()