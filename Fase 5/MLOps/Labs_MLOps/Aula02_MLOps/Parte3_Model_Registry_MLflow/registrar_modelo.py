"""Aula 02 - Parte 3: registra o melhor run da Parte 2 e o marca como candidato.

    python registrar_modelo.py            # registra o run com maior f1_score
    python registrar_modelo.py --ultimo   # registra o run mais recente

Pega um run do experimento "previsao-churn", cria uma nova versão de
"churn-model" e atribui a ela o alias @challenger.
"""
import argparse
from pathlib import Path

import mlflow
from mlflow import MlflowClient

RAIZ = Path(__file__).resolve().parents[2]
EXPERIMENTO = "previsao-churn"
NOME_MODELO = "churn-model"

parser = argparse.ArgumentParser()
parser.add_argument("--ultimo", action="store_true", help="usa o run mais recente, não o melhor")
args = parser.parse_args()

mlflow.set_tracking_uri(f"sqlite:///{RAIZ / 'mlflow.db'}")
client = MlflowClient()

experimento = client.get_experiment_by_name(EXPERIMENTO)
runs = client.search_runs(
    experiment_ids=[experimento.experiment_id],
    order_by=["attributes.start_time DESC" if args.ultimo else "metrics.f1_score DESC"],
    max_results=1,
) if experimento else []
if not runs:
    raise SystemExit("Nenhum run encontrado. Rode o treino da Parte 2 primeiro.")

run = runs[0]
print(f"Run escolhido: {run.info.run_id[:8]} | f1_score={run.data.metrics['f1_score']:.3f}")

# No MLflow 3, o modelo salvo pelo run fica em models:/<model_id> (não mais em runs:/<id>/model)
modelo_do_run = run.outputs.model_outputs[0].model_id
versao = mlflow.register_model(f"models:/{modelo_do_run}", NOME_MODELO).version
client.set_registered_model_alias(NOME_MODELO, "challenger", versao)
print(f"{NOME_MODELO} versão {versao} registrada como @challenger")
