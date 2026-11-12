"""Aula 02 · Lab GitHub — o app de churn da Parte 3, publicado como imagem no GHCR."""
import getpass
from pathlib import Path

import joblib
import pandas as pd
import streamlit as st

PASTA_MODELOS = Path(__file__).parent / "modelos"


@st.cache_resource
def load_model():
    return joblib.load(PASTA_MODELOS / "modelo_churn.joblib")


model = load_model()
versao = (PASTA_MODELOS / "versao.txt").read_text(encoding="utf-8").strip()

st.sidebar.write(f"Versão do modelo: **{versao}**")
st.sidebar.write(f"Processo rodando como: `{getpass.getuser()}`")

st.title("Previsão de Churn de Clientes")
st.caption("Aula 02 · Lab GitHub — imagem publicada no GitHub Container Registry")

idade = st.slider("Idade do cliente", 18, 90, 35)
meses = st.number_input("Meses como cliente", min_value=0, max_value=120, value=12)
valor = st.number_input("Valor mensal (R$)", min_value=0.0, value=79.90, step=10.0)

if st.button("Prever"):
    entrada = pd.DataFrame([[idade, meses, valor]], columns=["idade", "meses", "valor_mensal"])
    proba = model.predict_proba(entrada)[0][1]
    st.metric("Probabilidade de churn", f"{proba:.1%}")
    if proba > 0.5:
        st.warning("Cliente em risco — sugerir ação de retenção.")
    else:
        st.success("Cliente com baixo risco de cancelamento.")
