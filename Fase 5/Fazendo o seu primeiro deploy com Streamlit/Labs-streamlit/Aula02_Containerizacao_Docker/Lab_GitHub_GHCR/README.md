# Aula 02 · Lab GitHub — Publicando a imagem no GitHub Container Registry (≈ 15 min)

**Objetivo:** deixar o GitHub Actions construir a imagem do app a cada push e publicá-la num registry, de onde qualquer máquina consegue baixá-la e rodá-la.
**Conceitos:** registry de imagens, tags (`latest` vs. SHA do commit), build automatizado (CI), rodar uma imagem publicada.

O GitHub Container Registry (`ghcr.io`) cumpre o papel do Docker Hub ou do registry de um provedor de nuvem: guarda as imagens versionadas, ligadas ao seu repositório.

```bash
cd Labs-streamlit/Aula02_Containerizacao_Docker/Lab_GitHub_GHCR
```
Esta pasta tem o mesmo app, `Dockerfile` e `.dockerignore` da Parte 3, mais o workflow `ghcr.yml`.

## 1. Ligue o workflow (3 min)
Leia o `ghcr.yml`: ele faz login no `ghcr.io` com o token que o próprio GitHub fornece ao workflow, constrói a imagem e a publica com duas tags.
```bash
cd "$(git rev-parse --show-toplevel)"
mkdir -p .github/workflows
cp Labs-streamlit/Aula02_Containerizacao_Docker/Lab_GitHub_GHCR/ghcr.yml .github/workflows/
git add .github/workflows/ghcr.yml
git commit -m "Publica a imagem no GHCR"
git push
```
Na aba **Actions**, acompanhe o job `publicar` (≈ 2 min).

## 2. Encontre a imagem publicada (3 min)
No seu perfil do GitHub, abra a aba **Packages** → `churn-app`. Veja as duas tags: `latest` e o SHA do commit.

A imagem nasce **privada**. Para este lab, em **Package settings → Danger Zone → Change visibility**, deixe-a **Public**.

## 3. Rode a imagem publicada (4 min)
No Codespaces, a variável `$GITHUB_USER` já tem o seu usuário:
```bash
IMAGEM=ghcr.io/$(echo "$GITHUB_USER" | tr '[:upper:]' '[:lower:]')/churn-app
docker run --rm -p 8501:8501 $IMAGEM:latest
```
O Docker baixou a imagem do registry, como faria qualquer servidor. Abra a porta 8501 e confira o app. Para mandar o link a um colega, na aba **Ports** clique com o botão direito na 8501 → **Port Visibility → Public**. Pare com Ctrl+C.

## 4. Publique uma versão nova (5 min)
No `app.py`, mude o texto do `st.caption(...)`. Depois:
```bash
git add Labs-streamlit/Aula02_Containerizacao_Docker/Lab_GitHub_GHCR/app.py
git commit -m "Nova versão do app"
git push
```
Quando o workflow terminar, rode `docker pull $IMAGEM:latest` e depois o `docker run` do passo 3: o texto novo aparece. A versão anterior continua disponível pela tag do SHA antigo (veja em **Packages**). Rodar essa tag é o rollback.

## Para discutir
- Por que usar a tag com o SHA do commit em produção, e não `latest`?
- A imagem inclui o modelo (`modelos/`). O que muda no fluxo quando o modelo é re-treinado toda semana?
