"""Aula 01 - Parte 2: registra o modelo da Parte 1 no Model Registry do MLflow.

    python registrar_modelo.py

A nova versão entra com o status "PendingManualApproval": ninguém deve
colocá-la em produção antes de passar pelo gate de qualidade (aprovar_modelo.py).
"""
import hashlib
import logging
import warnings
from pathlib import Path

import joblib
import mlflow
import mlflow.sklearn
import pandas as pd
from mlflow import MlflowClient
from sklearn.metrics import accuracy_score, f1_score, recall_score
from sklearn.model_selection import train_test_split

warnings.filterwarnings("ignore")  # saída limpa para a aula
logging.getLogger("mlflow").setLevel(logging.ERROR)

AQUI = Path(__file__).parent
RAIZ = AQUI.parents[1]                      # pasta Labs_MLOps
DADOS = RAIZ / "dados" / "clientes.csv"
MODELO = AQUI.parent / "Parte1_EDA_e_Treino" / "model.joblib"
NOME_MODELO = "churn-model"
EXPERIMENTO = "ciclo-de-vida"

if not MODELO.exists():
    raise SystemExit("model.joblib não encontrado: rode antes a Parte 1 (treinar_modelo.py).")

# MLflow local: banco SQLite + pasta de artefatos, compartilhados por todos os labs
mlflow.set_tracking_uri(f"sqlite:///{RAIZ / 'mlflow.db'}")
if mlflow.get_experiment_by_name(EXPERIMENTO) is None:
    mlflow.create_experiment(EXPERIMENTO, artifact_location=(RAIZ / "mlartifacts").as_uri())
mlflow.set_experiment(EXPERIMENTO)

modelo = joblib.load(MODELO)
df = pd.read_csv(DADOS)
X, y = df.drop(columns="churn"), df["churn"]
_, X_test, _, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
y_pred = modelo.predict(X_test)

with mlflow.start_run(run_name="modelo-parte1"):
    mlflow.log_metric("accuracy", accuracy_score(y_test, y_pred))
    mlflow.log_metric("recall", recall_score(y_test, y_pred))
    mlflow.log_metric("f1_score", f1_score(y_test, y_pred))
    mlflow.set_tag("versao_dados_md5", hashlib.md5(DADOS.read_bytes()).hexdigest()[:10])
    info = mlflow.sklearn.log_model(
        modelo,
        name="model",
        input_example=X_test.head(3),
        # cloudpickle: formato clássico do sklearn. Só carregue modelos de fontes confiáveis.
        serialization_format="cloudpickle",
        registered_model_name=NOME_MODELO,
    )

versao = info.registered_model_version
client = MlflowClient()
client.set_model_version_tag(NOME_MODELO, versao, "aprovacao", "PendingManualApproval")
client.update_model_version(
    NOME_MODELO, versao,
    description="RandomForest treinado na Aula 01 - Parte 1. Aguardando aprovação.",
)
print(f"Registrado: {NOME_MODELO} versão {versao} | aprovacao=PendingManualApproval")
