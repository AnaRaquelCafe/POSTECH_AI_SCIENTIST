# Labs — MLOps

Doze laboratórios práticos, três por aula (um por parte), de 10 a 15 minutos cada. Todos rodam no **GitHub Codespaces**: você só precisa de uma conta gratuita no GitHub, sem instalar nada, sem cartão de crédito e sem conta em nuvem.

Os labs usam o mesmo cenário do começo ao fim: um modelo de **previsão de churn** (`dados/clientes.csv`), que é treinado, registrado, publicado, monitorado, testado num pipeline de CI e servido em containers.

| Aula | Parte 1 | Parte 2 | Parte 3 |
|---|---|---|---|
| **01 — Ciclo de vida de modelos** | [EDA e treino](Aula01_Ciclo_de_Vida_de_Modelos/Parte1_EDA_e_Treino/) (12 min) | [Model Registry com gate de aprovação](Aula01_Ciclo_de_Vida_de_Modelos/Parte2_Model_Registry/) (12 min) | [Deploy e monitoramento de drift](Aula01_Ciclo_de_Vida_de_Modelos/Parte3_Deploy_e_Monitor/) (15 min) |
| **02 — MLOps** | [Caça ao tesouro no ecossistema](Aula02_MLOps/Parte1_Explorando_o_Ecossistema/) (10 min) | [Experiment tracking com MLflow](Aula02_MLOps/Parte2_Experiment_Tracking_MLflow/) (12 min) | [Promoção com aliases no Model Registry](Aula02_MLOps/Parte3_Model_Registry_MLflow/) (15 min) |
| **03 — CI/CD para ML** | [CI com GitHub Actions](Aula03_CICD_para_ML/Parte1_CI_GitHub_Actions/) (15 min) | [Testes de dados e de modelo no pipeline](Aula03_CICD_para_ML/Parte2_Testes_Dados_e_Modelo/) (15 min) | [Canary release](Aula03_CICD_para_ML/Parte3_Canary_Release/) (15 min) |
| **04 — Deploy de APIs e containers** | [API com FastAPI](Aula04_Deploy_APIs_e_Containers/Parte1_API_com_FastAPI/) (12 min) | [Docker e registry de imagens](Aula04_Deploy_APIs_e_Containers/Parte2_Docker_e_Registry/) (15 min) | [Escalando com Docker Compose](Aula04_Deploy_APIs_e_Containers/Parte3_Escala_com_Docker_Compose/) (15 min) |

📘 **Comece pelo [Roteiro do aluno](ROTEIRO_DO_ALUNO.md):** ele guia os 12 labs na ordem, com o que fazer, como saber que deu certo e o que fazer se der errado.

Cada pasta tem seu próprio `README.md` com o passo a passo. Os comandos partem da raiz do repositório.

## Antes da primeira aula (5 min, uma única vez)
1. No topo da página do repositório no GitHub, clique em **Use this template → Create a new repository** e crie o repositório na sua conta (público).
2. No **seu** repositório: **Code → Codespaces → Create codespace on main**.
3. Aguarde o ambiente terminar de montar. As dependências (`Labs_MLOps/requirements.txt`) são instaladas automaticamente; espere o terminal ficar livre.

Nas aulas seguintes, reabra o mesmo codespace em https://github.com/codespaces. O que você fez nas aulas anteriores (experimentos, modelos registrados) continua lá.

## Portas usadas
| Porta | O quê |
|---|---|
| 5000 | Interface do MLflow (`Labs_MLOps/ui_mlflow.sh`) |
| 5001 | Endpoint do modelo (Aula 01, Parte 3) |
| 5050 | Registry de imagens Docker (Aula 04, Parte 2) |
| 8000 | APIs FastAPI e relatórios HTML |
| 8080 | Balanceador de carga (Aula 04, Parte 3) |

## Dicas
- Quando um app sobe numa porta, o Codespaces oferece **Open in Browser**. Se não aparecer, use a aba **Ports**.
- A Aula 01 e a Aula 02 alimentam o mesmo MLflow (`Labs_MLOps/mlflow.db`). Para começar do zero, apague `mlflow.db` e a pasta `mlartifacts/`.
- Ao terminar, **pare o codespace** (github.com/codespaces → ⋯ → Stop). Ele consome a sua cota gratuita enquanto está ligado.
