"""Aula 03 - Parte 3: endpoint único com duas variantes (canary release).

    uvicorn roteador:app --port 8000

Cada requisição vai para o @champion ("Principal") ou para o @challenger
("Canario"), sorteada de acordo com os pesos. Os pesos mudam em tempo real,
sem derrubar o endpoint, pelo POST /pesos.
"""
import logging
import random
import warnings
from contextlib import asynccontextmanager
from pathlib import Path

import mlflow
import pandas as pd
from fastapi import FastAPI
from mlflow import MlflowClient
from pydantic import BaseModel, Field

warnings.filterwarnings("ignore")
logging.getLogger("mlflow").setLevel(logging.ERROR)

RAIZ = Path(__file__).resolve().parents[2]
NOME_MODELO = "churn-model"
variantes = {}                                  # nome -> (versão, modelo)
pesos = {"Principal": 90, "Canario": 10}


@asynccontextmanager
async def lifespan(app: FastAPI):
    mlflow.set_tracking_uri(f"sqlite:///{RAIZ / 'mlflow.db'}")
    client = MlflowClient()
    for nome, alias in [("Principal", "champion"), ("Canario", "challenger")]:
        versao = client.get_model_version_by_alias(NOME_MODELO, alias).version
        variantes[nome] = (versao, mlflow.sklearn.load_model(f"models:/{NOME_MODELO}@{alias}"))
        print(f"{nome}: {NOME_MODELO} v{versao} (@{alias})")
    yield


app = FastAPI(title="Canary de churn", lifespan=lifespan)


class Cliente(BaseModel):
    idade: float = Field(..., ge=18, le=100)
    meses: int = Field(..., ge=0)
    valor_mensal: float = Field(..., gt=0)
    chamados_suporte: int = Field(..., ge=0)


class Pesos(BaseModel):
    principal: int = Field(..., ge=0)
    canario: int = Field(..., ge=0)


@app.post("/predict")
def predict(cliente: Cliente):
    nome = random.choices(list(pesos), weights=list(pesos.values()))[0]
    versao, modelo = variantes[nome]
    proba = modelo.predict_proba(pd.DataFrame([cliente.model_dump()]))[0][1]
    return {"variante": nome, "versao": versao, "probabilidade_churn": round(float(proba), 3)}


@app.get("/pesos")
def ver_pesos():
    return pesos


@app.post("/pesos")
def ajustar_pesos(novos: Pesos):
    pesos.update({"Principal": novos.principal, "Canario": novos.canario})
    return pesos
