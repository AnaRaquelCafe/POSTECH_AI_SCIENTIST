"""Promove uma versão do modelo 'churn' atribuindo um alias no Model Registry.

    python promover.py --versao 1 --alias champion

Obs.: o MLflow usa aliases no lugar dos antigos "stages" Staging/Production/Archived,
que foram descontinuados ('champion' para o modelo em produção, 'challenger' para o candidato).
"""
import argparse
import logging
import warnings
from pathlib import Path

import mlflow
from mlflow import MlflowClient

warnings.filterwarnings("ignore")
logging.getLogger("mlflow").setLevel(logging.ERROR)  # esconde avisos internos do MLflow
AQUI = Path(__file__).parent

parser = argparse.ArgumentParser()
parser.add_argument("--versao", required=True)
parser.add_argument("--alias", default="champion")
args = parser.parse_args()

mlflow.set_tracking_uri(f"sqlite:///{AQUI / 'mlflow.db'}")
MlflowClient().set_registered_model_alias("churn", args.alias, args.versao)
print(f"Versão {args.versao} do modelo 'churn' agora é '@{args.alias}'.")
