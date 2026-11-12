# Aula 02 · Parte 2 — Escrevendo um Dockerfile (≈ 15 min)

**Objetivo:** empacotar o app de churn da Aula 01 numa imagem Docker e descobrir, na prática, por que a ordem das instruções do Dockerfile importa.
**Conceitos da parte:** `FROM`, `WORKDIR`, `COPY`, `RUN`, `EXPOSE`, `CMD`, build e run, mapeamento de portas, camadas e cache de build.

> Se algum app ainda estiver rodando na porta 8501, pare-o antes (Ctrl+C no terminal dele).

```bash
cd Labs-streamlit/Aula02_Containerizacao_Docker/Parte2_Escrevendo_um_Dockerfile
```

## 1. Construa e rode a imagem (4 min)
Leia o `Dockerfile` (são 6 instruções). Depois:
```bash
docker build -t churn-app .
docker run --rm -p 8501:8501 churn-app
```
Abra a porta 8501, confira o app e pare com Ctrl+C. Anote quanto tempo o build levou.

## 2. Mude uma linha de código e reconstrua (3 min)
Em `app.py`, altere o texto do `st.caption(...)`. Depois:
```bash
docker build -t churn-app .
```
Observe a saída: o `pip install` rodou **de novo**, inteiro, só porque você mudou um texto. Por quê?

## 3. Corrija o Dockerfile (5 min)
Dica: cada instrução gera uma camada, e o Docker só reaproveita uma camada se ela e **todas as anteriores** não mudaram. O `COPY . .` vem antes do `pip install`…

Reorganize o Dockerfile e faça um build. Depois altere o `app.py` de novo e reconstrua: agora a etapa do `pip install` deve aparecer como `CACHED` e o build termina em segundos.

A resposta está em `solucao/Dockerfile`.

## 4. Inspecione a imagem (3 min)
```bash
docker images churn-app          # tamanho final
docker history churn-app         # as camadas, uma por instrução
```
No `docker history`, a camada do `pip install` é de longe a maior. É justamente ela que o cache evita refazer.

## Para discutir
- Em projetos de ML, instalar dependências pode levar vários minutos. Quanto tempo essa ordem economiza por dia numa equipe?
- Um *multi-stage build* separa a fase de build da fase de execução. O que poderia ficar de fora da imagem final num projeto de ML?
