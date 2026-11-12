"""Treina o modelo de churn e registra tudo no MLflow.

    python treinar.py --n-estimators 50 --max-depth 3
    python treinar.py --n-estimators 200 --max-depth 8
    python treinar.py --n-estimators 200 --max-depth 8 --registrar
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
from sklearn.metrics import accuracy_score, f1_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

warnings.filterwarnings("ignore")  # saída limpa para a aula
logging.getLogger("mlflow").setLevel(logging.ERROR)  # esconde avisos internos do MLflow

AQUI = Path(__file__).parent
DADOS = AQUI / "dados" / "clientes.csv"
EXPERIMENTO = "previsao-churn"

parser = argparse.ArgumentParser()
parser.add_argument("--n-estimators", type=int, default=100)
parser.add_argument("--max-depth", type=int, default=5)
parser.add_argument("--registrar", action="store_true",
                    help="registra o modelo no MLflow Model Registry")
args = parser.parse_args()

# Tracking local: banco SQLite + pasta de artefatos, ambos dentro do lab
mlflow.set_tracking_uri(f"sqlite:///{AQUI / 'mlflow.db'}")
if mlflow.get_experiment_by_name(EXPERIMENTO) is None:
    mlflow.create_experiment(EXPERIMENTO, artifact_location=(AQUI / "mlartifacts").as_uri())
mlflow.set_experiment(EXPERIMENTO)

df = pd.read_csv(DADOS)
X, y = df.drop(columns="churn").astype(float), df["churn"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Impressão digital do dataset: liga o experimento à versão exata dos dados
hash_dados = hashlib.md5(DADOS.read_bytes()).hexdigest()[:10]

with mlflow.start_run():
    mlflow.log_param("n_estimators", args.n_estimators)
    mlflow.log_param("max_depth", args.max_depth)
    mlflow.set_tag("versao_dados_md5", hash_dados)
    mlflow.set_tag("linhas_dados", len(df))

    pipeline = Pipeline([
        ("scaler", StandardScaler()),
        ("model", RandomForestClassifier(n_estimators=args.n_estimators,
                                         max_depth=args.max_depth, random_state=42)),
    ])
    pipeline.fit(X_train, y_train)
    pred = pipeline.predict(X_test)

    f1 = f1_score(y_test, pred)
    mlflow.log_metric("f1_score", f1)
    mlflow.log_metric("accuracy", accuracy_score(y_test, pred))

    mlflow.sklearn.log_model(
        pipeline,
        name="model",
        input_example=X_test.head(3),
        serialization_format="cloudpickle",
        registered_model_name="churn" if args.registrar else None,
    )
    print(f"F1={f1:.3f} | dados md5={hash_dados} | registrado={args.registrar}")
