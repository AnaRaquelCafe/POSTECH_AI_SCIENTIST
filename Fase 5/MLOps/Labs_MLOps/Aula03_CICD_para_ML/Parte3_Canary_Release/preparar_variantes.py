"""Aula 03 - Parte 3: garante as duas variantes do canary no Model Registry.

    python preparar_variantes.py

- @champion: o modelo em produção (se não existir, treina e registra um).
- @challenger: uma versão nova, treinada agora com outros hiperparâmetros.
"""
import logging
import warnings
from pathlib import Path

import mlflow
import mlflow.sklearn
import pandas as pd
from mlflow import MlflowClient
from mlflow.exceptions import MlflowException
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.metrics import f1_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline

warnings.filterwarnings("ignore")
logging.getLogger("mlflow").setLevel(logging.ERROR)

RAIZ = Path(__file__).resolve().parents[2]
NOME_MODELO = "churn-model"
EXPERIMENTO = "canary"

mlflow.set_tracking_uri(f"sqlite:///{RAIZ / 'mlflow.db'}")
if mlflow.get_experiment_by_name(EXPERIMENTO) is None:
    mlflow.create_experiment(EXPERIMENTO, artifact_location=(RAIZ / "mlartifacts").as_uri())
mlflow.set_experiment(EXPERIMENTO)
client = MlflowClient()

df = pd.read_csv(RAIZ / "dados" / "clientes.csv")
X, y = df.drop(columns="churn"), df["churn"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)


def treinar_e_registrar(n_estimators, max_depth, alias):
    with mlflow.start_run(run_name=alias):
        modelo = Pipeline([
            ("imputer", SimpleImputer(strategy="median")),
            ("modelo", RandomForestClassifier(n_estimators=n_estimators, max_depth=max_depth,
                                              random_state=42)),
        ]).fit(X_train, y_train)
        mlflow.log_params({"n_estimators": n_estimators, "max_depth": max_depth})
        mlflow.log_metric("f1_score", f1_score(y_test, modelo.predict(X_test)))
        info = mlflow.sklearn.log_model(modelo, name="model", input_example=X_test.head(3),
                                        serialization_format="cloudpickle",
                                        registered_model_name=NOME_MODELO)
    client.set_registered_model_alias(NOME_MODELO, alias, info.registered_model_version)
    print(f"@{alias} -> versão {info.registered_model_version}")


try:
    champion = client.get_model_version_by_alias(NOME_MODELO, "champion")
    print(f"@champion já existe -> versão {champion.version}")
except MlflowException:
    treinar_e_registrar(100, 5, "champion")

treinar_e_registrar(200, 8, "challenger")
