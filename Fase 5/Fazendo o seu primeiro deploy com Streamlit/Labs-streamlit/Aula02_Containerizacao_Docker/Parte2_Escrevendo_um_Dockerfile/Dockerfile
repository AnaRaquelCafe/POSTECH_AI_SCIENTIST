# ATENÇÃO: este Dockerfile funciona, mas tem um problema de performance
# proposital. Descobrir e corrigir esse problema é o exercício desta parte.

FROM python:3.12-slim

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
