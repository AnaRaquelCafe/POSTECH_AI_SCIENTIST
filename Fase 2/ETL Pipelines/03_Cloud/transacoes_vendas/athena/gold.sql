-- ============================================================
-- 1.4 Gold — por categoria
CREATE EXTERNAL TABLE IF NOT EXISTS datalake_demo.transacoes_vendas_gold_por_categoria (
    categoria                   STRING,
    total_transacoes            BIGINT,
    receita_total               DOUBLE,
    ticket_medio                DOUBLE,
    itens_vendidos              BIGINT,
    desconto_medio_pct          DOUBLE,
    lojas_ativas                BIGINT,
    `_gold_processed_at`        STRING,
    `_ingestion_date`           STRING
)
PARTITIONED BY (anomesdia STRING)
STORED AS PARQUET
LOCATION 's3://420411424817-etl-csv-ingestao/gold/transacoes_vendas/por_categoria/'
TBLPROPERTIES ('parquet.compression'='SNAPPY');

-- Executar separadamente apos o CREATE acima
MSCK REPAIR TABLE datalake_demo.transacoes_vendas_gold_por_categoria;


-- ============================================================
-- 1.5 Gold — por regiao
CREATE EXTERNAL TABLE IF NOT EXISTS datalake_demo.transacoes_vendas_gold_por_regiao (
    regiao                      STRING,
    total_transacoes            BIGINT,
    receita_total               DOUBLE,
    ticket_medio                DOUBLE,
    clientes_unicos             BIGINT,
    lojas_ativas                BIGINT,
    `_gold_processed_at`        STRING,
    `_ingestion_date`           STRING
)
PARTITIONED BY (anomesdia STRING)
STORED AS PARQUET
LOCATION 's3://420411424817-etl-csv-ingestao/gold/transacoes_vendas/por_regiao/'
TBLPROPERTIES ('parquet.compression'='SNAPPY');

-- Executar separadamente apos o CREATE acima
MSCK REPAIR TABLE datalake_demo.transacoes_vendas_gold_por_regiao;


-- ============================================================
-- 1.6 Gold — por status
CREATE EXTERNAL TABLE IF NOT EXISTS datalake_demo.transacoes_vendas_gold_por_status (
    status                      STRING,
    total_transacoes            BIGINT,
    valor_total                 DOUBLE,
    ticket_medio                DOUBLE,
    `_gold_processed_at`        STRING,
    `_ingestion_date`           STRING
)
PARTITIONED BY (anomesdia STRING)
STORED AS PARQUET
LOCATION 's3://420411424817-etl-csv-ingestao/gold/transacoes_vendas/por_status/'
TBLPROPERTIES ('parquet.compression'='SNAPPY');

-- Executar separadamente apos o CREATE acima
MSCK REPAIR TABLE datalake_demo.transacoes_vendas_gold_por_status;