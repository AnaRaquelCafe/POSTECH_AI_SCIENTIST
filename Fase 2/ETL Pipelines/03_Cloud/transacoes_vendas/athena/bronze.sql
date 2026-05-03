CREATE EXTERNAL TABLE IF NOT EXISTS datalake_demo.transacoes_vendas_bronze (
    transaction_id         STRING,
    cliente_nome           STRING,
    cliente_cpf            STRING,
    cliente_email          STRING,
    produto                STRING,
    categoria              STRING,
    quantidade             INT,
    preco_unitario         DOUBLE,
    valor_total            DOUBLE,
    status                 STRING,
    data_transacao         STRING,
    loja_id                STRING,
    regiao                 STRING,
    parcelas               INT,
    desconto_pct           DOUBLE,
    `_ingestion_timestamp` STRING,
    `_ingestion_date`      STRING,
    `_source_path`         STRING,
    `_source_entity`       STRING,
    `_job_name`            STRING,
    `_environment`         STRING,
    `_record_hash`         STRING
)
PARTITIONED BY (anomesdia STRING)
STORED AS PARQUET
LOCATION 's3://420411424817-etl-csv-ingestao/bronze/transacoes_vendas/'
TBLPROPERTIES ('parquet.compression'='SNAPPY');

MSCK REPAIR TABLE datalake_demo.transacoes_vendas_bronze;