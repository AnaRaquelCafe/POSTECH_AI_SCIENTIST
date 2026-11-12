"""Estágio "treinar" do pipeline (dvc.yaml). Rode com "dvc repro", não direto."""
import argparse
import json
from pathlib import Path

import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, f1_score
from sklearn.model_selection import train_test_split

AQUI = Path(__file__).parent

parser = argparse.ArgumentParser()
parser.add_argument("--n-estimators", type=int, required=True)
parser.add_argument("--max-depth", type=int, required=True)
args = parser.parse_args()

df = pd.read_csv(AQUI / "dados" / "clientes.csv")
X, y = df.drop(columns="churn"), df["churn"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

modelo = RandomForestClassifier(n_estimators=args.n_estimators, max_depth=args.max_depth, random_state=42)
modelo.fit(X_train, y_train)
pred = modelo.predict(X_test)

metricas = {"linhas": len(df), "f1": round(f1_score(y_test, pred), 4),
            "acuracia": round(accuracy_score(y_test, pred), 4)}
joblib.dump(modelo, AQUI / "modelo.joblib")
(AQUI / "metricas.json").write_text(json.dumps(metricas, indent=2) + "\n")
print(f"Modelo treinado com {metricas['linhas']} linhas | F1={metricas['f1']:.3f}")
