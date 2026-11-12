# Aula 04 · Parte 3 — DVC para dados e pipelines (≈ 15 min)

**Objetivo:** versionar o dataset com DVC, treinar com um pipeline reprodutível (`dvc.yaml`) e voltar no tempo para dados **e** modelo de uma versão anterior.
**Conceitos da parte:** ponteiros `.dvc`, armazenamento remoto, `dvc.yaml` e `dvc repro`, métricas versionadas, o fluxo integrado Git + DVC.

```bash
cd Labs-streamlit/Aula04_Versionamento_MLflow_DVC/Parte3_DVC_para_Dados_e_Pipelines
```

## 1. Inicialize o DVC e configure um remote (2 min)
O remote aqui é uma pasta local; na empresa seria um storage de objetos na nuvem, e só a URL muda.
```bash
python gerar_dados.py --versao 1
dvc init --subdir
dvc remote add -d local ~/dvc-remote
git add .dvc .dvcignore && git commit -m "Inicializa DVC"
```

## 2. Versione os dados (2 min)
```bash
dvc add dados/clientes.csv
cat dados/clientes.csv.dvc
```
O Git vai guardar só esse ponteiro, com o `md5` do arquivo. O CSV em si fica no cache do DVC e depois vai para o remote.

## 3. Treine com o pipeline (3 min)
Leia o `dvc.yaml`: um estágio `treinar` que depende dos dados e do `treinar.py` e produz o modelo e as métricas.
```bash
dvc repro
dvc repro
dvc metrics show
```
O segundo `dvc repro` não treina de novo: nada mudou, então ele pula o estágio. Registre essa versão:
```bash
git add dados/clientes.csv.dvc dvc.lock metricas.json .gitignore
git commit -m "Dados v1 + modelo v1"
dvc push
```

## 4. Os dados mudaram (3 min)
```bash
python gerar_dados.py --versao 2
dvc status
dvc add dados/clientes.csv
dvc repro
dvc metrics diff
```
O `dvc status` percebeu a mudança, o `dvc repro` retreinou sozinho e o `dvc metrics diff` compara as métricas com a versão anterior. Registre:
```bash
git add dados/clientes.csv.dvc dvc.lock metricas.json
git commit -m "Dados v2 + modelo v2"
dvc push
```

## 5. Volte no tempo (3 min)
```bash
git checkout HEAD~1 -- dados/clientes.csv.dvc dvc.lock metricas.json
dvc checkout
wc -l dados/clientes.csv      # 2001 linhas: os dados v1 voltaram
dvc metrics show              # e as métricas do modelo v1 também
```
O `dvc checkout` trouxe de volta o dataset **e** o `modelo.joblib` da v1. Para retornar à v2:
```bash
git checkout HEAD -- dados/clientes.csv.dvc dvc.lock metricas.json
dvc checkout
```

## 6. Extra: recupere do remote (2 min)
```bash
rm dados/clientes.csv modelo.joblib
dvc pull
```
Os dois arquivos voltam do remote. Numa máquina nova, `git clone` + `dvc pull` recupera tudo.

> **Rodando o lab de novo?** Se o `dvc init` disser que o DVC já foi inicializado, pule o passo 1 (só gere os dados com `python gerar_dados.py --versao 1`).

## Lab GitHub
A pasta [`Lab_GitHub_DVC_no_CI`](../Lab_GitHub_DVC_no_CI/) roda o pipeline DVC no GitHub Actions a cada pull request e comenta no PR a diferença de métricas em relação ao `main`.

## Para discutir
- Reproduzir um resultado de meses atrás = `git checkout` + `dvc pull` + `dvc repro`. O que cada um dos três comandos recupera?
- Se o `treinar.py` registrasse cada execução no MLflow (Parte 2), que informação a tag `versao_dados_md5` ligaria entre as duas ferramentas?
