"""Aula 01 · Parte 1 — Um pipeline de ML organizado em etapas.

    python train.py

Ingestão → pré-processamento + treino (um único Pipeline) → avaliação → serialização.
Dados sintéticos, só para fins didáticos.
"""
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression  # noqa: F401  (usado no exercício 4)
from sklearn.metrics import f1_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

AQUI = Path(__file__).parent
DESTINO = AQUI / "modelo_churn.joblib"

# EXERCÍCIO 5: troque 42 por None, rode duas vezes e compare o F1.
SEMENTE = 42


def ingerir(n=3000):
    """Etapa 1 — Ingestão. Aqui geramos dados; na empresa seria um banco ou um data lake."""
    rng = np.random.default_rng(SEMENTE)
    df = pd.DataFrame({
        "idade": rng.integers(18, 90, n),
        "meses": rng.integers(0, 72, n),
        "valor_mensal": rng.uniform(20, 200, n).round(2),
    })
    # Regra sintética: cliente novo e com mensalidade alta cancela mais
    logito = 0.03 * (40 - df["idade"]) + 0.06 * (12 - df["meses"]) + 0.015 * (df["valor_mensal"] - 90)
    y = (rng.random(n) < 1 / (1 + np.exp(-logito))).astype(int)
    return df, y


def construir_pipeline():
    """Etapa 2 — Pré-processamento + modelo encadeados em um único objeto."""
    return Pipeline([
        ("scaler", StandardScaler()),
        ("model", RandomForestClassifier(n_estimators=100, max_depth=6, random_state=SEMENTE)),
        # EXERCÍCIO 4: troque a linha acima por
        # ("model", LogisticRegression()),
    ])


def avaliar(pipeline, X_test, y_test):
    """Etapa 3 — Avaliação em dados que o modelo nunca viu."""
    return f1_score(y_test, pipeline.predict(X_test))


def serializar(pipeline):
    """Etapa 4 — Serialização: pré-processamento + modelo em um único artefato."""
    joblib.dump(pipeline, DESTINO)


if __name__ == "__main__":
    X, y = ingerir()
    print(f"[1/4] Ingestão ............ {len(X)} clientes, {y.mean():.0%} cancelaram")

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=SEMENTE)
    pipeline = construir_pipeline()
    pipeline.fit(X_train, y_train)
    print(f"[2/4] Treino .............. {' → '.join(pipeline.named_steps)}"
          f" ({type(pipeline.named_steps['model']).__name__})")

    print(f"[3/4] Avaliação ........... F1 no teste = {avaliar(pipeline, X_test, y_test):.3f}")

    serializar(pipeline)
    print(f"[4/4] Serialização ........ {DESTINO.name} ({DESTINO.stat().st_size / 1024:.0f} KB)")
