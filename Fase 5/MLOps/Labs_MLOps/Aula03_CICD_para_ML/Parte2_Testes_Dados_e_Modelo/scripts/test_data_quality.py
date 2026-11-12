"""Valida schema e qualidade básica dos dados antes de treinar.
Sai com código != 0 (falha o build) se alguma checagem não passar.

    python scripts/test_data_quality.py
"""
import sys
from pathlib import Path

import pandas as pd

DADOS = Path(__file__).resolve().parents[3] / "dados" / "clientes.csv"

COLUNAS_ESPERADAS = {"idade", "meses", "valor_mensal", "chamados_suporte", "churn"}
MAX_NULOS = 0.05                 # no máximo 5% de valores ausentes por coluna
TAXA_CHURN = (0.05, 0.60)        # fora dessa faixa, o rótulo provavelmente está errado


def validar(df: pd.DataFrame) -> list[str]:
    erros = []
    faltando = COLUNAS_ESPERADAS - set(df.columns)
    if faltando:
        return [f"Colunas faltando: {faltando}"]
    if len(df) < 1000:
        erros.append(f"Poucas linhas para treinar: {len(df)}")
    for col, frac in df.isnull().mean().items():
        if frac > MAX_NULOS:
            erros.append(f"{col}: {frac:.1%} de nulos (máximo {MAX_NULOS:.0%})")
    if not df["idade"].dropna().between(18, 100).all():
        erros.append("Existem idades fora da faixa 18-100")
    if (df["valor_mensal"] <= 0).any():
        erros.append("Existem valores mensais <= 0")
    if not set(df["churn"].unique()) <= {0, 1}:
        erros.append("A coluna churn tem valores diferentes de 0 e 1")
    taxa = df["churn"].mean()
    if not TAXA_CHURN[0] <= taxa <= TAXA_CHURN[1]:
        erros.append(f"Taxa de churn suspeita: {taxa:.1%}")
    return erros


def main():
    erros = validar(pd.read_csv(DADOS))
    if erros:
        print("FALHOU - problemas de qualidade de dados:")
        for e in erros:
            print(" -", e)
        sys.exit(1)
    print("Dados OK - todas as checagens de qualidade passaram.")


if __name__ == "__main__":
    main()
