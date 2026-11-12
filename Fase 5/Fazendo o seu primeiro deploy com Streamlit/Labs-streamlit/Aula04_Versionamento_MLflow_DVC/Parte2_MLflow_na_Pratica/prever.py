"""Carrega o modelo pelo alias (não pelo número da versão) e faz uma predição.

    python prever.py                     # usa churn@champion
    python prever.py --alias challenger

Quem consome o modelo pede 'churn@champion' e não precisa saber qual versão é.
Trocar o modelo em produção = mover o alias (rollback incluso).
"""
import argparse
import logging
import warnings
from pathlib import Path

import mlflow
import pandas as pd
from mlflow import MlflowClient

warnings.filterwarnings("ignore")
logging.getLogger("mlflow").setLevel(logging.ERROR)  # esconde avisos internos do MLflow
AQUI = Path(__file__).parent

parser = argparse.ArgumentParser()
parser.add_argument("--alias", default="champion")
args = parser.parse_args()

mlflow.set_tracking_uri(f"sqlite:///{AQUI / 'mlflow.db'}")

versao = MlflowClient().get_model_version_by_alias("churn", args.alias).version
modelo = mlflow.sklearn.load_model(f"models:/churn@{args.alias}")
cliente = pd.DataFrame([[22.0, 1.0, 190.0]], columns=["idade", "meses", "valor_mensal"])
print(f"churn@{args.alias} = versão {versao} | "
      f"probabilidade de churn: {modelo.predict_proba(cliente)[0][1]:.1%}")
