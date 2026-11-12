# Aula 02 · Parte 3 — Boas práticas, volumes e Docker Compose (≈ 15 min)

**Objetivo:** aplicar boas práticas de segurança e tamanho de imagem, tirar o modelo de dentro da imagem com um volume e subir dois serviços juntos com o Docker Compose.
**Conceitos da parte:** usuário não-root, `.dockerignore`, imagem base slim com versão fixada, volumes, `docker-compose.yml`, scanning de vulnerabilidades.

> Se algum app ainda estiver rodando na porta 8501, pare-o antes (Ctrl+C no terminal dele).

```bash
cd Labs-streamlit/Aula02_Containerizacao_Docker/Parte3_Boas_Praticas_e_Compose
```

## 1. Rode como usuário não-root (3 min)
Leia o `Dockerfile`: cada boa prática está comentada. Depois:
```bash
docker build -t churn-app:seguro .
docker run --rm churn-app:seguro whoami
docker run --rm python:3.12-slim whoami
```
A nossa imagem roda como `appuser`; a imagem base, como `root`. Se alguém explorar uma falha no app, quanto estrago consegue fazer em cada caso?

## 2. O que não deve entrar na imagem (4 min)
Simule um dataset bruto de 100 MB esquecido na pasta do projeto:
```bash
mkdir -p dados && head -c 100000000 /dev/urandom > dados/historico_bruto.csv
docker build -t churn-app:seguro .
```
Procure na saída a linha `transferring context`: menos de 1 kB, porque o `.dockerignore` exclui a pasta `dados/`. Agora comente a linha `dados/` no `.dockerignore` (coloque `#` na frente) e reconstrua:
```bash
docker build -t churn-app:seguro .
docker images churn-app
```
O contexto passou de 100 MB e a imagem cresceu na mesma proporção. Desfaça o comentário e apague o arquivo:
```bash
rm -rf dados
```

## 3. Modelo fora da imagem, com volume (3 min)
```bash
docker run --rm -p 8501:8501 -v "$(pwd)/modelos:/app/modelos" churn-app:seguro
```
Abra a porta 8501: a barra lateral mostra a versão do modelo e o usuário do processo. Num **segundo terminal**, na mesma pasta, simule a chegada de um modelo novo:
```bash
echo "v2 (retreinado)" > modelos/versao.txt
```
Volte ao app e clique em **Rerun** (menu ⋮ no canto superior direito): a versão mudou **sem reconstruir a imagem**. Pare com Ctrl+C e restaure o arquivo:
```bash
echo "v1 (treinado em set/2026)" > modelos/versao.txt
```

## 4. Dois serviços com Docker Compose (4 min)
O `docker-compose.yml` sobe o app e um segundo serviço, `monitor`, que verifica a saúde do app a cada 5 segundos:
```bash
docker compose up --build
```
Observe os logs: no início o monitor diz `app fora do ar` (o Streamlit ainda está subindo) e depois `app saudável`. O monitor chama o app pelo **nome do serviço** (`http://app:8501`): o Compose cria uma rede onde os serviços se enxergam pelo nome. Pare com Ctrl+C e remova tudo:
```bash
docker compose down
```

## Para ir além (opcional, ≈ 2 min): scanning de vulnerabilidades
```bash
docker run --rm -v /var/run/docker.sock:/var/run/docker.sock aquasec/trivy:0.69.3 image --severity HIGH,CRITICAL --scanners vuln churn-app:seguro
```
O Trivy lista as vulnerabilidades conhecidas nos pacotes da imagem. Em pipelines de CI/CD, essa verificação roda a cada build.

## Lab GitHub
A pasta [`Lab_GitHub_GHCR`](../Lab_GitHub_GHCR/) faz o GitHub Actions construir esta imagem a cada push e publicá-la no GitHub Container Registry, de onde você a roda com uma URL pública.

## Para discutir
- O modelo deveria ir dentro da imagem ou num volume? Pense em quem retreina o modelo e com que frequência.
- Por que "uma responsabilidade por container" (app e monitor separados) é melhor do que colocar tudo no mesmo container?
