# 🚀 FIAP — Pós-Graduação IAST: MLOps
### Deploy, Automação, CI/CD e Monitoramento de Modelos de Machine Learning

[![GitHub](https://img.shields.io/badge/GitHub-Repository-181717?logo=github&logoColor=white)](https://github.com/rntavares/iast-mlops)
[![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python&logoColor=white)](https://www.python.org/)
[![Codespaces](https://img.shields.io/badge/Labs-GitHub_Codespaces-181717?logo=github&logoColor=white)](https://github.com/features/codespaces)
[![Docker](https://img.shields.io/badge/Container-Docker-2496ED?logo=docker&logoColor=white)](https://www.docker.com/)
[![FastAPI](https://img.shields.io/badge/API-FastAPI-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![MLflow](https://img.shields.io/badge/Tracking-MLflow-0194E2?logo=mlflow&logoColor=white)](https://mlflow.org/)

Repositório oficial de materiais, documentação técnica, apresentações e laboratórios práticos da disciplina de **MLOps** do curso de **Pós-Graduação em Inteligência Artificial para Soluções Tecnológicas (IAST)** da **FIAP**.

🔗 **Repositório GitHub:** [https://github.com/rntavares/iast-mlops](https://github.com/rntavares/iast-mlops)

---

## 🎯 Visão Geral da Disciplina

O objetivo desta disciplina é capacitar engenheiros e cientistas de dados a levar modelos de Machine Learning do ambiente de experimentação para a produção de forma escalável, segura e automatizada. Durante as aulas, são explorados conceitos fundamentais e avançados de MLOps utilizando ferramentas open source de mercado (MLflow, Evidently, GitHub Actions, FastAPI, Docker), com paralelos com as plataformas gerenciadas de nuvem (SageMaker, Vertex AI, Azure ML). Todos os laboratórios rodam no **GitHub Codespaces**, sem conta em nuvem e sem custo.

```
 ┌─────────────┐     ┌──────────────┐     ┌─────────────┐     ┌─────────────┐
 │   AULA 01   │ ──▶ │   AULA 02    │ ──▶ │   AULA 03   │ ──▶ │   AULA 04   │
 │Ciclo de Vida│     │  MLOps com   │     │ CI/CD para  │     │ Deploy APIs │
 │  de Modelos │     │    MLflow    │     │     ML      │     │& Containers │
 └─────────────┘     └──────────────┘     └─────────────┘     └─────────────┘
```

---

## 💻 Primeiros Passos & Clonando o Repositório

### Clonar via HTTPS:
```bash
git clone https://github.com/rntavares/iast-mlops.git
cd iast-mlops
```

### Clonar via SSH:
```bash
git clone git@github.com:rntavares/iast-mlops.git
cd iast-mlops
```

### Vincular um repositório local existente:
```bash
git remote set-url origin https://github.com/rntavares/iast-mlops.git
git branch -M main
git push -u origin main
```

---

## 📂 Estrutura do Repositório

```text
iast-mlops/
├── 📚 Docs-Aulas-MLOps/            # Apostilas, capítulos teóricos e desafios
│   ├── capitulos/                  # Documentos detalhados de cada aula (01 a 04)
│   ├── desafio/                    # Especificação do Desafio Final Integrado
│   └── roteiros/                   # Planejamento e roteiro pedagógico
│
├── .devcontainer/                  # Ambiente do GitHub Codespaces (labs)
│
├── 🛠️ Labs_MLOps/                  # Laboratórios práticos (12 labs, 10 a 15 min cada)
│   ├── ROTEIRO_DO_ALUNO.md         # Roteiro dos 12 labs, na ordem das aulas
│   ├── dados/                      # Dataset de churn usado em todos os labs
│   ├── Aula01_Ciclo_de_Vida_de_Modelos/
│   │   ├── Parte1_EDA_e_Treino/
│   │   ├── Parte2_Model_Registry/
│   │   └── Parte3_Deploy_e_Monitor/
│   ├── Aula02_MLOps/
│   │   ├── Parte1_Explorando_o_Ecossistema/
│   │   ├── Parte2_Experiment_Tracking_MLflow/
│   │   └── Parte3_Model_Registry_MLflow/
│   ├── Aula03_CICD_para_ML/
│   │   ├── Parte1_CI_GitHub_Actions/
│   │   ├── Parte2_Testes_Dados_e_Modelo/
│   │   └── Parte3_Canary_Release/
│   ├── Aula04_Deploy_APIs_e_Containers/
│   │   ├── Parte1_API_com_FastAPI/
│   │   ├── Parte2_Docker_e_Registry/
│   │   └── Parte3_Escala_com_Docker_Compose/
│   └── requirements.txt            # Ambiente dos labs (versões fixadas)
│
└── 📊 PPTs-Aulas-MLOps/            # Slides e apresentações (PowerPoint)
    ├── Aula01_Ciclo_de_Vida_de_Modelos.pptx
    ├── Aula02_MLOps.pptx
    ├── Aula03_CICD_Machine_Learning.pptx
    └── Aula04_Deploy_APIs_Containers.pptx
```

---

## 📖 Trilha de Aprendizagem & Conteúdo das Aulas

### 🔹 Aula 01 — Ciclo de Vida de Modelos e Fundamentos na Nuvem
* **Teoria:** Da exploração dos dados à produção: desafios do ciclo de vida tradicional vs. MLOps, governança e versionamento.
* **Labs Práticos (`Labs_MLOps/Aula01_...`):**
  * `Parte 1`: Análise exploratória (EDA), treino e comparação com o baseline.
  * `Parte 2`: Registro e versionamento no MLflow Model Registry, com gate de aprovação.
  * `Parte 3`: Deploy de um endpoint real-time, data capture e monitoramento de drift com Evidently.

### 🔹 Aula 02 — MLOps, Rastreabilidade e Gestão de Experimentos
* **Teoria:** Experiment Tracking, reprodutibilidade, comparação de hiperparâmetros e arquiteturas de MLflow integradas à nuvem.
* **Labs Práticos (`Labs_MLOps/Aula02_...`):**
  * `Parte 1`: Caça ao tesouro no ecossistema MLOps e níveis de maturidade.
  * `Parte 2`: Rastreamento de experimentos com MLflow (métricas, artefatos, parâmetros).
  * `Parte 3`: Promoção e rollback de modelos com aliases (`@champion` / `@challenger`) no MLflow Model Registry.

### 🔹 Aula 03 — CI/CD para Machine Learning (CT/CD)
* **Teoria:** Integração e Entrega Contínuas aplicadas a dados e modelos, validação automatizada de drift e estratégias de rollout (Canary, Blue/Green).
* **Labs Práticos (`Labs_MLOps/Aula03_...`):**
  * `Parte 1`: Criação de pipeline de CI com GitHub Actions.
  * `Parte 2`: Implementação de testes automatizados de dados (schema/data quality) e validação de performance do modelo.
  * `Parte 3`: Canary release com divisão de tráfego ajustável e rollback.

### 🔹 Aula 04 — Deploy de APIs, Conteinerização e Serverless
* **Teoria:** Microsserviços de inferência, conteinerização com Docker, orquestração e deploy serverless em escala.
* **Labs Práticos (`Labs_MLOps/Aula04_...`):**
  * `Parte 1`: Construção de API de inferência com FastAPI e Pydantic.
  * `Parte 2`: Imagem Docker multi-stage e publicação num registry de imagens.
  * `Parte 3`: Réplicas, load balancing e failover com Docker Compose, com URL pública.

---

## 🛠️ Pré-requisitos & Ambiente de Desenvolvimento

📘 **Roteiro dos labs:** [`Labs_MLOps/ROTEIRO_DO_ALUNO.md`](Labs_MLOps/ROTEIRO_DO_ALUNO.md).

Para os laboratórios práticos, basta uma **conta gratuita no GitHub**. Os labs rodam no **GitHub Codespaces**, que já vem com Python 3.12, Docker e todas as dependências instaladas (`.devcontainer/`). Não é preciso conta em nuvem nem cartão de crédito. O passo a passo inicial está em `Labs_MLOps/README.md`.

> **Cota gratuita:** o Codespaces consome a cota gratuita da sua conta enquanto está ligado. Ao terminar cada aula, **pare o codespace** (github.com/codespaces → ⋯ → Stop).

Para rodar fora do Codespaces: Python 3.12, Docker e `pip install -r Labs_MLOps/requirements.txt`.

---

## 🏆 Desafio Final Integrado

O diretório `Docs-Aulas-MLOps/desafio/` contém a especificação do **Desafio Final Integrado**, onde os alunos consolidam todo o conhecimento da disciplina construindo um pipeline de MLOps completo de ponta a ponta.

---

## 👨‍🏫 Autor & Coordenação

* **Professor / Autor:** Rafael Tavares ([@rntavares](https://github.com/rntavares))
* **Curso:** Pós-Graduação em Inteligência Artificial para Soluções Tecnológicas (IAST)
* **Instituição:** [FIAP](https://www.fiap.com.br)
