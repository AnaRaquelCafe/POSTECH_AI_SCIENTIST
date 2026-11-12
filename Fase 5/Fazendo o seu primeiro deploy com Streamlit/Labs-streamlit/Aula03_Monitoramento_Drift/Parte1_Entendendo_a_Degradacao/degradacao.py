"""Aula 03 · Parte 1 — Por que (e como) um modelo degrada em produção.

    python degradacao.py estavel
    python degradacao.py dados_quebrados
    python degradacao.py data_drift
    python degradacao.py concept_drift

O modelo é treinado no mês 0 e depois "vive" 12 meses em produção.
A cada mês olhamos os três níveis de monitoramento: infraestrutura, dados e modelo.
"""
import sys
import time

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import f1_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

CENARIOS = ["estavel", "dados_quebrados", "data_drift", "concept_drift"]
cenario = sys.argv[1] if len(sys.argv) > 1 else "estavel"
if cenario not in CENARIOS:
    raise SystemExit(f"Cenário inválido. Use um destes: {', '.join(CENARIOS)}")

rng = np.random.default_rng(0)


def gerar_mes(n, mes):
    """Clientes de um mês. O cenário escolhido decide o que muda com o tempo."""
    idade = np.clip(rng.normal(45, 14, n), 18, 90).round()
    if cenario == "data_drift":
        idade = np.clip(idade - 2 * mes, 18, 90)      # base de clientes cada vez mais jovem
    meses = rng.integers(0, 72, n)
    valor = rng.uniform(20, 200, n).round(2)

    efeito_idade = 0.08
    if cenario == "concept_drift":
        efeito_idade = 0.08 - 0.016 * mes             # um concorrente passa a atrair os mais velhos
    logito = efeito_idade * (40 - idade) + 0.10 * (12 - meses) + 0.04 * (valor - 90)
    churn = (rng.random(n) < 1 / (1 + np.exp(-logito))).astype(int)

    valor_recebido = valor.copy()
    if cenario == "dados_quebrados" and mes >= 6:
        # Uma mudança no sistema de origem passa a enviar 0 quando o campo vem vazio
        valor_recebido[rng.random(n) < 0.3] = 0.0

    X = pd.DataFrame({"idade": idade, "meses": meses, "valor_mensal": valor_recebido})
    return X, churn


# Mês 0: treino
X_treino, y_treino = gerar_mes(5000, mes=0)
modelo = Pipeline([
    ("scaler", StandardScaler()),
    ("model", RandomForestClassifier(n_estimators=100, max_depth=6, random_state=42)),
]).fit(X_treino, y_treino)

print(f"Cenário: {cenario}\n")
print(f"{'':>4} | {'INFRA':^11} | {'DADOS':^25} | {'PROXY':^11} | {'MODELO':^9}")
print(f"{'mês':>4} | {'latência':>11} | {'idade média':>11} {'% valor = 0':>13} |"
      f" {'churn prev.':>11} | {'F1 real*':>9}")
print("-" * 83)
for mes in range(1, 13):
    X, y = gerar_mes(3000, mes)
    inicio = time.perf_counter()
    pred = modelo.predict(X)
    latencia_ms = (time.perf_counter() - inicio) * 1000 / len(X)
    print(f"{mes:>4} | {latencia_ms:>8.3f} ms | {X['idade'].mean():>11.1f}"
          f" {(X['valor_mensal'] == 0).mean():>13.0%} | {pred.mean():>11.0%} |"
          f" {f1_score(y, pred):>9.2f}")

print("\n* F1 real: no mundo real só é conhecido ~30 dias depois, quando o churn se confirma"
      " (ground truth atrasado).")
