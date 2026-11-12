# Versão corrigida do Dockerfile da Aula 02 · Parte 2.
FROM python:3.12-slim

WORKDIR /app

# 1) Copia SÓ as dependências primeiro e instala.
#    Essa camada só é refeita quando o requirements.txt muda.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 2) Copia o código depois. Mudar o app.py agora só refaz esta camada.
COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
