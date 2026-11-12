"""Aula 02 - Parte 3: o "consumidor" do modelo. Sempre carrega o @champion.

    python prever.py
"""
import warnings
from pathlib import Path

import mlflow
import pandas as pd
from mlflow import MlflowClient
from mlflow.exceptions import MlflowException

warnings.filterwarnings("ignore")
RAIZ = Path(__file__).resolve().parents[2]
mlflow.set_tracking_uri(f"sqlite:///{RAIZ / 'mlflow.db'}")

try:
    versao = MlflowClient().get_model_version_by_alias("churn-model", "champion").version
except MlflowException:
    raise SystemExit("Ainda não há @champion. Rode registrar_modelo.py e promover_modelo.py.")
modelo = mlflow.sklearn.load_model("models:/churn-model@champion")

cliente = pd.DataFrame([[23.0, 2, 210.0, 4]],
                       columns=["idade", "meses", "valor_mensal", "chamados_suporte"])
print(f"Modelo em produção: churn-model v{versao}")
print(f"Probabilidade de churn: {modelo.predict_proba(cliente)[0][1]:.1%}")
