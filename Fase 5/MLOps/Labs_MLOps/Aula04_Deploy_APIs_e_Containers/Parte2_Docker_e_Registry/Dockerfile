# Contexto do build: a pasta da Parte 1 (main.py, requirements.txt, model.joblib)
#   docker build -t churn-api -f Dockerfile ../Parte1_API_com_FastAPI

# Estágio 1: builder - instala as dependências
FROM python:3.12-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# Estágio 2: imagem final, enxuta (sem cache de pip nem ferramentas de build)
FROM python:3.12-slim
WORKDIR /app

# usuário não-root (boa prática de segurança)
RUN useradd --create-home appuser
COPY --from=builder /install /usr/local
COPY --chown=appuser:appuser main.py model.joblib ./
USER appuser

EXPOSE 8000

HEALTHCHECK --interval=10s --timeout=3s --start-period=10s \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')" || exit 1

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
