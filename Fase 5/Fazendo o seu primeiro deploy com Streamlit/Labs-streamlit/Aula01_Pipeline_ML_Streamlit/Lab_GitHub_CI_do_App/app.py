"""Aula 01 · Lab GitHub — o mesmo app da Parte 3, agora protegido por testes automáticos.

    streamlit run app.py      # rodar o app
    pytest tests/ -v          # rodar os testes
"""
from pathlib import Path

import joblib
import pandas as pd
import streamlit as st

MODELO = Path(__file__).parent / "modelo_churn.joblib"

# EXERCÍCIO 2: coloque o seu nome aqui
AUTOR = "Seu nome"


@st.cache_resource  # carrega o modelo UMA vez, não a cada interação
def load_model():
    return joblib.load(MODELO)


model = load_model()

st.title("Previsão de Churn de Clientes")
st.caption(f"Publicado por {AUTOR} · POSTECH · Deploy e Monitoramento de ML")

idade = st.slider("Idade do cliente", 18, 90, 35)
meses = st.number_input("Meses como cliente", min_value=0, max_value=120, value=12)
valor = st.number_input("Valor mensal (R$)", min_value=0.0, value=79.90, step=10.0)
limiar = st.slider("Limiar de risco", 0.1, 0.9, 0.5)

if st.button("Prever"):
    entrada = pd.DataFrame([[idade, meses, valor]], columns=["idade", "meses", "valor_mensal"])
    proba = model.predict_proba(entrada)[0][1]
    st.metric("Probabilidade de churn", f"{proba:.1%}")
    if proba > limiar:
        st.warning("Cliente em risco — sugerir ação de retenção.")
    else:
        st.success("Cliente com baixo risco de cancelamento.")
