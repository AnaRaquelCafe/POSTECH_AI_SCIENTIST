"""Gera o dataset do Lab 04 em duas versões, para simular a evolução dos dados.

    python gerar_dados.py --versao 1   # 2.000 clientes
    python gerar_dados.py --versao 2   # 4.000 clientes, perfil mais jovem
"""
import argparse
from pathlib import Path

import numpy as np
import pandas as pd

parser = argparse.ArgumentParser()
parser.add_argument("--versao", type=int, choices=[1, 2], default=1)
args = parser.parse_args()

rng = np.random.default_rng(args.versao)
n = 2000 if args.versao == 1 else 4000
idade_media = 45 if args.versao == 1 else 35

df = pd.DataFrame({
    "idade": np.clip(rng.normal(idade_media, 14, n), 18, 90).round(),
    "meses": rng.integers(0, 72, n),
    "valor_mensal": rng.uniform(20, 200, n).round(2),
})
logito = 0.03 * (40 - df["idade"]) + 0.06 * (12 - df["meses"]) + 0.015 * (df["valor_mensal"] - 90)
df["churn"] = (rng.random(n) < 1 / (1 + np.exp(-logito))).astype(int)

destino = Path(__file__).parent / "dados" / "clientes.csv"
destino.parent.mkdir(exist_ok=True)
df.to_csv(destino, index=False)
print(f"Versão {args.versao} gerada: {len(df)} linhas em {destino}")
