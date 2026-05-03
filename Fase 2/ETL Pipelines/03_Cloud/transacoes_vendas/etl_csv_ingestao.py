import sys
import logging
from datetime import datetime, timezone

from awsglue.utils import getResolvedOptions
from awsglue.context import GlueContext
from awsglue.job import Job
from pyspark.context import SparkContext
from pyspark.sql import functions as F
from pyspark.sql.types import (
    StructType, StructField,
    StringType, IntegerType, DoubleType, TimestampType
)

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
#   --CSV_PATH      s3://420411424817-etl-csv-ingestao/input/transacoes_vendas.csv
#   --BUCKET_SOR    420411424817-etl-csv-ingestao
#   --BUCKET_SOT    420411424817-etl-csv-ingestao
#   --BUCKET_SPEC   420411424817-etl-csv-ingestao
#   --ENTIDADE      transacoes_vendas
#   --ENVIRONMENT   dev

## @params: [JOB_NAME, CSV_PATH, BUCKET_SOR, BUCKET_SOT, BUCKET_SPEC, ENTIDADE, ENVIRONMENT]
args = getResolvedOptions(sys.argv, [
    'JOB_NAME',
    'CSV_PATH',
    'BUCKET_SOR',
    'BUCKET_SOT',
    'BUCKET_SPEC',
    'ENTIDADE',
    'ENVIRONMENT',
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
CSV_PATH       = args['CSV_PATH']
BUCKET_SOR     = args['BUCKET_SOR']
BUCKET_SOT     = args['BUCKET_SOT']
BUCKET_SPEC    = args['BUCKET_SPEC']
ENTIDADE       = args['ENTIDADE']
ENVIRONMENT    = args['ENVIRONMENT']
INGESTION_TS   = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
INGESTION_DATE = datetime.now(timezone.utc).strftime("%Y-%m-%d")

# Partição no formato anomesdia (ex: 20240315)
ANOMESDIA = datetime.now(timezone.utc).strftime("%Y%m%d")

# Paths por camada
# sor  = Bronze (dado bruto com metadados)
# sot  = quarentena (registros que falharam no DQ) e pass (registros válidos pré-gold)
# spec = Gold (dado limpo e agregado para consumo)
BRONZE_PATH     = f"s3://{BUCKET_SOR}/bronze/{ENTIDADE}/anomesdia={ANOMESDIA}/"
QUARENTENA_PATH = f"s3://{BUCKET_SOT}/quarentena/{ENTIDADE}/anomesdia={ANOMESDIA}/"
PASS_PATH       = f"s3://{BUCKET_SOT}/pass/{ENTIDADE}/anomesdia={ANOMESDIA}/"
GOLD_PATH       = f"s3://{BUCKET_SPEC}/gold/{ENTIDADE}/anomesdia={ANOMESDIA}/"

log.info("=" * 65)
log.info(f"JOB         : {JOB_NAME}")
log.info(f"ENTIDADE    : {ENTIDADE}")
log.info(f"ENVIRONMENT : {ENVIRONMENT}")
log.info(f"CSV_PATH    : {CSV_PATH}")
log.info(f"ANOMESDIA   : {ANOMESDIA}")
log.info(f"BRONZE      : {BRONZE_PATH}")
log.info(f"QUARENTENA  : {QUARENTENA_PATH}")
log.info(f"PASS        : {PASS_PATH}")
log.info(f"GOLD        : {GOLD_PATH}")
log.info("=" * 65)

# ============================================================
# SCHEMA EXPLÍCITO
# ============================================================
# Definir o schema evita inferência automática do Spark,
# que pode errar tipos em CSVs com valores nulos ou mistos.

SCHEMA = StructType([
    StructField("transaction_id",  StringType(),  True),
    StructField("cliente_nome",    StringType(),  True),
    StructField("cliente_cpf",     StringType(),  True),
    StructField("cliente_email",   StringType(),  True),
    StructField("produto",         StringType(),  True),
    StructField("categoria",       StringType(),  True),
    StructField("quantidade",      IntegerType(), True),
    StructField("preco_unitario",  DoubleType(),  True),
    StructField("valor_total",     DoubleType(),  True),
    StructField("status",          StringType(),  True),
    StructField("data_transacao",  StringType(),  True),
    StructField("loja_id",         StringType(),  True),
    StructField("regiao",          StringType(),  True),
    StructField("parcelas",        IntegerType(), True),
    StructField("desconto_pct",    DoubleType(),  True),
])

# ============================================================
# ETAPA 1 — LEITURA DO CSV (SOR / BRONZE)
# ============================================================

def ler_csv(path):
    """Lê o CSV com schema explícito e retorna Spark DataFrame."""
    log.info(f"[BRONZE] Lendo CSV: {path}")
    try:
        df = spark.read \
            .option("header", "true") \
            .option("delimiter", ",") \
            .option("encoding", "UTF-8") \
            .option("mode", "PERMISSIVE") \
            .schema(SCHEMA) \
            .csv(path)

        total = df.count()
        log.info(f"[BRONZE] {total} registros lidos | colunas={len(df.columns)}")
        return df
    except Exception as e:
        log.error(f"[BRONZE] Falha ao ler CSV: {e}")
        raise

def construir_bronze(df):
    """Adiciona metadados de auditoria ao dado bruto."""
    log.info("[BRONZE] Adicionando metadados de ingestao")
    return (df
        .withColumn("_ingestion_timestamp", F.lit(INGESTION_TS))
        .withColumn("_ingestion_date",      F.lit(INGESTION_DATE))
        .withColumn("_source_path",         F.lit(CSV_PATH))
        .withColumn("_source_entity",       F.lit(ENTIDADE))
        .withColumn("_job_name",            F.lit(JOB_NAME))
        .withColumn("_environment",         F.lit(ENVIRONMENT))
        .withColumn("_record_hash", F.md5(
            F.concat_ws("|",
                F.col("transaction_id"),
                F.col("cliente_cpf"),
                F.col("data_transacao"),
            )
        ))
    )

def salvar_bronze(df):
    """Salva Bronze no bucket sor particionado por anomesdia."""
    log.info(f"[BRONZE] Salvando em: {BRONZE_PATH}")
    df.write.mode("overwrite").parquet(BRONZE_PATH)
    log.info(f"[BRONZE] {df.count()} registros salvos")

# ============================================================
# ETAPA 2 — DATA QUALITY E ROTEAMENTO (SOT)
# ============================================================
# Cada regra gera uma coluna booleana _dq_<nome>.
# Registros com qualquer falha vão para quarentena.
# Registros que passam em todos os checks vão para pass.

STATUS_VALIDOS = ["APROVADO", "PENDENTE", "CANCELADO", "PROCESSANDO"]

def aplicar_regras_dq(df):
    """
    Aplica todas as regras de DQ como colunas booleanas.
    True  = regra passou (dado OK)
    False = regra falhou (dado problemático)
    """
    log.info("[DQ] Aplicando regras de qualidade como colunas booleanas")

    return (df
        # Regra 1: transaction_id nao pode ser nulo ou vazio
        .withColumn("_dq_transaction_id_valido",
            F.col("transaction_id").isNotNull() &
            (F.trim(F.col("transaction_id")) != "")
        )
        # Regra 2: email deve ter formato válido
        .withColumn("_dq_email_valido",
            F.col("cliente_email").isNotNull() &
            F.col("cliente_email").rlike(r"^[\w\.\-]+@[\w\.\-]+\.\w+$")
        )
        # Regra 3: valor_total deve ser positivo
        .withColumn("_dq_valor_positivo",
            F.col("valor_total").isNotNull() &
            (F.col("valor_total") > 0)
        )
        # Regra 4: status deve ser um dos valores válidos
        .withColumn("_dq_status_valido",
            F.col("status").isin(STATUS_VALIDOS)
        )
        # Regra 5: quantidade deve ser maior que zero
        .withColumn("_dq_quantidade_valida",
            F.col("quantidade").isNotNull() &
            (F.col("quantidade") > 0)
        )
        # Regra 6: cliente_nome nao pode ser nulo
        .withColumn("_dq_nome_valido",
            F.col("cliente_nome").isNotNull() &
            (F.trim(F.col("cliente_nome")) != "")
        )
        # Coluna consolidada: passou em TODAS as regras
        .withColumn("_dq_passou",
            F.col("_dq_transaction_id_valido") &
            F.col("_dq_email_valido") &
            F.col("_dq_valor_positivo") &
            F.col("_dq_status_valido") &
            F.col("_dq_quantidade_valida") &
            F.col("_dq_nome_valido")
        )
    )

def logar_resultado_dq(df_com_dq):
    """Loga o resultado de cada regra e o total por destino."""
    total = df_com_dq.count()

    regras = [
        "_dq_transaction_id_valido",
        "_dq_email_valido",
        "_dq_valor_positivo",
        "_dq_status_valido",
        "_dq_quantidade_valida",
        "_dq_nome_valido",
    ]

    log.info(f"[DQ] Resultado por regra (total={total}):")
    for regra in regras:
        falhou = df_com_dq.filter(F.col(regra) == False).count()
        pct    = round(falhou / total * 100, 1)
        status = "OK  " if falhou == 0 else "WARN"
        log.info(f"[DQ] {status} | {regra:<35} | falhas={falhou} ({pct}%)")

    passou     = df_com_dq.filter(F.col("_dq_passou") == True).count()
    quarentena = total - passou
    log.info(f"[DQ] ----------------------------------------")
    log.info(f"[DQ] PASS (-> sot/pass)       : {passou}     ({round(passou/total*100,1)}%)")
    log.info(f"[DQ] QUARENTENA (-> sot/quar) : {quarentena} ({round(quarentena/total*100,1)}%)")

def separar_e_salvar_sot(df_com_dq):
    """
    Separa os registros em dois destinos no bucket sot:
    - quarentena: registros que falharam em pelo menos uma regra
    - pass: registros que passaram em todas as regras
    """
    # Quarentena: falhou em pelo menos uma regra DQ
    df_quarentena = df_com_dq.filter(F.col("_dq_passou") == False) \
        .withColumn("_quarentena_motivo",
            F.concat_ws(", ",
                F.when(~F.col("_dq_transaction_id_valido"), F.lit("transaction_id nulo/vazio")),
                F.when(~F.col("_dq_email_valido"),          F.lit("email invalido")),
                F.when(~F.col("_dq_valor_positivo"),        F.lit("valor_total negativo/nulo")),
                F.when(~F.col("_dq_status_valido"),         F.lit("status invalido")),
                F.when(~F.col("_dq_quantidade_valida"),     F.lit("quantidade zero/nula")),
                F.when(~F.col("_dq_nome_valido"),           F.lit("nome nulo/vazio")),
            )
        )

    # Pass: passou em todas as regras — pronto para Gold
    df_pass = df_com_dq.filter(F.col("_dq_passou") == True)

    log.info(f"[SOT] Salvando quarentena em: {QUARENTENA_PATH}")
    df_quarentena.write.mode("overwrite").parquet(QUARENTENA_PATH)
    log.info(f"[SOT] {df_quarentena.count()} registros em quarentena salvos")

    log.info(f"[SOT] Salvando pass em: {PASS_PATH}")
    df_pass.write.mode("overwrite").parquet(PASS_PATH)
    log.info(f"[SOT] {df_pass.count()} registros pass salvos")

    return df_quarentena, df_pass

# ============================================================
# ETAPA 3 — GOLD (SPEC)
# ============================================================
# Lê apenas os registros pass e gera agregações para consumo.

def construir_gold(df_pass):
    """
    Gera três visões analíticas a partir dos registros válidos:
    1. Resumo por categoria
    2. Resumo por região
    3. Resumo por status
    """
    log.info("[GOLD] Gerando agregacoes analiticas")

    # Visão 1: métricas por categoria
    gold_categoria = df_pass.groupBy("categoria").agg(
        F.count("transaction_id").alias("total_transacoes"),
        F.round(F.sum("valor_total"), 2).alias("receita_total"),
        F.round(F.avg("valor_total"), 2).alias("ticket_medio"),
        F.sum("quantidade").alias("itens_vendidos"),
        F.round(F.avg("desconto_pct"), 2).alias("desconto_medio_pct"),
        F.countDistinct("loja_id").alias("lojas_ativas"),
    ).withColumn("_gold_processed_at", F.lit(INGESTION_TS)) \
     .withColumn("_ingestion_date",    F.lit(INGESTION_DATE))

    # Visão 2: métricas por região
    gold_regiao = df_pass.groupBy("regiao").agg(
        F.count("transaction_id").alias("total_transacoes"),
        F.round(F.sum("valor_total"), 2).alias("receita_total"),
        F.round(F.avg("valor_total"), 2).alias("ticket_medio"),
        F.countDistinct("cliente_cpf").alias("clientes_unicos"),
        F.countDistinct("loja_id").alias("lojas_ativas"),
    ).withColumn("_gold_processed_at", F.lit(INGESTION_TS)) \
     .withColumn("_ingestion_date",    F.lit(INGESTION_DATE))

    # Visão 3: métricas por status
    gold_status = df_pass.groupBy("status").agg(
        F.count("transaction_id").alias("total_transacoes"),
        F.round(F.sum("valor_total"), 2).alias("valor_total"),
        F.round(F.avg("valor_total"), 2).alias("ticket_medio"),
    ).withColumn("_gold_processed_at", F.lit(INGESTION_TS)) \
     .withColumn("_ingestion_date",    F.lit(INGESTION_DATE))

    return gold_categoria, gold_regiao, gold_status

def salvar_gold(gold_categoria, gold_regiao, gold_status):
    """Salva as três visões Gold no bucket spec."""
    visoes = {
        "por_categoria": gold_categoria,
        "por_regiao":    gold_regiao,
        "por_status":    gold_status,
    }
    for nome, df in visoes.items():
        path = f"s3://{BUCKET_SPEC}/gold/{ENTIDADE}/{nome}/anomesdia={ANOMESDIA}/"
        log.info(f"[GOLD] Salvando visao '{nome}' em: {path}")
        df.write.mode("overwrite").parquet(path)
        log.info(f"[GOLD] {df.count()} registros salvos | visao={nome}")

# ============================================================
# EXECUÇÃO DO PIPELINE
# ============================================================

# Etapa 1 — Bronze (sor)
df_raw    = ler_csv(CSV_PATH)
df_bronze = construir_bronze(df_raw)
salvar_bronze(df_bronze)

# Etapa 2 — DQ + Roteamento (sot)
df_com_dq              = aplicar_regras_dq(df_bronze)
logar_resultado_dq(df_com_dq)
df_quarentena, df_pass = separar_e_salvar_sot(df_com_dq)

# Etapa 3 — Gold (spec)
gold_categoria, gold_regiao, gold_status = construir_gold(df_pass)
salvar_gold(gold_categoria, gold_regiao, gold_status)

# ============================================================
# SUMÁRIO FINAL
# ============================================================

total_lido      = df_bronze.count()
total_pass      = df_pass.count()
total_quarentena = df_quarentena.count()

log.info("=" * 65)
log.info("SUMARIO FINAL")
log.info(f"  Entidade         : {ENTIDADE}")
log.info(f"  Environment      : {ENVIRONMENT}")
log.info(f"  Anomesdia        : {ANOMESDIA}")
log.info(f"  Total lido       : {total_lido}")
log.info(f"  Pass (sot/pass)  : {total_pass}  ({round(total_pass/total_lido*100,1)}%)")
log.info(f"  Quarentena       : {total_quarentena} ({round(total_quarentena/total_lido*100,1)}%)")
log.info(f"  Bronze  (sor)    : {BRONZE_PATH}")
log.info(f"  Quarent.(sot)    : {QUARENTENA_PATH}")
log.info(f"  Pass    (sot)    : {PASS_PATH}")
log.info(f"  Gold    (spec)   : {GOLD_PATH}")
log.info("=" * 65)

job.commit()
