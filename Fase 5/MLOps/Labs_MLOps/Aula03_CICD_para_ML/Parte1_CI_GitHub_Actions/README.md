# Parte 1 — CI com GitHub Actions (≈ 15 min)

**Objetivo:** criar um pipeline de integração contínua que roda os testes a cada push e bloqueia código quebrado.
**Conceitos da aula:** CI vs CD vs Continuous Deployment, testes de código em ML, pipeline como código.

```bash
cd Labs_MLOps/Aula03_CICD_para_ML/Parte1_CI_GitHub_Actions
```

**1. Rode os testes localmente (2 min):**
```bash
pytest tests/ -v
```
`src/features.py` é o feature engineering do modelo; `tests/test_features.py` garante que ele não devolve nulos, mantém a idade numa faixa válida e não deixa o `churn` vazar para as features.

**2. Crie o pipeline (3 min).** O GitHub só executa workflows que estão em `.github/workflows/` na raiz do repositório:
```bash
cd "$(git rev-parse --show-toplevel)"    # raiz do repositório
mkdir -p .github/workflows
cp Labs_MLOps/Aula03_CICD_para_ML/Parte1_CI_GitHub_Actions/ci.yml .github/workflows/ci-mlops.yml
git add .github/workflows/ci-mlops.yml
git commit -m "Adiciona pipeline de CI"
git push
```

**3. Acompanhe o build (3 min):** no seu repositório no GitHub, abra a aba **Actions** → **CI MLOps**. Clique no run e abra o job `test-code` para ver cada passo e a saída do pytest.

**4. Quebre o build de propósito (5 min):** em `src/features.py`, apague o `.clip(18, 100)`. Rode `pytest` localmente, veja o teste falhar e faça commit e push mesmo assim. O run no Actions fica vermelho, e o GitHub avisa por e-mail. Desfaça a alteração, faça push de novo e confira o build verde.

## Para discutir
- O `ci.yml` só dispara quando arquivos da Aula 03 mudam (`paths`). Por que isso importa num repositório com muitos projetos?
- Este pipeline testa só o código. O que pode quebrar um modelo em produção mesmo com todos esses testes passando? (Parte 2.)
