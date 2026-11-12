"""Aula 03 · Parte 3 — Reagindo ao drift: alertas, gatilho de re-treino e Evidently.

    python monitorar.py

Simula 12 semanas de produção. Toda semana o PSI de cada feature é comparado
com a referência. Alertas repetidos disparam o re-treino, e o modelo novo
passa a usar os dados recentes como referência.
"""
from pathlib import Path

import numpy as np
import pandas as pd

AQUI = Path(__file__).parent

# ---------------------------------------------------------------------------
# EXERCÍCIO: ajuste a política de alertas e rode de novo.
# ---------------------------------------------------------------------------
LIMIAR_ALERTA = 0.2                  # PSI a partir do qual a semana gera alerta
SEMANAS_SEGUIDAS_PARA_RETREINO = 2   # alertas consecutivos que disparam o re-treino

rng = np.random.default_rng(11)


def gerar(n, desloc_idade=0.0):
    return pd.DataFrame({
        "idade": np.clip(rng.normal(45, 14, n) + desloc_idade, 18, 90).round(),
        "meses": np.clip(rng.normal(24, 15, n), 0, 120).round(),
        "valor_mensal": rng.uniform(20, 200, n).round(2),
    })


def deslocamento_da_semana(semana):
    if semana == 3:
        return -8.0                          # campanha pontual para universitários
    if semana >= 6:
        return 2.5 * (semana - 5)            # a base envelhece de forma contínua
    return 0.0


def psi(ref, atual, bins=10):
    cortes = np.unique(np.quantile(ref, np.linspace(0, 1, bins + 1)))
    cortes[0], cortes[-1] = -np.inf, np.inf
    p_ref = np.clip(np.histogram(ref, cortes)[0] / len(ref), 1e-6, None)
    p_atual = np.clip(np.histogram(atual, cortes)[0] / len(atual), 1e-6, None)
    return float(np.sum((p_atual - p_ref) * np.log(p_atual / p_ref)))


referencia = gerar(5000)
historico = []                 # semanas recentes, usadas no re-treino
alertas_seguidos = 0
retreinos = 0
pior = None                    # (psi, semana, dados) da semana mais problemática

print(f"Política: alerta se PSI ≥ {LIMIAR_ALERTA}; re-treino após "
      f"{SEMANAS_SEGUIDAS_PARA_RETREINO} alerta(s) seguido(s)\n")
print(f"{'semana':>6}  {'PSI idade':>9}  {'PSI meses':>9}  {'PSI valor':>9}  ação")
print("-" * 70)
for semana in range(1, 13):
    atual = gerar(1000, deslocamento_da_semana(semana))
    historico = (historico + [atual])[-SEMANAS_SEGUIDAS_PARA_RETREINO:]
    valores = {col: psi(referencia[col], atual[col]) for col in referencia.columns}
    maior = max(valores.values())
    if pior is None or maior > pior[0]:
        pior = (maior, semana, atual)

    if maior >= LIMIAR_ALERTA:
        alertas_seguidos += 1
        acao = f"ALERTA ({alertas_seguidos}/{SEMANAS_SEGUIDAS_PARA_RETREINO})"
        if alertas_seguidos >= SEMANAS_SEGUIDAS_PARA_RETREINO:
            referencia = pd.concat(historico, ignore_index=True)   # nova referência
            alertas_seguidos = 0
            retreinos += 1
            acao += "  -> RE-TREINO disparado"
    else:
        alertas_seguidos = 0
        acao = "ok"
    print(f"{semana:>6}  {valores['idade']:>9.3f}  {valores['meses']:>9.3f}"
          f"  {valores['valor_mensal']:>9.3f}  {acao}")

print(f"\nTotal de re-treinos em 12 semanas: {retreinos}")

# Relatório visual do Evidently (API da versão 0.7.x) para a pior semana
from evidently import Report  # noqa: E402
from evidently.presets import DataDriftPreset  # noqa: E402

_, semana_pior, dados_pior = pior
resultado = Report([DataDriftPreset()]).run(reference_data=gerar(5000), current_data=dados_pior)
saida = AQUI / "relatorio_drift.html"
resultado.save_html(str(saida))
print(f"\nRelatório do Evidently (semana {semana_pior} vs. dados de treino) salvo em {saida.name}")
print("Para abrir: python -m http.server 8000  (e abra a porta 8000)")
