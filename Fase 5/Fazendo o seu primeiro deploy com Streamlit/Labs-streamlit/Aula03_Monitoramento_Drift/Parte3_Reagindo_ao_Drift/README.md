# Aula 03 · Parte 3 — Reagindo ao drift (≈ 13 min)

**Objetivo:** transformar a medição de drift em ação: alertas sem ruído, gatilho de re-treino e um relatório visual com o Evidently.
**Conceitos da parte:** alertas acionáveis, gatilhos de re-treino, atualização da janela de referência, ferramentas de ML observability (Evidently AI).

```bash
cd Labs-streamlit/Aula03_Monitoramento_Drift/Parte3_Reagindo_ao_Drift
```

## 1. Doze semanas de monitoramento (4 min)
```bash
python monitorar.py
```
Toda semana, o script calcula o PSI de cada feature contra a referência. A política padrão é: alerta se o PSI ≥ 0,2; re-treino após **2 alertas seguidos**. Leia a tabela e responda:
- Na semana 3 houve uma campanha pontual para universitários. Ela gerou alerta? Disparou re-treino?
- A partir da semana 6, a base de clientes começa a envelhecer. Em que semana o re-treino foi disparado?
- Depois do re-treino, os dados recentes viram a nova referência. O que aconteceu com o PSI na semana seguinte?

## 2. Ajuste a política de alertas (4 min)
No topo do `monitorar.py`, teste uma alteração por vez (volte ao padrão entre os testes):

| Alteração | Quantos re-treinos? | O que deu errado ou certo? |
|---|---|---|
| padrão (`0.2` e `2`) | | |
| `SEMANAS_SEGUIDAS_PARA_RETREINO = 1` | | |
| `LIMIAR_ALERTA = 0.1` | | |

Dica para a segunda linha: olhe a semana 4. O modelo foi re-treinado com os dados da campanha, que não representavam o público de verdade.

## 3. O relatório do Evidently (5 min)
Cada execução gera `relatorio_drift.html`, que compara a pior semana com os dados de treino. Para abrir no Codespaces:
```bash
python -m http.server 8000
```
Abra a porta 8000 e clique em `relatorio_drift.html`. O Evidently deve apontar drift em 1 de 3 colunas, a `idade`, a mesma conclusão do nosso PSI feito à mão, embora ele use outro teste (a distância de Wasserstein). Expanda a linha da `idade` e compare as duas distribuições. Pare o servidor com Ctrl+C.

## Lab GitHub
A pasta [`Lab_GitHub_Monitoramento_Agendado`](../Lab_GitHub_Monitoramento_Agendado/) transforma este monitoramento num job agendado do GitHub Actions: toda semana ele calcula o drift, guarda o relatório do Evidently e abre uma issue quando há alerta.

## Para discutir
- Um alerta que dispara toda semana acaba sendo ignorado. Como você equilibraria sensibilidade e ruído?
- Re-treinar automaticamente é sempre seguro? Que verificação você faria antes de colocar o modelo re-treinado em produção?
