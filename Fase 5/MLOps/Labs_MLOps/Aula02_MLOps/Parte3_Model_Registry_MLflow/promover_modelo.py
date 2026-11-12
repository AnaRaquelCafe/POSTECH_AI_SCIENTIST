"""Aula 02 - Parte 3: valida o @challenger e, se ele for melhor, o promove a @champion.

    python promover_modelo.py              # promoção com validação
    python promover_modelo.py --versao 1   # move @champion à força para a versão 1 (ex.: rollback)

Promover ou voltar atrás é só mover o alias. Quem consome o modelo carrega
"models:/churn-model@champion" e não precisa mudar nada.
"""
import argparse
from pathlib import Path

import mlflow
from mlflow import MlflowClient
from mlflow.exceptions import MlflowException

RAIZ = Path(__file__).resolve().parents[2]
NOME_MODELO = "churn-model"
F1_MINIMO = 0.55

parser = argparse.ArgumentParser()
parser.add_argument("--versao", help="força @champion para esta versão (rollback)")
args = parser.parse_args()

mlflow.set_tracking_uri(f"sqlite:///{RAIZ / 'mlflow.db'}")
client = MlflowClient()


def versao_do_alias(alias):
    try:
        return client.get_model_version_by_alias(NOME_MODELO, alias)
    except MlflowException:
        return None


def f1(versao):
    return client.get_run(versao.run_id).data.metrics["f1_score"]


if args.versao:
    client.set_registered_model_alias(NOME_MODELO, "champion", args.versao)
    print(f"@champion movido manualmente: agora aponta para a versão {args.versao} (sem validação).")
    raise SystemExit(0)

challenger = versao_do_alias("challenger")
if challenger is None:
    raise SystemExit("Não há @challenger. Rode registrar_modelo.py primeiro.")
champion = versao_do_alias("champion")

print(f"@challenger = v{challenger.version} | f1={f1(challenger):.3f}")
if champion:
    print(f"@champion   = v{champion.version} | f1={f1(champion):.3f}")
else:
    print("@champion   = (nenhum ainda)")

# Validação simulada: passa no mínimo do negócio e não é pior que o modelo atual
if f1(challenger) < F1_MINIMO:
    print(f"NÃO promovido: f1 abaixo do mínimo de {F1_MINIMO}.")
elif champion and f1(challenger) < f1(champion):
    print("NÃO promovido: o candidato é pior que o modelo em produção.")
else:
    client.set_registered_model_alias(NOME_MODELO, "champion", challenger.version)
    client.delete_registered_model_alias(NOME_MODELO, "challenger")
    print(f"Promovido: @champion agora aponta para a versão {challenger.version}.")
