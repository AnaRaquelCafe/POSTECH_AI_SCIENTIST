# Aula 03 · Lab GitHub — Monitoramento agendado com alerta (≈ 13 min)

**Objetivo:** tirar o monitoramento do "rodo quando lembro" e colocá-lo num job agendado, que guarda o relatório e abre um alerta quando detecta drift.
**Conceitos:** monitoramento contínuo, janela de referência vs. dados recentes, alertas acionáveis, jobs agendados (cron).

Na Parte 3 você rodou o `monitorar.py` à mão. Em produção, ninguém deve precisar lembrar de rodar: um agendador executa o monitoramento, e um humano só é chamado quando há algo a fazer. Aqui o agendador é o GitHub Actions, e o alerta é uma **issue** no seu repositório.

```bash
cd Labs-streamlit/Aula03_Monitoramento_Drift/Lab_GitHub_Monitoramento_Agendado
```

## 1. Rode o job localmente (3 min)
```bash
python monitorar_semana.py
DESLOCAMENTO_IDADE=8 python monitorar_semana.py
```
Na primeira execução as três features ficam `ok`; na segunda, a `idade` passa do limiar e o resultado vira "drift detectado". O script também gera `relatorio_drift.html` (Evidently) e `resumo.md`, o texto que vai no alerta.

## 2. Agende no GitHub (3 min)
Leia o `monitoramento.yml`: roda toda segunda às 8h (Brasília) e também sob demanda; guarda o relatório como artefato; abre uma issue se houver drift.
```bash
cd "$(git rev-parse --show-toplevel)"
mkdir -p .github/workflows
cp Labs-streamlit/Aula03_Monitoramento_Drift/Lab_GitHub_Monitoramento_Agendado/monitoramento.yml .github/workflows/
git add .github/workflows/monitoramento.yml
git commit -m "Monitoramento de drift agendado"
git push
```

## 3. Uma semana normal (3 min)
Na aba **Actions** → **Monitoramento de drift** → **Run workflow**, deixe o deslocamento em `0` e rode. Abra o run: o **Summary** mostra a tabela de PSI, e em **Artifacts** está o `relatorio-drift` para baixar. Nenhuma issue foi aberta.

## 4. Uma semana com drift (4 min)
Rode de novo com o deslocamento `8`. Agora o job abre uma issue **"Drift detectado"** com a tabela de PSI. Abra a aba **Issues**: é ela que chegaria por e-mail para o time. Baixe o artefato e abra o relatório do Evidently para ver a distribuição da idade.

## Para discutir
- Esse job roda toda segunda e "vê" uma semana de dados. Se o drift acontecer na terça, quando você fica sabendo? Qual seria a frequência certa para o seu negócio?
- Abrir uma issue por semana com drift pode virar ruído. Como combinar com a política de "N alertas seguidos" da Parte 3?

> Workflows agendados rodam só no branch principal e o GitHub os desliga depois de 60 dias sem atividade no repositório.
