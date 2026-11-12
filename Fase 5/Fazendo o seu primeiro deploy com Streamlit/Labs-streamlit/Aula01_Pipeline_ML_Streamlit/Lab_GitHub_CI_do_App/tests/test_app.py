"""Testes automáticos do app: simulam um usuário clicando na interface.

    pytest tests/ -v
"""
from pathlib import Path

from streamlit.testing.v1 import AppTest

APP = str(Path(__file__).parents[1] / "app.py")


def abrir_app():
    at = AppTest.from_file(APP, default_timeout=30).run()
    assert not at.exception, "o app quebrou ao abrir"
    return at


def preencher_e_prever(at, idade, meses, valor):
    at.slider[0].set_value(idade)          # idade
    at.number_input[0].set_value(meses)    # meses como cliente
    at.number_input[1].set_value(valor)    # valor mensal
    at.button[0].click().run()
    assert not at.exception
    return at


def test_app_abre_com_titulo():
    at = abrir_app()
    assert at.title[0].value == "Previsão de Churn de Clientes"


def test_cliente_de_alto_risco_gera_alerta():
    at = preencher_e_prever(abrir_app(), idade=22, meses=1, valor=190.0)
    assert at.metric[0].value.endswith("%")
    assert len(at.warning) == 1


def test_cliente_fiel_nao_gera_alerta():
    at = preencher_e_prever(abrir_app(), idade=60, meses=60, valor=30.0)
    assert len(at.success) == 1
    assert len(at.warning) == 0


def test_probabilidade_entre_0_e_100():
    at = preencher_e_prever(abrir_app(), idade=35, meses=12, valor=79.9)
    valor = float(at.metric[0].value.rstrip("%").replace(",", "."))
    assert 0 <= valor <= 100
