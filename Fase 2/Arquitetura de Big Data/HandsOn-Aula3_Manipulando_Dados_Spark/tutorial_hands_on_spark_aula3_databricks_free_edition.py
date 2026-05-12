# Databricks notebook source
# MAGIC %md
# MAGIC # Aula 3 — Tutorial prático de manipulação de dados com PySpark no Databricks Free Edition
# MAGIC 
# MAGIC Este tutorial adapta o notebook da Aula 3 para estudantes que vão executar o exercício no **Databricks Free Edition**.
# MAGIC 
# MAGIC A ideia é começar do zero: abrir o Databricks, entender a tela inicial, criar ou importar o notebook, iniciar a sessão Serverless e então executar as células de PySpark em ordem.
# MAGIC 
# MAGIC ## Referências oficiais usadas nesta versão
# MAGIC - Cadastro no Free Edition: https://docs.databricks.com/aws/en/getting-started/free-edition
# MAGIC - Interface do workspace: https://docs.databricks.com/gcp/en/workspace/navigate-workspace
# MAGIC - Criação e gerenciamento de notebooks: https://docs.databricks.com/aws/en/notebooks/notebooks-manage
# MAGIC - Importação de notebooks: https://docs.databricks.com/gcp/en/notebooks/notebook-export-import
# MAGIC - Compute em notebooks: https://docs.databricks.com/aws/en/notebooks/notebook-compute

# COMMAND ----------
# MAGIC %md
# MAGIC # Parte 0 — Primeiro acesso ao Databricks Free Edition
# MAGIC **Tempo sugerido:** 10 a 15 minutos
# MAGIC 
# MAGIC ## Objetivo
# MAGIC Entrar no Databricks Free Edition, reconhecer os principais componentes da interface e deixar o notebook pronto para executar PySpark.
# MAGIC 
# MAGIC ## O que é o Databricks Free Edition
# MAGIC O Databricks Free Edition é uma versão gratuita da plataforma, voltada para aprendizado, protótipos e experimentos. Ele cria um workspace Databricks para você trabalhar com notebooks, SQL, dados, dashboards e recursos de IA.
# MAGIC 
# MAGIC Na Free Edition, o ambiente é **serverless** e possui **cotas de uso**. Isso significa que você não precisa criar um cluster manualmente para este exercício: o Databricks provisiona a capacidade de execução quando você roda o notebook.
# MAGIC 
# MAGIC ## Link de acesso
# MAGIC 1. Abra o link: https://login.databricks.com/?dbx_source=docs&intent=CE_SIGN_UP
# MAGIC 2. Escolha uma forma de cadastro ou login.
# MAGIC 3. Aguarde a criação automática do workspace.
# MAGIC 4. Quando o workspace abrir, você estará na página inicial do Databricks.
# MAGIC 
# MAGIC Se o link pedir login novamente, use a mesma conta escolhida no cadastro. Em ambientes de aula, use preferencialmente o e-mail indicado pelo professor ou pela instituição.

# COMMAND ----------
# MAGIC %md
# MAGIC # Conhecendo a tela inicial e o menu esquerdo
# MAGIC 
# MAGIC A tela inicial do Databricks Free Edition é organizada em três áreas principais: a barra superior, a área central e o menu esquerdo.
# MAGIC 
# MAGIC ## Barra superior
# MAGIC É a faixa no topo da página. Na interface atual, ela mostra o logo do Databricks, a busca global, o workspace selecionado e atalhos do lado direito.
# MAGIC 
# MAGIC ![Diagrama da barra superior do Databricks](imagens/databricks_barra_superior.png)
# MAGIC 
# MAGIC Use a busca global para localizar dados, notebooks, objetos recentes, tabelas, queries e outros recursos do workspace. O seletor **workspace** aparece no lado direito e indica o ambiente aberto.
# MAGIC 
# MAGIC ## Área central
# MAGIC É onde o conteúdo principal aparece. Na tela inicial do Free Edition, você verá a mensagem **Welcome to Databricks**, cards de progresso, cursos, demos interativas e a seção **Your resources**.
# MAGIC 
# MAGIC ![Diagrama da área central do Databricks](imagens/databricks_area_central.png)
# MAGIC 
# MAGIC Para esta aula, a área central será mais importante depois que você abrir o notebook, porque ela vira o editor das células de código e Markdown.
# MAGIC 
# MAGIC ## Menu esquerdo
# MAGIC O menu esquerdo é a navegação principal. Na interface atual do Free Edition, ele começa com **New**, **Home**, **Learn**, **Workspace**, **Recents**, **Catalog**, **Jobs & Pipelines**, **Compute**, **Discover** e **Marketplace**. Depois aparecem grupos como **SQL**, **Data Engineering** e **AI/ML**.
# MAGIC 
# MAGIC ![Diagrama do menu esquerdo do Databricks](imagens/databricks_menu_esquerdo.png)
# MAGIC 
# MAGIC Principais itens:
# MAGIC 
# MAGIC - **New**: cria novos objetos, como Notebook, Query, Dashboard, Job, Pipeline e recursos de ingestão.
# MAGIC - **Home**: volta para a página inicial, onde aparecem cursos, demos e recursos recentes.
# MAGIC - **Learn**: abre trilhas de aprendizagem e cursos do Databricks Free Edition.
# MAGIC - **Workspace**: mostra seus arquivos, pastas e notebooks. É o lugar mais usado para organizar e abrir notebooks da aula.
# MAGIC - **Recents**: lista objetos abertos recentemente, como notebooks, queries, dashboards e tabelas.
# MAGIC - **Catalog**: permite navegar por catálogos, schemas, tabelas, views e volumes.
# MAGIC - **Jobs & Pipelines**: mostra execuções agendadas, jobs e pipelines. Para este exercício, não precisamos criar job.
# MAGIC - **Compute**: lista recursos de computação. Na Free Edition, o uso principal será Serverless, então você normalmente não precisa criar cluster.
# MAGIC - **Discover / Marketplace**: áreas para explorar recursos, soluções, demos e conteúdos disponíveis.
# MAGIC - **SQL Editor**: ambiente para escrever consultas SQL.
# MAGIC - **Queries**: lista consultas SQL salvas.
# MAGIC - **Dashboards**: área para criar e visualizar dashboards.
# MAGIC - **Genie spaces**: recurso de análise assistida por linguagem natural, quando disponível.
# MAGIC - **Alerts**: alertas baseados em consultas e métricas.
# MAGIC - **Query History**: histórico das consultas SQL executadas.
# MAGIC - **SQL Warehouses**: recursos de computação usados para SQL.
# MAGIC - **Runs**: histórico e acompanhamento de execuções.
# MAGIC - **Data Ingestion**: assistentes para ingestão/carregamento de dados.
# MAGIC - **Playground, AI Gateway, Experiments, Features, Models e Serving**: recursos de IA, machine learning, experimentação e publicação de modelos.
# MAGIC 
# MAGIC Para esta aula, concentre-se principalmente em **New**, **Workspace**, **Catalog**, **Compute** e no editor do notebook.
# MAGIC 
# MAGIC > Observação para importação do arquivo `.py` no Databricks: envie também a pasta `imagens` junto com o material da aula para que os PNGs apareçam no notebook.

# COMMAND ----------
# MAGIC %md
# MAGIC # Criando ou importando o notebook da aula
# MAGIC 
# MAGIC Você pode seguir por dois caminhos.
# MAGIC 
# MAGIC ## Caminho A — Criar um notebook novo
# MAGIC 1. No menu esquerdo, clique em **+ New**.
# MAGIC 2. Escolha **Notebook**.
# MAGIC 3. Dê um nome, por exemplo: `Aula 3 - Manipulacao de Dados com PySpark`.
# MAGIC 4. Confirme que a linguagem está como **Python**.
# MAGIC 5. Cole as células deste tutorial no notebook ou importe este arquivo `.ipynb` pelo caminho B.
# MAGIC 
# MAGIC ## Caminho B — Importar este arquivo `.ipynb`
# MAGIC 1. No menu esquerdo, clique em **Workspace**.
# MAGIC 2. Entre na sua pasta de usuário ou em uma pasta indicada pelo professor.
# MAGIC 3. Clique no menu de três pontos, ou clique com o botão direito em uma pasta.
# MAGIC 4. Escolha **Import**.
# MAGIC 5. Selecione o arquivo `tutorial_hands_on_spark_aula3_databricks_free_edition.ipynb`.
# MAGIC 6. Clique em **Import**.
# MAGIC 7. Abra o notebook importado.
# MAGIC 
# MAGIC O Databricks aceita notebooks no formato `.ipynb`, então este arquivo pode ser importado diretamente.

# COMMAND ----------
# MAGIC %md
# MAGIC # Criando a sessão de execução Serverless
# MAGIC 
# MAGIC Para executar PySpark, o notebook precisa estar conectado a uma sessão de compute.
# MAGIC 
# MAGIC Na Free Edition, use **Serverless**:
# MAGIC 
# MAGIC 1. Abra o notebook.
# MAGIC 2. No topo do notebook, procure o seletor de compute. Ele pode aparecer como **Connect**, **Compute** ou com o nome do recurso conectado.
# MAGIC 3. Selecione **Serverless**, caso ainda não esteja selecionado.
# MAGIC 4. Execute a primeira célula de código.
# MAGIC 5. Aguarde a sessão iniciar. A primeira execução pode demorar um pouco mais.
# MAGIC 
# MAGIC Em workspaces com Unity Catalog e Serverless habilitado, notebooks novos normalmente conectam automaticamente ao Serverless quando você executa uma célula sem selecionar outro compute.
# MAGIC 
# MAGIC ## Como executar células
# MAGIC - Para executar uma célula, clique no botão de executar da célula ou use o atalho exibido pela própria interface.
# MAGIC - Execute as células em ordem, de cima para baixo.
# MAGIC - Depois de executar uma célula com `display(df)`, observe a tabela renderizada abaixo da célula.
# MAGIC - Se a sessão ficar parada por muito tempo, ela pode desconectar. Nesse caso, reconecte ao Serverless e execute novamente as células necessárias.

# COMMAND ----------
# MAGIC %md
# MAGIC # Como acompanhar os resultados durante a aula
# MAGIC 
# MAGIC Durante o tutorial, observe quatro coisas em cada etapa:
# MAGIC 
# MAGIC 1. **Nome do DataFrame criado**: por exemplo, `df_vendas`, `df_base`, `df_limpo` e `df_enriquecido`.
# MAGIC 2. **Transformação aplicada**: seleção, filtro, limpeza, join, agregação, janela ou persistência.
# MAGIC 3. **Resultado exibido com `display()`**: confira linhas, colunas e valores calculados.
# MAGIC 4. **Mensagens impressas com `print()` ou `explain()`**: ajudam a entender contagem, partições e plano de execução.
# MAGIC 
# MAGIC A partir da próxima célula, começa o conteúdo prático original da Aula 3.

# COMMAND ----------
# MAGIC %md
# MAGIC # Aula 3 — Tutorial prático de manipulação de dados com PySpark
# MAGIC 
# MAGIC Este notebook usa uma linguagem de tutorial e foi organizado em **4 partes de 15 a 20 minutos**.
# MAGIC 
# MAGIC ## O que é PySpark
# MAGIC PySpark é a API do Apache Spark para Python.  
# MAGIC Ele permite ler, transformar, agregar e gravar dados distribuídos usando **DataFrames**.
# MAGIC 
# MAGIC Um DataFrame no Spark é uma estrutura tabular distribuída, com colunas nomeadas e execução paralela no cluster.
# MAGIC 
# MAGIC ## Como usar este tutorial
# MAGIC 1. Leia o objetivo da parte.
# MAGIC 2. Execute as células na ordem.
# MAGIC 3. Compare o resultado antes e depois de cada transformação.
# MAGIC 4. Observe o plano de execução e o número de partições no final.
# MAGIC 
# MAGIC ## Organização do notebook
# MAGIC - **Formatos de arquivos em Data Lake — CSV, JSON, Avro, Parquet, ORC e Delta**
# MAGIC - **Lakehouse — Arquitetura Medallion com camadas Bronze, Silver e Gold**
# MAGIC - **Parte 1 — Leitura, inspeção e seleção de dados**
# MAGIC - **Parte 2 — Transformação, limpeza e padronização**
# MAGIC - **Parte 3 — Combinação, agregação e análise com janelas**
# MAGIC - **Parte 4 — Estatística rápida, performance e persistência**
# MAGIC 

# COMMAND ----------
# MAGIC %md
# MAGIC # Lakehouse de exemplo com arquitetura Medallion
# MAGIC 
# MAGIC Neste tutorial, além das transformações com PySpark, vamos montar um **Lakehouse de exemplo** usando a arquitetura **Medallion**.
# MAGIC 
# MAGIC A arquitetura Medallion organiza os dados em camadas progressivas de qualidade:
# MAGIC 
# MAGIC - **Bronze**: camada de entrada, com dados brutos ou quase brutos, preservando rastreabilidade.
# MAGIC - **Silver**: camada tratada, com tipos corrigidos, dados limpos, duplicidades removidas e regras técnicas aplicadas.
# MAGIC - **Gold**: camada de negócio, com tabelas agregadas e prontas para análise, dashboards, SQL e consumo por outras aplicações.
# MAGIC 
# MAGIC ![Desenho da arquitetura Medallion no Lakehouse](imagens/arquitetura_medallion_lakehouse.png)
# MAGIC 
# MAGIC No Databricks, cada camada será criada como um **schema** do Lakehouse:
# MAGIC 
# MAGIC - `bronze`
# MAGIC - `silver`
# MAGIC - `gold`
# MAGIC 
# MAGIC E as tabelas serão gravadas em formato Delta gerenciado usando `saveAsTable()`.
# MAGIC 
# MAGIC > Observação para importação do arquivo `.py` no Databricks: envie também a pasta `imagens` junto com o material da aula para que o desenho da arquitetura apareça no notebook.

# COMMAND ----------
# MAGIC %md
# MAGIC # Estrutura das tabelas no Databricks
# MAGIC 
# MAGIC Quando o notebook for executado, as tabelas serão organizadas no **Catalog** do Databricks em três schemas, seguindo a arquitetura Medallion.
# MAGIC 
# MAGIC ![Diagrama da estrutura das tabelas no Databricks](imagens/estrutura_tabelas_databricks.png)
# MAGIC 
# MAGIC No menu esquerdo do Databricks, você pode conferir essa estrutura em **Catalog**. A navegação esperada será parecida com:
# MAGIC 
# MAGIC ```text
# MAGIC catalogo_atual
# MAGIC ├── bronze
# MAGIC │   ├── aula3_dynamodb_vendas_raw
# MAGIC │   ├── aula3_dms_clientes_raw
# MAGIC │   ├── aula3_vendas_raw
# MAGIC │   └── aula3_clientes_raw
# MAGIC ├── silver
# MAGIC │   ├── aula3_vendas_tratadas
# MAGIC │   └── aula3_clientes_tratados
# MAGIC └── gold
# MAGIC     ├── aula3_analitico_categoria
# MAGIC     └── aula3_analitico_estado_segmento
# MAGIC ```
# MAGIC 
# MAGIC A camada Bronze guarda dados brutos e rastreáveis, a Silver guarda dados tratados e a Gold guarda tabelas analíticas prontas para consumo.
# MAGIC 
# MAGIC > Observação para importação do arquivo `.py` no Databricks: envie também a pasta `imagens` junto com o material da aula para que o diagrama de tabelas apareça no notebook.

# COMMAND ----------
# MAGIC %md
# MAGIC # Tipos de arquivos em Data Lake e Lakehouse
# MAGIC 
# MAGIC Em projetos de dados, o formato do arquivo influencia custo, performance, facilidade de leitura e governança. Antes de gravar Bronze, Silver e Gold, vale entender os formatos mais comuns.
# MAGIC 
# MAGIC ## Formatos linha a linha
# MAGIC 
# MAGIC ### CSV
# MAGIC CSV é um formato texto, simples e muito usado para troca de dados.
# MAGIC 
# MAGIC Pontos positivos:
# MAGIC 
# MAGIC - fácil de abrir em planilhas e editores de texto;
# MAGIC - bom para integração simples com sistemas legados;
# MAGIC - bastante conhecido.
# MAGIC 
# MAGIC Pontos de atenção:
# MAGIC 
# MAGIC - não guarda schema de forma rica;
# MAGIC - geralmente ocupa mais espaço;
# MAGIC - leitura pode ser mais lenta em grandes volumes;
# MAGIC - tipos como data, número e booleano precisam ser inferidos ou definidos.
# MAGIC 
# MAGIC Uso comum: chegada de arquivos simples na camada Bronze.
# MAGIC 
# MAGIC ### JSON
# MAGIC JSON é um formato texto muito usado por APIs, eventos, logs e bancos NoSQL.
# MAGIC 
# MAGIC Pontos positivos:
# MAGIC 
# MAGIC - suporta objetos aninhados e arrays;
# MAGIC - combina bem com eventos semiestruturados, como DynamoDB Streams;
# MAGIC - é fácil de inspecionar manualmente.
# MAGIC 
# MAGIC Pontos de atenção:
# MAGIC 
# MAGIC - pode ocupar bastante espaço;
# MAGIC - parsing é mais custoso que formatos colunares;
# MAGIC - campos muito aninhados exigem tratamento com `select`, `explode`, `from_json` e acesso a structs.
# MAGIC 
# MAGIC Uso comum: eventos, logs, APIs, CDC semiestruturado e camada Bronze.
# MAGIC 
# MAGIC ### Avro
# MAGIC Avro é um formato binário orientado a linhas, com schema embutido.
# MAGIC 
# MAGIC Pontos positivos:
# MAGIC 
# MAGIC - bom para streaming e troca entre sistemas;
# MAGIC - suporta evolução de schema;
# MAGIC - comum em pipelines com Kafka e CDC.
# MAGIC 
# MAGIC Pontos de atenção:
# MAGIC 
# MAGIC - não é tão eficiente quanto Parquet para consultas analíticas colunares;
# MAGIC - nem sempre é o formato final ideal para Silver e Gold.
# MAGIC 
# MAGIC Uso comum: ingestão, streaming, CDC e Bronze.
# MAGIC 
# MAGIC ## Formatos colunares
# MAGIC 
# MAGIC ### Parquet
# MAGIC Parquet é um formato colunar muito usado em Data Lakes.
# MAGIC 
# MAGIC Pontos positivos:
# MAGIC 
# MAGIC - excelente para consultas analíticas;
# MAGIC - lê apenas as colunas necessárias;
# MAGIC - comprime bem;
# MAGIC - guarda schema;
# MAGIC - funciona muito bem com Spark.
# MAGIC 
# MAGIC Pontos de atenção:
# MAGIC 
# MAGIC - não traz sozinho controle transacional ACID;
# MAGIC - updates, deletes e merges exigem mecanismos adicionais ou regravações.
# MAGIC 
# MAGIC Uso comum: Silver e Gold quando não há necessidade de transação Delta.
# MAGIC 
# MAGIC ### ORC
# MAGIC ORC também é um formato colunar. Ele é comum no ecossistema Hive.
# MAGIC 
# MAGIC Pontos positivos:
# MAGIC 
# MAGIC - boa compressão;
# MAGIC - eficiente para consultas analíticas;
# MAGIC - guarda estatísticas úteis para otimização.
# MAGIC 
# MAGIC Pontos de atenção:
# MAGIC 
# MAGIC - em Databricks e Spark moderno, Parquet e Delta costumam aparecer com mais frequência;
# MAGIC - a escolha geralmente depende do padrão da empresa.
# MAGIC 
# MAGIC Observação: quando alguém escreve “PRC”, normalmente está se referindo a **ORC** ou a **Parquet**. No Spark, os formatos comuns são `parquet` e `orc`.
# MAGIC 
# MAGIC ## Formato de tabela Lakehouse
# MAGIC 
# MAGIC ### Delta Lake
# MAGIC Delta Lake não é apenas um arquivo. Ele é uma camada de tabela sobre arquivos Parquet, com um log transacional chamado `_delta_log`.
# MAGIC 
# MAGIC Pontos positivos:
# MAGIC 
# MAGIC - transações ACID;
# MAGIC - suporte a `UPDATE`, `DELETE` e `MERGE`;
# MAGIC - versionamento e histórico;
# MAGIC - leitura eficiente com Parquet por baixo;
# MAGIC - ótimo encaixe com Lakehouse e arquitetura Medallion.
# MAGIC 
# MAGIC Pontos de atenção:
# MAGIC 
# MAGIC - é mais do que um arquivo único: é uma pasta de tabela com arquivos Parquet e log Delta;
# MAGIC - deve ser acessado como tabela Delta, não como um Parquet qualquer.
# MAGIC 
# MAGIC Uso comum: Bronze, Silver e Gold no Databricks.
# MAGIC 
# MAGIC ## Como escolher no tutorial
# MAGIC 
# MAGIC Neste notebook, vamos usar:
# MAGIC 
# MAGIC - **JSON** para simular origens transacionais e semiestruturadas;
# MAGIC - **Delta** para gravar as tabelas do Lakehouse nas camadas Bronze, Silver e Gold;
# MAGIC - exemplos didáticos de **CSV**, **Parquet**, **ORC** e **Delta** para comparar leitura e escrita.
# MAGIC 
# MAGIC Regra prática para explicar em aula:
# MAGIC 
# MAGIC - se o dado chegou bruto e semiestruturado, JSON pode aparecer na Bronze;
# MAGIC - se a consulta é analítica e colunar, Parquet é eficiente;
# MAGIC - se precisa de tabela confiável, histórico e operações como merge, use Delta;
# MAGIC - se a empresa usa Hive/ORC como padrão, ORC pode aparecer em integrações específicas.

# COMMAND ----------
# MAGIC %md
# MAGIC # Parte 1 — Leitura, inspeção e seleção de dados
# MAGIC **Tempo sugerido:** 15 a 20 minutos
# MAGIC 
# MAGIC ## Objetivo
# MAGIC Criar os DataFrames do exercício, inspecionar o schema e aplicar os primeiros comandos de seleção e filtro.
# MAGIC 
# MAGIC ## Funções usadas nesta parte
# MAGIC 
# MAGIC ### `spark.createDataFrame()`
# MAGIC Cria um DataFrame a partir de dados em memória.  
# MAGIC É útil para exemplos didáticos e para montar bases pequenas sem depender de download.
# MAGIC 
# MAGIC ### `display()`
# MAGIC Exibe o DataFrame na interface do Databricks.
# MAGIC 
# MAGIC ### `printSchema()`
# MAGIC Mostra o nome das colunas e os tipos de dados.
# MAGIC 
# MAGIC ### `show()`
# MAGIC Mostra uma amostra textual do DataFrame.
# MAGIC 
# MAGIC ### `count()`
# MAGIC Conta quantas linhas existem no DataFrame.
# MAGIC 
# MAGIC ### `select()`
# MAGIC Seleciona colunas específicas.
# MAGIC 
# MAGIC ### `selectExpr()`
# MAGIC Seleciona colunas usando expressões no estilo SQL.  
# MAGIC Use quando quiser escrever expressões como `quantidade * preco_unitario AS valor_total`.
# MAGIC 
# MAGIC ### `filter()` e `where()`
# MAGIC Aplicam filtros. Os dois métodos são equivalentes em muitos cenários.
# MAGIC 
# MAGIC ### `col()`
# MAGIC Referencia uma coluna pelo nome.  
# MAGIC É muito usada junto com funções do módulo `pyspark.sql.functions`.
# MAGIC 

# COMMAND ----------
# MAGIC %md
# MAGIC # Origem dos dados — DynamoDB, CDC/DMS e arquivos
# MAGIC 
# MAGIC Antes de criar as camadas Medallion, vamos simular três formas comuns de chegada de dados em um Lakehouse:
# MAGIC 
# MAGIC ## 1. Sistema transacional estilo DynamoDB
# MAGIC O DynamoDB é um banco NoSQL usado em aplicações transacionais. Os dados costumam chegar ao Lakehouse por eventos, por exportações ou por streams.
# MAGIC 
# MAGIC Neste tutorial, vamos simular eventos no formato parecido com **DynamoDB Streams**, com campos aninhados como `NewImage`, atributos tipados (`S`, `N`, `NULL`) e uma lista de itens da venda.
# MAGIC 
# MAGIC Para transformar esse JSON em tabela, vamos usar:
# MAGIC 
# MAGIC - `spark.createDataFrame()` para criar uma coluna com o JSON bruto sem usar `sparkContext`;
# MAGIC - `from_json()` para interpretar o texto JSON usando um schema;
# MAGIC - `explode()` para abrir a lista de itens da venda;
# MAGIC - acesso a campos aninhados como `dynamodb.NewImage.id_venda.N`;
# MAGIC - `cast()` para converter texto em número.
# MAGIC 
# MAGIC ## Observação importante sobre atributos tipados do DynamoDB
# MAGIC 
# MAGIC Nos eventos do DynamoDB, os valores costumam vir acompanhados do tipo do atributo. Por isso aparecem marcações como `S`, `N` e `NULL`.
# MAGIC 
# MAGIC Exemplo simplificado:
# MAGIC 
# MAGIC ```json
# MAGIC {
# MAGIC   "id_venda": { "N": "1" },
# MAGIC   "produto": { "S": "Notebook" },
# MAGIC   "cupom": { "NULL": true }
# MAGIC }
# MAGIC ```
# MAGIC 
# MAGIC Significado:
# MAGIC 
# MAGIC - `S` significa **String**, ou seja, texto. Exemplo: `{ "S": "Notebook" }`.
# MAGIC - `N` significa **Number**, ou seja, número. No JSON do DynamoDB, o número vem como texto, por exemplo `{ "N": "1" }`, então no Spark usamos `cast()` para converter.
# MAGIC - `NULL` indica valor nulo, por exemplo `{ "NULL": true }`.
# MAGIC 
# MAGIC Por isso, para pegar o `id_venda`, usamos algo como:
# MAGIC 
# MAGIC ```python
# MAGIC F.col("dynamodb.NewImage.id_venda.N").cast("int")
# MAGIC ```
# MAGIC 
# MAGIC A leitura é: entrar em `id_venda`, pegar o valor dentro de `N` e converter para inteiro.
# MAGIC 
# MAGIC ## 2. CDC ou DMS
# MAGIC CDC significa **Change Data Capture**. Ele captura mudanças feitas em uma origem transacional, como inserts, updates e deletes.
# MAGIC 
# MAGIC O AWS DMS pode entregar esses eventos para arquivos, filas ou storage. Aqui vamos simular eventos CDC/DMS da tabela de clientes.
# MAGIC 
# MAGIC ## 3. Arquivos
# MAGIC Também vamos mostrar uma opção de chegada por arquivos JSON em uma área de aterrissagem. No mundo real, essa área poderia receber arquivos CSV, JSON, Parquet ou Avro vindos de integrações, sistemas externos ou pipelines de ingestão. Nesta versão para Databricks Serverless, a simulação de arquivos usa JSON Lines em memória para evitar o erro de Public DBFS root desabilitado.
# MAGIC 
# MAGIC Depois dessas origens, o restante do tutorial continua usando os DataFrames `df_vendas` e `df_clientes`.
# MAGIC 
# MAGIC > No Databricks Serverless, evitamos `spark.sparkContext.parallelize()` porque o acesso direto ao SparkContext/JVM não é suportado. Por isso, os exemplos usam `spark.createDataFrame()` e `from_json()`.

# COMMAND ----------
from pyspark.sql import functions as F
from pyspark.sql import types as T
from pyspark.sql import Window
import json

# -----------------------------------------------------------------------------
# 1) Origem transacional simulada: DynamoDB Streams
# -----------------------------------------------------------------------------
# Cada evento representa uma venda gravada em um sistema transacional.
# O campo itens.L é uma lista de objetos. Vamos usar explode() para abrir essa lista.

eventos_dynamodb_vendas = [
    {
        "eventID": "evt-001",
        "eventName": "INSERT",
        "eventSource": "aws:dynamodb",
        "dynamodb": {
            "Keys": {"pk": {"S": "VENDA#1"}},
            "NewImage": {
                "id_venda": {"N": "1"},
                "data_venda": {"S": "2026-01-02"},
                "estado": {"S": "SP"},
                "id_cliente": {"N": "101"},
                "cupom": {"NULL": True},
                "origem": {"S": "Loja-SP"},
                "status_bruto": {"S": "ok"},
                "itens": {"L": [{"M": {"produto": {"S": "Notebook"}, "categoria": {"S": "Eletronicos"}, "quantidade": {"N": "1"}, "preco_unitario": {"N": "3500.00"}}}]}
            }
        }
    },
    {
        "eventID": "evt-002",
        "eventName": "INSERT",
        "eventSource": "aws:dynamodb",
        "dynamodb": {"Keys": {"pk": {"S": "VENDA#2"}}, "NewImage": {"id_venda": {"N": "2"}, "data_venda": {"S": "2026-01-02"}, "estado": {"S": "SP"}, "id_cliente": {"N": "101"}, "cupom": {"S": "CUPOM10"}, "origem": {"S": "Loja-SP"}, "status_bruto": {"S": "ok"}, "itens": {"L": [{"M": {"produto": {"S": "Mouse"}, "categoria": {"S": "Eletronicos"}, "quantidade": {"N": "2"}, "preco_unitario": {"N": "80.00"}}}]}}}
    },
    {
        "eventID": "evt-003",
        "eventName": "INSERT",
        "eventSource": "aws:dynamodb",
        "dynamodb": {"Keys": {"pk": {"S": "VENDA#3"}}, "NewImage": {"id_venda": {"N": "3"}, "data_venda": {"S": "2026-01-03"}, "estado": {"S": "RJ"}, "id_cliente": {"N": "102"}, "cupom": {"NULL": True}, "origem": {"S": "Loja-RJ"}, "status_bruto": {"S": " ok "}, "itens": {"L": [{"M": {"produto": {"S": "Teclado"}, "categoria": {"S": "Eletronicos"}, "quantidade": {"N": "1"}, "preco_unitario": {"N": "150.00"}}}]}}}
    },
    {
        "eventID": "evt-004",
        "eventName": "INSERT",
        "eventSource": "aws:dynamodb",
        "dynamodb": {"Keys": {"pk": {"S": "VENDA#4"}}, "NewImage": {"id_venda": {"N": "4"}, "data_venda": {"S": "2026-01-03"}, "estado": {"S": "MG"}, "id_cliente": {"N": "103"}, "cupom": {"NULL": True}, "origem": {"S": "Loja-MG"}, "status_bruto": {"S": "erro-cadastro"}, "itens": {"L": [{"M": {"produto": {"S": "Cadeira"}, "categoria": {"S": "Moveis"}, "quantidade": {"N": "1"}, "preco_unitario": {"N": "900.00"}}}]}}}
    },
    {
        "eventID": "evt-005",
        "eventName": "INSERT",
        "eventSource": "aws:dynamodb",
        "dynamodb": {"Keys": {"pk": {"S": "VENDA#5"}}, "NewImage": {"id_venda": {"N": "5"}, "data_venda": {"S": "2026-01-04"}, "estado": {"S": "SP"}, "id_cliente": {"N": "104"}, "cupom": {"S": "FRETE"}, "origem": {"S": "Loja-SP"}, "status_bruto": {"S": "ok"}, "itens": {"L": [{"M": {"produto": {"S": "Mesa"}, "categoria": {"S": "Moveis"}, "quantidade": {"N": "1"}, "preco_unitario": {"N": "1200.00"}}}]}}}
    },
    {
        "eventID": "evt-006",
        "eventName": "INSERT",
        "eventSource": "aws:dynamodb",
        "dynamodb": {"Keys": {"pk": {"S": "VENDA#6"}}, "NewImage": {"id_venda": {"N": "6"}, "data_venda": {"S": "2026-01-04"}, "estado": {"NULL": True}, "id_cliente": {"N": "105"}, "cupom": {"NULL": True}, "origem": {"S": "Loja-SP"}, "status_bruto": {"S": "ok"}, "itens": {"L": [{"M": {"produto": {"S": "Monitor"}, "categoria": {"S": "Eletronicos"}, "quantidade": {"N": "2"}, "preco_unitario": {"N": "1100.00"}}}]}}}
    },
    {
        "eventID": "evt-007",
        "eventName": "INSERT",
        "eventSource": "aws:dynamodb",
        "dynamodb": {"Keys": {"pk": {"S": "VENDA#7"}}, "NewImage": {"id_venda": {"N": "7"}, "data_venda": {"S": "2026-01-05"}, "estado": {"S": "BA"}, "id_cliente": {"N": "106"}, "cupom": {"S": "CUPOM5"}, "origem": {"S": "Loja-BA"}, "status_bruto": {"S": "pendente"}, "itens": {"L": [{"M": {"produto": {"S": "Headset"}, "categoria": {"S": "Eletronicos"}, "quantidade": {"N": "3"}, "preco_unitario": {"NULL": True}}}]}}}
    },
    {
        "eventID": "evt-008",
        "eventName": "INSERT",
        "eventSource": "aws:dynamodb",
        "dynamodb": {"Keys": {"pk": {"S": "VENDA#8"}}, "NewImage": {"id_venda": {"N": "8"}, "data_venda": {"S": "2026-01-05"}, "estado": {"S": "BA"}, "id_cliente": {"N": "106"}, "cupom": {"NULL": True}, "origem": {"S": "Loja-BA"}, "status_bruto": {"S": "ok"}, "itens": {"L": [{"M": {"produto": {"S": "Webcam"}, "categoria": {"S": "Eletronicos"}, "quantidade": {"N": "1"}, "preco_unitario": {"N": "420.00"}}}]}}}
    },
    {
        "eventID": "evt-009",
        "eventName": "INSERT",
        "eventSource": "aws:dynamodb",
        "dynamodb": {"Keys": {"pk": {"S": "VENDA#9"}}, "NewImage": {"id_venda": {"N": "9"}, "data_venda": {"S": "2026-01-06"}, "estado": {"S": "SP"}, "id_cliente": {"N": "107"}, "cupom": {"NULL": True}, "origem": {"S": "Loja-SP"}, "status_bruto": {"S": "ok"}, "itens": {"L": [{"M": {"produto": {"S": "Notebook"}, "categoria": {"S": "Eletronicos"}, "quantidade": {"N": "1"}, "preco_unitario": {"N": "3600.00"}}}]}}}
    },
    {
        "eventID": "evt-010",
        "eventName": "INSERT",
        "eventSource": "aws:dynamodb",
        "dynamodb": {"Keys": {"pk": {"S": "VENDA#10"}}, "NewImage": {"id_venda": {"N": "10"}, "data_venda": {"S": "2026-01-06"}, "estado": {"S": "RJ"}, "id_cliente": {"N": "108"}, "cupom": {"NULL": True}, "origem": {"S": "Loja-RJ"}, "status_bruto": {"S": "ok"}, "itens": {"L": [{"M": {"produto": {"S": "Cadeira"}, "categoria": {"S": "Moveis"}, "quantidade": {"N": "2"}, "preco_unitario": {"N": "850.00"}}}]}}}
    },
    # Evento duplicado para demonstrar dropDuplicates() na camada Silver.
    {
        "eventID": "evt-010-duplicado",
        "eventName": "INSERT",
        "eventSource": "aws:dynamodb",
        "dynamodb": {"Keys": {"pk": {"S": "VENDA#10"}}, "NewImage": {"id_venda": {"N": "10"}, "data_venda": {"S": "2026-01-06"}, "estado": {"S": "RJ"}, "id_cliente": {"N": "108"}, "cupom": {"NULL": True}, "origem": {"S": "Loja-RJ"}, "status_bruto": {"S": "ok"}, "itens": {"L": [{"M": {"produto": {"S": "Cadeira"}, "categoria": {"S": "Moveis"}, "quantidade": {"N": "2"}, "preco_unitario": {"N": "850.00"}}}]}}}
    },
    {
        "eventID": "evt-011",
        "eventName": "INSERT",
        "eventSource": "aws:dynamodb",
        "dynamodb": {"Keys": {"pk": {"S": "VENDA#11"}}, "NewImage": {"id_venda": {"N": "11"}, "data_venda": {"S": "2026-01-07"}, "estado": {"S": "SP"}, "id_cliente": {"N": "104"}, "cupom": {"NULL": True}, "origem": {"S": "Loja-SP"}, "status_bruto": {"S": "ok"}, "itens": {"L": [{"M": {"produto": {"S": "Mesa"}, "categoria": {"S": "Moveis"}, "quantidade": {"N": "1"}, "preco_unitario": {"N": "1250.00"}}}]}}}
    }
]

json_dynamodb_vendas = [json.dumps(evento) for evento in eventos_dynamodb_vendas]

# Serverless não permite acesso direto ao SparkContext/JVM.
# Por isso, criamos um DataFrame de strings JSON e fazemos o parsing com from_json().
schema_atributo_s = T.StructType([
    T.StructField("S", T.StringType(), True)
])

schema_atributo_n = T.StructType([
    T.StructField("N", T.StringType(), True)
])

schema_atributo_s_null = T.StructType([
    T.StructField("S", T.StringType(), True),
    T.StructField("NULL", T.BooleanType(), True)
])

schema_atributo_n_null = T.StructType([
    T.StructField("N", T.StringType(), True),
    T.StructField("NULL", T.BooleanType(), True)
])

schema_item_venda = T.StructType([
    T.StructField("M", T.StructType([
        T.StructField("produto", schema_atributo_s, True),
        T.StructField("categoria", schema_atributo_s, True),
        T.StructField("quantidade", schema_atributo_n, True),
        T.StructField("preco_unitario", schema_atributo_n_null, True)
    ]), True)
])

schema_dynamodb_vendas = T.StructType([
    T.StructField("eventID", T.StringType(), True),
    T.StructField("eventName", T.StringType(), True),
    T.StructField("eventSource", T.StringType(), True),
    T.StructField("dynamodb", T.StructType([
        T.StructField("Keys", T.StructType([
            T.StructField("pk", schema_atributo_s, True)
        ]), True),
        T.StructField("NewImage", T.StructType([
            T.StructField("id_venda", schema_atributo_n, True),
            T.StructField("data_venda", schema_atributo_s, True),
            T.StructField("estado", schema_atributo_s_null, True),
            T.StructField("id_cliente", schema_atributo_n, True),
            T.StructField("cupom", schema_atributo_s_null, True),
            T.StructField("origem", schema_atributo_s, True),
            T.StructField("status_bruto", schema_atributo_s, True),
            T.StructField("itens", T.StructType([
                T.StructField("L", T.ArrayType(schema_item_venda), True)
            ]), True)
        ]), True)
    ]), True)
])

df_json_dynamodb_vendas = spark.createDataFrame([(linha,) for linha in json_dynamodb_vendas], "json_evento STRING")
df_raw_dynamodb_vendas = (
    df_json_dynamodb_vendas
    .select(F.from_json(F.col("json_evento"), schema_dynamodb_vendas).alias("evento"))
    .select("evento.*")
)

display(df_raw_dynamodb_vendas.select("eventID", "eventName", "eventSource", "dynamodb.NewImage"))

# explode() abre o array de itens da venda. Cada item vira uma linha.
df_vendas = (
    df_raw_dynamodb_vendas
    .withColumn("item", F.explode(F.col("dynamodb.NewImage.itens.L")))
    .select(
        F.col("dynamodb.NewImage.id_venda.N").cast("int").alias("id_venda"),
        F.col("dynamodb.NewImage.data_venda.S").alias("data_venda"),
        F.col("item.M.produto.S").alias("produto"),
        F.col("item.M.categoria.S").alias("categoria"),
        F.col("item.M.quantidade.N").cast("int").alias("quantidade"),
        F.col("item.M.preco_unitario.N").cast("double").alias("preco_unitario"),
        F.col("dynamodb.NewImage.estado.S").alias("estado"),
        F.col("dynamodb.NewImage.id_cliente.N").cast("int").alias("id_cliente"),
        F.col("dynamodb.NewImage.cupom.S").alias("cupom"),
        F.col("dynamodb.NewImage.origem.S").alias("origem"),
        F.col("dynamodb.NewImage.status_bruto.S").alias("status_bruto")
    )
)

# -----------------------------------------------------------------------------
# 2) Origem simulada: CDC/DMS para cadastro de clientes
# -----------------------------------------------------------------------------
# O campo Op representa a operação capturada: I = insert, U = update, D = delete.
# Neste exemplo, vamos manter apenas inserts e updates como estado final de clientes.

eventos_dms_clientes = [
    {"Op": "I", "table_name": "clientes", "commit_timestamp": "2026-01-01T09:00:00", "data": {"id_cliente": 101, "nome_cliente": "Ana", "segmento": "Premium", "data_cadastro": "2026/01/01"}},
    {"Op": "I", "table_name": "clientes", "commit_timestamp": "2026-01-02T09:00:00", "data": {"id_cliente": 102, "nome_cliente": "Bruno", "segmento": "Standard", "data_cadastro": "2026/01/02"}},
    {"Op": "I", "table_name": "clientes", "commit_timestamp": "2026-01-02T10:00:00", "data": {"id_cliente": 103, "nome_cliente": "Carla", "segmento": "Premium", "data_cadastro": "2026/01/02"}},
    {"Op": "I", "table_name": "clientes", "commit_timestamp": "2026-01-03T09:00:00", "data": {"id_cliente": 104, "nome_cliente": "Diego", "segmento": "Standard", "data_cadastro": "2026/01/03"}},
    {"Op": "I", "table_name": "clientes", "commit_timestamp": "2026-01-03T10:00:00", "data": {"id_cliente": 105, "nome_cliente": "Erica", "segmento": "Premium", "data_cadastro": "2026/01/03"}},
    {"Op": "I", "table_name": "clientes", "commit_timestamp": "2026-01-04T09:00:00", "data": {"id_cliente": 106, "nome_cliente": "Fabio", "segmento": "Novo", "data_cadastro": "2026/01/04"}},
    {"Op": "I", "table_name": "clientes", "commit_timestamp": "2026-01-04T10:00:00", "data": {"id_cliente": 107, "nome_cliente": "Gabriela", "segmento": "Novo", "data_cadastro": "2026/01/04"}},
    {"Op": "I", "table_name": "clientes", "commit_timestamp": "2026-01-05T09:00:00", "data": {"id_cliente": 108, "nome_cliente": "Helena", "segmento": "Premium", "data_cadastro": "2026/01/05"}},
    {"Op": "U", "table_name": "clientes", "commit_timestamp": "2026-01-06T09:00:00", "data": {"id_cliente": 106, "nome_cliente": "Fabio", "segmento": "Standard", "data_cadastro": "2026/01/04"}}
]

json_dms_clientes = [json.dumps(evento) for evento in eventos_dms_clientes]

schema_dms_clientes = T.StructType([
    T.StructField("Op", T.StringType(), True),
    T.StructField("table_name", T.StringType(), True),
    T.StructField("commit_timestamp", T.StringType(), True),
    T.StructField("data", T.StructType([
        T.StructField("id_cliente", T.IntegerType(), True),
        T.StructField("nome_cliente", T.StringType(), True),
        T.StructField("segmento", T.StringType(), True),
        T.StructField("data_cadastro", T.StringType(), True)
    ]), True)
])

df_json_dms_clientes = spark.createDataFrame([(linha,) for linha in json_dms_clientes], "json_evento STRING")
df_raw_dms_clientes = (
    df_json_dms_clientes
    .select(F.from_json(F.col("json_evento"), schema_dms_clientes).alias("evento"))
    .select("evento.*")
)

display(df_raw_dms_clientes)

janela_cliente_cdc = Window.partitionBy("data.id_cliente").orderBy(F.col("commit_timestamp").desc())

df_clientes = (
    df_raw_dms_clientes
    .filter(F.col("Op").isin("I", "U"))
    .withColumn("ordem_evento", F.row_number().over(janela_cliente_cdc))
    .filter(F.col("ordem_evento") == 1)
    .select(
        F.col("data.id_cliente").cast("int").alias("id_cliente"),
        F.col("data.nome_cliente").alias("nome_cliente"),
        F.col("data.segmento").alias("segmento"),
        F.col("data.data_cadastro").alias("data_cadastro")
    )
)

# -----------------------------------------------------------------------------
# 3) Opção de origem por arquivos JSON
# -----------------------------------------------------------------------------
# Esta fonte simula arquivos chegando em uma pasta de landing.
# Ela é exibida como alternativa de ingestão e poderia alimentar a Bronze também.

vendas_arquivos = [
    (12, "2026-01-08", "Mesa Lateral", "Moveis", 1, 500.00, "PR", 109, None, "Arquivo-PR", "ok"),
    (13, "2026-01-08", "Mouse Gamer", "Eletronicos", 1, 220.00, "SP", 101, "CUPOM15", "Arquivo-SP", "ok")
]

schema_vendas_arquivos = """
id_venda INT,
data_venda STRING,
produto STRING,
categoria STRING,
quantidade INT,
preco_unitario DOUBLE,
estado STRING,
id_cliente INT,
cupom STRING,
origem STRING,
status_bruto STRING
"""

df_vendas_arquivos_origem = spark.createDataFrame(vendas_arquivos, schema=schema_vendas_arquivos)

# Em muitos workspaces Serverless, o Public DBFS root fica desabilitado.
# Por isso, esta simulação não grava em dbfs:/tmp. Ela representa arquivos JSON Lines
# já recebidos por uma landing zone e faz a leitura do conteúdo JSON de forma segura.
json_vendas_arquivos = [json.dumps(linha.asDict()) for linha in df_vendas_arquivos_origem.collect()]

df_json_vendas_arquivos = spark.createDataFrame(
    [(linha,) for linha in json_vendas_arquivos],
    "json_linha STRING"
)

schema_vendas_arquivos_struct = T.StructType([
    T.StructField("id_venda", T.IntegerType(), True),
    T.StructField("data_venda", T.StringType(), True),
    T.StructField("produto", T.StringType(), True),
    T.StructField("categoria", T.StringType(), True),
    T.StructField("quantidade", T.IntegerType(), True),
    T.StructField("preco_unitario", T.DoubleType(), True),
    T.StructField("estado", T.StringType(), True),
    T.StructField("id_cliente", T.IntegerType(), True),
    T.StructField("cupom", T.StringType(), True),
    T.StructField("origem", T.StringType(), True),
    T.StructField("status_bruto", T.StringType(), True)
])

df_vendas_arquivos = (
    df_json_vendas_arquivos
    .select(F.from_json(F.col("json_linha"), schema_vendas_arquivos_struct).alias("arquivo"))
    .select("arquivo.*")
)

print("Origem por arquivos simulada com JSON Lines em memória, sem usar dbfs:/tmp.")
display(df_vendas_arquivos)

# DataFrame principal usado pelo restante do tutorial.
display(df_vendas)

# COMMAND ----------
# MAGIC %md
# MAGIC # Demonstração prática — lendo e escrevendo formatos de arquivo
# MAGIC 
# MAGIC Agora que `df_vendas` foi criado a partir da origem transacional simulada, vamos ver os comandos de leitura e escrita para alguns formatos.
# MAGIC 
# MAGIC No Databricks Free Edition, o caminho `dbfs:/tmp` pode estar bloqueado com o erro `DBFS_DISABLED`. Por isso, a célula abaixo é segura por padrão: ela mostra os comandos e só grava arquivos se você informar manualmente um caminho válido, como um Volume do Unity Catalog.

# COMMAND ----------
# Demonstração prática: formatos de arquivo no Spark
# Serverless Free Edition pode bloquear o Public DBFS root, então esta célula NÃO grava em dbfs:/tmp.
# Ela mostra os comandos e só executa escrita se você informar um caminho de storage válido.

formatos_para_testar = [
    ("json", "JSON", "bom para eventos, logs e dados semiestruturados"),
    ("csv", "CSV", "simples para troca de arquivos, mas sem schema rico"),
    ("parquet", "Parquet", "colunar, comprimido e eficiente para análise"),
    ("orc", "ORC", "colunar, comum em ambientes Hive"),
    ("delta", "Delta Lake", "tabela lakehouse com transações e _delta_log")
]

df_formatos = spark.createDataFrame(formatos_para_testar, ["formato_spark", "nome", "uso_comum"])
display(df_formatos)

print("Exemplos de comandos de escrita e leitura:")
for formato, nome, _ in formatos_para_testar:
    print()
    print("#", nome)
    print(f'df_vendas.write.format("{formato}").mode("overwrite").save("<caminho_valido>/{formato}")')
    print(f'spark.read.format("{formato}").load("<caminho_valido>/{formato}")')

# Opcional: para executar de verdade, informe um caminho válido de storage.
# Em Databricks com Unity Catalog, prefira um Volume, por exemplo:
# CAMINHO_STORAGE_VALIDO = "/Volumes/<catalogo>/<schema>/<volume>/aula3_lakehouse_formatos"

EXECUTAR_DEMO_FORMATOS = False
CAMINHO_STORAGE_VALIDO = ""

if not EXECUTAR_DEMO_FORMATOS:
    print()
    print("Demonstração de escrita não executada.")
    print("Para executar, defina EXECUTAR_DEMO_FORMATOS = True e CAMINHO_STORAGE_VALIDO com um caminho válido, como um Volume do Unity Catalog.")
elif not CAMINHO_STORAGE_VALIDO:
    print("Informe CAMINHO_STORAGE_VALIDO antes de executar a escrita dos formatos.")
else:
    df_demo_formatos = df_vendas.limit(5)

    for formato, nome, _ in formatos_para_testar:
        caminho = f"{CAMINHO_STORAGE_VALIDO}/{formato}"
        print()
        print("Formato:", nome)
        print("Caminho:", caminho)

        writer = df_demo_formatos.write.format(formato).mode("overwrite")
        if formato == "csv":
            writer = writer.option("header", "true")
        writer.save(caminho)

        reader = spark.read.format(formato)
        if formato == "csv":
            reader = reader.option("header", "true")
        df_lido = reader.load(caminho)

        print("Linhas lidas:", df_lido.count())
        df_lido.printSchema()

# COMMAND ----------
# MAGIC %md
# MAGIC # Camada Bronze — dados brutos no Lakehouse
# MAGIC 
# MAGIC A camada Bronze recebe os dados como chegaram ao pipeline, preservando rastreabilidade e histórico de ingestão.
# MAGIC 
# MAGIC Neste exemplo, vamos gravar quatro tipos de tabela Bronze:
# MAGIC 
# MAGIC - eventos brutos simulados de DynamoDB Streams;
# MAGIC - eventos brutos simulados de CDC/DMS;
# MAGIC - vendas já explodidas a partir do JSON transacional;
# MAGIC - clientes consolidados a partir dos eventos CDC/DMS.
# MAGIC 
# MAGIC Na prática, é comum manter tanto o bruto original quanto uma primeira versão estruturada para facilitar reprocessamentos e auditoria.

# COMMAND ----------
# Camada Bronze: cria schemas e grava dados brutos no Lakehouse

catalogo_atual = spark.sql("SELECT current_catalog() AS catalogo").first()["catalogo"]
schema_atual = spark.sql("SELECT current_schema() AS schema").first()["schema"]

print("Catálogo atual:", catalogo_atual)
print("Schema atual:", schema_atual)

for camada in ["bronze", "silver", "gold"]:
    spark.sql(f"CREATE SCHEMA IF NOT EXISTS {camada}")

bronze_dynamodb_vendas_raw = "bronze.aula3_dynamodb_vendas_raw"
bronze_dms_clientes_raw = "bronze.aula3_dms_clientes_raw"
bronze_vendas = "bronze.aula3_vendas_raw"
bronze_clientes = "bronze.aula3_clientes_raw"

(
    df_raw_dynamodb_vendas
    .withColumn("_data_ingestao", F.current_timestamp())
    .withColumn("_fonte", F.lit("dynamodb_stream_simulado"))
    .write
    .format("delta")
    .mode("overwrite")
    .option("overwriteSchema", "true")
    .saveAsTable(bronze_dynamodb_vendas_raw)
)

(
    df_raw_dms_clientes
    .withColumn("_data_ingestao", F.current_timestamp())
    .withColumn("_fonte", F.lit("dms_cdc_simulado"))
    .write
    .format("delta")
    .mode("overwrite")
    .option("overwriteSchema", "true")
    .saveAsTable(bronze_dms_clientes_raw)
)

df_bronze_vendas = (
    df_vendas
    .withColumn("_data_ingestao", F.current_timestamp())
    .withColumn("_fonte", F.lit("dynamodb_stream_explodido"))
)

df_bronze_clientes = (
    df_clientes
    .withColumn("_data_ingestao", F.current_timestamp())
    .withColumn("_fonte", F.lit("dms_cdc_consolidado"))
)

(
    df_bronze_vendas
    .write
    .format("delta")
    .mode("overwrite")
    .option("overwriteSchema", "true")
    .saveAsTable(bronze_vendas)
)

(
    df_bronze_clientes
    .write
    .format("delta")
    .mode("overwrite")
    .option("overwriteSchema", "true")
    .saveAsTable(bronze_clientes)
)

print("Tabelas Bronze criadas:")
for tabela in [bronze_dynamodb_vendas_raw, bronze_dms_clientes_raw, bronze_vendas, bronze_clientes]:
    print("-", tabela)

display(spark.read.table(bronze_vendas))

# COMMAND ----------
display(df_clientes)

# COMMAND ----------
# Inspeção inicial
df_vendas.printSchema()
df_vendas.show(5, truncate=False)
print("Quantidade de linhas em vendas:", df_vendas.count())
print("Colunas:", df_vendas.columns)
print("Tipos:", df_vendas.dtypes)

# COMMAND ----------
# select() escolhe apenas as colunas necessárias para o trabalho
df_base = df_vendas.select(
    "id_venda",
    "data_venda",
    "produto",
    "categoria",
    "quantidade",
    "preco_unitario",
    "estado",
    "id_cliente",
    "cupom",
    "origem",
    "status_bruto"
)

display(df_base)

# COMMAND ----------
# selectExpr() faz a seleção usando expressões SQL
df_expr = df_base.selectExpr(
    "id_venda",
    "produto",
    "quantidade",
    "preco_unitario",
    "quantidade * preco_unitario AS valor_total_expr",
    "upper(categoria) AS categoria_maiuscula"
)

display(df_expr)

# COMMAND ----------
# filter() mantém apenas as linhas que atendem à condição
df_eletronicos = df_base.filter(F.col("categoria") == "Eletronicos")
display(df_eletronicos)

# where() é uma alternativa equivalente ao filter()
df_sp = df_base.where(F.col("estado") == "SP")
display(df_sp)

# COMMAND ----------
# MAGIC %md
# MAGIC # Parte 2 — Transformação, limpeza e padronização
# MAGIC **Tempo sugerido:** 15 a 20 minutos
# MAGIC 
# MAGIC ## Objetivo
# MAGIC Criar colunas derivadas, tratar nulos, padronizar texto e converter datas.
# MAGIC 
# MAGIC ## Funções usadas nesta parte
# MAGIC 
# MAGIC ### `withColumn()`
# MAGIC Cria ou substitui uma coluna.
# MAGIC 
# MAGIC ### `withColumnRenamed()`
# MAGIC Renomeia uma coluna.
# MAGIC 
# MAGIC ### `drop()`
# MAGIC Remove colunas que não serão mais usadas.
# MAGIC 
# MAGIC ### `lit()`
# MAGIC Cria um valor literal constante.
# MAGIC 
# MAGIC ### `when(...).otherwise(...)`
# MAGIC Cria regras condicionais.
# MAGIC 
# MAGIC ### `coalesce()`
# MAGIC Retorna o primeiro valor não nulo entre as colunas informadas.  
# MAGIC É muito útil para definir um valor final quando existem alternativas.
# MAGIC 
# MAGIC ### `regexp_replace()`
# MAGIC Substitui trechos de texto usando expressão regular.  
# MAGIC Serve para limpar padrões como barras, espaços extras ou caracteres indesejados.
# MAGIC 
# MAGIC ### `trim()`
# MAGIC Remove espaços no começo e no fim do texto.
# MAGIC 
# MAGIC ### `to_date()`
# MAGIC Converte texto para tipo data.
# MAGIC 
# MAGIC ### `fillna()`
# MAGIC Substitui valores nulos por um valor definido.
# MAGIC 
# MAGIC ### `dropna()`
# MAGIC Remove linhas com nulos em colunas específicas.
# MAGIC 

# COMMAND ----------
# withColumnRenamed() altera o nome de uma coluna
df_renomeado = df_base.withColumnRenamed("data_venda", "dt_venda")
display(df_renomeado)

# COMMAND ----------
# withColumn() cria novas colunas
# lit() adiciona um valor constante
df_metricas = (
    df_renomeado
    .withColumn("valor_total", F.col("quantidade") * F.col("preco_unitario"))
    .withColumn("canal", F.lit("Loja Online"))
)

display(df_metricas)

# COMMAND ----------
# when(...).otherwise(...) cria classificações condicionais
df_classificado = (
    df_metricas
    .withColumn(
        "faixa_valor",
        F.when(F.col("valor_total") >= 3000, F.lit("Alta"))
         .when(F.col("valor_total") >= 1000, F.lit("Media"))
         .otherwise(F.lit("Baixa"))
    )
)

display(df_classificado.orderBy(F.desc("valor_total")))

# COMMAND ----------
# regexp_replace(), trim() e to_date() ajudam a padronizar dados
# coalesce() retorna o primeiro valor não nulo entre as opções informadas
df_limpo = (
    df_classificado
    .withColumn("status_tratado", F.trim(F.regexp_replace(F.col("status_bruto"), "-", " ")))
    .withColumn("dt_venda", F.to_date(F.col("dt_venda"), "yyyy-MM-dd"))
    .withColumn("estado_final", F.coalesce(F.col("estado"), F.lit("NAO_INFORMADO")))
    .withColumn("origem_padronizada", F.regexp_replace(F.col("origem"), "-", "_"))
)

display(df_limpo)

# COMMAND ----------
# fillna() substitui nulos com valores definidos
# dropna() remove linhas que continuam sem informação em colunas críticas
df_tratado = (
    df_limpo
    .fillna({"preco_unitario": 0.0, "cupom": "SEM_CUPOM"})
    .dropna(subset=["produto", "id_cliente"])
)

display(df_tratado)

# COMMAND ----------
# drop() remove colunas que não serão mais usadas
df_tratado = df_tratado.drop("estado", "status_bruto")
display(df_tratado)

# COMMAND ----------
# MAGIC %md
# MAGIC # Camada Silver — dados tratados e padronizados
# MAGIC 
# MAGIC A camada Silver representa dados confiáveis para reuso técnico. Aqui entram regras como padronização de datas, tratamento de nulos, remoção de duplicidades e seleção de colunas úteis.
# MAGIC 
# MAGIC Neste tutorial, vamos gravar:
# MAGIC 
# MAGIC - `silver.aula3_vendas_tratadas`
# MAGIC - `silver.aula3_clientes_tratados`
# MAGIC 
# MAGIC Essas tabelas Silver serão a base para análises e agregações da camada Gold.

# COMMAND ----------
# Camada Silver: grava dados limpos e padronizados no Lakehouse

silver_vendas = "silver.aula3_vendas_tratadas"
silver_clientes = "silver.aula3_clientes_tratados"

df_silver_vendas = (
    df_tratado
    .dropDuplicates(["id_venda", "produto", "id_cliente", "dt_venda"])
    .withColumn("_data_processamento", F.current_timestamp())
)

df_silver_clientes = (
    df_clientes
    .withColumn("data_cadastro", F.to_date(F.col("data_cadastro"), "yyyy/MM/dd"))
    .dropDuplicates(["id_cliente"])
    .withColumn("_data_processamento", F.current_timestamp())
)

(
    df_silver_vendas
    .write
    .format("delta")
    .mode("overwrite")
    .option("overwriteSchema", "true")
    .saveAsTable(silver_vendas)
)

(
    df_silver_clientes
    .write
    .format("delta")
    .mode("overwrite")
    .option("overwriteSchema", "true")
    .saveAsTable(silver_clientes)
)

print("Tabelas Silver criadas:")
print("-", silver_vendas)
print("-", silver_clientes)

display(spark.read.table(silver_vendas).orderBy("id_venda"))

# COMMAND ----------
# MAGIC %md
# MAGIC # Parte 3 — Combinação, agregação e análise com janelas
# MAGIC **Tempo sugerido:** 15 a 20 minutos
# MAGIC 
# MAGIC ## Objetivo
# MAGIC Remover duplicidades, combinar bases, unir datasets com schemas parecidos, gerar métricas agregadas e usar funções de janela.
# MAGIC 
# MAGIC ## Funções usadas nesta parte
# MAGIC 
# MAGIC ### `dropDuplicates()`
# MAGIC Remove linhas duplicadas.
# MAGIC 
# MAGIC ### `unionByName()`
# MAGIC Une DataFrames usando o nome das colunas em vez da posição.  
# MAGIC É muito útil quando a ordem das colunas muda entre duas fontes.
# MAGIC 
# MAGIC ### `join()`
# MAGIC Combina dois DataFrames usando uma chave em comum.
# MAGIC 
# MAGIC ### `groupBy()`
# MAGIC Agrupa registros por uma ou mais colunas.
# MAGIC 
# MAGIC ### `agg()`
# MAGIC Aplica métricas de agregação sobre os grupos.
# MAGIC 
# MAGIC ### `sum()`, `avg()`, `count()`, `countDistinct()`
# MAGIC Calculam soma, média, quantidade de linhas e quantidade distinta.
# MAGIC 
# MAGIC ### `orderBy()`
# MAGIC Ordena o resultado.
# MAGIC 
# MAGIC ### `Window.partitionBy()` e `Window.orderBy()`
# MAGIC Definem o grupo e a ordenação usados por funções analíticas.
# MAGIC 
# MAGIC ### `row_number()`
# MAGIC Numera as linhas dentro de uma janela.
# MAGIC 
# MAGIC ### `lag()` e `lead()`
# MAGIC Permitem olhar a linha anterior e a próxima linha dentro da mesma janela.
# MAGIC 

# COMMAND ----------
# dropDuplicates() remove linhas repetidas
df_sem_duplicidade = df_tratado.dropDuplicates()

print("Linhas antes:", df_tratado.count())
print("Linhas depois:", df_sem_duplicidade.count())
display(df_sem_duplicidade)

# COMMAND ----------
# unionByName() combina bases pelo nome das colunas
# A base abaixo simula novas vendas com a mesma estrutura, mas em ordem diferente
dados_vendas_extra = [
    ("Loja-PR", None, 109, "PR", 500.0, "Moveis", 1, "Mesa Lateral", 12, "2026-01-08", "ok"),
    ("Loja-SP", "CUPOM15", 101, "SP", 220.0, "Eletronicos", 1, "Mouse Gamer", 13, "2026-01-08", "ok")
]

colunas_extra = [
    "origem", "cupom", "id_cliente", "estado", "preco_unitario",
    "categoria", "quantidade", "produto", "id_venda", "data_venda", "status_bruto"
]

df_vendas_extra = spark.createDataFrame(dados_vendas_extra, schema=colunas_extra)

df_extra_tratado = (
    df_vendas_extra
    .withColumnRenamed("data_venda", "dt_venda")
    .withColumn("valor_total", F.col("quantidade") * F.col("preco_unitario"))
    .withColumn("canal", F.lit("Loja Online"))
    .withColumn(
        "faixa_valor",
        F.when(F.col("valor_total") >= 3000, F.lit("Alta"))
         .when(F.col("valor_total") >= 1000, F.lit("Media"))
         .otherwise(F.lit("Baixa"))
    )
    .withColumn("status_tratado", F.trim(F.regexp_replace(F.col("status_bruto"), "-", " ")))
    .withColumn("dt_venda", F.to_date(F.col("dt_venda"), "yyyy-MM-dd"))
    .withColumn("estado_final", F.coalesce(F.col("estado"), F.lit("NAO_INFORMADO")))
    .withColumn("origem_padronizada", F.regexp_replace(F.col("origem"), "-", "_"))
    .fillna({"preco_unitario": 0.0, "cupom": "SEM_CUPOM"})
    .drop("estado", "status_bruto")
)

df_unificado = df_sem_duplicidade.unionByName(df_extra_tratado, allowMissingColumns=True)
display(df_unificado.orderBy("id_venda"))

# COMMAND ----------
# join() enriquece a base de vendas com a base de clientes
# A data de cadastro também será convertida para data
df_clientes_tratado = df_clientes.withColumn(
    "data_cadastro", F.to_date(F.col("data_cadastro"), "yyyy/MM/dd")
)

df_enriquecido = df_unificado.join(df_clientes_tratado, on="id_cliente", how="left")
display(df_enriquecido)

# COMMAND ----------
# groupBy() + agg() gera métricas agregadas
df_analitico_categoria = (
    df_enriquecido
    .groupBy("categoria")
    .agg(
        F.count("*").alias("qtd_registros"),
        F.sum("valor_total").alias("faturamento_total"),
        F.avg("valor_total").alias("ticket_medio"),
        F.countDistinct("id_cliente").alias("clientes_distintos")
    )
    .withColumn("faturamento_total", F.round(F.col("faturamento_total"), 2))
    .withColumn("ticket_medio", F.round(F.col("ticket_medio"), 2))
    .orderBy(F.desc("faturamento_total"))
)

display(df_analitico_categoria)

# COMMAND ----------
# Outro corte analítico por estado e segmento
df_analitico_estado_segmento = (
    df_enriquecido
    .groupBy("estado_final", "segmento")
    .agg(
        F.sum("valor_total").alias("faturamento_total"),
        F.count("*").alias("qtd_vendas")
    )
    .withColumn("faturamento_total", F.round(F.col("faturamento_total"), 2))
    .orderBy("estado_final", F.desc("faturamento_total"))
)

display(df_analitico_estado_segmento)

# COMMAND ----------
# MAGIC %md
# MAGIC # Camada Gold — tabelas analíticas para consumo
# MAGIC 
# MAGIC A camada Gold contém dados prontos para perguntas de negócio. Normalmente são tabelas agregadas, indicadores, visões por período, produto, cliente, região ou qualquer outro corte usado por dashboards e análises.
# MAGIC 
# MAGIC Neste tutorial, vamos gravar:
# MAGIC 
# MAGIC - `gold.aula3_analitico_categoria`
# MAGIC - `gold.aula3_analitico_estado_segmento`
# MAGIC 
# MAGIC Essas tabelas podem ser consultadas no **Catalog**, no **SQL Editor** ou em dashboards.

# COMMAND ----------
# Camada Gold: grava tabelas analíticas de negócio no Lakehouse

gold_categoria = "gold.aula3_analitico_categoria"
gold_estado_segmento = "gold.aula3_analitico_estado_segmento"

(
    df_analitico_categoria
    .write
    .format("delta")
    .mode("overwrite")
    .option("overwriteSchema", "true")
    .saveAsTable(gold_categoria)
)

(
    df_analitico_estado_segmento
    .write
    .format("delta")
    .mode("overwrite")
    .option("overwriteSchema", "true")
    .saveAsTable(gold_estado_segmento)
)

print("Tabelas Gold criadas:")
print("-", gold_categoria)
print("-", gold_estado_segmento)

display(spark.read.table(gold_categoria))

# COMMAND ----------
# Window.partitionBy() define o grupo
# Window.orderBy() define a ordenação dentro do grupo
# row_number() numera as linhas da janela
# lag() lê a linha anterior
# lead() lê a próxima linha

janela_cliente = Window.partitionBy("id_cliente").orderBy("dt_venda", "id_venda")

df_janela = (
    df_enriquecido
    .withColumn("ordem_venda_cliente", F.row_number().over(janela_cliente))
    .withColumn("valor_total_anterior", F.lag("valor_total", 1).over(janela_cliente))
    .withColumn("valor_total_proximo", F.lead("valor_total", 1).over(janela_cliente))
)

display(df_janela.orderBy("id_cliente", "ordem_venda_cliente"))

# COMMAND ----------
# MAGIC %md
# MAGIC # Parte 4 — Estatística rápida, performance e persistência
# MAGIC **Tempo sugerido:** 15 a 20 minutos
# MAGIC 
# MAGIC ## Objetivo
# MAGIC Fazer leitura exploratória rápida, observar decisões de particionamento e salvar o resultado final.
# MAGIC 
# MAGIC ## Funções usadas nesta parte
# MAGIC 
# MAGIC ### `sample()`
# MAGIC Cria uma amostra aleatória do DataFrame.
# MAGIC 
# MAGIC ### `approxQuantile()`
# MAGIC Calcula quantis aproximados de forma eficiente em ambiente distribuído.  
# MAGIC É útil para avaliar distribuição de valores sem custo tão alto quanto alguns cálculos exatos.
# MAGIC 
# MAGIC ### `cache()`
# MAGIC Mantém o DataFrame em memória para reutilização.  
# MAGIC Faz sentido quando o mesmo DataFrame será lido várias vezes.
# MAGIC 
# MAGIC ### `repartition()`
# MAGIC Redistribui os dados entre partições.  
# MAGIC Normalmente envolve shuffle e é útil para aumentar paralelismo ou reorganizar a escrita.
# MAGIC 
# MAGIC ### `coalesce()`
# MAGIC Reduz o número de partições.  
# MAGIC Em reduções, costuma trabalhar com dependência estreita e evita shuffle desnecessário em vários casos.
# MAGIC 
# MAGIC ### `rdd.getNumPartitions()`
# MAGIC Mostra quantas partições o DataFrame possui.
# MAGIC 
# MAGIC ### `explain("formatted")` e `explain("extended")`
# MAGIC Mostram o plano de execução.  
# MAGIC `formatted` é mais legível.  
# MAGIC `extended` mostra mais detalhes do plano lógico e físico.
# MAGIC 
# MAGIC ### `write.mode().saveAsTable()`
# MAGIC Grava o DataFrame como tabela.
# MAGIC 
# MAGIC ### `spark.read.table()`
# MAGIC Lê uma tabela já persistida.
# MAGIC 

# COMMAND ----------
# MAGIC %md
# MAGIC # Configurações e boas práticas para reduzir shuffle e skew
# MAGIC 
# MAGIC Antes de gravar ou analisar performance, é importante entender dois problemas comuns em Spark:
# MAGIC 
# MAGIC ## Shuffle
# MAGIC Shuffle acontece quando o Spark precisa redistribuir dados entre partições. Ele aparece com frequência em operações como `join()`, `groupBy()`, `distinct()`, `dropDuplicates()`, `orderBy()`, `repartition()` e funções de janela.
# MAGIC 
# MAGIC Nem todo shuffle é ruim: muitas análises precisam dele. O objetivo é **evitar shuffle desnecessário** e tornar os shuffles inevitáveis mais eficientes.
# MAGIC 
# MAGIC ## Skew
# MAGIC Skew acontece quando uma ou poucas chaves concentram muitos registros. Exemplo: muitas vendas no estado `SP` e poucas nos demais estados. Isso cria partições muito maiores que outras, fazendo algumas tarefas demorarem muito mais.
# MAGIC 
# MAGIC ## Configurações importantes
# MAGIC 
# MAGIC ### `spark.sql.adaptive.enabled`
# MAGIC Ativa o **Adaptive Query Execution (AQE)**. Com AQE, o Spark pode ajustar o plano durante a execução, depois de observar estatísticas reais dos dados.
# MAGIC 
# MAGIC ### `spark.sql.adaptive.coalescePartitions.enabled`
# MAGIC Permite que o AQE junte partições pequenas após shuffle. Ajuda a reduzir overhead quando existem partições demais para pouco dado.
# MAGIC 
# MAGIC ### `spark.sql.adaptive.skewJoin.enabled`
# MAGIC Permite que o AQE tente tratar joins com skew, dividindo partições muito grandes em partes menores.
# MAGIC 
# MAGIC ### `spark.sql.shuffle.partitions`
# MAGIC Define o número padrão de partições após shuffle. O padrão costuma ser alto para bases pequenas de aula. Em produção, esse número deve ser escolhido conforme volume, tamanho dos arquivos, quantidade de workers e tempo de execução.
# MAGIC 
# MAGIC ### `spark.sql.autoBroadcastJoinThreshold`
# MAGIC Define até que tamanho uma tabela pode ser enviada por broadcast automaticamente. Broadcast é útil quando uma tabela pequena será usada em join com uma tabela maior, evitando redistribuir os dois lados do join.
# MAGIC 
# MAGIC ## Pontos importantes para citar em aula
# MAGIC 
# MAGIC - Filtre linhas e selecione colunas antes de `join()` e `groupBy()`.
# MAGIC - Use `broadcast()` quando uma tabela pequena será combinada com uma tabela maior.
# MAGIC - Evite `orderBy()` global sem necessidade, porque ele costuma gerar shuffle caro.
# MAGIC - Prefira `coalesce()` para reduzir partições antes de salvar poucos arquivos; use `repartition()` quando precisar redistribuir os dados.
# MAGIC - Ao fazer `join()` ou agregações, observe se a chave é muito concentrada em poucos valores.
# MAGIC - Para skew severo, considere técnicas como salting, pré-agregação, broadcast da dimensão pequena ou mudança da chave de particionamento.
# MAGIC - Use `explain("formatted")` para verificar se o Spark está usando `BroadcastHashJoin`, `SortMergeJoin`, `Exchange`, `AdaptiveSparkPlan` e outras etapas do plano.
# MAGIC - Não existe configuração mágica: ajuste com base no volume, no plano de execução e no tempo observado.

# COMMAND ----------
# Configurações úteis para a aula
# Em Databricks Free Edition, o ambiente é serverless, mas estas configs SQL podem ser ajustadas na sessão do notebook.

spark.conf.set("spark.sql.adaptive.enabled", "true")
spark.conf.set("spark.sql.adaptive.coalescePartitions.enabled", "true")
spark.conf.set("spark.sql.adaptive.skewJoin.enabled", "true")

# Para uma base pequena de aula, poucas partições de shuffle são suficientes.
# Em produção, não use este número no automático: avalie volume de dados, workers e tamanho das partições.
spark.conf.set("spark.sql.shuffle.partitions", "8")

# Permite broadcast automático de tabelas pequenas até 50 MB.
# Aumentar demais este valor pode causar pressão de memória.
spark.conf.set("spark.sql.autoBroadcastJoinThreshold", str(50 * 1024 * 1024))

configs_importantes = [
    "spark.sql.adaptive.enabled",
    "spark.sql.adaptive.coalescePartitions.enabled",
    "spark.sql.adaptive.skewJoin.enabled",
    "spark.sql.shuffle.partitions",
    "spark.sql.autoBroadcastJoinThreshold"
]

for chave in configs_importantes:
    print(chave, "=", spark.conf.get(chave))

# Exemplo 1: broadcast explícito da tabela pequena de clientes
# Neste tutorial, df_clientes_tratado é pequeno, então faz sentido enviá-lo para todos os executores.
df_enriquecido_broadcast = df_unificado.join(
    F.broadcast(df_clientes_tratado),
    on="id_cliente",
    how="left"
)

display(df_enriquecido_broadcast)

# Exemplo 2: reparticionar por uma chave usada em agregação ou join
# Use com cuidado: repartition() também gera shuffle, então ele só compensa quando melhora etapas seguintes.
df_particionado_estado = df_enriquecido.repartition("estado_final")
print("Partições após repartition por estado_final:", df_particionado_estado.rdd.getNumPartitions())

# Exemplo 3: validar o plano de execução
# Procure termos como AdaptiveSparkPlan, Exchange, BroadcastHashJoin e SortMergeJoin.
df_enriquecido_broadcast.explain("formatted")

# COMMAND ----------
# sample() gera uma amostra rápida para exploração
df_amostra = df_enriquecido.sample(withReplacement=False, fraction=0.4, seed=42)
display(df_amostra)

# COMMAND ----------
# approxQuantile() calcula quantis aproximados
quantis = df_enriquecido.approxQuantile("valor_total", [0.25, 0.5, 0.75], 0.05)
print("Quantis aproximados de valor_total (25%, 50%, 75%):", quantis)

# COMMAND ----------
# cache() guarda o DataFrame para reutilização
df_cache = df_enriquecido.cache()
print("Quantidade de registros em df_cache:", df_cache.count())

# COMMAND ----------
# Número atual de partições
particoes_atuais = df_cache.rdd.getNumPartitions()
print("Partições atuais:", particoes_atuais)

# repartition() aumenta ou redistribui partições
df_reparticionado = df_cache.repartition(4)
print("Partições após repartition(4):", df_reparticionado.rdd.getNumPartitions())

# coalesce() reduz o número de partições
df_coalescido = df_reparticionado.coalesce(2)
print("Partições após coalesce(2):", df_coalescido.rdd.getNumPartitions())

# COMMAND ----------
# explain('formatted') mostra o plano físico de forma mais legível
df_analitico_categoria.explain("formatted")

# COMMAND ----------
# explain('extended') mostra detalhes extras do plano lógico e físico
df_analitico_categoria.explain("extended")

# COMMAND ----------
# Validação final da camada Gold
# A tabela abaixo já foi gravada na arquitetura Medallion como resultado analítico de negócio.

nome_tabela = "gold.aula3_analitico_categoria"

print(f"Tabela Gold disponível para consumo: {nome_tabela}")
spark.sql("SHOW TABLES IN gold").show(truncate=False)

# COMMAND ----------
# Leitura da tabela Gold para validar a persistência no Lakehouse
df_resultado_final = spark.read.table("gold.aula3_analitico_categoria")
display(df_resultado_final)

# COMMAND ----------
# MAGIC %md
# MAGIC # Limpeza opcional do ambiente
# MAGIC 
# MAGIC Esta etapa remove as tabelas, schemas e pastas temporárias criadas durante o tutorial.
# MAGIC 
# MAGIC **Importante:** não execute esta célula durante a aula prática normal. Ela deve ser usada apenas no final, quando você quiser limpar o ambiente, ou quando o professor solicitar.
# MAGIC 
# MAGIC A célula de código abaixo vem travada com `EXECUTAR_LIMPEZA = False`. Assim, se você usar **Run all**, nada será apagado por acidente.
# MAGIC 
# MAGIC Para limpar o ambiente, altere manualmente para:
# MAGIC 
# MAGIC ```python
# MAGIC EXECUTAR_LIMPEZA = True
# MAGIC ```
# MAGIC 
# MAGIC Depois execute somente essa célula.

# COMMAND ----------
# Limpeza opcional: execute somente quando quiser apagar os objetos criados no tutorial.
# A trava abaixo evita exclusão acidental quando o notebook inteiro é executado.

EXECUTAR_LIMPEZA = False

if not EXECUTAR_LIMPEZA:
    print("Limpeza não executada.")
    print("Para apagar os objetos criados no tutorial, altere EXECUTAR_LIMPEZA para True e execute esta célula novamente.")
else:
    tabelas_para_remover = [
        "bronze.aula3_dynamodb_vendas_raw",
        "bronze.aula3_dms_clientes_raw",
        "bronze.aula3_vendas_raw",
        "bronze.aula3_clientes_raw",
        "silver.aula3_vendas_tratadas",
        "silver.aula3_clientes_tratados",
        "gold.aula3_analitico_categoria",
        "gold.aula3_analitico_estado_segmento",
        "default.aula3_spark_analitico_categoria_v4"
    ]

    for tabela in tabelas_para_remover:
        print(f"Removendo tabela, se existir: {tabela}")
        spark.sql(f"DROP TABLE IF EXISTS {tabela}")

    # DROP SCHEMA só funciona se o schema estiver vazio.
    # Como as tabelas do tutorial foram removidas acima, estes comandos devem funcionar para o ambiente da aula.
    for schema in ["gold", "silver", "bronze"]:
        print(f"Removendo schema, se estiver vazio: {schema}")
        spark.sql(f"DROP SCHEMA IF EXISTS {schema}")

    print("Limpeza finalizada.")
    print("Observação: esta limpeza não remove arquivos externos em Volumes. Se você configurou CAMINHO_STORAGE_VALIDO na demonstração de formatos, remova esse caminho manualmente se necessário.")

# COMMAND ----------
# MAGIC %md
# MAGIC # Resumo das funções do tutorial
# MAGIC 
# MAGIC ## Leitura e inspeção
# MAGIC - `spark.createDataFrame()` cria DataFrames
# MAGIC - `display()` mostra o resultado na interface
# MAGIC - `printSchema()` mostra o schema
# MAGIC - `show()` mostra uma amostra textual
# MAGIC - `count()` conta linhas
# MAGIC - `select()` seleciona colunas
# MAGIC - `selectExpr()` usa expressões SQL
# MAGIC 
# MAGIC ## Transformação e limpeza
# MAGIC - `withColumn()` cria ou substitui colunas
# MAGIC - `withColumnRenamed()` renomeia colunas
# MAGIC - `drop()` remove colunas
# MAGIC - `filter()` e `where()` aplicam filtros
# MAGIC - `lit()` cria valores fixos
# MAGIC - `when(...).otherwise(...)` cria regras condicionais
# MAGIC - `coalesce()` pega o primeiro valor não nulo
# MAGIC - `regexp_replace()` limpa e padroniza texto
# MAGIC - `trim()` remove espaços extras
# MAGIC - `to_date()` converte texto em data
# MAGIC - `fillna()` substitui nulos
# MAGIC - `dropna()` remove linhas incompletas
# MAGIC 
# MAGIC ## Combinação e agregação
# MAGIC - `dropDuplicates()` remove duplicidades
# MAGIC - `unionByName()` une bases pelo nome das colunas
# MAGIC - `join()` enriquece o DataFrame com outra base
# MAGIC - `groupBy()` cria grupos
# MAGIC - `agg()` aplica métricas
# MAGIC - `sum()`, `avg()`, `countDistinct()` calculam indicadores
# MAGIC - `orderBy()` ordena o resultado
# MAGIC 
# MAGIC ## Funções analíticas
# MAGIC - `Window.partitionBy()` define grupos da janela
# MAGIC - `Window.orderBy()` define a ordem da janela
# MAGIC - `row_number()` numera linhas
# MAGIC - `lag()` lê a linha anterior
# MAGIC - `lead()` lê a próxima linha
# MAGIC 
# MAGIC ## Estatística rápida e performance
# MAGIC - `sample()` cria amostra aleatória
# MAGIC - `approxQuantile()` calcula quantis aproximados
# MAGIC - `cache()` mantém dados em memória para reuso
# MAGIC - `repartition()` redistribui partições
# MAGIC - `coalesce()` reduz partições
# MAGIC - `rdd.getNumPartitions()` mostra quantas partições existem
# MAGIC - `explain("formatted")` e `explain("extended")` mostram o plano de execução
# MAGIC 
# MAGIC ## Persistência
# MAGIC - `write.mode().saveAsTable()` grava em tabela
# MAGIC - `spark.read.table()` lê a tabela gravada
# MAGIC 
# MAGIC ## Configurações e performance Spark
# MAGIC - `spark.conf.set()` ajusta configurações da sessão
# MAGIC - `spark.sql.adaptive.enabled` ativa Adaptive Query Execution
# MAGIC - `spark.sql.adaptive.coalescePartitions.enabled` junta partições pequenas após shuffle
# MAGIC - `spark.sql.adaptive.skewJoin.enabled` ajuda no tratamento de joins com skew
# MAGIC - `spark.sql.shuffle.partitions` define partições padrão de shuffle
# MAGIC - `spark.sql.autoBroadcastJoinThreshold` controla broadcast automático
# MAGIC - `broadcast()` força broadcast de uma tabela pequena em joins
# MAGIC 
# MAGIC ## Lakehouse e arquitetura Medallion
# MAGIC - `CREATE SCHEMA IF NOT EXISTS` cria as camadas Bronze, Silver e Gold
# MAGIC - `write.format("delta").saveAsTable()` grava tabelas Delta gerenciadas
# MAGIC - `spark.read.table()` lê tabelas do Lakehouse
# MAGIC - Bronze mantém dados brutos e metadados de ingestão
# MAGIC - Silver guarda dados tratados, padronizados e deduplicados
# MAGIC - Gold guarda tabelas analíticas prontas para consumo
# MAGIC - `SHOW TABLES IN gold` lista tabelas publicadas na camada Gold
# MAGIC 
# MAGIC ## Origens simuladas
# MAGIC - DynamoDB Streams foi simulado com JSON aninhado e atributos tipados
# MAGIC - `spark.createDataFrame()` é compatível com Serverless para criar dados didáticos em memória
# MAGIC - `S`, `N` e `NULL` representam tipos de atributos em eventos DynamoDB
# MAGIC - `from_json()` interpreta eventos JSON em formato semiestruturado sem usar `sparkContext`
# MAGIC - `dbfs:/tmp` pode estar bloqueado no Serverless com `DBFS_DISABLED`
# MAGIC - `explode()` abre arrays de objetos, como a lista de itens de uma venda
# MAGIC - CDC/DMS foi simulado com operações `I`, `U` e timestamp de commit
# MAGIC - `row_number()` ajuda a consolidar o estado mais recente de uma entidade no CDC
# MAGIC - Arquivos JSON foram simulados como JSON Lines em memória para evitar dependência de `dbfs:/tmp`
# MAGIC 
# MAGIC ## Tipos de arquivos
# MAGIC - CSV é simples, textual e comum em integrações, mas não preserva schema rico
# MAGIC - JSON é útil para eventos, APIs, logs e objetos aninhados
# MAGIC - Avro é binário, orientado a linhas e comum em streaming/CDC
# MAGIC - Parquet é colunar, comprimido e eficiente para consultas analíticas
# MAGIC - ORC é colunar e comum em ambientes Hive
# MAGIC - Delta Lake usa Parquet com log transacional `_delta_log`
# MAGIC - `write.format(...).save()` grava arquivos em uma pasta
# MAGIC - `write.format("delta").saveAsTable()` grava tabelas Delta gerenciadas no Lakehouse
# MAGIC 
# MAGIC ## Limpeza do ambiente
# MAGIC - `DROP TABLE IF EXISTS` remove tabelas criadas no tutorial
# MAGIC - `DROP SCHEMA IF EXISTS` remove schemas vazios
# MAGIC - A variável `EXECUTAR_LIMPEZA = False` evita apagar objetos por acidente
# MAGIC 
# MAGIC ## Estrutura no Catalog
# MAGIC - O schema `bronze` guarda dados brutos e rastreáveis
# MAGIC - O schema `silver` guarda dados tratados e reutilizáveis
# MAGIC - O schema `gold` guarda tabelas analíticas prontas para consumo
# MAGIC - O menu **Catalog** permite navegar pelas tabelas criadas no Lakehouse
# MAGIC 
