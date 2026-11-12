#!/bin/bash
# Sobe a interface do MLflow no Codespaces.
# O MLflow 3 bloqueia (HTTP 403) acessos cujo endereço não esteja liberado; no
# Codespaces o navegador chega por um endereço *.app.github.dev (ou por
# localhost:5000, se você usa o VS Code no desktop), então é preciso liberá-los.
cd "$(dirname "$0")"
mlflow ui \
  --backend-store-uri sqlite:///mlflow.db \
  --port 5000 \
  --allowed-hosts "*.app.github.dev,*.app.github.dev:*,localhost,localhost:*,127.0.0.1,127.0.0.1:*" \
  --cors-allowed-origins "https://*.app.github.dev"
