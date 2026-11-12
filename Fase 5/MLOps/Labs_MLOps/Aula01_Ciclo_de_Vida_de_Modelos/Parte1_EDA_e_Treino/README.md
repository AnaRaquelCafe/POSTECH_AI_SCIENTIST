# Parte 1 — EDA e treino (≈ 12 min)

**Objetivo:** explorar os dados, treinar um modelo de churn e compará-lo com o baseline (a regra usada hoje, sem ML).
**Conceitos da aula:** definição do problema, métrica técnica vs baseline, EDA, separação treino/teste, data leakage.

Os dados estão em `Labs_MLOps/dados/clientes.csv`: 3.000 clientes de uma empresa de assinatura, com idade, tempo de casa (`meses`), valor mensal, chamados ao suporte nos últimos 90 dias e se cancelou (`churn`).

```bash
cd Labs_MLOps/Aula01_Ciclo_de_Vida_de_Modelos/Parte1_EDA_e_Treino
python treinar_modelo.py
```

O script faz: carga do CSV → EDA rápida → treino de um `RandomForestClassifier` dentro de um `Pipeline` → avaliação contra o baseline → salva `model.joblib`.

## Exercício (5 min)
1. Na EDA, qual coluna tem valores ausentes? Onde eles são tratados no código?
2. O modelo supera o baseline em qual métrica? Para uma campanha de retenção, você priorizaria **recall** ou **precision**? Por quê?
3. Troque `max_depth=5` por `max_depth=None` e rode de novo. A métrica de teste melhorou ou piorou? O que isso sugere?

O `model.joblib` gerado aqui é o artefato que vamos registrar na Parte 2.
