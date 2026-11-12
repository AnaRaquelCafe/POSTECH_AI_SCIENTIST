"""Treina o modelo e checa se ele atinge o mínimo exigido e supera o baseline.
Sai com código != 0 (falha o build) se não atingir.

    python scripts/test_model_quality.py
"""
import sys
from pathlib import Path

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline

DADOS = Path(__file__).resolve().parents[3] / "dados" / "clientes.csv"
THRESHOLD_ACCURACY = 0.75


def main():
    df = pd.read_csv(DADOS)
    X, y = df.drop(columns="churn"), df["churn"]
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    modelo = Pipeline([
        ("imputer", SimpleImputer(strategy="median")),
        ("modelo", RandomForestClassifier(n_estimators=100, max_depth=5, random_state=42)),
    ]).fit(X_train, y_train)

    acc = accuracy_score(y_test, modelo.predict(X_test))
    baseline = accuracy_score(y_test, ((X_test["meses"] < 6) | (X_test["chamados_suporte"] >= 3)))
    print(f"Accuracy: modelo {acc:.3f} | baseline {baseline:.3f} | mínimo {THRESHOLD_ACCURACY}")

    if acc < THRESHOLD_ACCURACY:
        print("FALHOU - accuracy abaixo do mínimo.")
        sys.exit(1)
    if acc <= baseline:
        print("FALHOU - o modelo não supera o baseline (a regra sem ML).")
        sys.exit(1)
    print("Modelo OK.")


if __name__ == "__main__":
    main()
