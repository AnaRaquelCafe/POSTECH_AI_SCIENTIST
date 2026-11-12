"""Aula 01 - Parte 3: sobe um endpoint real-time com a última versão APROVADA.

    python deploy_endpoint.py

Usa o servidor de modelos do próprio MLflow (porta 5001). Deixe este terminal
aberto; para "derrubar o endpoint", pressione Ctrl+C.
"""
import os
from pathlib import Path

import mlflow
from mlflow import MlflowClient

RAIZ = Path(__file__).resolve().parents[2]
NOME_MODELO = "churn-model"
TRACKING_URI = f"sqlite:///{RAIZ / 'mlflow.db'}"

mlflow.set_tracking_uri(TRACKING_URI)
aprovadas = MlflowClient().search_model_versions(
    f"name='{NOME_MODELO}' and tags.aprovacao='Approved'"
)
if not aprovadas:
    raise SystemExit("Nenhuma versão aprovada. Faça a Parte 2 (registrar + aprovar) primeiro.")

versao = max(aprovadas, key=lambda v: int(v.version)).version
print(f"Fazendo deploy de {NOME_MODELO} v{versao} em http://localhost:5001 ...")

os.environ["MLFLOW_TRACKING_URI"] = TRACKING_URI
os.execvp("mlflow", [
    "mlflow", "models", "serve",
    "--model-uri", f"models:/{NOME_MODELO}/{versao}",
    "--port", "5001",
    "--env-manager", "local",   # usa o Python do codespace, sem criar outro ambiente
])
