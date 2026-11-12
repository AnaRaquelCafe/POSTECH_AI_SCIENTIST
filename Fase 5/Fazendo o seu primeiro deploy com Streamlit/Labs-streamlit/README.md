# Labs — Fazendo o seu primeiro deploy com Streamlit

📘 **Comece pelo [Roteiro do aluno](ROTEIRO_DO_ALUNO.md)**: o passo a passo de todos os labs, com o que conferir em cada um e uma tabela para marcar o seu progresso.

Os labs seguem as partes de cada aula: **um lab por parte**, de 12 a 15 minutos, feitos no **GitHub Codespaces**. Só é preciso uma conta gratuita no GitHub: sem instalar nada, sem cartão de crédito e sem conta em nuvem.

Cada parte é **independente**: a pasta já traz tudo de que o lab precisa. Se você perdeu a Parte 1, pode fazer a Parte 2 normalmente.

Cada aula também tem um **Lab GitHub** (pasta `Lab_GitHub_*`), citado no fim da Parte 03. Ele leva o assunto da aula para o GitHub Actions: testes antes do deploy, publicação da imagem, monitoramento agendado e pipeline de dados no pull request.

| Aula | Parte 1 | Parte 2 | Parte 3 | Lab GitHub |
|---|---|---|---|---|
| **01 — Pipeline de ML e Deploy no Streamlit** | [Estruturando o pipeline](Aula01_Pipeline_ML_Streamlit/Parte1_Estruturando_o_Pipeline/) (≈ 12 min) | [Interface com Streamlit](Aula01_Pipeline_ML_Streamlit/Parte2_Interface_Streamlit/) (≈ 13 min) | [Publicando na web](Aula01_Pipeline_ML_Streamlit/Parte3_Publicando_na_Web/) (≈ 14 min) | [CI do app](Aula01_Pipeline_ML_Streamlit/Lab_GitHub_CI_do_App/) (≈ 12 min) |
| **02 — Containerização com Docker** | [Entendendo containers](Aula02_Containerizacao_Docker/Parte1_Entendendo_Containers/) (≈ 12 min) | [Escrevendo um Dockerfile](Aula02_Containerizacao_Docker/Parte2_Escrevendo_um_Dockerfile/) (≈ 15 min) | [Boas práticas e Compose](Aula02_Containerizacao_Docker/Parte3_Boas_Praticas_e_Compose/) (≈ 15 min) | [Imagem no GHCR](Aula02_Containerizacao_Docker/Lab_GitHub_GHCR/) (≈ 15 min) |
| **03 — Monitoramento de Drift** | [Entendendo a degradação](Aula03_Monitoramento_Drift/Parte1_Entendendo_a_Degradacao/) (≈ 12 min) | [Detectando drift](Aula03_Monitoramento_Drift/Parte2_Detectando_Drift/) (≈ 13 min) | [Reagindo ao drift](Aula03_Monitoramento_Drift/Parte3_Reagindo_ao_Drift/) (≈ 13 min) | [Monitoramento agendado](Aula03_Monitoramento_Drift/Lab_GitHub_Monitoramento_Agendado/) (≈ 13 min) |
| **04 — Versionamento com MLflow e DVC** | *conceitual, sem lab* | [MLflow na prática](Aula04_Versionamento_MLflow_DVC/Parte2_MLflow_na_Pratica/) (≈ 14 min) | [DVC para dados e pipelines](Aula04_Versionamento_MLflow_DVC/Parte3_DVC_para_Dados_e_Pipelines/) (≈ 15 min) | [DVC no CI](Aula04_Versionamento_MLflow_DVC/Lab_GitHub_DVC_no_CI/) (≈ 15 min) |

Cada pasta tem seu próprio `README.md` com o passo a passo completo.

```
Labs-streamlit/
├── ROTEIRO_DO_ALUNO.md       # passo a passo de todos os labs para o aluno
├── Aula01_Pipeline_ML_Streamlit/
│   ├── Parte1_Estruturando_o_Pipeline/
│   ├── Parte2_Interface_Streamlit/
│   ├── Parte3_Publicando_na_Web/
│   └── Lab_GitHub_CI_do_App/
├── Aula02_Containerizacao_Docker/
│   ├── Parte1_Entendendo_Containers/
│   ├── Parte2_Escrevendo_um_Dockerfile/
│   ├── Parte3_Boas_Praticas_e_Compose/
│   └── Lab_GitHub_GHCR/
├── Aula03_Monitoramento_Drift/
│   ├── Parte1_Entendendo_a_Degradacao/
│   ├── Parte2_Detectando_Drift/
│   ├── Parte3_Reagindo_ao_Drift/
│   └── Lab_GitHub_Monitoramento_Agendado/
├── Aula04_Versionamento_MLflow_DVC/
│   ├── Parte2_MLflow_na_Pratica/
│   ├── Parte3_DVC_para_Dados_e_Pipelines/
│   └── Lab_GitHub_DVC_no_CI/
└── requirements.txt          # ambiente único dos labs Codespaces
```

## Labs Codespaces

### Antes da primeira aula (5 min, uma única vez)
1. No topo da página do repositório no GitHub, clique em **Use this template → Create a new repository** e crie o repositório na sua conta (público).
2. No **seu** repositório: **Code → Codespaces → Create codespace on main**.
3. Aguarde o ambiente terminar de montar. As dependências (`Labs-streamlit/requirements.txt`) são instaladas automaticamente; espere o terminal ficar livre.

Nas aulas seguintes, reabra o mesmo codespace em https://github.com/codespaces. Os comandos dos READMEs partem da raiz do repositório.

### Dicas
- Quando um app sobe numa porta, o Codespaces oferece **Open in Browser**. Se não aparecer, use a aba **Ports**.
- Vários labs usam a porta 8501. Antes de começar um lab novo, pare o app do anterior (Ctrl+C no terminal dele).
- Ao terminar, **pare o codespace** (github.com/codespaces → ⋯ → Stop). Ele consome a sua cota gratuita enquanto está ligado.

## Labs GitHub

Os labs GitHub rodam workflows do **GitHub Actions** no seu repositório. O GitHub só executa workflows que estão em `.github/workflows/` na raiz do repositório, então cada lab traz o seu arquivo `.yml` e o README mostra como copiá-lo para lá. Acompanhe as execuções na aba **Actions** do repositório.
