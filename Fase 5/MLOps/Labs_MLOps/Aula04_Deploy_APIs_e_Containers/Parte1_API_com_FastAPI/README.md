# Parte 1 — API de predição com FastAPI (≈ 12 min)

**Objetivo:** servir o modelo de churn como uma API HTTP com validação de entrada e documentação automática.
**Conceitos da aula:** batch vs real-time, FastAPI, Pydantic, carregar o modelo uma vez na inicialização, `/health`.

```bash
cd Labs_MLOps/Aula04_Deploy_APIs_e_Containers/Parte1_API_com_FastAPI
python treinar_modelo_exemplo.py
uvicorn main:app --reload --port 8000
```

**1. Abra a porta 8000 e acrescente `/docs` ao endereço.** A interface Swagger foi gerada sozinha a partir do código.

**2. Teste o `POST /predict`** (Try it out) com:
```json
{"idade": 23, "meses": 2, "valor_mensal": 210, "chamados_suporte": 4}
```
Depois troque para um cliente antigo e tranquilo (`"meses": 60, "chamados_suporte": 0`) e compare a probabilidade.

**3. Mande um dado inválido:** `"idade": 12` ou `"meses": "dois"`. O Pydantic devolve **422** explicando o erro, e o modelo nem chega a ser chamado.

**4. Teste o `GET /health`:** deve responder `"model_loaded": true`. É esse endpoint que o Docker (Parte 2) e o balanceador (Parte 3) usam para saber se o serviço está saudável.

**5.** Ctrl+C para parar a API.

## Para discutir
- Por que carregar o modelo no `lifespan` e não dentro do `predict`?
- O desafio da disciplina pede também um scoring **batch** semanal. Você usaria esta API para isso? Por quê?
