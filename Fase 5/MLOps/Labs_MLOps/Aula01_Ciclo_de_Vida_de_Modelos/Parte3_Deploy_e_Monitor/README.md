# Parte 3 — Deploy e monitoramento (≈ 15 min)

**Objetivo:** colocar a versão aprovada no ar como um endpoint real-time, gravar o que chega em produção (data capture) e comparar com os dados de treino.
**Conceitos da aula:** deploy real-time, data capture, data drift, monitoramento contínuo e o gatilho de re-treino.

> Pré-requisito: uma versão do `churn-model` aprovada na Parte 2.

```bash
cd Labs_MLOps/Aula01_Ciclo_de_Vida_de_Modelos/Parte3_Deploy_e_Monitor
```

**1. Faça o deploy do endpoint** (este terminal fica ocupado com o servidor):
```bash
python deploy_endpoint.py
```
Espere aparecer `Uvicorn running on http://127.0.0.1:5001`. O script escolhe sozinho a última versão com `aprovacao=Approved`.

**2. Em outro terminal, invoque o endpoint:**
```bash
cd Labs_MLOps/Aula01_Ciclo_de_Vida_de_Modelos/Parte3_Deploy_e_Monitor
python invocar_endpoint.py
```

**3. Simule um dia de produção em que o perfil dos clientes mudou e monitore:**
```bash
python simular_producao.py --drift
python monitorar.py
python -m http.server 8000
```
Abra a porta 8000 e clique em `relatorio_monitoramento.html`. Quais colunas o Evidently marcou com drift? A taxa de churn prevista mudou?

> Se sobrar tempo: rode `simular_producao.py` sem `--drift` e `monitorar.py` de novo. Sem mudança no perfil, o relatório não deve acusar drift.

**4. Derrube o endpoint:** Ctrl+C no primeiro terminal. Na nuvem, esquecer um endpoint ligado custa dinheiro todo mês.

## Para discutir
- O relatório mostra drift, mas ainda não sabemos se os clientes realmente cancelaram (o ground truth chega 30 dias depois). Você re-treinaria agora ou esperaria?
- Na nuvem, o que corresponde a cada peça deste lab? (endpoint gerenciado, data capture num bucket, job de monitoramento agendado)
