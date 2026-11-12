# Parte 2 — Model Registry (≈ 12 min)

**Objetivo:** transformar o `model.joblib` da Parte 1 numa versão registrada, rastreável e com um gate de aprovação antes de ir para produção.
**Conceitos da aula:** empacotamento e serialização, versionamento de modelos, Model Registry, aprovação como gate de qualidade.

> Pré-requisito: `model.joblib` gerado na Parte 1.

```bash
cd Labs_MLOps/Aula01_Ciclo_de_Vida_de_Modelos/Parte2_Model_Registry
```

**1. Registre o modelo:**
```bash
python registrar_modelo.py
```
O modelo vai para o Model Registry do MLflow como `churn-model`, versão 1, com a tag `aprovacao=PendingManualApproval`. Junto com ele ficam as métricas, a versão dos dados (`versao_dados_md5`) e um exemplo de entrada.

**2. Passe pelo gate de qualidade:**
```bash
python aprovar_modelo.py
```
A versão só é aprovada se o recall passar do mínimo definido pelo negócio. Rode `registrar_modelo.py` de novo e depois `python aprovar_modelo.py --rejeitar` para ver o outro caminho.

**3. Confira na interface** (num segundo terminal):
```bash
Labs_MLOps/ui_mlflow.sh
```
Abra a porta 5000 → **Models** → `churn-model`. Veja as versões, a tag `aprovacao` de cada uma e, clicando numa versão, o run de origem com as métricas.

## Para discutir
- Por que registrar o `Pipeline` inteiro (imputação + modelo), e não só o classificador?
- Quem deveria poder aprovar um modelo na sua empresa? O que mais entraria no gate além do recall (fairness, latência, revisão jurídica)?
