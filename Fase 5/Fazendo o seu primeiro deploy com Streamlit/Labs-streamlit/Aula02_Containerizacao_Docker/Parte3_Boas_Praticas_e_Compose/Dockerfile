# Aula 02 · Parte 3 — Dockerfile com boas práticas.

# Imagem slim, com a versão fixada (nada de python:latest)
FROM python:3.12-slim

WORKDIR /app

# Dependências antes do código: aproveita o cache de build (Parte 2)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Segurança: cria um usuário sem privilégios para rodar o app
RUN useradd --create-home appuser

COPY . .

USER appuser

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
