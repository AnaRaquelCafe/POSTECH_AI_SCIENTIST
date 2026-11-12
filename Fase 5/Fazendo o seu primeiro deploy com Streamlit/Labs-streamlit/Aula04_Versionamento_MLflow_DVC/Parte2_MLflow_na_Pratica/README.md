# Aula 04 · Parte 2 — MLflow na prática (≈ 14 min)

**Objetivo:** registrar e comparar experimentos no MLflow e promover um modelo no Model Registry com aliases, incluindo o rollback.
**Conceitos da parte:** MLflow Tracking (parâmetros, métricas, artefatos, tags), comparação de runs, Model Registry, aliases `@champion` e `@challenger`.

> A Parte 1 desta aula é conceitual e não tem lab.

```bash
cd Labs-streamlit/Aula04_Versionamento_MLflow_DVC/Parte2_MLflow_na_Pratica
python gerar_dados.py
```

## 1. Registre dois experimentos (3 min)
```bash
python treinar.py --n-estimators 50 --max-depth 3 --registrar
python treinar.py --n-estimators 200 --max-depth 8 --registrar
```
Cada execução é um *run*: o MLflow guarda os hiperparâmetros, o F1, a acurácia, o modelo e a tag `versao_dados_md5`, a impressão digital do dataset usado. Com `--registrar`, o modelo também vira uma nova versão do modelo `churn` no Model Registry (versões 1 e 2).

## 2. Compare na interface (4 min)
Num **segundo terminal**:
```bash
cd Labs-streamlit/Aula04_Versionamento_MLflow_DVC/Parte2_MLflow_na_Pratica
./ui_mlflow.sh
```
Abra a porta 5000 e entre no experimento `previsao-churn`. Selecione os dois runs e clique em **Compare**: qual combinação de hiperparâmetros foi melhor? Depois abra a aba **Models** e veja as duas versões do `churn`.

> Use o script, não `mlflow ui` puro: no Codespaces o MLflow 3 responde **403** sem as opções de host que o script passa.

## 3. Promova com segurança: challenger → champion (5 min)
Volte ao primeiro terminal. A versão 1 está em produção:
```bash
python promover.py --versao 1 --alias champion
python prever.py
```
A versão 2 chega como candidata e é validada **sem** afetar quem consome o `@champion`:
```bash
python promover.py --versao 2 --alias challenger
python prever.py --alias challenger
python prever.py
```
Aprovada, ela assume a produção. Mover o alias é todo o "deploy":
```bash
python promover.py --versao 2 --alias champion
python prever.py
```
Na aba **Models** da interface, recarregue a página e veja os aliases em cada versão.

## 4. Rollback (1 min)
Deu problema em produção? Volte o alias:
```bash
python promover.py --versao 1 --alias champion
python prever.py
```
O `prever.py` não mudou uma linha em nenhum desses passos: ele sempre pede `churn@champion`.

> Se você encontrar em tutoriais antigos os estágios Staging/Production/Archived, saiba que eles foram descontinuados no MLflow. Os aliases cumprem o mesmo papel.

Ao terminar, pare a interface com Ctrl+C no segundo terminal.

## Para discutir
- Seu melhor modelo foi treinado há 3 meses. Que informações do MLflow você usaria para reproduzi-lo? O que ainda falta (dica: a Parte 3)?
- Quem deveria ter permissão para mover o alias `@champion` numa empresa?
