"""Aula 02 - Parte 2: treina um modelo e registra o experimento no MLflow.

    python treino_com_mlflow.py --n-estimators 50 --max-depth 3
    python treino_com_mlflow.py --n-estimators 100 --max-depth 5
    python treino_com_mlflow.py --n-estimators 300
"""
import argparse
import hashlib
import logging
import warnings
from pathlib import Path

import mlflow
import mlflow.sklearn
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.metrics import accuracy_score, f1_score, recall_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline

warnings.filterwarnings("ignore")  # saída limpa para a aula
logging.getLogger("mlflow").setLevel(logging.ERROR)

RAIZ = Path(__file__).resolve().parents[2]      # pasta Labs_MLOps
DADOS = RAIZ / "dados" / "clientes.csv"
EXPERIMENTO = "previsao-churn"

parser = argparse.ArgumentParser()
parser.add_argument("--n-estimators", type=int, default=100)
parser.add_argument("--max-depth", type=int, default=None)
args = parser.parse_args()

# MLflow local: banco SQLite + pasta de artefatos, compartilhados por todos os labs
mlflow.set_tracking_uri(f"sqlite:///{RAIZ / 'mlflow.db'}")
if mlflow.get_experiment_by_name(EXPERIMENTO) is None:
    mlflow.create_experiment(EXPERIMENTO, artifact_location=(RAIZ / "mlartifacts").as_uri())
mlflow.set_experiment(EXPERIMENTO)

df = pd.read_csv(DADOS)
X, y = df.drop(columns="churn"), df["churn"]
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

with mlflow.start_run():
    mlflow.log_param("n_estimators", args.n_estimators)
    mlflow.log_param("max_depth", args.max_depth)
    # Impressão digital do dataset: liga o experimento à versão exata dos dados
    mlflow.set_tag("versao_dados_md5", hashlib.md5(DADOS.read_bytes()).hexdigest()[:10])

    modelo = Pipeline([
        ("imputer", SimpleImputer(strategy="median")),
        ("modelo", RandomForestClassifier(n_estimators=args.n_estimators,
                                          max_depth=args.max_depth, random_state=42)),
    ])
    modelo.fit(X_train, y_train)
    y_pred = modelo.predict(X_test)

    acc, rec, f1 = accuracy_score(y_test, y_pred), recall_score(y_test, y_pred), f1_score(y_test, y_pred)
    mlflow.log_metric("accuracy", acc)
    mlflow.log_metric("recall", rec)
    mlflow.log_metric("f1_score", f1)

    mlflow.sklearn.log_model(
        modelo,
        name="model",
        input_example=X_test.head(3),
        # cloudpickle: formato clássico do sklearn. Só carregue modelos de fontes confiáveis.
        serialization_format="cloudpickle",
    )
    print(f"Run registrado. accuracy={acc:.3f} recall={rec:.3f} f1={f1:.3f}")
