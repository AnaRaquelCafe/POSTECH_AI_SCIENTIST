# Aula 02 · Parte 1 — Entendendo containers (≈ 12 min)

**Objetivo:** usar os comandos essenciais do Docker e sentir na prática a diferença entre imagem, container e registry.
**Conceitos da parte:** o problema que o Docker resolve, imagem (molde imutável) vs container (instância em execução), registry, `pull`/`run`/`ps`/`logs`/`stop`/`rm`.

O Docker já vem instalado no Codespaces. Todos os comandos abaixo rodam em qualquer pasta.

## 1. "Na minha máquina funciona" (3 min)
```bash
python --version
docker run --rm python:3.10-slim python --version
docker run --rm python:3.13-slim python --version
```
O Codespaces tem Python 3.12, mas cada container trouxe **o seu próprio** Python, sem instalar nada na máquina. Na primeira vez o Docker baixa a imagem do **Docker Hub**: esse é o **registry**. Veja as imagens que ficaram guardadas localmente:
```bash
docker images python
```

## 2. Um container rodando em segundo plano (4 min)
```bash
docker run -d --name meu-servidor -p 8000:8000 python:3.12-slim python -m http.server 8000
docker ps
```
Abra a porta 8000 (aba **Ports** do Codespaces): é um servidor web rodando **dentro** do container. Depois:
```bash
docker logs meu-servidor      # o que o processo escreveu na saída
docker stop meu-servidor      # para o container (leva ~10 s, veja a nota abaixo)
docker ps                     # não aparece mais...
docker ps -a                  # ...mas ele ainda existe, parado
docker rm meu-servidor        # agora sim, removido
```
> O `docker stop` pede educadamente para o processo terminar (sinal SIGTERM) e espera 10 segundos antes de forçar. Esse servidor de teste ignora o pedido, por isso a espera.

## 3. O container é descartável; a imagem, imutável (3 min)
```bash
docker run --name teste python:3.12-slim sh -c "echo 'dados importantes' > /nota.txt && cat /nota.txt"
docker run --rm python:3.12-slim cat /nota.txt
```
O segundo comando falha com `No such file or directory`: cada `docker run` cria um container **novo** a partir da mesma imagem, que não foi alterada. O arquivo só existe dentro do primeiro container, que continua parado:
```bash
docker diff teste     # A /nota.txt  →  arquivo adicionado neste container, não na imagem
docker rm teste       # removeu o container, removeu a nota
```
Por isso modelos treinados, logs e bancos de dados não podem morar só dentro do container. Veremos a solução (volumes) na Parte 3.

## 4. Imagens leves (2 min)
```bash
docker pull python:3.12-alpine
docker images python
```
Compare o tamanho das imagens `slim` e `alpine`. Uma máquina virtual com um sistema operacional completo ocuparia gigabytes e levaria minutos para iniciar; os containers compartilham o kernel do hospedeiro e iniciam em segundos.

## Para discutir
- Seu colega treinou um modelo com scikit-learn 1.5 e você tem a 1.8 instalada. Como o Docker resolve esse conflito?
- Se o container é descartável, onde você guardaria o arquivo `.joblib` de um modelo em produção?
