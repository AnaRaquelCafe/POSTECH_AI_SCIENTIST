"""Aula 04 - Parte 1: API de predição de churn com FastAPI + Pydantic."""
import socket
from contextlib import asynccontextmanager
from pathlib import Path

import joblib
import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel, Field

MODELO = Path(__file__).parent / "model.joblib"
modelo = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    global modelo
    # carrega o modelo UMA vez, na inicialização - não a cada requisição
    modelo = joblib.load(MODELO)
    yield


app = FastAPI(title="API de Predição de Churn", lifespan=lifespan)


class PredictionInput(BaseModel):
    idade: float = Field(..., ge=18, le=100, description="Idade do cliente")
    meses: int = Field(..., ge=0, description="Tempo de casa, em meses")
    valor_mensal: float = Field(..., gt=0, description="Valor da assinatura (R$)")
    chamados_suporte: int = Field(..., ge=0, description="Chamados nos últimos 90 dias")


class PredictionOutput(BaseModel):
    prediction: int
    probability: float


@app.get("/health")
def health():
    # hostname identifica qual container respondeu (útil quando houver réplicas)
    return {"status": "ok", "model_loaded": modelo is not None, "host": socket.gethostname()}


@app.post("/predict", response_model=PredictionOutput)
def predict(payload: PredictionInput):
    features = pd.DataFrame([payload.model_dump()])
    pred = modelo.predict(features)[0]
    proba = modelo.predict_proba(features)[0][1]
    return PredictionOutput(prediction=int(pred), probability=round(float(proba), 3))
