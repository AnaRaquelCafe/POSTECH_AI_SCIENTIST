# Parte 1 — Caça ao tesouro no ecossistema MLOps (≈ 10 min, sem código)

**Objetivo:** reconhecer onde cada peça de uma plataforma MLOps vive no nosso ambiente e relacioná-la aos níveis de maturidade do Google.
**Conceitos da aula:** o que é MLOps, níveis de maturidade 0, 1 e 2, o que se versiona, testa e monitora em ML.

> Funciona melhor depois da Aula 01, quando já existem experimentos e modelos registrados. Se você não fez a Aula 01, rode antes `python Labs_MLOps/Aula01_Ciclo_de_Vida_de_Modelos/Parte1_EDA_e_Treino/treinar_modelo.py` e o `registrar_modelo.py` da Parte 2.

Suba a interface do MLflow e abra a porta 5000:
```bash
Labs_MLOps/ui_mlflow.sh
```

Encontre cada item abaixo:

1. **Experiments (MLflow)** → abra o experimento `ciclo-de-vida`. Que métricas e tags foram registradas no run? Onde está o artefato do modelo?
2. **Model Registry (MLflow → Models)** → abra `churn-model`. Quantas versões existem? Qual foi aprovada e qual foi rejeitada?
3. **Pipelines** → no seu repositório do GitHub, abra a aba **Actions**. Existe algum pipeline rodando? (Vamos criar um na Aula 03.)
4. **Feature Store** → procure no ambiente. Não existe: por que um time só sente falta dela quando tem vários modelos usando as mesmas features? (Pesquise o Feast.)
5. Preencha a tabela relacionando cada peça com o nível de maturidade MLOps (0, 1 ou 2) visto na aula.

| Peça | O que faz | Onde está no nosso ambiente | Nível de maturidade associado |
|---|---|---|---|
| Experiment tracking | | | |
| Model Registry | | | |
| Pipeline de CI/CD | | | |
| Feature Store | | | |
| Monitoramento | | | |

Não tem gabarito único; o objetivo é a discussão em sala sobre por que cada ferramenta existe.

## Para discutir
- Em que nível de maturidade está o que fizemos na Aula 01 (scripts rodados à mão)? O que falta para chegar ao nível 1?
- Nas nuvens, essas peças vêm prontas (SageMaker, Vertex AI, Azure ML). O que se ganha e o que se perde em relação a montar com ferramentas open source como o MLflow?
