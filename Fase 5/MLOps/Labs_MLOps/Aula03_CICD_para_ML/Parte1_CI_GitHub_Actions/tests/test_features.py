"""Testes unitários da função de feature engineering."""
import os
import sys

import pandas as pd

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from features import COLUNAS, preparar_features  # noqa: E402


def _df_exemplo():
    return pd.DataFrame({
        "idade": [22, None, 130],
        "meses": [2, 40, 12],
        "valor_mensal": [99.9, 150.0, 80.0],
        "chamados_suporte": [3, 0, 1],
        "churn": [1, 0, 0],
    })


def test_nao_tem_nulos():
    assert preparar_features(_df_exemplo()).isnull().sum().sum() == 0


def test_idade_fica_em_faixa_valida():
    idade = preparar_features(_df_exemplo())["idade"]
    assert idade.between(18, 100).all()


def test_cliente_novo_e_binario():
    resultado = preparar_features(_df_exemplo())
    assert resultado["cliente_novo"].tolist() == [1, 0, 0]


def test_colunas_esperadas_e_sem_target():
    resultado = preparar_features(_df_exemplo())
    assert list(resultado.columns) == COLUNAS
    assert "churn" not in resultado.columns


def test_nao_altera_o_dataframe_original():
    df = _df_exemplo()
    preparar_features(df)
    assert df["idade"].isnull().sum() == 1
