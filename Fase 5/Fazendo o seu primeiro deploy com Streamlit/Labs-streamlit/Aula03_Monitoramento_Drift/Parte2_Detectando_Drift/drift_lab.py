"""Aula 03 · Parte 2 — Detectando drift: PSI, Kolmogorov-Smirnov e qui-quadrado.

Janela de referência = dados parecidos com os de treino.
Janela de análise    = dados "de produção", que você vai deslocar.

    python drift_lab.py
"""
import numpy as np
import pandas as pd
from scipy.stats import chi2_contingency, ks_2samp

# ---------------------------------------------------------------------------
# EXERCÍCIO: altere estes valores e rode de novo.
#   Tudo no valor padrão -> produção igual ao treino (não deve haver drift).
# ---------------------------------------------------------------------------
DESLOCAMENTO_IDADE = 0       # anos somados à idade dos clientes em produção
FATOR_VALOR_MENSAL = 1.0     # 1.2 = mensalidades 20% mais altas
PROPORCAO_PREMIUM = 0.15     # fração de clientes no plano premium (no treino: 0.15)
TAMANHO_ANALISE = 1500       # quantos clientes de produção entram na janela de análise

rng = np.random.default_rng(7)


def gerar(n, desloc_idade=0, fator_valor=1.0, prop_premium=0.15):
    prop_basico = (1 - prop_premium) * 0.6
    return pd.DataFrame({
        "idade": np.clip(rng.normal(45, 14, n) + desloc_idade, 18, 90).round(),
        "valor_mensal": (rng.uniform(20, 200, n) * fator_valor).round(2),
        "plano": rng.choice(["basico", "padrao", "premium"], n,
                            p=[prop_basico, 1 - prop_basico - prop_premium, prop_premium]),
    })


referencia = gerar(5000)
analise = gerar(TAMANHO_ANALISE, DESLOCAMENTO_IDADE, FATOR_VALOR_MENSAL, PROPORCAO_PREMIUM)


def psi(ref, atual, bins=10):
    """Population Stability Index com faixas definidas pelos quantis da referência."""
    cortes = np.unique(np.quantile(ref, np.linspace(0, 1, bins + 1)))
    cortes[0], cortes[-1] = -np.inf, np.inf
    p_ref = np.histogram(ref, cortes)[0] / len(ref)
    p_atual = np.histogram(atual, cortes)[0] / len(atual)
    p_ref = np.clip(p_ref, 1e-6, None)        # evita log(0)
    p_atual = np.clip(p_atual, 1e-6, None)
    return float(np.sum((p_atual - p_ref) * np.log(p_atual / p_ref)))


def classificar(valor):
    if valor < 0.1:
        return "estável"
    if valor < 0.2:
        return "drift moderado (atenção)"
    return "drift significativo (ação necessária)"


print(f"Referência: {len(referencia)} clientes | Análise: {len(analise)} clientes\n")
print("Features numéricas")
print(f"{'feature':<14}{'PSI':>8}  {'KS p-valor':>11}  diagnóstico (PSI)")
print("-" * 70)
for col in ["idade", "valor_mensal"]:
    v_psi = psi(referencia[col], analise[col])
    p_ks = ks_2samp(referencia[col], analise[col]).pvalue
    print(f"{col:<14}{v_psi:>8.3f}  {p_ks:>11.4f}  {classificar(v_psi)}")

print("\nFeature categórica")
contagens = pd.DataFrame({
    "referência": referencia["plano"].value_counts(),
    "análise": analise["plano"].value_counts(),
}).fillna(0)
p_chi2 = chi2_contingency(contagens).pvalue
print(f"{'plano':<14}{'referência':>11}{'análise':>10}")
print("-" * 35)
for plano, linha in (contagens / contagens.sum()).iterrows():
    print(f"{plano:<14}{linha['referência']:>11.0%}{linha['análise']:>10.0%}")
print(f"qui-quadrado p-valor: {p_chi2:.4f}")

print("\nKS e qui-quadrado: p-valor < 0,05 indica que as distribuições são estatisticamente diferentes.")
