# Aula 01 · Parte 3 — Publicando o modelo na web (≈ 14 min)

**Objetivo:** publicar o app de predição no Streamlit Community Cloud e ganhar um link público, atualizado a cada `git push`.
**Conceitos da parte:** os três arquivos de um deploy (`app.py` + modelo + `requirements.txt`), versões fixadas, deploy a partir do GitHub, quando usar (e não usar) o Streamlit.

```bash
cd Labs-streamlit/Aula01_Pipeline_ML_Streamlit/Parte3_Publicando_na_Web
```

## 1. Confira o que vai para o deploy (2 min)
```bash
ls
cat requirements.txt
pip show scikit-learn | grep Version
```
São três arquivos: `app.py`, `modelo_churn.joblib` e `requirements.txt`. A versão do scikit-learn no `requirements.txt` precisa ser **a mesma** que gerou o `.joblib`. Versão diferente é a causa mais comum de erro nesse tipo de deploy.

## 2. Personalize e teste localmente (2 min)
No `app.py`, troque `AUTOR = "Seu nome"` pelo seu nome. Depois:
```bash
streamlit run app.py
```
Confira o app na porta 8501 e pare com Ctrl+C.

## 3. Envie para o GitHub (1 min)
```bash
git add app.py
git commit -m "Personaliza o app"
git push
```

## 4. Publique no Streamlit Community Cloud (5 min)
1. Acesse https://share.streamlit.io e entre com a sua conta do GitHub.
2. **Create app** → **Deploy a public app from GitHub**.
3. Repositório: o seu. Branch: `main`. Main file path:
   `Labs-streamlit/Aula01_Pipeline_ML_Streamlit/Parte3_Publicando_na_Web/app.py`
4. Em **Advanced settings**, escolha **Python 3.12**.
5. **Deploy**. O primeiro build leva de 2 a 4 minutos. Enquanto isso, acompanhe o log: ele instala exatamente o `requirements.txt` desta pasta.

Quando terminar, abra o link público no celular: o app está na internet.

## 5. Atualização contínua (3 min)
Mude o texto do `st.title(...)` no `app.py` e rode de novo os comandos do passo 3. Em cerca de um minuto, o app publicado se atualiza sozinho, sem clicar em nada no Streamlit Cloud.

## Lab GitHub
A pasta [`Lab_GitHub_CI_do_App`](../Lab_GitHub_CI_do_App/) coloca testes automáticos antes do deploy: o GitHub Actions testa a interface do app a cada push, para que um erro não derrube o app publicado.

## Para discutir
- Esse app aguentaria 1.000 requisições por segundo? Quando trocar por uma API (FastAPI)?
- O link é público. Que cuidado você teria antes de publicar um modelo treinado com dados reais de clientes?
