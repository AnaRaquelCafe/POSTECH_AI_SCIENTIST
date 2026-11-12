"""Aula 01 - Parte 3: simula um dia de produção e grava o Data Capture.

    python simular_producao.py              # clientes parecidos com os do treino
    python simular_producao.py --drift      # perfil de clientes mudou

Cada requisição enviada ao endpoint e cada resposta recebida são gravadas em
captura/captura.csv. É isso que o monitoramento vai analisar depois.
"""
import argparse
from pathlib import Path

import pandas as pd
import requests

URL = "http://localhost:5001/invocations"
AQUI = Path(__file__).parent
DADOS = AQUI.parents[1] / "dados" / "clientes.csv"

parser = argparse.ArgumentParser()
parser.add_argument("--drift", action="store_true", help="simula mudança no perfil dos clientes")
parser.add_argument("-n", type=int, default=500, help="quantidade de requisições")
args = parser.parse_args()

producao = pd.read_csv(DADOS).drop(columns="churn").sample(args.n, replace=True, random_state=7)
producao = producao.fillna(producao["idade"].median()).reset_index(drop=True)
if args.drift:
    # Nova campanha de marketing trouxe clientes mais jovens, com planos mais caros
    producao["idade"] = (producao["idade"] - 10).clip(lower=18)
    producao["valor_mensal"] = (producao["valor_mensal"] * 1.3).round(2)

resp = requests.post(URL, json={"dataframe_split": producao.to_dict(orient="split", index=False)},
                     timeout=30)
resp.raise_for_status()
producao["predicao"] = resp.json()["predictions"]

pasta = AQUI / "captura"
pasta.mkdir(exist_ok=True)
producao.to_csv(pasta / "captura.csv", index=False)
print(f"{len(producao)} requisições capturadas em {pasta / 'captura.csv'}")
print(f"Taxa de churn prevista: {producao['predicao'].mean():.1%}")
