"""Aula 01 - Parte 3: envia um cliente para o endpoint e mostra a predição."""
import requests

URL = "http://localhost:5001/invocations"

cliente = {
    "dataframe_split": {
        "columns": ["idade", "meses", "valor_mensal", "chamados_suporte"],
        "data": [[23, 2, 210.0, 4]],   # jovem, cliente novo, mensalidade alta, muitos chamados
    }
}
resp = requests.post(URL, json=cliente, timeout=10)
resp.raise_for_status()
print("Resposta do endpoint:", resp.json())
