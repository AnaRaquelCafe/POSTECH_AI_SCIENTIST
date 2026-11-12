"""Gera o dataset de churn usado em todos os labs (clientes.csv).

    python gerar_dados.py              # 3.000 clientes, semente fixa

Cada linha é um cliente de uma empresa de assinatura. A coluna `churn`
indica se ele cancelou nos 30 dias seguintes (1) ou não (0).
"""
from pathlib import Path

import numpy as np
import pandas as pd

rng = np.random.default_rng(42)
n = 3000

df = pd.DataFrame({
    "idade": np.clip(rng.normal(42, 13, n), 18, 85).round(),
    "meses": rng.integers(0, 72, n),                          # tempo de casa
    "valor_mensal": rng.uniform(30, 250, n).round(2),
    "chamados_suporte": rng.poisson(1.2, n),                  # últimos 90 dias
})
logito = (
    -0.8
    + 0.05 * (40 - df["idade"])
    + 0.15 * (12 - df["meses"]).clip(lower=-12)
    + 0.022 * (df["valor_mensal"] - 120)
    + 0.9 * (df["chamados_suporte"] - 1)
)
df["churn"] = (rng.random(n) < 1 / (1 + np.exp(-logito))).astype(int)

# Alguns valores ausentes, como em qualquer base real (para a EDA ter o que mostrar)
faltantes = rng.choice(n, size=45, replace=False)
df.loc[faltantes, "idade"] = np.nan

destino = Path(__file__).parent / "clientes.csv"
df.to_csv(destino, index=False)
print(f"{len(df)} clientes gerados em {destino} (taxa de churn: {df['churn'].mean():.1%})")
