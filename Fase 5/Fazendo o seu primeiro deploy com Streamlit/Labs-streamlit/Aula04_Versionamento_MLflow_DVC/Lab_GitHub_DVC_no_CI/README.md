# Aula 04 · Lab GitHub — Pipeline DVC no CI, com métricas no pull request (≈ 15 min)

**Objetivo:** fazer o GitHub Actions reproduzir o pipeline DVC a cada pull request e comentar no PR quanto as métricas mudaram, para que a equipe decida o merge olhando números, e não só código.
**Conceitos:** `params.yaml`, pipeline com mais de um estágio, `dvc params diff` e `dvc metrics diff`, experimentos em branches, CI para ML.

```bash
cd Labs-streamlit/Aula04_Versionamento_MLflow_DVC/Lab_GitHub_DVC_no_CI
```
Leia o `dvc.yaml`: dois estágios, `gerar_dados` e `treinar`, com os parâmetros vindos do `params.yaml`. Como os dados são gerados pelo próprio pipeline, o CI consegue reproduzir tudo sem precisar baixar nada de um storage.

## 1. Rode o pipeline e ligue o CI (4 min)
```bash
dvc init --subdir
dvc repro
dvc metrics show
```
Registre a versão de referência e o workflow no `main`:
```bash
cd "$(git rev-parse --show-toplevel)"
mkdir -p .github/workflows
cp Labs-streamlit/Aula04_Versionamento_MLflow_DVC/Lab_GitHub_DVC_no_CI/dvc-ci.yml .github/workflows/
git add .github/workflows/dvc-ci.yml Labs-streamlit/Aula04_Versionamento_MLflow_DVC/Lab_GitHub_DVC_no_CI
git commit -m "Pipeline DVC + CI"
git push
```

## 2. Um experimento num branch (4 min)
```bash
cd Labs-streamlit/Aula04_Versionamento_MLflow_DVC/Lab_GitHub_DVC_no_CI
git checkout -b experimento-profundidade
```
No `params.yaml`, troque `max_depth: 8` por `max_depth: 3`. Depois:
```bash
dvc repro
dvc params diff main
dvc metrics diff main
```
O `dvc repro` só re-treinou (os dados não mudaram), e os dois `diff` mostram o que mudou e o efeito no F1.

## 3. Abra o pull request (5 min)
```bash
git add params.yaml dvc.lock metricas.json
git commit -m "Experimento: max_depth 3"
git push -u origin experimento-profundidade
gh pr create --fill
```
(Se preferir, clique no link "Create a pull request" que o `git push` mostrou.) No GitHub, abra o PR. O workflow **Pipeline DVC** roda sozinho e, em cerca de um minuto, **comenta no PR** as tabelas de parâmetros e de métricas: `main` → este PR. Com esses números na mão, você faria o merge?

## 4. Extra: mais dados (2 min)
No mesmo branch, mude `versao_dados: 1` para `versao_dados: 2` (4.000 clientes), rode `dvc repro`, faça commit e push. O workflow roda de novo e comenta a nova comparação no mesmo PR.

## Para discutir
- Aqui o pipeline gera os próprios dados. Num projeto real, o CI precisaria baixar o dataset com `dvc pull` de um storage remoto. Onde ficariam as credenciais desse storage? (Dica: **Settings → Secrets and variables → Actions**.)
- Que regra você colocaria no PR: bloquear o merge se o F1 cair mais que X?
