# Parte 2 — Experiment tracking com MLflow (≈ 12 min)

**Objetivo:** registrar parâmetros, métricas e artefatos de cada treino e comparar os experimentos na interface do MLflow.
**Conceitos da aula:** experiment tracking, reprodutibilidade, os componentes do MLflow (Tracking, Models, Registry).

```bash
cd Labs_MLOps/Aula02_MLOps/Parte2_Experiment_Tracking_MLflow
```

**1. Rode três experimentos com hiperparâmetros diferentes:**
```bash
python treino_com_mlflow.py --n-estimators 50 --max-depth 3
python treino_com_mlflow.py --n-estimators 100 --max-depth 5
python treino_com_mlflow.py --n-estimators 300
```

**2. Compare na interface** (num segundo terminal):
```bash
Labs_MLOps/ui_mlflow.sh
```
Abra a porta 5000 → experimento `previsao-churn` → selecione os três runs → **Compare**. Qual teve o melhor `f1_score`? E o melhor `recall`? São o mesmo run?

**3. Abra um run** e encontre: os parâmetros, as métricas, a tag `versao_dados_md5` (qual versão dos dados gerou este resultado) e, em **Artifacts**, o modelo salvo com seu `input_example`.

> Use o script, não `mlflow ui` puro: no Codespaces o MLflow 3 responde **403** sem as opções de host que o script passa.

## Para discutir
- Seu melhor modelo foi treinado há 3 meses. O que exatamente você precisa para reproduzi-lo? O MLflow guarda tudo isso?
- O código de treino não foi versionado no MLflow. Onde ele está versionado? (Dica: `git log`.)
