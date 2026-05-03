import sys
import logging
from datetime import datetime, timezone

from awsglue.utils import getResolvedOptions
from awsglue.context import GlueContext
from awsglue.job import Job
from pyspark.context import SparkContext
from pyspark.sql import functions as F
from pyspark.sql.types import IntegerType

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
#   --BUCKET_SOT  420411424817-data-sot
#   --BUCKET_SPEC 420411424817-data-spec

## @params: [JOB_NAME, ENTIDADE, BUCKET_SOT, BUCKET_SPEC]
args = getResolvedOptions(sys.argv, [
    'JOB_NAME',
    'ENTIDADE',
    'BUCKET_SOT',
    'BUCKET_SPEC',
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
BUCKET_SOT     = args['BUCKET_SOT']
BUCKET_SPEC    = args['BUCKET_SPEC']
INGESTION_DATE = datetime.now(timezone.utc).strftime("%Y-%m-%d")
ano, mes, dia  = INGESTION_DATE.split("-")

# Lê a partição do dia atual gerada pelo job Silver
SILVER_PATH = f"s3://{BUCKET_SOT}/silver/{ENTIDADE}/ano={ano}/mes={mes}/dia={dia}/"

log.info("=" * 60)
log.info(f"JOB       : {JOB_NAME}")
log.info(f"ENTIDADE  : {ENTIDADE}")
log.info(f"LENDO DE  : {SILVER_PATH}")
log.info(f"CAMADA    : GOLD -> s3://{BUCKET_SPEC}/gold/{ENTIDADE}")
log.info("=" * 60)

# ============================================================
# FUNÇÕES — AGREGAÇÕES POR ENTIDADE
# ============================================================

def gold_users(df):
    log.info("[GOLD] Gerando visao analitica: users")
    return df.select(
        "id", "name", "email", "addr_city", "company_name",
        "_ingestion_date", "_job_name"
    )

def gold_posts(df):
    log.info("[GOLD] Gerando agregacao: posts por usuario")
    return df.groupBy("user_id").agg(
        F.count("post_id").alias("total_posts"),
        F.round(F.avg("body_length"), 2).alias("avg_body_length"),
        F.round(F.avg("title_word_count"), 2).alias("avg_title_words"),
        F.first("_ingestion_date").alias("_ingestion_date"),
    )

def gold_todos(df):
    log.info("[GOLD] Gerando agregacao: todos por usuario")
    return df.groupBy("user_id").agg(
        F.count("todo_id").alias("total_tarefas"),
        F.sum(F.col("completed").cast(IntegerType())).alias("concluidas"),
        F.sum((~F.col("completed")).cast(IntegerType())).alias("pendentes"),
        F.round(
            F.sum(F.col("completed").cast(IntegerType())) / F.count("todo_id") * 100, 1
        ).alias("taxa_conclusao_pct"),
        F.first("_ingestion_date").alias("_ingestion_date"),
    )

TRANSFORMACOES = {
    "users": gold_users,
    "posts": gold_posts,
    "todos": gold_todos,
}

def construir_gold(df_silver):
    log.info("[GOLD] Iniciando transformacao")
    df      = df_silver.drop("ano", "mes", "dia")
    gold_fn = TRANSFORMACOES.get(ENTIDADE, lambda d: d)
    df      = gold_fn(df)
    return (df
        .withColumn("_gold_processed_at", F.lit(datetime.now(timezone.utc).isoformat()))
        .withColumn("ano", F.lit(ano))
        .withColumn("mes", F.lit(mes))
        .withColumn("dia", F.lit(dia))
    )

def checar_qualidade(df, checks):
    log.info(f"[DQ:GOLD] Iniciando verificacoes | checks={len(checks)}")
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
            log.info(f"[DQ:GOLD] {status} | {tipo} | coluna={coluna} | {detalhe}")
        else:
            falhou += 1
            if critico:
                criticos += 1
                log.error(f"[DQ:GOLD] {status} | {tipo} | coluna={coluna} | {detalhe}")
            else:
                log.warning(f"[DQ:GOLD] {status} | {tipo} | coluna={coluna} | {detalhe}")

    score = round(passou / len(checks) * 100, 1)
    log.info(f"[DQ:GOLD] Score={score}% | PASS={passou} FAIL={falhou}")

    if criticos > 0:
        raise Exception(f"[DQ:GOLD] {criticos} check(s) critico(s) falharam. Job interrompido.")

def salvar_gold(df):
    path = f"s3://{BUCKET_SPEC}/gold/{ENTIDADE}"
    log.info(f"[GOLD] Salvando em: {path}")
    df.write.partitionBy("ano", "mes", "dia").mode("overwrite").parquet(path)
    log.info(f"[GOLD] {df.count()} registros salvos")
    return path

# ============================================================
# REGRAS DE QUALIDADE
# ============================================================

CHECKS = {
    "users": [
        {"tipo": "min_count", "valor": 1,      "critico": True},
        {"tipo": "not_null",  "coluna": "id",   "critico": True},
        {"tipo": "not_null",  "coluna": "email","critico": True},
    ],
    "posts": [
        {"tipo": "min_count", "valor": 1,             "critico": True},
        {"tipo": "not_null",  "coluna": "user_id",    "critico": True},
        {"tipo": "range",     "coluna": "total_posts", "valor": (1, 9999), "critico": False},
    ],
    "todos": [
        {"tipo": "min_count", "valor": 1,                    "critico": True},
        {"tipo": "not_null",  "coluna": "user_id",           "critico": True},
        {"tipo": "range",     "coluna": "taxa_conclusao_pct", "valor": (0, 100), "critico": True},
    ],
}

# ============================================================
# EXECUÇÃO
# ============================================================

log.info(f"[GOLD] Lendo Silver de: {SILVER_PATH}")
df_silver = spark.read.parquet(SILVER_PATH)
log.info(f"[GOLD] {df_silver.count()} registros lidos da Silver")

df_gold   = construir_gold(df_silver)
checks    = CHECKS.get(ENTIDADE, [])
if checks:
    checar_qualidade(df_gold, checks)
else:
    log.warning(f"[DQ:GOLD] Nenhuma regra definida para '{ENTIDADE}' — pulando verificacao")

gold_path = salvar_gold(df_gold)

log.info("=" * 60)
log.info("SUMARIO GOLD")
log.info(f"  Lido de  : {SILVER_PATH}")
log.info(f"  Destino  : {gold_path}/ano={ano}/mes={mes}/dia={dia}/")
log.info(f"  Pipeline completo para entidade: {ENTIDADE}")
log.info("=" * 60)

job.commit()