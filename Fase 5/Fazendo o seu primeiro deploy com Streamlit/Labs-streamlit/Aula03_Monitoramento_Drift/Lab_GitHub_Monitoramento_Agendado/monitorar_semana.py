"""Aula 03 · Lab GitHub — o job de monitoramento que o GitHub Actions roda toda semana.

    python monitorar_semana.py                       # semana normal
    DESLOCAMENTO_IDADE=8 python monitorar_semana.py  # clientes 8 anos mais velhos

Compara os dados "desta semana" com a referência (dados de treino), calcula o
PSI de cada feature, gera o relatório do Evidently e decide se há drift.
Quando roda no GitHub Actions, também escreve o resumo do job e avisa o
workflow se deve abrir uma issue.
"""
import datetime as dt
import os
from pathlib import Path

import numpy as np
import pandas as pd
from evidently import Report
from evidently.presets import DataDriftPreset

AQUI = Path(__file__).parent
LIMIAR_ALERTA = 0.2
DESLOCAMENTO_IDADE = float(os.environ.get("DESLOCAMENTO_IDADE", "0") or 0)
SEMANA = dt.date.today().isocalendar().week


def gerar(n, semente, desloc_idade=0.0):
    rng = np.random.default_rng(semente)
    return pd.DataFrame({
        "idade": np.clip(rng.normal(45, 14, n) + desloc_idade, 18, 90).round(),
        "meses": np.clip(rng.normal(24, 15, n), 0, 120).round(),
        "valor_mensal": rng.uniform(20, 200, n).round(2),
    })


def psi(ref, atual, bins=10):
    cortes = np.unique(np.quantile(ref, np.linspace(0, 1, bins + 1)))
    cortes[0], cortes[-1] = -np.inf, np.inf
    p_ref = np.clip(np.histogram(ref, cortes)[0] / len(ref), 1e-6, None)
    p_atual = np.clip(np.histogram(atual, cortes)[0] / len(atual), 1e-6, None)
    return float(np.sum((p_atual - p_ref) * np.log(p_atual / p_ref)))


referencia = gerar(5000, semente=0)                              # dados de treino
atual = gerar(1000, semente=SEMANA, desloc_idade=DESLOCAMENTO_IDADE)  # dados desta semana

valores = {col: psi(referencia[col], atual[col]) for col in referencia.columns}
drift = max(valores.values()) >= LIMIAR_ALERTA

linhas = [f"## Monitoramento de drift — semana {SEMANA}", "",
          f"Deslocamento simulado da idade: {DESLOCAMENTO_IDADE:+.0f} anos · limiar de alerta: PSI ≥ {LIMIAR_ALERTA}", "",
          "| feature | PSI | situação |", "|---|---|---|"]
for col, v in valores.items():
    linhas.append(f"| {col} | {v:.3f} | {'**DRIFT**' if v >= LIMIAR_ALERTA else 'ok'} |")
linhas += ["", "**Resultado:** " + ("drift detectado — avaliar re-treino." if drift else "sem drift relevante.")]
resumo = "\n".join(linhas) + "\n"

(AQUI / "resumo.md").write_text(resumo, encoding="utf-8")
Report([DataDriftPreset()]).run(reference_data=referencia, current_data=atual) \
    .save_html(str(AQUI / "relatorio_drift.html"))
print(resumo)
print("Relatório do Evidently: relatorio_drift.html")

# Integração com o GitHub Actions (essas variáveis só existem dentro do workflow)
if os.environ.get("GITHUB_STEP_SUMMARY"):
    with open(os.environ["GITHUB_STEP_SUMMARY"], "a", encoding="utf-8") as f:
        f.write(resumo)
if os.environ.get("GITHUB_OUTPUT"):
    with open(os.environ["GITHUB_OUTPUT"], "a", encoding="utf-8") as f:
        f.write(f"drift={'true' if drift else 'false'}\n")
