# Parte 2 — Testes de dados e de modelo no pipeline (≈ 15 min)

**Objetivo:** estender o pipeline da Parte 1 com as outras duas camadas de testes de ML e ver o build falhar quando o modelo não atinge o mínimo.
**Conceitos da aula:** testes de código, dados e modelo; thresholds de performance; comparação com baseline; jobs encadeados com `needs`.

> Pré-requisito: o pipeline da Parte 1 funcionando no seu repositório.

```bash
cd Labs_MLOps/Aula03_CICD_para_ML/Parte2_Testes_Dados_e_Modelo
```

**1. Rode as validações localmente (2 min):**
```bash
python scripts/test_data_quality.py
python scripts/test_model_quality.py
```

**2. Troque o pipeline (3 min):**
```bash
cd "$(git rev-parse --show-toplevel)"    # raiz do repositório
cp Labs_MLOps/Aula03_CICD_para_ML/Parte2_Testes_Dados_e_Modelo/ci.yml .github/workflows/ci-mlops.yml
git add .github/workflows/ci-mlops.yml
git commit -m "Pipeline com testes de dados e modelo"
git push
```
Na aba **Actions**, o run agora mostra três jobs em sequência: `test-code` → `test-data` → `test-model`. Cada um só começa se o anterior passar.

**3. Faça o pipeline falhar de propósito (5 min):** em `scripts/test_model_quality.py`, suba `THRESHOLD_ACCURACY` para `0.99`. Commit e push. O job `test-model` fica vermelho, e é isso que impediria esse modelo de chegar à produção.

**4. Corrija (2 min):** volte o threshold para `0.75`, faça push e confira os três jobs verdes.

## Para discutir
- Os testes de código passaram, mas os de modelo falharam. Que tipo de problema só o teste de dados ou o de modelo pega?
- O `test-model` compara com o baseline. Por que "passar no threshold" não basta? E como comparar com o modelo que já está em produção (`@champion`)?
