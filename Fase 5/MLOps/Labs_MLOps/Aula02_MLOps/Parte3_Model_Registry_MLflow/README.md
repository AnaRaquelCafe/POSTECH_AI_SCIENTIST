# Parte 3 — Promovendo um modelo no MLflow Model Registry (≈ 15 min)

**Objetivo:** levar o melhor experimento ao Model Registry, validá-lo como candidato e promovê-lo a produção, com rollback em um comando.
**Conceitos da aula:** Model Registry, aliases `@champion` (produção) e `@challenger` (candidato), promoção e rollback.

> Pré-requisito: runs da Parte 2 no experimento `previsao-churn`.

```bash
cd Labs_MLOps/Aula02_MLOps/Parte3_Model_Registry_MLflow
```

**1. Registre o melhor run como candidato:**
```bash
python registrar_modelo.py
```

**2. Valide e promova:**
```bash
python promover_modelo.py
python prever.py
```
O `prever.py` carrega `models:/churn-model@champion` sem saber o número da versão. Trocar o modelo em produção é mover o alias.

**3. Treine um modelo pior e tente promovê-lo:**
```bash
python ../Parte2_Experiment_Tracking_MLflow/treino_com_mlflow.py --n-estimators 5 --max-depth 2
python registrar_modelo.py --ultimo
python promover_modelo.py
```
O `--ultimo` registra o run mais recente (o ruim) em vez do melhor. A validação deve barrar a promoção, e o `@champion` continua onde estava.

**4. Simule um incidente e faça o rollback.** Use os números de versão que o `promover_modelo.py` do passo 3 mostrou. Primeiro, alguém força o modelo ruim (o `@challenger` barrado) para produção, pulando a validação:
```bash
python promover_modelo.py --versao <versão do @challenger>
python prever.py
```
A probabilidade de churn do mesmo cliente muda (cai de cerca de 96% para 72%): o modelo ruim está em produção. Rollback, de volta ao `@champion` anterior:
```bash
python promover_modelo.py --versao <versão do @champion>
python prever.py
```
O `prever.py` não mudou uma linha: só o alias se moveu.

**5. Veja o histórico na interface** (`Labs_MLOps/ui_mlflow.sh`, porta 5000) → **Models → churn-model**: cada versão, seus aliases e o run de origem.

> Em tutoriais antigos você vai encontrar os estágios Staging/Production/Archived. Eles foram descontinuados no MLflow; os aliases cumprem o mesmo papel com mais flexibilidade.

## Para discutir
- Por que o consumidor carrega `@champion` e não `versão 3`? O que aconteceria num rollback se cada serviço tivesse a versão fixada no código?
- A validação aqui é uma métrica num conjunto de teste. O que mais você exigiria antes de promover um modelo de crédito ou de saúde?
