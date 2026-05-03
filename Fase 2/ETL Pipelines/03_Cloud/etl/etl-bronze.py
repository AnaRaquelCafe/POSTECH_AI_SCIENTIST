import sys
import logging
import hashlib
from datetime import datetime, timezone

import requests
import pandas as pd

from awsglue.utils import getResolvedOptions
from awsglue.context import GlueContext
from awsglue.job import Job
from pyspark.context import SparkContext
from pyspark.sql import functions as F

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
#
#   --API_URL     https://jsonplaceholder.typicode.com/users
#   --ENTIDADE    users
#   --BUCKET_SOR  420411424817-data-sor

## @params: [JOB_NAME, API_URL, ENTIDADE, BUCKET_SOR]
args = getResolvedOptions(sys.argv, [
    'JOB_NAME',
    'API_URL',
    'ENTIDADE',
    'BUCKET_SOR',
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
API_URL        = args['API_URL']
ENTIDADE       = args['ENTIDADE']
BUCKET_SOR     = args['BUCKET_SOR']
INGESTION_TS   = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
INGESTION_DATE = datetime.now(timezone.utc).strftime("%Y-%m-%d")
ano, mes, dia  = INGESTION_DATE.split("-")

log.info("=" * 60)
log.info(f"JOB       : {JOB_NAME}")
log.info(f"ENTIDADE  : {ENTIDADE}")
log.info(f"FONTE     : {API_URL}")
log.info(f"DATA      : {INGESTION_DATE}")
log.info(f"CAMADA    : BRONZE -> s3://{BUCKET_SOR}/bronze/{ENTIDADE}")
log.info("=" * 60)

# ============================================================
# FUNÇÕES
# ============================================================

def ingerir_api(url):
    log.info(f"[INGESTAO] Consumindo: {url}")
    try:
        response = requests.get(url, timeout=15)
        response.raise_for_status()
        dados = response.json()
        log.info(f"[INGESTAO] {len(dados)} registros recebidos | status={response.status_code}")
        return dados
    except Exception as e:
        log.error(f"[INGESTAO] Falha: {e}")
        raise

def construir_bronze(dados):
    log.info("[BRONZE] Adicionando metadados e convertendo para Spark DataFrame")

    df_pandas = pd.json_normalize(dados)

    df_pandas["_ingestion_timestamp"] = INGESTION_TS
    df_pandas["_ingestion_date"]      = INGESTION_DATE
    df_pandas["_source_url"]          = API_URL
    df_pandas["_source_entity"]       = ENTIDADE
    df_pandas["_job_name"]            = JOB_NAME
    df_pandas["_record_hash"]         = df_pandas.drop(
        columns=[c for c in df_pandas.columns if c.startswith("_")],
        errors="ignore"
    ).apply(lambda r: hashlib.md5(str(r.values).encode()).hexdigest(), axis=1)

    return (spark
        .createDataFrame(df_pandas)
        .withColumn("ano", F.lit(ano))
        .withColumn("mes", F.lit(mes))
        .withColumn("dia", F.lit(dia))
    )

def checar_qualidade(df, checks):
    log.info(f"[DQ:BRONZE] Iniciando verificacoes | checks={len(checks)}")
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
        except Exception as e:
            ok      = False
            detalhe = f"Erro: {e}"

        status = "PASS" if ok else ("FAIL" if critico else "WARN")
        if ok:
            passou += 1
            log.info(f"[DQ:BRONZE] {status} | {tipo} | coluna={coluna} | {detalhe}")
        else:
            falhou += 1
            if critico:
                criticos += 1
                log.error(f"[DQ:BRONZE] {status} | {tipo} | coluna={coluna} | {detalhe}")
            else:
                log.warning(f"[DQ:BRONZE] {status} | {tipo} | coluna={coluna} | {detalhe}")

    score = round(passou / len(checks) * 100, 1)
    log.info(f"[DQ:BRONZE] Score={score}% | PASS={passou} FAIL={falhou}")

    if criticos > 0:
        raise Exception(f"[DQ:BRONZE] {criticos} check(s) critico(s) falharam. Job interrompido.")

def salvar_bronze(df):
    path = f"s3://{BUCKET_SOR}/bronze/{ENTIDADE}"
    log.info(f"[BRONZE] Salvando em: {path}")
    df.write.partitionBy("ano", "mes", "dia").mode("overwrite").parquet(path)
    log.info(f"[BRONZE] {df.count()} registros salvos")
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
        {"tipo": "min_count", "valor": 1,          "critico": True},
        {"tipo": "not_null",  "coluna": "id",      "critico": True},
        {"tipo": "not_null",  "coluna": "userId",  "critico": True},
    ],
    "todos": [
        {"tipo": "min_count", "valor": 1,          "critico": True},
        {"tipo": "not_null",  "coluna": "id",      "critico": True},
        {"tipo": "not_null",  "coluna": "userId",  "critico": True},
    ],
}

# ============================================================
# EXECUÇÃO
# ============================================================

dados_raw  = ingerir_api(API_URL)
df_bronze  = construir_bronze(dados_raw)

checks = CHECKS.get(ENTIDADE, [])
if checks:
    checar_qualidade(df_bronze, checks)
else:
    log.warning(f"[DQ:BRONZE] Nenhuma regra definida para '{ENTIDADE}' — pulando verificacao")

bronze_path = salvar_bronze(df_bronze)

log.info("=" * 60)
log.info("SUMARIO BRONZE")
log.info(f"  Destino : {bronze_path}/ano={ano}/mes={mes}/dia={dia}/")
log.info(f"  Proxima etapa: executar job etl-silver com BUCKET_SOR={BUCKET_SOR}")
log.info("=" * 60)

job.commit()