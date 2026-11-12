# Aula 01 · Parte 2 — Construindo a interface com Streamlit (≈ 13 min)

**Objetivo:** rodar um app de predição em Streamlit e ver, na prática, a execução reativa e o efeito do cache.
**Conceitos da parte:** execução reativa (o script roda inteiro a cada interação), widgets de entrada, `st.metric`, `@st.cache_resource`.

O modelo (`modelo_churn.joblib`) já vem pronto; é o mesmo tipo de artefato gerado na Parte 1.

```bash
cd Labs-streamlit/Aula01_Pipeline_ML_Streamlit/Parte2_Interface_Streamlit
```

## 1. Rode o app (2 min)
```bash
streamlit run app.py
```
O Codespaces abre a porta 8501 no navegador. Teste um cliente jovem, com 1 mês de casa e mensalidade alta: deve aparecer como risco.

## 2. Execução reativa (3 min)
Mova o slider de idade algumas vezes e observe:
- na barra lateral, o contador **Execuções do script** sobe a cada interação: o Streamlit roda o `app.py` inteiro de novo, do início ao fim;
- no terminal, a mensagem `Carregando o modelo do disco...` apareceu **uma única vez**.

## 3. E sem cache? (3 min)
No `app.py`, comente a linha do `@st.cache_resource`, salve e clique em **Rerun** no canto superior direito do app. Mova o slider de novo: agora cada interação demora 2 segundos e o terminal mostra o modelo sendo recarregado toda vez. Descomente a linha ao terminar.

> `@st.cache_resource` serve para recursos compartilhados (modelos, conexões). Para funções que retornam dados, como ler um CSV, use `@st.cache_data`.

## 4. Limiar de decisão ajustável (3 min)
Troque a linha `limiar = 0.5` (marcada com `TODO`) por um slider:
```python
limiar = st.slider("Limiar de risco", 0.1, 0.9, 0.5)
```
Salve, clique em **Rerun**, faça uma predição e mova o limiar. O mesmo cliente muda de "baixo risco" para "em risco" sem o modelo mudar: o limiar é uma decisão de negócio, não do modelo.

## 5. Desafio extra: predição em lote (2 min, se sobrar tempo)
Cole no final do `app.py`:
```python
st.divider()
st.subheader("Predição em lote")
arquivo = st.file_uploader("CSV com as colunas idade, meses e valor_mensal", type="csv")
if arquivo is not None:
    lote = pd.read_csv(arquivo)
    lote["prob_churn"] = model.predict_proba(lote[["idade", "meses", "valor_mensal"]])[:, 1]
    lote["em_risco"] = lote["prob_churn"] > limiar
    st.dataframe(lote)
    st.download_button("Baixar resultado", lote.to_csv(index=False), "predicoes.csv")
```
Para testar, baixe o `clientes_exemplo.csv` desta pasta (no Explorer do Codespaces: botão direito → **Download**) e envie pelo app.

Ao terminar, pare o app com Ctrl+C no terminal.

## Para discutir
- Se o script roda inteiro a cada clique, o que acontece com um app que consulta um banco de dados lento sem cache?
- Por que o resultado da predição some quando você mexe no slider depois de clicar em **Prever**?
