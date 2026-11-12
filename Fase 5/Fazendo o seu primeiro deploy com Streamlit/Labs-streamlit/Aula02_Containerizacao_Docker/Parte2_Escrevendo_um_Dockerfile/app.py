from pathlib import Path

import joblib
import pandas as pd
import streamlit as st

MODELO = Path(__file__).parent / "modelo_churn.joblib"


@st.cache_resource  # carrega o modelo UMA vez, não a cada interação
def load_model():
    return joblib.load(MODELO)


model = load_model()

st.title("Previsão de Churn de Clientes")
st.caption("Aula 02 · Parte 2 — rodando dentro de um container Docker")

idade = st.slider("Idade do cliente", 18, 90, 35)
meses = st.number_input("Meses como cliente", min_value=0, max_value=120, value=12)
valor = st.number_input("Valor mensal (R$)", min_value=0.0, value=79.90, step=10.0)

# TODO (exercício 1): adicione aqui um widget para o limiar de decisão,
# por exemplo: limiar = st.slider("Limiar de risco", 0.1, 0.9, 0.5)
limiar = 0.5

if st.button("Prever"):
    entrada = pd.DataFrame([[idade, meses, valor]], columns=["idade", "meses", "valor_mensal"])
    proba = model.predict_proba(entrada)[0][1]
    st.metric("Probabilidade de churn", f"{proba:.1%}")
    if proba > limiar:
        st.warning("Cliente em risco — sugerir ação de retenção.")
    else:
        st.success("Cliente com baixo risco de cancelamento.")
