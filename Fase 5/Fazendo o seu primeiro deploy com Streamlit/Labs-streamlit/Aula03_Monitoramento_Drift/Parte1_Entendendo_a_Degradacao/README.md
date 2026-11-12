# Aula 03 · Parte 1 — Entendendo a degradação (≈ 12 min)

**Objetivo:** ver um modelo de churn "envelhecer" ao longo de 12 meses em produção e descobrir qual nível de monitoramento percebe cada tipo de problema e quando percebe.
**Conceitos da parte:** por que modelos degradam, os três níveis de monitoramento (infraestrutura, dados e modelo), ground truth atrasado, métricas de proxy.

```bash
cd Labs-streamlit/Aula03_Monitoramento_Drift/Parte1_Entendendo_a_Degradacao
```

O `degradacao.py` treina um modelo no mês 0 e o coloca em produção por 12 meses. A cada mês ele mostra:

| Coluna | Nível | O que mede |
|---|---|---|
| latência | infraestrutura | tempo de resposta por predição |
| idade média, % valor = 0 | dados | como estão chegando as entradas |
| churn prev. | proxy | quantos clientes o modelo marca como risco (sem precisar do ground truth) |
| F1 real | modelo | a performance de verdade, que só se conhece ~30 dias depois |

## 1. O mundo parado (2 min)
```bash
python degradacao.py estavel
```
Tudo estável: essa é a linha de base. Repare que o F1 oscila um pouco de um mês para o outro só por acaso.

## 2. Três formas de o mundo mudar (7 min)
Rode um cenário por vez:
```bash
python degradacao.py dados_quebrados
python degradacao.py data_drift
python degradacao.py concept_drift
```
Para cada um, anote no caderno:

| Cenário | A infra percebeu? | Os dados denunciaram? | O proxy mudou? | O F1 caiu? |
|---|---|---|---|---|
| `dados_quebrados` | | | | |
| `data_drift` | | | | |
| `concept_drift` | | | | |

O que cada cenário simula está comentado na função `gerar_mes()` do script.

## 3. Conclusão (3 min)
Em qual cenário **nenhuma** métrica disponível no dia a dia (infra, dados e proxy) acusou o problema, e só o F1 real, que chega com atraso, mostrou a queda? Esse é o "92% vira 70% em silêncio" da aula.

## Para discutir
- No `data_drift`, a base ficou bem mais jovem e o F1 **não** caiu. Então drift nos dados é sempre um problema? Por que vale monitorar mesmo assim?
- No `dados_quebrados`, qual equipe você acionaria primeiro: a de ciência de dados ou a de engenharia de dados?
