# Aula 01 · Lab GitHub — Testes automáticos do app (≈ 12 min)

**Objetivo:** garantir que só código testado chegue ao app publicado: o GitHub Actions roda testes da interface Streamlit a cada push.
**Conceitos:** deploy contínuo a partir do GitHub, testes de interface com `AppTest`, integração contínua (CI).

Na Parte 3, cada `git push` atualiza o app no Streamlit Community Cloud automaticamente. É prático, mas perigoso: um push com erro derruba o app publicado. Este lab coloca um "porteiro" antes do deploy.

```bash
cd Labs-streamlit/Aula01_Pipeline_ML_Streamlit/Lab_GitHub_CI_do_App
```

## 1. Rode os testes localmente (3 min)
```bash
pytest tests/ -v
```
Leia `tests/test_app.py`. O `AppTest` do Streamlit roda o `app.py` sem navegador e simula um usuário: muda o slider, preenche os campos e clica em **Prever**. Os testes conferem que o app abre, que um cliente de alto risco gera alerta e que um cliente fiel não gera.

## 2. Ligue o workflow no GitHub (3 min)
O GitHub só executa workflows que estão em `.github/workflows/`, na raiz do repositório:
```bash
cd "$(git rev-parse --show-toplevel)"
mkdir -p .github/workflows
cp Labs-streamlit/Aula01_Pipeline_ML_Streamlit/Lab_GitHub_CI_do_App/ci-app.yml .github/workflows/
git add .github/workflows/ci-app.yml
git commit -m "CI do app Streamlit"
git push
```
No seu repositório no GitHub, abra a aba **Actions** → **CI do app Streamlit** e acompanhe o job `testar-app`.

## 3. Quebre o app de propósito (4 min)
No `app.py`, troque `columns=["idade", "meses", "valor_mensal"]` por `columns=["idade", "meses", "valor"]` (um erro de digitação comum). Rode `pytest tests/ -v` e veja os testes falharem. Faça commit e push mesmo assim: o run no Actions fica vermelho e o GitHub avisa por e-mail. Desfaça a alteração e faça push de novo para ver o build verde.

## 4. Fechando a porta (2 min, leitura)
O CI avisa, mas não impede o push de chegar ao `main`, que é de onde o Streamlit Cloud publica. Numa equipe, o fluxo é:
1. Cada mudança vai para um branch e vira um **pull request**.
2. Em **Settings → Branches → Branch protection rules**, o `main` passa a exigir que o check `testar-app` esteja verde antes do merge.
3. Só código testado chega ao `main`, e só o `main` é publicado.

## Para discutir
- Os testes usam o modelo real (`modelo_churn.joblib`). O que acontece com o teste "cliente de alto risco" quando o modelo for re-treinado? Isso é um bug do teste ou um aviso útil?
- O que mais você testaria antes de publicar um app de ML? (tempo de resposta, entradas inválidas, versão do modelo…)
