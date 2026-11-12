# Aula 03 · Parte 2 — Detectando drift (≈ 13 min)

**Objetivo:** simular dados de produção que se afastam dos dados de treino e medir esse afastamento com PSI, Kolmogorov-Smirnov e qui-quadrado.
**Conceitos da parte:** janela de referência vs janela de análise, data drift, PSI e suas faixas de decisão, teste KS (features numéricas), teste qui-quadrado (features categóricas).

```bash
cd Labs-streamlit/Aula03_Monitoramento_Drift/Parte2_Detectando_Drift
```

## 1. Rode sem drift (2 min)
```bash
python drift_lab.py
```
Com os parâmetros no valor padrão, tudo deve aparecer como **estável** e os p-valores ficam bem acima de 0,05. O PSI está implementado "na mão" na função `psi()`, com cerca de 10 linhas; vale ler.

## 2. Provoque o drift (6 min)
No topo do `drift_lab.py`, altere **um valor por vez**, rode de novo e volte o valor ao padrão antes do próximo teste:

| Alteração | O que você deve observar |
|---|---|
| `DESLOCAMENTO_IDADE = 5` | PSI da idade entra na faixa de atenção (entre 0,1 e 0,2) |
| `DESLOCAMENTO_IDADE = 7` | PSI da idade passa de 0,2: ação necessária |
| `FATOR_VALOR_MENSAL = 1.2` | mensalidades 20% maiores já geram drift significativo |
| `PROPORCAO_PREMIUM = 0.18` | o plano premium foi de 15% para 18%, e o qui-quadrado já acusa (p < 0,05) |
| `DESLOCAMENTO_IDADE = 2` | o PSI diz "estável", mas o KS acusa diferença (p < 0,05) |

## 3. O tamanho da janela importa (3 min)
Mantenha `DESLOCAMENTO_IDADE = 2` e mude o tamanho da janela de análise:

| Alteração | O que você deve observar |
|---|---|
| `TAMANHO_ANALISE = 150` | o KS **deixa** de acusar a mesma diferença de 2 anos |
| `TAMANHO_ANALISE = 20000` | o p-valor do KS vai a praticamente zero |

A diferença real é a mesma nos dois casos; só a quantidade de dados mudou. Volte tudo ao padrão ao terminar.

## Para discutir
- Com muitos dados, o KS detecta diferenças minúsculas. Qual dos dois (PSI ou KS) você usaria para disparar um alerta que acorda alguém de madrugada?
- Janela de análise pequena demais esconde drift; grande demais demora para perceber mudanças. Para um app com 500 clientes novos por dia, você usaria uma janela de um dia ou de uma semana?
