#!/usr/bin/env bash
# Faz build da imagem e publica no registry local (porta 5050).
#   ./build_and_push.sh [tag]      (tag padrão: v1)
set -euo pipefail
cd "$(dirname "$0")"

TAG="${1:-v1}"
REGISTRY="localhost:5050"
IMAGEM="${REGISTRY}/churn-api:${TAG}"

# 1. sobe o registry, se ainda não estiver rodando
docker ps --format '{{.Names}}' | grep -q '^registry$' \
  || docker run -d -p 5050:5000 --name registry registry:2

# 2. build (contexto = pasta da Parte 1)
docker build -t churn-api -f Dockerfile ../Parte1_API_com_FastAPI

# 3. tag com o endereço do registry e push
docker tag churn-api "$IMAGEM"
docker push "$IMAGEM"

echo "Imagem publicada em: $IMAGEM"
