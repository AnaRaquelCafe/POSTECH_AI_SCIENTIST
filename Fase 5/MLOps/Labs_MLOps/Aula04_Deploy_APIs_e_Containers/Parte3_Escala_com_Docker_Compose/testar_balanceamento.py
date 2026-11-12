"""Aula 04 - Parte 3: chama o balanceador várias vezes e conta qual réplica respondeu.

    python testar_balanceamento.py
"""
from collections import Counter

import requests

URL = "http://localhost:8080"
N = 60
cliente = {"idade": 23, "meses": 2, "valor_mensal": 210, "chamados_suporte": 4}

print("Predição via balanceador:", requests.post(f"{URL}/predict", json=cliente, timeout=5).json())
contagem = Counter(requests.get(f"{URL}/health", timeout=5).json()["host"] for _ in range(N))
print(f"\nRéplicas que responderam em {N} chamadas:")
for host, qtd in sorted(contagem.items()):
    print(f"  container {host}: {qtd}")
