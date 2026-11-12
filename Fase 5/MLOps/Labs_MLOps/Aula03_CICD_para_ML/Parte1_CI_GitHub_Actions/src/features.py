"""Funções de feature engineering usadas pelo pipeline de treino."""
import pandas as pd

COLUNAS = ["idade", "meses", "valor_mensal", "chamados_suporte", "cliente_novo"]


def preparar_features(df: pd.DataFrame) -> pd.DataFrame:
    """Recebe o dataframe cru de clientes e devolve as features prontas para o modelo."""
    df = df.copy()
    df["idade"] = df["idade"].fillna(df["idade"].median()).clip(18, 100)
    df["cliente_novo"] = (df["meses"] < 6).astype(int)
    return df[COLUNAS]
