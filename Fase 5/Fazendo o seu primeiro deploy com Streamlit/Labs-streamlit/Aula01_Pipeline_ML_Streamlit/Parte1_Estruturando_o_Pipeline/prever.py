"""Aula 01 · Parte 1 — Serving: usa o artefato gerado pelo train.py.

    python prever.py --idade 22 --meses 1 --valor 190

Repare: este script não sabe nada de StandardScaler nem de RandomForest.
Ele só carrega o artefato e chama predict_proba() com os dados crus.
"""
import argparse
from pathlib import Path

import joblib
import pandas as pd

MODELO = Path(__file__).parent / "modelo_churn.joblib"

parser = argparse.ArgumentParser()
parser.add_argument("--idade", type=int, default=35)
parser.add_argument("--meses", type=int, default=12)
parser.add_argument("--valor", type=float, default=79.90)
args = parser.parse_args()

if not MODELO.exists():
    raise SystemExit("Modelo não encontrado. Rode antes: python train.py")

pipeline = joblib.load(MODELO)
cliente = pd.DataFrame([[args.idade, args.meses, args.valor]],
                       columns=["idade", "meses", "valor_mensal"])
proba = pipeline.predict_proba(cliente)[0][1]

print(f"Etapas dentro do artefato: {list(pipeline.named_steps)}")
print(f"Cliente: idade={args.idade}, meses={args.meses}, valor=R$ {args.valor:.2f}")
print(f"Probabilidade de churn: {proba:.1%}")
