# Parte 2 — Docker e registry de imagens (≈ 15 min)

**Objetivo:** empacotar a API da Parte 1 numa imagem Docker otimizada e publicá-la num registry, de onde qualquer servidor consegue baixá-la.
**Conceitos da aula:** Dockerfile multi-stage, usuário não-root, `HEALTHCHECK`, cache de camadas, registry de imagens.

> Pré-requisito: `model.joblib` gerado na Parte 1 (`python treinar_modelo_exemplo.py`).

```bash
cd Labs_MLOps/Aula04_Deploy_APIs_e_Containers/Parte2_Docker_e_Registry
```

**1. Build e execução local (5 min):**
```bash
docker build -t churn-api -f Dockerfile ../Parte1_API_com_FastAPI
docker run --rm -d -p 8000:8000 --name churn churn-api
docker ps          # aguarde a coluna STATUS mostrar (healthy)
curl localhost:8000/health
docker stop churn
```
Leia o `Dockerfile`: o estágio `builder` instala as dependências e a imagem final só copia o resultado, roda como `appuser` e tem um `HEALTHCHECK` batendo no `/health`.

**2. Suba um registry e publique a imagem (5 min).** O registry é o "repositório de imagens" (como ECR, GHCR ou Docker Hub). Aqui ele roda num container, na porta 5050:
```bash
docker run -d -p 5050:5000 --name registry registry:2
docker tag churn-api localhost:5050/churn-api:v1
docker push localhost:5050/churn-api:v1
curl localhost:5050/v2/_catalog
```

**3. Prove que a imagem vem do registry (3 min):**
```bash
docker rmi churn-api localhost:5050/churn-api:v1
docker run --rm -d -p 8000:8000 --name churn localhost:5050/churn-api:v1
curl localhost:8000/health
docker stop churn
```
O `docker run` baixou a imagem do registry, exatamente o que um servidor em produção faz.

> Os passos 1 e 2 estão juntos em `./build_and_push.sh`. Deixe o registry rodando: a Parte 3 usa a imagem publicada aqui.

## Para discutir
- Por que `COPY requirements.txt` + `pip install` vêm **antes** de copiar o código? O que acontece com o tempo de build quando você muda só o `main.py`?
- Numa empresa, quem deveria poder dar `push` no registry: qualquer desenvolvedor ou só o pipeline de CI?
