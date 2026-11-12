"""Aula 01 - Parte 1: EDA e treino de um modelo de churn.

    python treinar_modelo.py

Carrega os dados, faz uma EDA rápida, compara o modelo com um baseline
(regra de negócio sem ML), avalia e salva o modelo em model.joblib.
"""
from pathlib import Path

import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.metrics import accuracy_score, classification_report, f1_score, recall_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline

AQUI = Path(__file__).parent
DADOS = AQUI.parents[1] / "dados" / "clientes.csv"


def eda_rapida(df: pd.DataFrame) -> None:
    print("=== INFO ===")
    df.info()
    print("\n=== DESCRIBE ===")
    print(df.describe().round(2))
    print("\n=== NULOS POR COLUNA ===")
    print(df.isnull().sum())
    print(f"\n=== TAXA DE CHURN: {df['churn'].mean():.1%} ===")


def baseline(X: pd.DataFrame) -> pd.Series:
    """Regra usada hoje, sem ML: cliente novo ou que abriu muitos chamados vai cancelar."""
    return ((X["meses"] < 6) | (X["chamados_suporte"] >= 3)).astype(int)


def main():
    df = pd.read_csv(DADOS)
    eda_rapida(df)

    X, y = df.drop(columns="churn"), df["churn"]
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    # O Pipeline guarda o pré-processamento junto com o modelo: em produção,
    # o dado bruto passa pelas mesmas transformações do treino.
    modelo = Pipeline([
        ("imputer", SimpleImputer(strategy="median")),
        ("modelo", RandomForestClassifier(n_estimators=100, max_depth=5, random_state=42)),
    ])
    modelo.fit(X_train, y_train)
    y_pred = modelo.predict(X_test)

    print("\n=== AVALIACAO ===")
    print(f"{'':<10}{'accuracy':>10}{'recall':>10}{'f1':>10}")
    for nome, pred in [("baseline", baseline(X_test)), ("modelo", y_pred)]:
        print(f"{nome:<10}{accuracy_score(y_test, pred):>10.3f}"
              f"{recall_score(y_test, pred):>10.3f}{f1_score(y_test, pred):>10.3f}")
    print("\n" + classification_report(y_test, y_pred))

    joblib.dump(modelo, AQUI / "model.joblib")
    print(f"Modelo salvo em {AQUI / 'model.joblib'}")


if __name__ == "__main__":
    main()
