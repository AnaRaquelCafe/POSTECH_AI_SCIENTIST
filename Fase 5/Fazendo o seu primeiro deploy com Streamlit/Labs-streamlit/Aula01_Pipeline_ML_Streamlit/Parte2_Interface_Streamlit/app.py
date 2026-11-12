"""Aula 01 · Parte 2 — Interface de predição com Streamlit.

    streamlit run app.py
"""
import time
from pathlib import Path

import joblib
import pandas as pd
import streamlit as st

MODELO = Path(__file__).parent / "modelo_churn.joblib"


@st.cache_resource  # EXERCÍCIO 3: comente esta linha e veja o que acontece
def load_model():
    print("Carregando o modelo do disco...", flush=True)  # aparece no terminal
    time.sleep(2)  # simula um modelo grande, que demora para carregar
    return joblib.load(MODELO)


model = load_model()

# Conta quantas vezes o script inteiro foi executado nesta sessão do navegador
st.session_state.execucoes = st.session_state.get("execucoes", 0) + 1
st.sidebar.metric("Execuções do script", st.session_state.execucoes)

st.title("Previsão de Churn de Clientes")
st.caption("Aula 01 · Parte 2 — POSTECH · Deploy e Monitoramento de ML")

idade = st.slider("Idade do cliente", 18, 90, 35)
meses = st.number_input("Meses como cliente", min_value=0, max_value=120, value=12)
valor = st.number_input("Valor mensal (R$)", min_value=0.0, value=79.90, step=10.0)

# TODO (exercício 4): troque a linha abaixo por um widget, por exemplo:
# limiar = st.slider("Limiar de risco", 0.1, 0.9, 0.5)
limiar = 0.5

if st.button("Prever"):
    entrada = pd.DataFrame([[idade, meses, valor]], columns=["idade", "meses", "valor_mensal"])
    proba = model.predict_proba(entrada)[0][1]
    st.metric("Probabilidade de churn", f"{proba:.1%}")
    if proba > limiar:
        st.warning("Cliente em risco — sugerir ação de retenção.")
    else:
        st.success("Cliente com baixo risco de cancelamento.")

# DESAFIO EXTRA (exercício 5): cole aqui o bloco de predição em lote do README.
