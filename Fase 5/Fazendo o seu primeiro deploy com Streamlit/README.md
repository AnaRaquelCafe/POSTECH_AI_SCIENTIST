# 🚀 FIAP — Pós-Graduação IAST: Fazendo o seu primeiro deploy com Streamlit
### Pipelines de Machine Learning, Containerização com Docker, Monitoramento de Drift e Versionamento

[![GitHub](https://img.shields.io/badge/GitHub-Repository-181717?logo=github&logoColor=white)](https://github.com/rntavares/iast-streamlit)
[![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Frontend-Streamlit-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Docker](https://img.shields.io/badge/Container-Docker-2496ED?logo=docker&logoColor=white)](https://www.docker.com/)
[![GitHub Actions](https://img.shields.io/badge/CI-GitHub_Actions-2088FF?logo=githubactions&logoColor=white)](https://github.com/features/actions)
[![MLflow](https://img.shields.io/badge/Tracking-MLflow-0194E2?logo=mlflow&logoColor=white)](https://mlflow.org/)
[![DVC](https://img.shields.io/badge/Data_Version-DVC-945DD6?logo=dvc&logoColor=white)](https://dvc.org/)

Repositório oficial de materiais, apresentações, documentação técnica e laboratórios práticos da disciplina **"Fazendo o seu primeiro deploy com Streamlit"** do curso de **Pós-Graduação em Inteligência Artificial para Soluções Tecnológicas (IAST)** da **FIAP**.

🔗 **Repositório GitHub:** [https://github.com/rntavares/iast-streamlit](https://github.com/rntavares/iast-streamlit)

---

## 🎯 Visão Geral da Disciplina

Esta disciplina guia os alunos por toda a jornada de transformação de um modelo de Machine Learning em uma aplicação web interativa e profissional utilizando **Streamlit**, avançando pelas etapas de **conteinerização com Docker**, **publicação e automação com o GitHub (Streamlit Community Cloud, GitHub Actions e GitHub Container Registry)**, **monitoramento contínuo de Drift** e **versionamento de ponta a ponta com MLflow e DVC**.

```
 ┌─────────────┐     ┌──────────────┐     ┌─────────────┐     ┌─────────────┐
 │   AULA 01   │ ──▶ │   AULA 02    │ ──▶ │   AULA 03   │ ──▶ │   AULA 04   │
 │Pipeline ML  │     │Container com │     │Monitoramento│     │Versionamento│
 │& Streamlit  │     │Docker & GHCR │     │  de Drift   │     │MLflow & DVC │
 └─────────────┘     └──────────────┘     └─────────────┘     └─────────────┘
```

---

## 💻 Primeiros Passos & Clonando o Repositório

### Clonar via HTTPS:
```bash
git clone https://github.com/rntavares/iast-streamlit.git
cd iast-streamlit
```

### Clonar via SSH:
```bash
git clone git@github.com:rntavares/iast-streamlit.git
cd iast-streamlit
```

### Vincular este diretório a um novo repositório Git:
```bash
git init
git remote add origin https://github.com/rntavares/iast-streamlit.git
git branch -M main
git add .
git commit -m "feat: initial commit - material completo do curso"
git push -u origin main
```

---

## 📂 Estrutura do Repositório

```text
iast-streamlit/
├── .devcontainer/                  # Ambiente do GitHub Codespaces (labs de sala)
├── 📚 Docs-Aulas-streamlit/        # Apostilas e documentação teórica
│   ├── capitulos/                  # Capítulos detalhados em .docx (Aulas 01 a 04)
│   ├── desafio/                    # Especificação do Desafio Final Integrado
│   └── roteiros/                   # Roteiro pedagógico da disciplina
│
├── 🛠️ Labs-streamlit/              # Um lab por parte de aula (Codespaces) + Lab GitHub por aula
│   ├── ROTEIRO_DO_ALUNO.md         # Roteiro do aluno: passo a passo de todos os labs
│   ├── Aula01_Pipeline_ML_Streamlit/   # Parte1 pipeline · Parte2 interface · Parte3 publicação · Lab_GitHub_CI_do_App
│   ├── Aula02_Containerizacao_Docker/  # Parte1 containers · Parte2 Dockerfile · Parte3 boas práticas · Lab_GitHub_GHCR
│   ├── Aula03_Monitoramento_Drift/     # Parte1 degradação · Parte2 detecção · Parte3 reação · Lab_GitHub_Monitoramento_Agendado
│   ├── Aula04_Versionamento_MLflow_DVC/ # Parte2 MLflow · Parte3 DVC · Lab_GitHub_DVC_no_CI
│   └── requirements.txt            # Ambiente dos labs Codespaces
│
└── 📊 PPTs-Aulas-streamlit/        # Slides e apresentações (PowerPoint)
    ├── Aula01_Pipeline_ML_Streamlit.pptx
    ├── Aula02_Containerizacao_Docker.pptx
    ├── Aula03_Monitoramento_Drift.pptx
    └── Aula04_Versionamento_MLflow_DVC.pptx
```

---

## 📖 Trilha de Aprendizagem & Conteúdo das Aulas

### 🔹 Aula 01 — Pipeline de ML e Deploy no Streamlit
* **Teoria:** Criação de interfaces de Machine Learning reativas e intuitivas com Streamlit, arquitetura de componentes, sessões e fluxo de dados.
* **Labs Codespaces (`Labs-streamlit/Aula01_Pipeline_ML_Streamlit`):**
  * Parte 1: pipeline scikit-learn em etapas, serialização e serving desacoplado.
  * Parte 2: app Streamlit, execução reativa, `@st.cache_resource` e limiar ajustável.
  * Parte 3: publicação no Streamlit Community Cloud com atualização a cada `git push`.
* **Lab GitHub (`Labs-streamlit/Aula01_Pipeline_ML_Streamlit/Lab_GitHub_CI_do_App`):**
  * Testes automáticos da interface com `AppTest`, rodando no GitHub Actions a cada push, antes do deploy.

### 🔹 Aula 02 — Containerização com Docker & Publicação da Imagem
* **Teoria:** Fundamentos de Docker para Data Science, escrita de `Dockerfile` otimizado, boas práticas de camadas (*multi-stage*) e isolamento de dependências.
* **Labs Codespaces (`Labs-streamlit/Aula02_Containerizacao_Docker`):**
  * Parte 1: imagem, container e registry com os comandos essenciais do Docker.
  * Parte 2: Dockerfile do app e cache de build.
  * Parte 3: usuário não-root, `.dockerignore`, volumes, Docker Compose e scanning com Trivy.
* **Lab GitHub (`Labs-streamlit/Aula02_Containerizacao_Docker/Lab_GitHub_GHCR`):**
  * Build automatizado da imagem no GitHub Actions e publicação no GitHub Container Registry (`ghcr.io`).
  * Execução da imagem publicada, tags por commit e rollback.

### 🔹 Aula 03 — Monitoramento de Modelos em Produção & Data Drift
* **Teoria:** Ciclo pós-deploy, identificação de *Data Drift* e *Concept Drift*, degradação de acurácia e estratégias de re-treinamento.
* **Labs Codespaces (`Labs-streamlit/Aula03_Monitoramento_Drift`):**
  * Parte 1: 12 meses de produção simulados, os três níveis de monitoramento e o concept drift silencioso.
  * Parte 2: PSI, Kolmogorov-Smirnov e qui-quadrado, e o efeito do tamanho da janela.
  * Parte 3: alertas, gatilho de re-treino e relatório do Evidently.
* **Lab GitHub (`Labs-streamlit/Aula03_Monitoramento_Drift/Lab_GitHub_Monitoramento_Agendado`):**
  * Monitoramento de drift agendado no GitHub Actions, com relatório do Evidently e issue de alerta quando há drift.

### 🔹 Aula 04 — Versionamento de Dados e Modelos com MLflow e DVC
* **Teoria:** Governança completa de dados (*Data Lineage*), rastreabilidade de experimentos e versionamento de grandes volumes de dados sem sobrecarregar o Git.
* **Labs Codespaces (`Labs-streamlit/Aula04_Versionamento_MLflow_DVC`):**
  * Parte 1: conceitual, sem lab.
  * Parte 2: experimentos no MLflow, Model Registry e promoção `@challenger` → `@champion` com rollback.
  * Parte 3: dados versionados com DVC, pipeline `dvc.yaml` e volta no tempo para dados e modelo.
* **Lab GitHub (`Labs-streamlit/Aula04_Versionamento_MLflow_DVC/Lab_GitHub_DVC_no_CI`):**
  * Pipeline DVC reproduzido no GitHub Actions a cada pull request, com a diferença de métricas comentada no PR.

---

## 🛠️ Pré-requisitos & Ambiente

Todos os labs precisam apenas de uma **conta gratuita no GitHub**: rodam no **GitHub Codespaces** (Python 3.12, Docker, DVC e as dependências já instaladas pelo `.devcontainer/`) e no **GitHub Actions**. Não é preciso conta em nuvem nem cartão de crédito. O passo a passo inicial está em `Labs-streamlit/README.md`.

📘 **Roteiro dos labs:** [`Labs-streamlit/ROTEIRO_DO_ALUNO.md`](Labs-streamlit/ROTEIRO_DO_ALUNO.md) guia o aluno por todos os labs, com o que conferir em cada um e uma tabela de progresso.

> **Cota gratuita:** o Codespaces consome a cota gratuita da sua conta enquanto está ligado. Ao terminar cada aula, **pare o codespace** (github.com/codespaces → ⋯ → Stop).

Para rodar fora do Codespaces: Python 3.12, Docker, Git e `pip install -r Labs-streamlit/requirements.txt`.

---

## 🏆 Desafio Final Integrado

O diretório `Docs-Aulas-streamlit/desafio/` traz a especificação do **Desafio Final Integrado**, onde os alunos desenvolvem e publicam uma aplicação completa em Streamlit conteinerizada na nuvem com versionamento e monitoramento.

---

## 👨‍🏫 Autor & Coordenação

* **Professor / Autor:** Rafael Tavares ([@rntavares](https://github.com/rntavares))
* **Curso:** Pós-Graduação em Inteligência Artificial para Soluções Tecnológicas (IAST)
* **Instituição:** [FIAP](https://www.fiap.com.br)
