# Parte 3 — Escalando com Docker Compose (≈ 15 min)

**Objetivo:** rodar várias réplicas da API atrás de um balanceador de carga, escalar para cima e para baixo e publicar uma URL pública.
**Conceitos da aula:** réplicas horizontais, load balancing, health checks, auto-scaling e o que Kubernetes automatiza.

> Pré-requisito: a imagem `localhost:5050/churn-api:v1` publicada na Parte 2 (ou o `model.joblib` da Parte 1, para o Compose fazer o build).

```bash
cd Labs_MLOps/Aula04_Deploy_APIs_e_Containers/Parte3_Escala_com_Docker_Compose
```

**1. Suba 3 réplicas + o balanceador (3 min):**
```bash
docker compose up -d
docker compose ps       # aguarde as 3 réplicas da api ficarem (healthy)
```
Leia o `docker-compose.yml` e o `nginx.conf`: o nginx só começa quando as réplicas passam no health check e distribui as requisições entre elas (round-robin).

**2. Veja o balanceamento (2 min):**
```bash
python testar_balanceamento.py
```
Cada réplica tem um hostname diferente; as chamadas se dividem entre as três.

**3. Escale para 5 réplicas (3 min):**
```bash
docker compose up -d --scale api=5
docker compose restart balanceador      # o nginx relê a lista de réplicas
python testar_balanceamento.py
```

**4. Derrube uma réplica e veja o serviço continuar (3 min):**
```bash
docker compose ps
docker stop <nome-de-uma-réplica>
python testar_balanceamento.py
```
O usuário não percebe nada: o balanceador tira a réplica do rodízio e manda as requisições para as outras. Agora rode `docker compose up -d` e depois `docker compose ps`: o Compose volta ao número de réplicas **declarado no arquivo** (`replicas: 3`), e não às 5 do `--scale`. Para manter 5, repita `docker compose up -d --scale api=5`. Num Kubernetes, o Deployment recria a réplica sozinho, sem ninguém rodar comando, e o HPA ajusta a quantidade de réplicas conforme a carga.

**5. URL pública (2 min):** na aba **Ports** do Codespaces, clique com o botão direito na porta 8080 → **Port Visibility → Public**. Abra o endereço em `/docs` e mande para um colega testar.

**6. Desligue tudo:**
```bash
docker compose down
docker rm -f registry
```

## Para discutir
- Aqui você escalou à mão. Que métrica você usaria para escalar automaticamente: CPU, latência p95 ou requisições por segundo?
- Serviços gerenciados de containers (App Runner, Cloud Run, Azure Container Apps) fazem os passos 1 a 5 por você. O que você perde de controle em troca?
