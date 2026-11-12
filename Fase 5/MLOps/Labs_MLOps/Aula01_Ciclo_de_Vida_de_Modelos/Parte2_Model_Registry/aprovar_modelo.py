"""Aula 01 - Parte 2: gate de qualidade. Aprova (ou rejeita) a última versão pendente.

    python aprovar_modelo.py            # aprova se passar no critério mínimo
    python aprovar_modelo.py --rejeitar # simula um revisor humano reprovando
"""
import argparse
from pathlib import Path

import mlflow
from mlflow import MlflowClient

RAIZ = Path(__file__).resolve().parents[2]
NOME_MODELO = "churn-model"
RECALL_MINIMO = 0.45   # critério de negócio: não deixar escapar clientes em risco

parser = argparse.ArgumentParser()
parser.add_argument("--rejeitar", action="store_true")
args = parser.parse_args()

mlflow.set_tracking_uri(f"sqlite:///{RAIZ / 'mlflow.db'}")
client = MlflowClient()

pendentes = client.search_model_versions(
    f"name='{NOME_MODELO}' and tags.aprovacao='PendingManualApproval'"
)
if not pendentes:
    raise SystemExit("Nenhuma versão pendente de aprovação. Rode registrar_modelo.py primeiro.")

versao = max(pendentes, key=lambda v: int(v.version))
recall = client.get_run(versao.run_id).data.metrics["recall"]
print(f"{NOME_MODELO} v{versao.version}: recall={recall:.3f} (mínimo {RECALL_MINIMO})")

if args.rejeitar or recall < RECALL_MINIMO:
    status = "Rejected"
else:
    status = "Approved"
client.set_model_version_tag(NOME_MODELO, versao.version, "aprovacao", status)
print(f"-> {status}")
