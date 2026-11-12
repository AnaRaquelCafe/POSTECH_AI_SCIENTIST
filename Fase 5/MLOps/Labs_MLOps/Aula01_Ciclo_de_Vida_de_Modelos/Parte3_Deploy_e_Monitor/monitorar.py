"""Aula 01 - Parte 3: compara o Data Capture com os dados de treino (baseline).

    python monitorar.py

Gera relatorio_monitoramento.html (Evidently) e imprime um resumo por coluna.
Em produção, este script rodaria agendado (ex.: a cada hora, via cron).
"""
from pathlib import Path

import pandas as pd
from evidently import Report
from evidently.presets import DataDriftPreset

AQUI = Path(__file__).parent
DADOS = AQUI.parents[1] / "dados" / "clientes.csv"
CAPTURA = AQUI / "captura" / "captura.csv"

if not CAPTURA.exists():
    raise SystemExit("Sem dados capturados: rode simular_producao.py primeiro.")

colunas = ["idade", "meses", "valor_mensal", "chamados_suporte"]
baseline = pd.read_csv(DADOS)[colunas]
atual = pd.read_csv(CAPTURA)[colunas]

resultado = Report([DataDriftPreset()]).run(reference_data=baseline, current_data=atual)
saida = AQUI / "relatorio_monitoramento.html"
resultado.save_html(str(saida))

print(f"{'coluna':<18}{'média baseline':>16}{'média produção':>16}")
for col in colunas:
    print(f"{col:<18}{baseline[col].mean():>16.1f}{atual[col].mean():>16.1f}")
print(f"\nRelatório completo: {saida}")
print("Para abrir: python -m http.server 8000  (e clique em relatorio_monitoramento.html)")
