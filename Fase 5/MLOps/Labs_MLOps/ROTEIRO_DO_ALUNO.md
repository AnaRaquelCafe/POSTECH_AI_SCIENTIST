# Roteiro do aluno — Labs de MLOps

Este roteiro guia você pelos 12 laboratórios da disciplina, na ordem em que acontecem nas aulas. Cada lab leva de 10 a 15 minutos e roda inteiro no **GitHub Codespaces**: você só precisa de uma conta gratuita no GitHub. Não é preciso instalar nada, cadastrar cartão de crédito nem ter conta em nuvem.

Todos os labs contam a mesma história. Uma empresa de assinatura quer prever quais clientes vão cancelar (**churn**). Ao longo das 4 aulas, você leva esse modelo do notebook até a produção:

| Aula | O que acontece com o modelo |
|---|---|
| 01 — Ciclo de vida | é treinado, registrado com aprovação, colocado no ar e monitorado |
| 02 — MLOps | tem os experimentos rastreados e é promovido para produção com segurança |
| 03 — CI/CD para ML | passa a ser testado automaticamente a cada mudança e entra em produção aos poucos (canary) |
| 04 — APIs e containers | vira uma API, é empacotado em Docker e escalado com várias réplicas |

Para cada lab, este roteiro diz **o que você vai fazer**, **o que precisa ter antes**, **os comandos**, **como saber que deu certo** e **o que fazer se der errado**. O `README.md` dentro da pasta de cada lab tem os mesmos passos com mais explicações.

---

## Como a disciplina está organizada

- **4 aulas**, cada uma com **3 partes** em vídeo.
- **1 lab por parte**, de 10 a 15 minutos: 12 labs no total.
- No fim, o **Desafio Final Integrado** (`Docs-Aulas-MLOps/desafio/`), que junta as quatro aulas num cenário único.

### Os labs formam uma linha contínua

Vários labs usam o que o anterior produziu, por isso **faça na ordem**. Se pular algum, a seção "Antes de começar" de cada lab mostra como gerar o que falta em poucos segundos.

| Lab | Usa o que foi feito em |
|---|---|
| 01.2 — Model Registry | o `model.joblib` do Lab 01.1 |
| 01.3 — Deploy e monitoramento | uma versão **aprovada** no Lab 01.2 |
| 02.1 — Caça ao tesouro | funciona melhor com a Aula 01 feita |
| 02.3 — Promoção com aliases | os experimentos do Lab 02.2 |
| 03.2 — Testes de dados e modelo | o pipeline do Lab 03.1, já no GitHub |
| 03.3 — Canary release | nada: o script cria o que faltar |
| 04.2 — Docker e registry | o `model.joblib` do Lab 04.1 |
| 04.3 — Docker Compose | a imagem publicada no Lab 04.2 (ou o Compose faz o build) |

As Aulas 01, 02 e 03 compartilham o **mesmo MLflow** (`Labs_MLOps/mlflow.db`): o que você registra numa aula continua lá na seguinte. **Não apague o `mlflow.db`** entre as aulas, a não ser que queira recomeçar do zero.

## Sugestão de ritmo

| Quando | O que fazer |
|---|---|
| Uma vez, antes da Aula 01 | preparar o ambiente (seção seguinte, ≈ 5 min) |
| Em cada parte de aula | assistir ao vídeo da parte → fazer o lab logo em seguida → anotar as respostas de "Anote para a discussão" |
| No fim de cada aula | marcar o seu progresso no fim deste roteiro e **parar o codespace** |
| Depois da Aula 04 | fazer o Desafio Final Integrado |

Fazer o lab logo depois do vídeo da parte é o que mais ajuda: os comandos fazem sentido enquanto o conceito ainda está fresco.

---

## Antes da primeira aula (5 min, uma única vez)

- [ ] Crie uma conta gratuita em https://github.com, se ainda não tiver. Com e-mail de estudante, peça também o **GitHub Student Developer Pack**: ele aumenta a sua cota gratuita do Codespaces.
- [ ] Abra o repositório da disciplina e clique em **Use this template → Create a new repository**. Deixe como **Public** e crie.
- [ ] No **seu** repositório: **Code → aba Codespaces → Create codespace on main**.
- [ ] Espere o ambiente montar. Na primeira vez leva de 3 a 4 minutos, e o editor abre no navegador.
- [ ] Abra um terminal (menu ☰ → **Terminal → New Terminal**) e rode:
  ```bash
  mlflow --version
  ```
  ✅ Deu certo se aparecer `mlflow, version 3.16.1`. Pronto: o seu ambiente está preparado para todas as aulas.

Nas aulas seguintes, reabra **o mesmo** codespace em https://github.com/codespaces. Ele volta em uns 30 segundos, com tudo o que você fez nas aulas anteriores.

> **Cuide da sua cota gratuita:** ao terminar cada aula, pare o codespace (github.com/codespaces → ⋯ → **Stop**). Ele também para sozinho depois de 30 minutos sem uso.

---

## Como usar o ambiente

- **Os comandos partem da raiz do repositório.** Se você se perder entre pastas, volte para a raiz com:
  ```bash
  cd /workspaces/*
  ```
- **Alguns labs usam dois terminais.** Quando um comando sobe um servidor (MLflow, endpoint, API), aquele terminal fica ocupado. Abra outro com o **+** no painel de terminais.
- **Portas:** quando um serviço sobe, o Codespaces oferece **Open in Browser**. Se o aviso sumir, abra a aba **Ports** e clique no ícone de globo da porta.

| Porta | O que roda nela |
|---|---|
| 5000 | interface do MLflow |
| 5001 | endpoint do modelo (Aula 01 · Parte 3) |
| 5050 | registry de imagens Docker (Aula 04 · Parte 2) |
| 8000 | APIs FastAPI e relatórios HTML |
| 8080 | balanceador de carga (Aula 04 · Parte 3) |

- **Interface do MLflow:** suba sempre com o script abaixo, e não com `mlflow ui`. No Codespaces, o `mlflow ui` puro responde **403**.
  ```bash
  Labs_MLOps/ui_mlflow.sh
  ```
- **Parar um servidor:** Ctrl+C no terminal dele.

---

# Aula 01 — Ciclo de vida de modelos

## Lab 01.1 — EDA e treino (≈ 12 min)

**Neste lab você vai** explorar os dados de 3.000 clientes, treinar um modelo de churn e compará-lo com o **baseline**, a regra que a empresa usa hoje sem machine learning.

**Antes de começar:** nada. É o primeiro lab.

**Passo a passo**
- [ ] Rode o treino:
  ```bash
  cd Labs_MLOps/Aula01_Ciclo_de_Vida_de_Modelos/Parte1_EDA_e_Treino
  python treinar_modelo.py
  ```
- [ ] Leia a saída da EDA: tamanho da base, colunas, valores ausentes, taxa de churn.
- [ ] Compare as linhas `baseline` e `modelo` na tabela de avaliação.
- [ ] No `treinar_modelo.py`, troque `max_depth=5` por `max_depth=None`, rode de novo e compare. Depois volte para `max_depth=5`.

✅ **Deu certo se** a saída termina com `Modelo salvo em .../model.joblib`. Esse arquivo é usado no próximo lab.

⚠️ **Se der errado:** `python: can't open file` quase sempre significa que você não está na pasta do lab. Rode o `cd` de novo.

📝 **Anote para a discussão:** qual coluna tem valores ausentes e onde eles são tratados no código? O modelo supera o baseline em quais métricas? Para uma campanha de retenção, você priorizaria recall ou precision? O que aconteceu com `max_depth=None`?

---

## Lab 01.2 — Model Registry com aprovação (≈ 12 min)

**Neste lab você vai** transformar o `model.joblib` numa **versão registrada** no MLflow, com métricas, versão dos dados e exemplo de entrada anexados, e passá-la por um **gate de aprovação** antes de ela poder ir para produção.

**Antes de começar:** o `model.joblib` do Lab 01.1. Se você faltou, rode antes:
```bash
python Labs_MLOps/Aula01_Ciclo_de_Vida_de_Modelos/Parte1_EDA_e_Treino/treinar_modelo.py
```

**Passo a passo**
- [ ] Registre o modelo:
  ```bash
  cd Labs_MLOps/Aula01_Ciclo_de_Vida_de_Modelos/Parte2_Model_Registry
  python registrar_modelo.py
  ```
- [ ] Passe pelo gate de qualidade:
  ```bash
  python aprovar_modelo.py
  ```
- [ ] Veja o outro caminho: registre de novo e rejeite.
  ```bash
  python registrar_modelo.py
  python aprovar_modelo.py --rejeitar
  ```
- [ ] Num **segundo terminal**, suba a interface e abra a porta 5000 → **Models** → `churn-model`:
  ```bash
  Labs_MLOps/ui_mlflow.sh
  ```

✅ **Deu certo se:**
- o primeiro registro mostra `churn-model versão 1 | aprovacao=PendingManualApproval`;
- o `aprovar_modelo.py` termina com `-> Approved`, e o `--rejeitar` termina com `-> Rejected`;
- na interface, a versão 1 aparece com a tag `aprovacao=Approved` e a versão 2 com `Rejected`.

⚠️ **Se der errado:** `model.joblib não encontrado` significa que o Lab 01.1 não foi feito. Se a interface responder 403, use o `ui_mlflow.sh`.

📝 **Anote para a discussão:** por que registrar o `Pipeline` inteiro, e não só o classificador? Quem deveria aprovar um modelo na sua empresa, e o que mais entraria no gate?

---

## Lab 01.3 — Deploy e monitoramento (≈ 15 min)

**Neste lab você vai** colocar a versão aprovada no ar como um **endpoint em tempo real**, gravar o que chega em produção (**data capture**) e comparar esses dados com os de treino para detectar **drift**.

**Antes de começar:** uma versão aprovada no Lab 01.2.

**Passo a passo**
- [ ] **Terminal 1**: faça o deploy. Este terminal fica ocupado com o servidor.
  ```bash
  cd Labs_MLOps/Aula01_Ciclo_de_Vida_de_Modelos/Parte3_Deploy_e_Monitor
  python deploy_endpoint.py
  ```
  Espere aparecer `Uvicorn running on http://127.0.0.1:5001` (10 a 15 segundos).
- [ ] **Terminal 2**: invoque o endpoint.
  ```bash
  cd Labs_MLOps/Aula01_Ciclo_de_Vida_de_Modelos/Parte3_Deploy_e_Monitor
  python invocar_endpoint.py
  ```
- [ ] Simule um dia de produção em que o perfil dos clientes mudou, e monitore:
  ```bash
  python simular_producao.py --drift
  python monitorar.py
  python -m http.server 8000
  ```
- [ ] Abra a porta 8000 e clique em `relatorio_monitoramento.html`.
- [ ] Se sobrar tempo: rode `simular_producao.py` **sem** `--drift` e `monitorar.py` de novo, e compare.
- [ ] Derrube o endpoint: Ctrl+C no terminal 1.

✅ **Deu certo se:**
- o terminal 1 mostra `Fazendo deploy de churn-model v1` e depois `Uvicorn running`;
- o `invocar_endpoint.py` responde `{'predictions': [1]}`;
- com `--drift`, o relatório do Evidently marca drift em algumas colunas, e sem `--drift` não marca nenhuma.

⚠️ **Se der errado:**
- `Nenhuma versão aprovada`: volte ao Lab 01.2 e rode o `aprovar_modelo.py`.
- `Connection refused` no terminal 2: o endpoint ainda não subiu. Espere o `Uvicorn running` no terminal 1.
- **`404 Not Found` no terminal 1 não é erro.** Ele aparece quando a porta 5001 é aberta no navegador: o servidor de modelos não tem página inicial, só responde em `/invocations`, `/ping` e `/health`.
- `Address already in use`: algum servidor anterior ficou ligado. Use Ctrl+C no terminal dele.

📝 **Anote para a discussão:** quais colunas tiveram drift, e a taxa de churn prevista mudou? Se o resultado real só chega 30 dias depois, você re-treinaria o modelo agora ou esperaria?

---

# Aula 02 — MLOps

## Lab 02.1 — Caça ao tesouro no ecossistema (≈ 10 min, sem código)

**Neste lab você vai** encontrar onde cada peça de uma plataforma MLOps vive no nosso ambiente e relacioná-la aos níveis de maturidade 0, 1 e 2.

**Antes de começar:** funciona melhor com a Aula 01 feita. Se você faltou, rode os comandos de "Antes de começar" do Lab 01.2 e depois o `registrar_modelo.py` da pasta `Parte2_Model_Registry`.

**Passo a passo**
- [ ] Suba a interface do MLflow e abra a porta 5000:
  ```bash
  Labs_MLOps/ui_mlflow.sh
  ```
- [ ] **Experiments:** abra o experimento `ciclo-de-vida`. Ache as métricas, as tags e o artefato do modelo.
- [ ] **Models:** abra `churn-model`. Quantas versões existem? Qual foi aprovada e qual foi rejeitada?
- [ ] **Pipelines:** no seu repositório do GitHub, abra a aba **Actions**. Existe algum pipeline? (Vamos criar um na Aula 03.)
- [ ] **Feature Store:** procure no ambiente. Ela não existe aqui. Por que um time só sente falta dela quando tem vários modelos?
- [ ] Preencha a tabela do README da pasta `Labs_MLOps/Aula02_MLOps/Parte1_Explorando_o_Ecossistema`.

✅ **Deu certo se** você achou as quatro peças (ou percebeu a ausência da Feature Store) e preencheu a tabela.

📝 **Anote para a discussão:** em que nível de maturidade está o que fizemos à mão na Aula 01? O que falta para chegar ao nível 1?

---

## Lab 02.2 — Experiment tracking com MLflow (≈ 12 min)

**Neste lab você vai** treinar o mesmo modelo com três combinações de hiperparâmetros e deixar o MLflow registrar parâmetros, métricas, o modelo e a versão dos dados de cada execução, para depois compará-las.

**Antes de começar:** nada.

**Passo a passo**
- [ ] Rode três experimentos (cada um leva uns 5 segundos):
  ```bash
  cd Labs_MLOps/Aula02_MLOps/Parte2_Experiment_Tracking_MLflow
  python treino_com_mlflow.py --n-estimators 50 --max-depth 3
  python treino_com_mlflow.py --n-estimators 100 --max-depth 5
  python treino_com_mlflow.py --n-estimators 300
  ```
- [ ] Num segundo terminal, suba a interface (`Labs_MLOps/ui_mlflow.sh`) e abra a porta 5000.
- [ ] Abra o experimento `previsao-churn`, selecione os três runs e clique em **Compare**.
- [ ] Abra um run e encontre: os parâmetros, as métricas, a tag `versao_dados_md5` e, em **Artifacts**, o modelo salvo.

✅ **Deu certo se** cada comando termina com `Run registrado. accuracy=... recall=... f1=...` e os três runs aparecem na interface.

📝 **Anote para a discussão:** o run com melhor `f1_score` é o mesmo de melhor `recall`? O que você precisaria para reproduzir um modelo treinado há 3 meses?

---

## Lab 02.3 — Promoção com aliases no Model Registry (≈ 15 min)

**Neste lab você vai** promover o melhor modelo para produção com **aliases**: a versão nova entra como `@challenger`, passa por uma validação e só então vira `@champion`. Também vai ver a validação barrar um modelo ruim e fazer um **rollback**.

**Antes de começar:** os runs do Lab 02.2.

**Passo a passo**
- [ ] Registre o melhor run como candidato, valide, promova e use o modelo:
  ```bash
  cd Labs_MLOps/Aula02_MLOps/Parte3_Model_Registry_MLflow
  python registrar_modelo.py
  python promover_modelo.py
  python prever.py
  ```
- [ ] Treine um modelo pior e tente promovê-lo:
  ```bash
  python ../Parte2_Experiment_Tracking_MLflow/treino_com_mlflow.py --n-estimators 5 --max-depth 2
  python registrar_modelo.py --ultimo
  python promover_modelo.py
  ```
- [ ] Simule um incidente: force o modelo ruim para produção e veja a predição mudar. Use os números de versão que o `promover_modelo.py` acabou de mostrar.
  ```bash
  python promover_modelo.py --versao <versão do @challenger>
  python prever.py
  ```
- [ ] Faça o rollback:
  ```bash
  python promover_modelo.py --versao <versão do @champion>
  python prever.py
  ```
- [ ] Na interface (`Labs_MLOps/ui_mlflow.sh`, porta 5000), veja em **Models → churn-model** as versões e os aliases.

✅ **Deu certo se:**
- o primeiro `promover_modelo.py` mostra `Promovido: @champion agora aponta para a versão N`;
- com o modelo ruim, aparece `NÃO promovido: f1 abaixo do mínimo`;
- no incidente, a probabilidade do `prever.py` muda, e volta ao valor anterior depois do rollback.

⚠️ **Se der errado:** `Nenhum run encontrado` significa que o Lab 02.2 não foi feito. `Ainda não há @champion` significa que nenhum modelo foi promovido ainda: rode `registrar_modelo.py` e `promover_modelo.py`. Os números de versão variam de aluno para aluno, e isso é normal.

📝 **Anote para a discussão:** por que o consumidor carrega `@champion`, e não uma versão fixa? O que mais você exigiria antes de promover um modelo de crédito ou de saúde?

---

# Aula 03 — CI/CD para ML

> Nesta aula, os pipelines rodam no **GitHub Actions** do seu repositório. O `git push` de dentro do codespace não pede senha. Cada execução leva de 30 segundos a 1 minuto e meio, e você acompanha tudo na aba **Actions**.

## Lab 03.1 — CI com GitHub Actions (≈ 15 min)

**Neste lab você vai** criar um pipeline de **integração contínua** que roda os testes a cada push e fica vermelho quando o código quebra.

**Antes de começar:** nada.

**Passo a passo**
- [ ] Rode os testes localmente:
  ```bash
  cd Labs_MLOps/Aula03_CICD_para_ML/Parte1_CI_GitHub_Actions
  pytest tests/ -v
  ```
- [ ] Crie o pipeline. O GitHub só executa workflows que estão em `.github/workflows/`, na raiz:
  ```bash
  cd "$(git rev-parse --show-toplevel)"
  mkdir -p .github/workflows
  cp Labs_MLOps/Aula03_CICD_para_ML/Parte1_CI_GitHub_Actions/ci.yml .github/workflows/ci-mlops.yml
  git add .github/workflows/ci-mlops.yml
  git commit -m "Adiciona pipeline de CI"
  git push
  ```
- [ ] No seu repositório no GitHub, abra **Actions → CI MLOps**, clique no run e abra o job `test-code`.
- [ ] Quebre de propósito: em `src/features.py`, apague o `.clip(18, 100)`, rode o `pytest` localmente e faça commit e push mesmo assim.
- [ ] Desfaça a alteração, faça commit e push de novo.

✅ **Deu certo se:**
- o `pytest` local mostra `5 passed`;
- o primeiro run fica **verde** em uns 30 segundos;
- o run com o `.clip` apagado fica **vermelho** (e chega um e-mail do GitHub), e o seguinte volta ao verde.

⚠️ **Se der errado:**
- o workflow não aparece em Actions: confira se o arquivo está em `.github/workflows/` **na raiz** (`ls .github/workflows`) e se o `git push` foi feito;
- o workflow não disparou: ele só roda quando o commit muda arquivos da Aula 03 ou o próprio `.yml`. Em último caso, use **Actions → CI MLOps → Run workflow**.

📝 **Anote para a discussão:** por que o pipeline só dispara quando arquivos da Aula 03 mudam? O que pode quebrar um modelo em produção mesmo com todos os testes de código passando?

---

## Lab 03.2 — Testes de dados e de modelo no pipeline (≈ 15 min)

**Neste lab você vai** acrescentar ao pipeline as duas camadas de teste que só existem em ML: **qualidade dos dados** e **qualidade do modelo**, em três jobs encadeados.

**Antes de começar:** o pipeline do Lab 03.1 funcionando.

**Passo a passo**
- [ ] Rode as validações localmente:
  ```bash
  cd Labs_MLOps/Aula03_CICD_para_ML/Parte2_Testes_Dados_e_Modelo
  python scripts/test_data_quality.py
  python scripts/test_model_quality.py
  ```
- [ ] Troque o pipeline:
  ```bash
  cd "$(git rev-parse --show-toplevel)"
  cp Labs_MLOps/Aula03_CICD_para_ML/Parte2_Testes_Dados_e_Modelo/ci.yml .github/workflows/ci-mlops.yml
  git add .github/workflows/ci-mlops.yml
  git commit -m "Pipeline com testes de dados e modelo"
  git push
  ```
- [ ] Faça o pipeline falhar: em `scripts/test_model_quality.py`, mude `THRESHOLD_ACCURACY` para `0.99`. Commit e push.
- [ ] Corrija: volte para `0.75`, commit e push.

✅ **Deu certo se:**
- localmente aparecem `Dados OK` e `Modelo OK.`;
- no Actions, três jobs rodam em sequência, `test-code → test-data → test-model`, todos verdes (cerca de 1 minuto e meio no total);
- com `0.99`, só o `test-model` fica vermelho, com `FALHOU - accuracy abaixo do mínimo`.

📝 **Anote para a discussão:** que tipo de problema só o teste de dados ou o de modelo pega? Por que "passar no threshold" não basta?

---

## Lab 03.3 — Canary release (≈ 15 min)

**Neste lab você vai** colocar um modelo novo no ar recebendo só **10% do tráfego**, aumentar essa fatia aos poucos e fazer um rollback, sem derrubar o serviço.

**Antes de começar:** nada. O primeiro comando cria o que faltar.

**Passo a passo**
- [ ] Prepare as duas variantes:
  ```bash
  cd Labs_MLOps/Aula03_CICD_para_ML/Parte3_Canary_Release
  python preparar_variantes.py
  ```
- [ ] **Terminal 1**: suba o roteador (ele fica ocupado).
  ```bash
  uvicorn roteador:app --port 8000
  ```
- [ ] **Terminal 2**: gere tráfego e ajuste os pesos.
  ```bash
  cd Labs_MLOps/Aula03_CICD_para_ML/Parte3_Canary_Release
  python invocar_varias_vezes.py
  python ajustar_pesos.py 50 50
  python invocar_varias_vezes.py
  python ajustar_pesos.py 0 100
  python invocar_varias_vezes.py
  python ajustar_pesos.py 100 0
  ```
- [ ] Ctrl+C no terminal 1.

✅ **Deu certo se** a distribuição acompanha os pesos: cerca de 90/10 no começo, cerca de 50/50 depois e 100% em uma variante nos extremos. Variações como 87/13 são normais, porque a divisão é sorteada.

⚠️ **Se der errado:** se o roteador não subir por falta de `@challenger`, rode o `preparar_variantes.py` de novo. `Address already in use`: algum servidor anterior ficou ligado na porta 8000.

📝 **Anote para a discussão:** quando você avançaria de 10% para 50%, olhando quais métricas? Como seria um shadow mode neste roteador?

---

# Aula 04 — Deploy de APIs e containers

## Lab 04.1 — API com FastAPI (≈ 12 min)

**Neste lab você vai** servir o modelo de churn como uma **API HTTP**, com validação de entrada pelo Pydantic e documentação gerada automaticamente.

**Antes de começar:** nada.

**Passo a passo**
- [ ] Gere o modelo e suba a API:
  ```bash
  cd Labs_MLOps/Aula04_Deploy_APIs_e_Containers/Parte1_API_com_FastAPI
  python treinar_modelo_exemplo.py
  uvicorn main:app --reload --port 8000
  ```
- [ ] Abra a porta 8000 (aba **Ports**) e acrescente `/docs` ao endereço.
- [ ] Teste o `POST /predict` (**Try it out**) com:
  ```json
  {"idade": 23, "meses": 2, "valor_mensal": 210, "chamados_suporte": 4}
  ```
  Depois troque para um cliente antigo e tranquilo (`"meses": 60, "chamados_suporte": 0`).
- [ ] Mande um dado inválido, como `"idade": 12`.
- [ ] Teste o `GET /health`.
- [ ] Ctrl+C para parar a API.

✅ **Deu certo se:**
- o cliente de risco recebe `"prediction": 1` com probabilidade alta, e o cliente tranquilo, uma probabilidade bem menor;
- o dado inválido recebe **422**, com a explicação do erro;
- o `/health` responde `"model_loaded": true`.

📝 **Anote para a discussão:** por que o modelo é carregado uma vez, na inicialização? Você usaria esta API para um scoring em lote semanal?

---

## Lab 04.2 — Docker e registry de imagens (≈ 15 min)

**Neste lab você vai** empacotar a API numa **imagem Docker** com boas práticas e publicá-la num **registry**, de onde qualquer servidor consegue baixá-la.

**Antes de começar:** o `model.joblib` do Lab 04.1. Se você faltou, rode `python treinar_modelo_exemplo.py` na pasta `Parte1_API_com_FastAPI`.

**Passo a passo**
- [ ] Faça o build e rode o container. O primeiro build leva cerca de 1 minuto:
  ```bash
  cd Labs_MLOps/Aula04_Deploy_APIs_e_Containers/Parte2_Docker_e_Registry
  docker build -t churn-api -f Dockerfile ../Parte1_API_com_FastAPI
  docker run --rm -d -p 8000:8000 --name churn churn-api
  docker ps
  curl localhost:8000/health
  docker stop churn
  ```
- [ ] Suba um registry e publique a imagem:
  ```bash
  docker run -d -p 5050:5000 --name registry registry:2
  docker tag churn-api localhost:5050/churn-api:v1
  docker push localhost:5050/churn-api:v1
  curl localhost:5050/v2/_catalog
  ```
- [ ] Prove que a imagem vem do registry:
  ```bash
  docker rmi churn-api localhost:5050/churn-api:v1
  docker run --rm -d -p 8000:8000 --name churn localhost:5050/churn-api:v1
  curl localhost:8000/health
  docker stop churn
  ```
- [ ] **Deixe o registry rodando:** o Lab 04.3 usa a imagem publicada aqui.

✅ **Deu certo se:**
- o `docker ps` mostra o container como `(healthy)` depois de uns 10 segundos;
- o `/health` responde `"model_loaded": true`;
- o catálogo do registry mostra `{"repositories":["churn-api"]}`;
- depois do `docker rmi`, o `docker run` baixa a imagem do registry e ela responde de novo.

⚠️ **Se der errado:**
- `Cannot connect to the Docker daemon`: o Docker do codespace ainda está iniciando. Espere 30 segundos;
- `container name "/registry" (ou "/churn") is already in use`: sobrou um container de outra tentativa. Rode `docker rm -f registry churn`;
- `port is already allocated`: rode `docker ps` e pare o container que está usando a porta.

📝 **Anote para a discussão:** por que o `pip install` vem antes de copiar o código no Dockerfile? Quem deveria poder publicar imagens no registry de uma empresa?

---

## Lab 04.3 — Escalando com Docker Compose (≈ 15 min)

**Neste lab você vai** rodar **várias réplicas** da API atrás de um **balanceador de carga**, escalar, derrubar uma réplica sem o serviço cair e ganhar uma **URL pública**.

**Antes de começar:** a imagem publicada no Lab 04.2. Se você faltou, tudo bem: o Compose faz o build sozinho, só leva um minuto a mais.

**Passo a passo**
- [ ] Suba 3 réplicas e o balanceador:
  ```bash
  cd Labs_MLOps/Aula04_Deploy_APIs_e_Containers/Parte3_Escala_com_Docker_Compose
  docker compose up -d
  docker compose ps
  ```
- [ ] Veja o balanceamento:
  ```bash
  python testar_balanceamento.py
  ```
- [ ] Escale para 5 réplicas:
  ```bash
  docker compose up -d --scale api=5
  docker compose restart balanceador
  python testar_balanceamento.py
  ```
- [ ] Derrube uma réplica (copie um nome da coluna NAME do `docker compose ps`):
  ```bash
  docker compose ps
  docker stop <nome-de-uma-réplica>
  python testar_balanceamento.py
  ```
- [ ] Rode `docker compose up -d` e `docker compose ps` de novo e veja quantas réplicas voltaram.
- [ ] URL pública: na aba **Ports**, clique com o botão direito na porta 8080 → **Port Visibility → Public**. Abra o endereço com `/docs` no final.
- [ ] Desligue tudo:
  ```bash
  docker compose down
  docker rm -f registry
  ```

✅ **Deu certo se:**
- com 3 réplicas, as 60 chamadas se dividem em 20 para cada container; com 5, em 12 para cada;
- depois de derrubar uma réplica, as chamadas continuam respondendo, divididas entre as que sobraram;
- o `docker compose up -d` volta para as **3** réplicas declaradas no arquivo, e não para as 5 do `--scale`.

⚠️ **Se der errado:** se o balanceador responder **502** logo depois de escalar, rode `docker compose restart balanceador` e espere uns segundos.

📝 **Anote para a discussão:** que métrica você usaria para escalar automaticamente? O que se perde de controle ao usar um serviço gerenciado, como App Runner ou Cloud Run?

---

## Registro de progresso

Marque cada lab quando ver o "✅ Deu certo se…" na sua tela.

| Aula | Parte 1 | Parte 2 | Parte 3 |
|---|---|---|---|
| 01 — Ciclo de vida | [ ] EDA e treino | [ ] Model Registry | [ ] Deploy e monitoramento |
| 02 — MLOps | [ ] Caça ao tesouro | [ ] Experiment tracking | [ ] Promoção com aliases |
| 03 — CI/CD para ML | [ ] CI com GitHub Actions | [ ] Testes de dados e modelo | [ ] Canary release |
| 04 — APIs e containers | [ ] API com FastAPI | [ ] Docker e registry | [ ] Docker Compose |

---

## Problemas comuns (em qualquer lab)

| Sintoma | O que fazer |
|---|---|
| `command not found` (`mlflow`, `pytest`, `uvicorn`) logo depois de criar o codespace | O ambiente ainda estava instalando quando o terminal abriu. Espere terminar e **abra um terminal novo** |
| O codespace abriu com aviso de *recovery mode* | *Command Palette* (Ctrl/Cmd+Shift+P) → **Codespaces: Rebuild Container**. Se continuar, apague o codespace e crie outro |
| A porta não abre no navegador | Aba **Ports** → ícone de globo da porta |
| `Address already in use` | Um servidor de outro lab ficou ligado. Ctrl+C no terminal dele |
| A interface do MLflow responde 403 | Suba com `Labs_MLOps/ui_mlflow.sh`, e não com `mlflow ui` |
| Quer recomeçar o MLflow do zero | Na pasta `Labs_MLOps`: `rm -rf mlflow.db mlartifacts` |
| Faltou a uma aula | Cada lab diz em "Antes de começar" o que precisa e como gerar rapidamente |

Ao terminar cada aula: **pare o codespace** em github.com/codespaces → ⋯ → **Stop**.

---

## E depois dos labs: o Desafio Final Integrado

O desafio (`Docs-Aulas-MLOps/desafio/Desafio_Final_Integrado.docx`) é uma atividade individual de reflexão: uma empresa de e-commerce tem um modelo de churn que funciona no notebook e precisa levá-lo para produção em 6 semanas. Você responde, em no máximo 2 páginas, uma pergunta por aula: o ciclo de vida do modelo, o uso de MLflow e de ferramentas MLOps, os testes e a estratégia de deploy, e como servir e escalar o modelo.

Os labs são a sua base para responder: tudo o que o desafio pergunta, você já fez na prática aqui. Releia as suas anotações de "Anote para a discussão" antes de começar. Não existe resposta certa; o que conta é justificar os trade-offs.
