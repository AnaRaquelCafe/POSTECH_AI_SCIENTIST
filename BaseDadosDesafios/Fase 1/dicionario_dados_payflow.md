# Dicionário de Dados — PayFlow Credit Risk (payflow_credit_risk.csv)

## Contexto
Dataset sintético para simular um cenário de **score de inadimplência** em uma fintech.

- **Unidade de análise:** cliente (id_cliente)
- **Objetivo analítico:** prever `default_90d` (0/1)
- **Observação importante:** o dataset contém colunas com *informação do futuro* (leakage) para testar governança/criticidade do pipeline.

## Colunas

| Coluna | Tipo | Descrição |
|---|---|---|
| id_cliente | int | Identificador do cliente (anônimo) |
| idade | int | Idade em anos |
| renda_mensal | float | Renda mensal declarada (R$). Pode conter valores ausentes |
| tempo_emprego_anos | float | Tempo de emprego em anos (pode ser ausente, ex.: autônomos) |
| autonomo | int | 1 se cliente é autônomo, 0 caso contrário |
| score_credito | float | Score de crédito (300 a 900) |
| valor_solicitado | float | Valor solicitado (R$) |
| prazo_meses | int | Prazo do contrato (meses) |
| juros_mensal_pct | float | Taxa de juros mensal (%) |
| qtde_cartoes | int | Qtde de cartões ativos |
| qtde_contratos_abertos | int | Qtde de contratos de crédito abertos |
| utilizacao_credito | float | Utilização do limite de crédito (0 a 1) |
| inadimplencias_anteriores | int | Qtde de inadimplências anteriores registradas |
| dias_atraso_max_12m | int | Maior atraso (dias) observado nos últimos 12 meses |
| reclamacoes_6m | int | Qtde de reclamações/atendimentos nos últimos 6 meses |
| possui_avalista | int | 1 se possui avalista/garantidor, 0 caso contrário |
| canal_aquisicao | str | Canal de aquisição (app/site/loja/parceiro) |
| regiao | str | Macro-região (Sudeste/Sul/Nordeste/Norte/Centro-Oeste) |
| tipo_produto | str | Produto (emprestimo_pessoal/cartao/bnpl) |
| parcelas_pagas_ate_3m | int | **LEAKAGE**: número de parcelas pagas até 3 meses após concessão |
| atraso_primeira_parcela_dias | int | **LEAKAGE**: atraso (dias) na primeira parcela |
| status_apos_90d | str | **LEAKAGE**: status 90 dias depois (em_dia/em_atraso_leve/default) |
| default_90d | int | **Target**: 1 se entrou em default em até 90 dias; 0 caso contrário |

## Sugestão de carga

```python
import pandas as pd

df = pd.read_csv('payflow_credit_risk.csv')
df.head()
```
