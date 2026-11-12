"""Gera o model.joblib servido pela API (mesmo modelo da Aula 01)."""
from pathlib import Path

import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline

AQUI = Path(__file__).parent
df = pd.read_csv(AQUI.parents[1] / "dados" / "clientes.csv")
X, y = df.drop(columns="churn"), df["churn"]

modelo = Pipeline([
    ("imputer", SimpleImputer(strategy="median")),
    ("modelo", RandomForestClassifier(n_estimators=100, max_depth=5, random_state=42)),
]).fit(X, y)
joblib.dump(modelo, AQUI / "model.joblib")
print("model.joblib gerado.")
