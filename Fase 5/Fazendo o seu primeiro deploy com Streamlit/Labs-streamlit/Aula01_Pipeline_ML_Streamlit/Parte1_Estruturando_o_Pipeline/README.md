# Aula 01 · Parte 1 — Estruturando o pipeline (≈ 12 min)

**Objetivo:** rodar um pipeline de ML organizado em etapas, separar o treino do serving e ver por que salvar o `Pipeline` inteiro facilita a vida.
**Conceitos da parte:** ingestão → pré-processamento → treino → avaliação → serving, código `.py` vs notebook, `Pipeline` do scikit-learn, `joblib.dump`, reprodutibilidade.

```bash
cd Labs-streamlit/Aula01_Pipeline_ML_Streamlit/Parte1_Estruturando_o_Pipeline
```

## 1. Rode o pipeline de treino (3 min)
```bash
python train.py
```
A saída mostra as quatro etapas. Abra o `train.py`: cada etapa é uma função com uma responsabilidade (`ingerir`, `construir_pipeline`, `avaliar`, `serializar`). É isso que diferencia um script de produção de um notebook gigante.

## 2. Faça predições com o artefato (2 min)
```bash
python prever.py --idade 22 --meses 1 --valor 190
python prever.py --idade 70 --meses 60 --valor 30
```
O primeiro cliente (jovem, novo e com mensalidade alta) deve ter probabilidade de churn bem maior que o segundo.

## 3. O que está dentro do artefato? (2 min)
Abra o `prever.py`. Ele não padroniza os dados e nem importa `StandardScaler`, e mesmo assim a predição sai correta. Por quê? Olhe a primeira linha da saída do passo 2: o artefato guarda as etapas `scaler` e `model` juntas.

## 4. Troque o modelo sem mexer no serving (3 min)
Em `construir_pipeline()`, troque o `RandomForestClassifier` pela `LogisticRegression` (a linha já está comentada no código). Depois:
```bash
python train.py
python prever.py --idade 22 --meses 1 --valor 190
```
O F1 muda, o `prever.py` continua funcionando sem nenhuma alteração. Treino e serving estão desacoplados.

## 5. Reprodutibilidade (2 min)
Rode `python train.py` duas vezes: o F1 é idêntico. Agora troque `SEMENTE = 42` por `SEMENTE = None` e rode mais duas vezes. O que acontece? Volte para `42` ao terminar.

## Para discutir
- Se o `scaler` fosse salvo num arquivo e o modelo em outro, o que poderia dar errado no dia do deploy?
- Por que fixar a semente é obrigatório quando você quer comparar dois modelos?
