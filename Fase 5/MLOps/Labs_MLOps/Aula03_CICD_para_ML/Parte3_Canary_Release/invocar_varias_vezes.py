"""Aula 03 - Parte 3: chama o endpoint várias vezes e conta quem respondeu.

    python invocar_varias_vezes.py
"""
from collections import Counter

import requests

URL = "http://localhost:8000"
N_CHAMADAS = 200
cliente = {"idade": 23, "meses": 2, "valor_mensal": 210.0, "chamados_suporte": 4}

print("Pesos atuais:", requests.get(f"{URL}/pesos", timeout=5).json())
contagem = Counter()
for _ in range(N_CHAMADAS):
    resp = requests.post(f"{URL}/predict", json=cliente, timeout=5).json()
    contagem[f"{resp['variante']} (v{resp['versao']})"] += 1

print(f"Distribuição de tráfego em {N_CHAMADAS} chamadas:")
for variante, qtd in sorted(contagem.items()):
    print(f"  {variante}: {qtd} ({qtd / N_CHAMADAS:.0%})")
