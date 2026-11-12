# Roteiro do aluno — Labs de "Fazendo o seu primeiro deploy com Streamlit"

Este roteiro guia você pelos labs da disciplina, na ordem das aulas. Cada lab leva de 12 a 15 minutos e roda no **GitHub Codespaces**: você só precisa de uma conta gratuita no GitHub. Não é preciso instalar nada, cadastrar cartão de crédito nem ter conta em nuvem.

Todos os labs usam o mesmo cenário: um modelo que prevê quais clientes de uma empresa de assinatura vão cancelar (**churn**). Ao longo das 4 aulas, ele vira um app publicado na web, é empacotado em Docker, é monitorado contra drift e ganha versionamento de dados e de modelos.

Para cada lab, este roteiro diz **o que você vai fazer**, **o que precisa ter antes**, **os comandos**, **como saber que deu certo** e **o que fazer se der errado**. O `README.md` dentro da pasta de cada lab tem os mesmos passos com mais explicações.

## Como a disciplina está organizada

- **4 aulas**, cada uma com **3 partes** em vídeo.
- **1 lab por parte** (a Parte 1 da Aula 04 é conceitual e não tem lab): 11 labs.
- **1 Lab GitHub por aula**, no fim da Parte 3: ele leva o assunto da aula para o GitHub Actions. São 4 labs.
- No fim, o **Desafio Final Integrado** (`Docs-Aulas-streamlit/desafio/`).

**Cada parte é independente:** a pasta de cada lab já traz o modelo, os dados ou os scripts de que ele precisa. Se você perdeu uma parte, pode fazer a seguinte normalmente.

## Sugestão de ritmo

| Quando | O que fazer |
|---|---|
| Uma vez, antes da Aula 01 | preparar o ambiente (seção seguinte, ≈ 5 min) |
| Em cada parte de aula | assistir ao vídeo da parte → fazer o lab logo em seguida → anotar as respostas de "Anote para a discussão" |
| No fim de cada aula | fazer o Lab GitHub, marcar o seu progresso no fim deste roteiro e **parar o codespace** |
| Depois da Aula 04 | fazer o Desafio Final Integrado |

---

## Antes da primeira aula (5 min, uma única vez)

- [ ] Crie uma conta gratuita em https://github.com, se ainda não tiver. Com e-mail de estudante, peça também o **GitHub Student Developer Pack**: ele aumenta a sua cota gratuita do Codespaces.
- [ ] Abra o repositório da disciplina e clique em **Use this template → Create a new repository**. Deixe como **Public** (o Streamlit Cloud e o GitHub Container Registry funcionam melhor com repositório público) e crie.
- [ ] No **seu** repositório: **Code → aba Codespaces → Create codespace on main**.
- [ ] Espere o ambiente montar. Na primeira vez leva de 3 a 4 minutos, e o editor abre no navegador.
- [ ] Abra um terminal (menu ☰ → **Terminal → New Terminal**) e rode:
  ```bash
  streamlit version
  ```
  ✅ Deu certo se aparecer `Streamlit, version 1.64.0`. Pronto: o seu ambiente está preparado para todas as aulas.

Nas aulas seguintes, reabra **o mesmo** codespace em https://github.com/codespaces. Ele volta em uns 30 segundos.

> **Cuide da sua cota gratuita:** ao terminar cada aula, pare o codespace (github.com/codespaces → ⋯ → **Stop**). Ele também para sozinho depois de 30 minutos sem uso.

## Como usar o ambiente

- **Os comandos partem da raiz do repositório.** Se você se perder entre pastas, volte para a raiz com `cd /workspaces/*`.
- **Porta 8501:** vários labs sobem um app Streamlit nela. **Antes de começar um lab novo, pare o app do anterior** (Ctrl+C no terminal dele).
- **Abrir uma porta:** quando um app sobe, o Codespaces oferece **Open in Browser**. Se o aviso sumir, abra a aba **Ports** e clique no ícone de globo da porta.
- **Labs GitHub:** os pipelines rodam no **GitHub Actions** do seu repositório. O `git push` de dentro do codespace não pede senha. Cada execução leva de 30 segundos a 2 minutos, e você acompanha na aba **Actions**.

---

# Aula 01 — Pipeline de ML e deploy no Streamlit

## Lab 01.1 — Estruturando o pipeline (≈ 12 min)

**Neste lab você vai** rodar um pipeline de treino organizado em etapas (ingestão, pré-processamento, treino, avaliação e serialização), usar o artefato gerado para fazer predições e ver por que treino e serving ficam desacoplados.

**Antes de começar:** nada.

**Passo a passo**
- [ ] Rode o treino:
  ```bash
  cd Labs-streamlit/Aula01_Pipeline_ML_Streamlit/Parte1_Estruturando_o_Pipeline
  python train.py
  ```
- [ ] Faça duas predições:
  ```bash
  python prever.py --idade 22 --meses 1 --valor 190
  python prever.py --idade 70 --meses 60 --valor 30
  ```
- [ ] Abra o `prever.py` e veja que ele não faz nenhum pré-processamento.
- [ ] Em `construir_pipeline()`, troque o `RandomForestClassifier` pela `LogisticRegression` (a linha já está comentada), rode `train.py` e `prever.py` de novo.
- [ ] Rode `train.py` duas vezes com `SEMENTE = 42` e duas vezes com `SEMENTE = None`. Volte para `42` ao terminar.

✅ **Deu certo se:**
- o `train.py` mostra as quatro etapas e salva o `modelo_churn.joblib`;
- o cliente jovem e novo tem probabilidade de churn bem maior que o cliente antigo (com o RandomForest, cerca de 83% contra 3%);
- com `SEMENTE = 42` o F1 se repete, e com `SEMENTE = None` muda a cada execução.

📝 **Anote para a discussão:** por que o `prever.py` funciona sem padronizar os dados? O que daria errado se o scaler e o modelo fossem salvos em arquivos separados? Por que fixar a semente para comparar modelos?

---

## Lab 01.2 — Interface com Streamlit (≈ 13 min)

**Neste lab você vai** rodar um app de predição em Streamlit, ver que o script inteiro roda de novo a cada interação e sentir na prática o efeito do cache.

**Antes de começar:** nada. O modelo já vem na pasta.

**Passo a passo**
- [ ] Suba o app:
  ```bash
  cd Labs-streamlit/Aula01_Pipeline_ML_Streamlit/Parte2_Interface_Streamlit
  streamlit run app.py
  ```
- [ ] Teste um cliente jovem, com 1 mês de casa e mensalidade alta.
- [ ] Mova o slider de idade várias vezes e observe o contador **Execuções do script** na barra lateral e o terminal.
- [ ] No `app.py`, comente a linha `@st.cache_resource`, salve, clique em **Rerun** e mova o slider de novo. Depois descomente.
- [ ] Troque `limiar = 0.5` (marcado com `TODO`) por `limiar = st.slider("Limiar de risco", 0.1, 0.9, 0.5)`, salve e clique em **Rerun**.
- [ ] Se sobrar tempo: faça o desafio de predição em lote do README da pasta.
- [ ] Ctrl+C para parar o app.

✅ **Deu certo se:**
- o contador sobe a cada interação, mas `Carregando o modelo do disco...` aparece **uma vez** no terminal;
- sem o cache, cada interação demora uns 2 segundos e o terminal mostra o modelo sendo recarregado toda vez;
- com o slider de limiar, o mesmo cliente muda de "baixo risco" para "em risco" sem o modelo mudar.

⚠️ **Se der errado:** `Port 8501 is already in use`: outro app ainda está rodando. Pare-o com Ctrl+C no terminal dele.

📝 **Anote para a discussão:** o que acontece com um app que consulta um banco lento sem cache? Por que o resultado da predição some quando você mexe no slider depois de clicar em **Prever**?

---

## Lab 01.3 — Publicando na web (≈ 14 min)

**Neste lab você vai** publicar o app no **Streamlit Community Cloud**, direto do seu repositório, e ganhar um link público que se atualiza sozinho a cada `git push`.

**Antes de começar:** o seu repositório precisa ser **público**.

**Passo a passo**
- [ ] Confira os três arquivos do deploy:
  ```bash
  cd Labs-streamlit/Aula01_Pipeline_ML_Streamlit/Parte3_Publicando_na_Web
  ls
  cat requirements.txt
  pip show scikit-learn | grep Version
  ```
- [ ] No `app.py`, troque `AUTOR = "Seu nome"` pelo seu nome. Teste com `streamlit run app.py` e pare com Ctrl+C.
- [ ] Envie para o GitHub:
  ```bash
  git add app.py
  git commit -m "Personaliza o app"
  git push
  ```
- [ ] Em https://share.streamlit.io, entre com a sua conta do GitHub e clique em **Create app → Deploy a public app from GitHub**.
- [ ] Preencha o formulário. Os campos já vêm com um texto de exemplo: **apague o texto antes de digitar**.
  - **Repository:** o seu (selecione na lista que aparece)
  - **Branch:** `main`
  - **Main file path:** `Labs-streamlit/Aula01_Pipeline_ML_Streamlit/Parte3_Publicando_na_Web/app.py`
  - **Advanced settings → Python version: 3.12** (o padrão vem com outra versão)
- [ ] Clique em **Deploy** e abra o link público no celular.
- [ ] Atualização contínua: mude o texto do `st.title(...)` no `app.py`, faça `git add`, `git commit` e `git push` de novo, e espere cerca de 1 minuto.

✅ **Deu certo se:**
- a versão do scikit-learn do `pip show` é a mesma do `requirements.txt`;
- o app abre no link público e a predição funciona;
- depois do último push, o título novo aparece no app publicado sem você clicar em nada no Streamlit Cloud.

⚠️ **Se der errado:**
- **"This repository does not exist"**: o seu repositório está privado. Deixe-o público em **Settings → General → Danger Zone → Change visibility**;
- campo ficou `mastermain` ou `streamlit_app.pyLabs-streamlit/...`: o texto de exemplo não foi apagado. Selecione tudo (Ctrl/Cmd+A) e digite de novo;
- a tela **"Your app is in the oven"** passou de 1 minuto: recarregue a página (F5). O app costuma estar no ar em menos de 30 segundos;
- erro ao carregar o modelo: confira se escolheu **Python 3.12** em Advanced settings.

📝 **Anote para a discussão:** esse app aguentaria 1.000 requisições por segundo? Que cuidado você teria antes de publicar um modelo treinado com dados reais de clientes?

---

## Lab GitHub 01 — Testes automáticos do app (≈ 12 min)

**Neste lab você vai** colocar testes da interface antes do deploy. Se cada push atualiza o app publicado, um push com erro derruba o app. O GitHub Actions passa a rodar os testes a cada push.

**Antes de começar:** nada.

**Passo a passo**
- [ ] Rode os testes localmente:
  ```bash
  cd Labs-streamlit/Aula01_Pipeline_ML_Streamlit/Lab_GitHub_CI_do_App
  pytest tests/ -v
  ```
- [ ] Ligue o workflow:
  ```bash
  cd "$(git rev-parse --show-toplevel)"
  mkdir -p .github/workflows
  cp Labs-streamlit/Aula01_Pipeline_ML_Streamlit/Lab_GitHub_CI_do_App/ci-app.yml .github/workflows/
  git add .github/workflows/ci-app.yml
  git commit -m "CI do app Streamlit"
  git push
  ```
- [ ] No GitHub, abra **Actions → CI do app Streamlit** e acompanhe o job `testar-app`.
- [ ] Quebre de propósito: no `app.py` desta pasta, troque `"valor_mensal"` por `"valor"` em `columns=[...]`. Rode o `pytest`, faça commit e push.
- [ ] Desfaça a alteração, faça commit e push de novo.

✅ **Deu certo se:**
- localmente aparece `4 passed`;
- o primeiro run fica **verde** em uns 30 segundos;
- com o erro de digitação, aparecem `3 failed, 1 passed` e o run fica **vermelho**; depois de desfazer, volta ao verde.

⚠️ **Se der errado:** o workflow não aparece em Actions: confira se o `.yml` está em `.github/workflows/` **na raiz** do repositório e se o `git push` foi feito.

📝 **Anote para a discussão:** quando o modelo for re-treinado, o teste "cliente de alto risco" pode falhar. Isso é um bug do teste ou um aviso útil? O que mais você testaria antes de publicar um app de ML?

---

# Aula 02 — Containerização com Docker

> Os builds de Docker desta aula levam cerca de 1 minuto na primeira vez. É normal, e no Lab 02.2 essa espera é justamente o assunto.

## Lab 02.1 — Entendendo containers (≈ 12 min)

**Neste lab você vai** usar os comandos essenciais do Docker e sentir na prática a diferença entre imagem, container e registry.

**Antes de começar:** nada. Os comandos rodam em qualquer pasta.

**Passo a passo**
- [ ] Rode três versões de Python sem instalar nada:
  ```bash
  python --version
  docker run --rm python:3.10-slim python --version
  docker run --rm python:3.13-slim python --version
  docker images python
  ```
- [ ] Suba um servidor web em segundo plano, abra a porta 8000 e depois pare e remova o container:
  ```bash
  docker run -d --name meu-servidor -p 8000:8000 python:3.12-slim python -m http.server 8000
  docker ps
  docker logs meu-servidor
  docker stop meu-servidor
  docker ps -a
  docker rm meu-servidor
  ```
- [ ] Veja que o container é descartável:
  ```bash
  docker run --name teste python:3.12-slim sh -c "echo 'dados importantes' > /nota.txt && cat /nota.txt"
  docker run --rm python:3.12-slim cat /nota.txt
  docker diff teste
  docker rm teste
  ```
- [ ] Compare imagens leves:
  ```bash
  docker pull python:3.12-alpine
  docker images python
  ```

✅ **Deu certo se:**
- cada container mostra a sua própria versão de Python (3.10 e 3.13), embora o codespace tenha a 3.12;
- o segundo `cat /nota.txt` **falha** com `No such file or directory`, e o `docker diff` mostra `A /nota.txt`;
- a imagem `alpine` é bem menor que a `slim`.

⚠️ **Se der errado:** o `docker stop` leva uns 10 segundos, e isso é esperado: o servidor de teste ignora o pedido para encerrar, e o Docker espera antes de forçar. `Cannot connect to the Docker daemon`: o Docker do codespace ainda está iniciando, espere 30 segundos.

📝 **Anote para a discussão:** como o Docker resolve o conflito entre o scikit-learn 1.5 do seu colega e o 1.8 instalado na sua máquina? Se o container é descartável, onde você guardaria o `.joblib` de um modelo em produção?

---

## Lab 02.2 — Escrevendo um Dockerfile (≈ 15 min)

**Neste lab você vai** empacotar o app de churn numa imagem Docker e descobrir por que a ordem das instruções do Dockerfile muda tudo no tempo de build.

**Antes de começar:** nenhum app rodando na porta 8501.

**Passo a passo**
- [ ] Leia o `Dockerfile` (6 instruções), faça o build e rode:
  ```bash
  cd Labs-streamlit/Aula02_Containerizacao_Docker/Parte2_Escrevendo_um_Dockerfile
  docker build -t churn-app .
  docker run --rm -p 8501:8501 churn-app
  ```
  Abra a porta 8501, confira o app e pare com Ctrl+C. **Anote quanto tempo o build levou.**
- [ ] Mude o texto do `st.caption(...)` no `app.py` e reconstrua com `docker build -t churn-app .`.
- [ ] Reorganize o `Dockerfile` para que o `pip install` venha antes de copiar o código. Faça um build, mude o `app.py` de novo e reconstrua. (A resposta está em `solucao/Dockerfile`.)
- [ ] Inspecione:
  ```bash
  docker images churn-app
  docker history churn-app
  ```

✅ **Deu certo se:**
- o primeiro build leva cerca de 1 minuto, e o segundo, só por mudar um texto, leva **o mesmo tempo** (o `pip install` rodou de novo);
- com o Dockerfile corrigido, o `pip install` aparece como `CACHED` e o build termina em poucos segundos;
- no `docker history`, a camada do `pip install` é a maior.

📝 **Anote para a discussão:** quanto tempo essa ordem economiza por dia numa equipe? Num multi-stage build, o que poderia ficar de fora da imagem final num projeto de ML?

---

## Lab 02.3 — Boas práticas, volumes e Compose (≈ 15 min)

**Neste lab você vai** aplicar quatro boas práticas: rodar como usuário sem privilégios, manter dados fora da imagem, trocar o modelo sem reconstruir a imagem e subir dois serviços juntos com o Docker Compose.

**Antes de começar:** nenhum app rodando na porta 8501.

**Passo a passo**
- [ ] Usuário sem privilégios:
  ```bash
  cd Labs-streamlit/Aula02_Containerizacao_Docker/Parte3_Boas_Praticas_e_Compose
  docker build -t churn-app:seguro .
  docker run --rm churn-app:seguro whoami
  docker run --rm python:3.12-slim whoami
  ```
- [ ] O que não deve entrar na imagem: crie um arquivo de 100 MB e reconstrua, olhando a linha `transferring context`.
  ```bash
  mkdir -p dados && head -c 100000000 /dev/urandom > dados/historico_bruto.csv
  docker build -t churn-app:seguro .
  ```
  Depois comente a linha `dados/` no `.dockerignore`, reconstrua e rode `docker images churn-app`. Desfaça o comentário e apague a pasta com `rm -rf dados`.
- [ ] Modelo fora da imagem, com volume:
  ```bash
  docker run --rm -p 8501:8501 -v "$(pwd)/modelos:/app/modelos" churn-app:seguro
  ```
  Num segundo terminal, na mesma pasta, rode `echo "v2 (retreinado)" > modelos/versao.txt`, volte ao app e clique em **Rerun**. Pare com Ctrl+C e restaure com `echo "v1 (treinado em set/2026)" > modelos/versao.txt`.
- [ ] Dois serviços com Compose (pare com Ctrl+C e depois remova):
  ```bash
  docker compose up --build
  docker compose down
  ```
- [ ] Opcional: escaneie a imagem com o Trivy (comando no README da pasta; leva cerca de 1 minuto na primeira vez).

✅ **Deu certo se:**
- a nossa imagem responde `appuser`, e a imagem base, `root`;
- com o `.dockerignore` ativo, o contexto fica abaixo de 1 kB; sem ele, passa de 100 MB;
- a versão do modelo na barra lateral muda **sem rebuild**;
- os logs do Compose mostram `app fora do ar` no começo e depois `app saudável`.

📝 **Anote para a discussão:** o modelo deveria ir dentro da imagem ou num volume? Por que separar app e monitor em containers diferentes?

---

## Lab GitHub 02 — Imagem no GitHub Container Registry (≈ 15 min)

**Neste lab você vai** deixar o GitHub Actions construir a imagem do app a cada push e publicá-la no GitHub Container Registry (`ghcr.io`), de onde qualquer máquina consegue baixá-la e rodá-la.

**Antes de começar:** nada.

**Passo a passo**
- [ ] Ligue o workflow:
  ```bash
  cd "$(git rev-parse --show-toplevel)"
  mkdir -p .github/workflows
  cp Labs-streamlit/Aula02_Containerizacao_Docker/Lab_GitHub_GHCR/ghcr.yml .github/workflows/
  git add .github/workflows/ghcr.yml
  git commit -m "Publica a imagem no GHCR"
  git push
  ```
- [ ] Na aba **Actions**, acompanhe o job `publicar` (cerca de 1 minuto e meio).
- [ ] No seu perfil do GitHub, abra **Packages → churn-app**. A imagem nasce **privada**: em **Package settings → Danger Zone → Change visibility**, deixe-a **Public**.
- [ ] Rode a imagem publicada e abra a porta 8501:
  ```bash
  IMAGEM=ghcr.io/$(echo "$GITHUB_USER" | tr '[:upper:]' '[:lower:]')/churn-app
  docker run --rm -p 8501:8501 $IMAGEM:latest
  ```
- [ ] Publique uma versão nova: mude o `st.caption(...)` no `app.py` desta pasta, faça commit e push, espere o workflow e rode `docker pull $IMAGEM:latest` e o `docker run` de novo.

✅ **Deu certo se:**
- o job `publicar` fica verde e o pacote `churn-app` aparece com duas tags: `latest` e o SHA do commit;
- o `docker run` baixa a imagem e o app abre na porta 8501;
- depois do segundo push, o texto novo aparece, e a tag do SHA antigo continua disponível em **Packages**.

⚠️ **Se der errado:** `denied` no `docker run`: o pacote ainda está privado. Mude a visibilidade para **Public**.

📝 **Anote para a discussão:** por que usar a tag do SHA em produção, e não `latest`? O que muda quando o modelo é re-treinado toda semana?

---

# Aula 03 — Monitoramento de drift

## Lab 03.1 — Entendendo a degradação (≈ 12 min)

**Neste lab você vai** ver um modelo "envelhecer" em 12 meses de produção simulada e descobrir qual nível de monitoramento (infraestrutura, dados, proxy ou F1 real) percebe cada tipo de problema.

**Antes de começar:** nada.

**Passo a passo**
- [ ] Rode a linha de base e os três cenários, um de cada vez:
  ```bash
  cd Labs-streamlit/Aula03_Monitoramento_Drift/Parte1_Entendendo_a_Degradacao
  python degradacao.py estavel
  python degradacao.py dados_quebrados
  python degradacao.py data_drift
  python degradacao.py concept_drift
  ```
- [ ] Para cada cenário, preencha a tabela do README da pasta: a infra percebeu? Os dados denunciaram? O proxy mudou? O F1 caiu?

✅ **Deu certo se** cada comando mostra uma tabela de 12 meses com latência, dados, churn previsto e F1 real, e você preencheu a tabela dos três cenários.

📝 **Anote para a discussão:** em qual cenário nenhuma métrica do dia a dia acusou o problema? Drift nos dados é sempre um problema? Qual equipe você acionaria no cenário `dados_quebrados`?

---

## Lab 03.2 — Detectando drift (≈ 13 min)

**Neste lab você vai** provocar drift nos dados e medi-lo com **PSI**, **Kolmogorov-Smirnov** e **qui-quadrado**, e ver como o tamanho da janela de análise muda a resposta.

**Antes de começar:** nada.

**Passo a passo**
- [ ] Rode sem drift:
  ```bash
  cd Labs-streamlit/Aula03_Monitoramento_Drift/Parte2_Detectando_Drift
  python drift_lab.py
  ```
- [ ] No topo do `drift_lab.py`, altere **um valor por vez**, rode de novo e volte ao padrão antes do próximo: `DESLOCAMENTO_IDADE = 5`, `DESLOCAMENTO_IDADE = 7`, `FATOR_VALOR_MENSAL = 1.2`, `PROPORCAO_PREMIUM = 0.18` e `DESLOCAMENTO_IDADE = 2`.
- [ ] Com `DESLOCAMENTO_IDADE = 2`, mude `TAMANHO_ANALISE` para `150` e depois para `20000`. Volte tudo ao padrão ao terminar.

✅ **Deu certo se** sem alterações tudo aparece como **estável**, e cada alteração produz o efeito descrito na tabela do README da pasta (por exemplo, idade +7 leva o PSI acima de 0,2).

📝 **Anote para a discussão:** qual dos dois, PSI ou KS, você usaria para disparar um alerta que acorda alguém de madrugada? Para 500 clientes novos por dia, janela de um dia ou de uma semana?

---

## Lab 03.3 — Reagindo ao drift (≈ 13 min)

**Neste lab você vai** transformar a medição em ação: 12 semanas de monitoramento com uma política de alertas e um gatilho de re-treino, mais o relatório visual do Evidently.

**Antes de começar:** nada.

**Passo a passo**
- [ ] Rode o monitoramento:
  ```bash
  cd Labs-streamlit/Aula03_Monitoramento_Drift/Parte3_Reagindo_ao_Drift
  python monitorar.py
  ```
- [ ] Leia a tabela das 12 semanas e responda às perguntas do README da pasta.
- [ ] Teste a política, uma alteração por vez: `SEMANAS_SEGUIDAS_PARA_RETREINO = 1` e `LIMIAR_ALERTA = 0.1`. Volte ao padrão entre os testes.
- [ ] Abra o relatório do Evidently:
  ```bash
  python -m http.server 8000
  ```
  Abra a porta 8000, clique em `relatorio_drift.html` e pare o servidor com Ctrl+C.

✅ **Deu certo se:**
- com a política padrão, a saída termina com `Total de re-treinos em 12 semanas: 1`;
- as duas alterações mudam o número de re-treinos;
- o relatório do Evidently aponta drift na coluna `idade`.

📝 **Anote para a discussão:** como equilibrar sensibilidade e ruído nos alertas? Re-treinar automaticamente é sempre seguro?

---

## Lab GitHub 03 — Monitoramento agendado (≈ 13 min)

**Neste lab você vai** colocar o monitoramento num **job agendado** do GitHub Actions, que guarda o relatório do Evidently e **abre uma issue** quando detecta drift.

**Antes de começar:** nada.

**Passo a passo**
- [ ] Rode o job localmente, sem e com drift:
  ```bash
  cd Labs-streamlit/Aula03_Monitoramento_Drift/Lab_GitHub_Monitoramento_Agendado
  python monitorar_semana.py
  DESLOCAMENTO_IDADE=8 python monitorar_semana.py
  ```
- [ ] Agende no GitHub:
  ```bash
  cd "$(git rev-parse --show-toplevel)"
  mkdir -p .github/workflows
  cp Labs-streamlit/Aula03_Monitoramento_Drift/Lab_GitHub_Monitoramento_Agendado/monitoramento.yml .github/workflows/
  git add .github/workflows/monitoramento.yml
  git commit -m "Monitoramento de drift agendado"
  git push
  ```
- [ ] Na aba **Actions → Monitoramento de drift → Run workflow**, rode com o deslocamento `0`. Abra o run, o **Summary** e o artefato `relatorio-drift`.
- [ ] Rode de novo com o deslocamento `8` e abra a aba **Issues**.

✅ **Deu certo se:**
- localmente, a primeira execução termina com `sem drift relevante`, e a segunda, com `drift detectado`;
- com `0`, o run fica verde (cerca de 1 minuto) e **nenhuma** issue é aberta;
- com `8`, aparece a issue **"Drift detectado — semana NN"** com a tabela de PSI.

⚠️ **Se der errado:** o botão **Run workflow** só aparece depois que o `.yml` está no branch `main`. Se a issue não aparecer, confira se a aba **Issues** está ativa em **Settings → General → Features**.

📝 **Anote para a discussão:** se o job roda toda segunda e o drift acontece na terça, quando você fica sabendo? Como evitar que uma issue por semana vire ruído?

---

# Aula 04 — Versionamento com MLflow e DVC

> A Parte 1 desta aula é conceitual e não tem lab.

## Lab 04.2 — MLflow na prática (≈ 14 min)

**Neste lab você vai** registrar e comparar experimentos no MLflow e promover um modelo no Model Registry com **aliases**, incluindo um rollback.

**Antes de começar:** nada.

**Passo a passo**
- [ ] Gere os dados e registre dois experimentos:
  ```bash
  cd Labs-streamlit/Aula04_Versionamento_MLflow_DVC/Parte2_MLflow_na_Pratica
  python gerar_dados.py
  python treinar.py --n-estimators 50 --max-depth 3 --registrar
  python treinar.py --n-estimators 200 --max-depth 8 --registrar
  ```
- [ ] Num **segundo terminal**, suba a interface e abra a porta 5000:
  ```bash
  cd Labs-streamlit/Aula04_Versionamento_MLflow_DVC/Parte2_MLflow_na_Pratica
  ./ui_mlflow.sh
  ```
  Compare os dois runs do experimento `previsao-churn` e veja a aba **Models**.
- [ ] De volta ao primeiro terminal, promova, valide e faça o rollback:
  ```bash
  python promover.py --versao 1 --alias champion
  python prever.py
  python promover.py --versao 2 --alias challenger
  python prever.py --alias challenger
  python prever.py
  python promover.py --versao 2 --alias champion
  python prever.py
  python promover.py --versao 1 --alias champion
  python prever.py
  ```
- [ ] Ctrl+C no segundo terminal para parar a interface.

✅ **Deu certo se:**
- os dois treinos terminam com `registrado=True` (F1 de cerca de 0,37 e 0,50);
- o `prever.py` mostra a probabilidade da versão que está no `@champion` naquele momento (cerca de 70% com a versão 1 e 92% com a versão 2), e volta ao valor da versão 1 depois do rollback.

⚠️ **Se der errado:** a interface responde 403: suba com o `./ui_mlflow.sh`, e não com `mlflow ui`.

📝 **Anote para a discussão:** que informações do MLflow você usaria para reproduzir um modelo de 3 meses atrás, e o que ainda falta? Quem deveria poder mover o alias `@champion`?

---

## Lab 04.3 — DVC para dados e pipelines (≈ 15 min)

**Neste lab você vai** versionar o dataset com DVC, treinar com um pipeline reprodutível e **voltar no tempo** para os dados e o modelo de uma versão anterior.

**Antes de começar:** nada. Se você já rodou este lab antes e o `dvc init` disser que o DVC já existe, pule o `dvc init` e o `dvc remote add`.

**Passo a passo**
- [ ] Inicialize o DVC e configure um remote:
  ```bash
  cd Labs-streamlit/Aula04_Versionamento_MLflow_DVC/Parte3_DVC_para_Dados_e_Pipelines
  python gerar_dados.py --versao 1
  dvc init --subdir
  dvc remote add -d local ~/dvc-remote
  git add .dvc .dvcignore && git commit -m "Inicializa DVC"
  ```
- [ ] Versione os dados e treine:
  ```bash
  dvc add dados/clientes.csv
  cat dados/clientes.csv.dvc
  dvc repro
  dvc repro
  dvc metrics show
  git add dados/clientes.csv.dvc dvc.lock metricas.json .gitignore
  git commit -m "Dados v1 + modelo v1"
  dvc push
  ```
- [ ] Os dados mudaram:
  ```bash
  python gerar_dados.py --versao 2
  dvc status
  dvc add dados/clientes.csv
  dvc repro
  dvc metrics diff
  git add dados/clientes.csv.dvc dvc.lock metricas.json
  git commit -m "Dados v2 + modelo v2"
  dvc push
  ```
- [ ] Volte no tempo e depois retorne à v2:
  ```bash
  git checkout HEAD~1 -- dados/clientes.csv.dvc dvc.lock metricas.json
  dvc checkout
  wc -l dados/clientes.csv
  dvc metrics show
  git checkout HEAD -- dados/clientes.csv.dvc dvc.lock metricas.json
  dvc checkout
  ```
- [ ] Extra: apague os arquivos e recupere do remote:
  ```bash
  rm dados/clientes.csv modelo.joblib
  dvc pull
  ```

✅ **Deu certo se:**
- o segundo `dvc repro` responde `Data and pipelines are up to date` (nada mudou, nada foi re-treinado);
- com a v2, o modelo é treinado com 4.000 linhas e o `dvc metrics diff` mostra o F1 subindo (de cerca de 0,50 para 0,61);
- na volta no tempo, o `wc -l` mostra **2001** linhas: os dados da v1 voltaram;
- o `dvc pull` traz de volta `dados/clientes.csv` e `modelo.joblib`.

📝 **Anote para a discussão:** o que cada um dos três comandos, `git checkout`, `dvc pull` e `dvc repro`, recupera? Que informação a tag `versao_dados_md5` ligaria entre o MLflow e o DVC?

---

## Lab GitHub 04 — DVC no CI, com métricas no pull request (≈ 15 min)

**Neste lab você vai** fazer o GitHub Actions reproduzir o pipeline DVC a cada pull request e **comentar no PR** quanto as métricas mudaram em relação ao `main`.

**Antes de começar:** nada.

**Passo a passo**
- [ ] Rode o pipeline e ligue o CI:
  ```bash
  cd Labs-streamlit/Aula04_Versionamento_MLflow_DVC/Lab_GitHub_DVC_no_CI
  dvc init --subdir
  dvc repro
  dvc metrics show
  cd "$(git rev-parse --show-toplevel)"
  mkdir -p .github/workflows
  cp Labs-streamlit/Aula04_Versionamento_MLflow_DVC/Lab_GitHub_DVC_no_CI/dvc-ci.yml .github/workflows/
  git add .github/workflows/dvc-ci.yml Labs-streamlit/Aula04_Versionamento_MLflow_DVC/Lab_GitHub_DVC_no_CI
  git commit -m "Pipeline DVC + CI"
  git push
  ```
- [ ] Crie um experimento num branch: no `params.yaml`, troque `max_depth: 8` por `max_depth: 3`.
  ```bash
  cd Labs-streamlit/Aula04_Versionamento_MLflow_DVC/Lab_GitHub_DVC_no_CI
  git checkout -b experimento-profundidade
  dvc repro
  dvc params diff main
  dvc metrics diff main
  ```
- [ ] Abra o pull request:
  ```bash
  git add params.yaml dvc.lock metricas.json
  git commit -m "Experimento: max_depth 3"
  git push -u origin experimento-profundidade
  gh pr create --fill
  ```
- [ ] No GitHub, abra o PR e espere cerca de 1 minuto.
- [ ] Extra: no mesmo branch, mude `versao_dados: 1` para `versao_dados: 2`, rode `dvc repro`, faça commit e push.

✅ **Deu certo se:**
- o `dvc metrics diff main` mostra o F1 caindo (de cerca de 0,51 para 0,37);
- o workflow **Pipeline DVC** roda no PR, e o `github-actions` publica um **comentário** com as tabelas de parâmetros e de métricas.

⚠️ **Se der errado:** se o `gh pr create` não funcionar, clique no link "Create a pull request" que o `git push` mostrou. Se o PR ficar sem comentário, faça mais um commit no branch: o `dvc-ci.yml` precisa estar no `main` antes de o PR ser aberto.

📝 **Anote para a discussão:** onde ficariam as credenciais do storage se o CI precisasse de `dvc pull`? Que regra de merge você colocaria no PR?

---

## Registro de progresso

Marque cada lab quando ver o "✅ Deu certo se…" na sua tela.

| Aula | Parte 1 | Parte 2 | Parte 3 | Lab GitHub |
|---|---|---|---|---|
| 01 — Pipeline e Streamlit | [ ] Estruturando o pipeline | [ ] Interface com Streamlit | [ ] Publicando na web | [ ] Testes do app |
| 02 — Docker | [ ] Entendendo containers | [ ] Escrevendo um Dockerfile | [ ] Boas práticas e Compose | [ ] Imagem no GHCR |
| 03 — Drift | [ ] Entendendo a degradação | [ ] Detectando drift | [ ] Reagindo ao drift | [ ] Monitoramento agendado |
| 04 — MLflow e DVC | *conceitual* | [ ] MLflow na prática | [ ] DVC para dados | [ ] DVC no CI |

---

## Problemas comuns (em qualquer lab)

| Sintoma | O que fazer |
|---|---|
| `command not found` (`streamlit`, `dvc`, `pytest`) logo depois de criar o codespace | O ambiente ainda estava instalando quando o terminal abriu. Espere terminar e **abra um terminal novo** |
| O codespace abriu com aviso de *recovery mode* | *Command Palette* (Ctrl/Cmd+Shift+P) → **Codespaces: Rebuild Container**. Se continuar, apague o codespace e crie outro |
| A porta não abre no navegador | Aba **Ports** → ícone de globo da porta |
| `Port 8501 is already in use` | Outro app ainda está rodando. Ctrl+C no terminal dele, ou `pkill -f "streamlit run"` |
| `Cannot connect to the Docker daemon` | O Docker do codespace ainda está iniciando. Espere 30 segundos |
| Workflow não aparece ou não dispara | Confira se o `.yml` está em `.github/workflows/` **na raiz** e se o `git push` foi feito. Os workflows só disparam quando o commit muda a pasta do lab ou o próprio `.yml` |

Ao terminar cada aula: **pare o codespace** em github.com/codespaces → ⋯ → **Stop**.

---

## E depois dos labs: o Desafio Final Integrado

O desafio (`Docs-Aulas-streamlit/desafio/`) junta as quatro aulas num cenário único: desenvolver e publicar uma aplicação Streamlit conteinerizada, com monitoramento e versionamento. Os labs são a sua base para ele: tudo o que o desafio pede, você já fez na prática aqui. Releia as suas anotações de "Anote para a discussão" antes de começar.
