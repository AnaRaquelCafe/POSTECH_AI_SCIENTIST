FROM mcr.microsoft.com/devcontainers/python:1-3.12

# A imagem base traz o repositório apt do Yarn com uma chave GPG vencida. Isso faz o
# "apt-get update" falhar e quebra a instalação do Docker-in-Docker (o Codespaces cai
# num container de recuperação, sem as dependências). Os labs não usam Yarn.
RUN rm -f /etc/apt/sources.list.d/yarn*.list

# O pip instala os pacotes do usuário em ~/.local. Colocamos ~/.local/bin no PATH desde
# o início, para que mlflow, streamlit, dvc, uvicorn, pytest etc. funcionem em qualquer
# terminal, inclusive nos abertos antes do fim da instalação.
ENV PATH="/home/vscode/.local/bin:${PATH}"
