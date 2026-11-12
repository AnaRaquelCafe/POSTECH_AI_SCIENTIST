"""Estágio "treinar" do pipeline DVC (dvc.yaml).

Lê dados/clientes.csv, treina o modelo e grava modelo.joblib + metricas.json.
Não rode direto: use "dvc repro", que só executa quando algo mudou.
"""
import json
from pathlib import Path

import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, f1_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

AQUI = Path(__file__).parent

df = pd.read_csv(AQUI / "dados" / "clientes.csv")
X, y = df.drop(columns="churn").astype(float), df["churn"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

pipeline = Pipeline([
    ("scaler", StandardScaler()),
    ("model", RandomForestClassifier(n_estimators=200, max_depth=8, random_state=42)),
])
pipeline.fit(X_train, y_train)
pred = pipeline.predict(X_test)

metricas = {
    "linhas": len(df),
    "f1": round(f1_score(y_test, pred), 4),
    "acuracia": round(accuracy_score(y_test, pred), 4),
}
joblib.dump(pipeline, AQUI / "modelo.joblib")
(AQUI / "metricas.json").write_text(json.dumps(metricas, indent=2) + "\n")
print(f"Modelo treinado com {metricas['linhas']} linhas | F1={metricas['f1']:.3f}")
