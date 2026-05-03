-- ============================================================
-- 1.2 Quarentena
CREATE EXTERNAL TABLE IF NOT EXISTS datalake_demo.transacoes_vendas_quarentena (
    transaction_id              STRING,
    cliente_nome                STRING,
    cliente_cpf                 STRING,
    cliente_email               STRING,
    produto                     STRING,
    categoria                   STRING,
    quantidade                  INT,
    preco_unitario              DOUBLE,
    valor_total                 DOUBLE,
    status                      STRING,
    data_transacao              STRING,
    loja_id                     STRING,
    regiao                      STRING,
    parcelas                    INT,
    desconto_pct                DOUBLE,
    `_ingestion_timestamp`      STRING,
    `_ingestion_date`           STRING,
    `_source_path`              STRING,
    `_source_entity`            STRING,
    `_job_name`                 STRING,
    `_environment`              STRING,
    `_record_hash`              STRING,
    `_dq_transaction_id_valido` BOOLEAN,
    `_dq_email_valido`          BOOLEAN,
    `_dq_valor_positivo`        BOOLEAN,
    `_dq_status_valido`         BOOLEAN,
    `_dq_quantidade_valida`     BOOLEAN,
    `_dq_nome_valido`           BOOLEAN,
    `_dq_passou`                BOOLEAN,
    `_quarentena_motivo`        STRING
)
PARTITIONED BY (anomesdia STRING)
STORED AS PARQUET
LOCATION 's3://420411424817-etl-csv-ingestao/quarentena/transacoes_vendas/'
TBLPROPERTIES ('parquet.compression'='SNAPPY');

-- Executar separadamente apos o CREATE acima
MSCK REPAIR TABLE datalake_demo.transacoes_vendas_quarentena;


-- ============================================================
-- 1.3 Pass
CREATE EXTERNAL TABLE IF NOT EXISTS datalake_demo.transacoes_vendas_pass (
    transaction_id              STRING,
    cliente_nome                STRING,
    cliente_cpf                 STRING,
    cliente_email               STRING,
    produto                     STRING,
    categoria                   STRING,
    quantidade                  INT,
    preco_unitario              DOUBLE,
    valor_total                 DOUBLE,
    status                      STRING,
    data_transacao              STRING,
    loja_id                     STRING,
    regiao                      STRING,
    parcelas                    INT,
    desconto_pct                DOUBLE,
    `_ingestion_timestamp`      STRING,
    `_ingestion_date`           STRING,
    `_source_path`              STRING,
    `_source_entity`            STRING,
    `_job_name`                 STRING,
    `_environment`              STRING,
    `_record_hash`              STRING,
    `_dq_transaction_id_valido` BOOLEAN,
    `_dq_email_valido`          BOOLEAN,
    `_dq_valor_positivo`        BOOLEAN,
    `_dq_status_valido`         BOOLEAN,
    `_dq_quantidade_valida`     BOOLEAN,
    `_dq_nome_valido`           BOOLEAN,
    `_dq_passou`                BOOLEAN
)
PARTITIONED BY (anomesdia STRING)
STORED AS PARQUET
LOCATION 's3://420411424817-etl-csv-ingestao/pass/transacoes_vendas/'
TBLPROPERTIES ('parquet.compression'='SNAPPY');

-- Executar separadamente apos o CREATE acima
MSCK REPAIR TABLE datalake_demo.transacoes_vendas_pass;