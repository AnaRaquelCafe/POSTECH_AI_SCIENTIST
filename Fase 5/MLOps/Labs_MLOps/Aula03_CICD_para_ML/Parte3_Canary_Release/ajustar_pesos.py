"""Aula 03 - Parte 3: muda a divisão de tráfego sem derrubar o endpoint.

    python ajustar_pesos.py 50 50    # avança o canário
    python ajustar_pesos.py 0 100    # canário assume todo o tráfego
    python ajustar_pesos.py 100 0    # rollback: tudo de volta para o principal
"""
import sys

import requests

if len(sys.argv) != 3:
    raise SystemExit("Uso: python ajustar_pesos.py <peso_principal> <peso_canario>")

novos = {"principal": int(sys.argv[1]), "canario": int(sys.argv[2])}
resp = requests.post("http://localhost:8000/pesos", json=novos, timeout=5)
resp.raise_for_status()
print("Pesos atualizados:", resp.json())
