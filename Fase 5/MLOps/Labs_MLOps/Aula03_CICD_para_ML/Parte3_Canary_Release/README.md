# Parte 3 — Canary release (≈ 15 min)

**Objetivo:** colocar um modelo novo no ar recebendo só uma fração do tráfego e aumentar essa fração aos poucos, com rollback imediato.
**Conceitos da aula:** blue-green, canary e shadow mode; exposição gradual e risco controlado.

```bash
cd Labs_MLOps/Aula03_CICD_para_ML/Parte3_Canary_Release
```

**1. Prepare as duas variantes (2 min):**
```bash
python preparar_variantes.py
```
Usa o `@champion` que você promoveu na Aula 02 (ou cria um) e registra uma versão nova como `@challenger`.

**2. Suba o endpoint com as duas variantes** (este terminal fica ocupado):
```bash
uvicorn roteador:app --port 8000
```
Ele começa com 90% do tráfego para o Principal (`@champion`) e 10% para o Canário (`@challenger`). Na porta 8000, em `/docs`, dá para testar o `/predict` pelo navegador.

**3. Em outro terminal, gere tráfego e observe a divisão (3 min):**
```bash
cd Labs_MLOps/Aula03_CICD_para_ML/Parte3_Canary_Release
python invocar_varias_vezes.py
```

**4. Avance o canário (5 min):** o endpoint continua no ar enquanto os pesos mudam.
```bash
python ajustar_pesos.py 50 50
python invocar_varias_vezes.py
python ajustar_pesos.py 0 100
python invocar_varias_vezes.py
```
Imagine que as métricas do canário pioraram: `python ajustar_pesos.py 100 0` é o rollback.

**5.** Ctrl+C no primeiro terminal para derrubar o endpoint.

## Para discutir
- Em que momento você decidiria avançar de 10% para 50%? Que métricas olharia, e por quanto tempo?
- Como seria um **shadow mode** neste roteador? (O canário recebe 100% das requisições, mas a resposta dele não volta para o usuário.)
