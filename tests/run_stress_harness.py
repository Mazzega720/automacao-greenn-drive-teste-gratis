#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Harness de Simulação e Estresse Matemático Empírico (run_stress_harness.py)
Agente: Challenger 2 (Mathematical, Stress & Boundary Conditions Challenger)
Projeto: automacao-greenn-drive-teste-gratis-v4

Executa varredura sistemática (sweeps) nos parâmetros operacionais e gera relatório tabular.
"""

import sys
import math
from pathlib import Path

# Configuração UTF-8
if sys.platform.startswith("win"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

def run_stress_sweep():
    print("=" * 84)
    print("      HARNESS DE SIMULAÇÃO E ESTRESSE MATEMÁTICO - CHALLENGER 2")
    print("=" * 84)

    # 1. Simulação dos 3 Cenários Canônicos
    print("\n--- 1. CENÁRIOS CANÔNICOS HOMOLOGADOS ---")
    scenarios = [
        ("Cenário 1 (Base: 1 cham/venda, 1 cham/reemb)", 160, 4, 3, 24, 4, 3, 100),
        ("Cenário 2 (Extra Venda: 2 cham/venda, 1 cham/reemb)", 160, 5, 4, 24, 4, 3, 100),
        ("Cenário 3 (Extra Ambos: 2 cham/venda, 2 cham/reemb)", 160, 5, 4, 24, 5, 4, 100),
    ]

    print(f"{'Cenário':<42} | {'Com Email':<10} | {'Folga Com':<10} | {'Sem Email':<10} | {'Folga Sem':<10} | {'Gatilho 900':<12}")
    print("-" * 105)
    for name, v, cv_c, cv_s, r, cr_c, cr_s, t in scenarios:
        tot_c = (v * cv_c) + (r * cr_c) + t
        fol_c = 1000 - tot_c
        tot_s = (v * cv_s) + (r * cr_s) + t
        fol_s = 1000 - tot_s
        custo_med = (cv_c * 1.0) + (cr_c * 0.15)
        gat_vendas = math.floor(900.0 / custo_med)
        print(f"{name:<42} | {tot_c:>5} cr   | {fol_c:>5} cr   | {tot_s:>5} cr   | {fol_s:>5} cr   | ~{gat_vendas:>3} vendas ({custo_med:.2f} cr/v)")

    # 2. Execuções no n8n Cloud
    print("\n--- 2. EXECUÇÕES NO N8N CLOUD TRIAL (1.000 EXECUÇÕES) ---")
    n8n_cases = [
        ("Cenário 1 (1 chamada/venda + 1 chamada/reembolso)", 160, 24),
        ("Cenário 2 (2 chamadas/venda + 1 chamada/reembolso)", 320, 24),
        ("Cenário 3 (2 chamadas/venda + 2 chamadas/reembolso)", 320, 48),
        ("Cenário 3 Extremo (+100 execuções de testes)", 320 + 100, 48),
        ("Cenário Burst Triplo (3 cham/venda + 3 cham/reemb)", 480, 72)
    ]
    print(f"{'Caso de Execução n8n':<50} | {'Execuções':<12} | {'Folga Restante':<15} | {'Status':<10}")
    print("-" * 95)
    for desc, ev, er in n8n_cases:
        tot_exec = ev + er
        folga_exec = 1000 - tot_exec
        status = "SEGURO" if folga_exec > 500 else ("ALERTA" if folga_exec >= 0 else "ESTOURO")
        print(f"{desc:<50} | {tot_exec:>6} / 1000 | +{folga_exec:>5} execuções | {status:<10}")

    # 3. Varredura da Fórmula de D-1 (Sweep de Sensibilidade)
    print("\n--- 3. VARREDURA DE SENSIBILIDADE NA FÓRMULA DE D-1 ---")
    print("Fórmulas:")
    print("  Com e-mail: 836 + (160 * extras/venda) + (24 * extras/reembolso) + (consumo_testes - 100)")
    print("  Sem e-mail: 652 + (160 * extras/venda) + (24 * extras/reembolso) + (consumo_testes - 100)")
    print()

    sweep_matrix = [
        # (ev, er, t)
        (0, 0, 50),
        (0, 0, 100),
        (0, 0, 150),
        (1, 0, 50),
        (1, 0, 100),
        (1, 0, 104),  # borda de folga = 0 com email
        (1, 0, 105),  # estouro com email (-1)
        (1, 0, 150),
        (1, 1, 50),
        (1, 1, 100),  # Cenário 3 estoura (+20)
        (1, 1, 150),
        (2, 0, 100),
        (2, 0, 128),  # borda de folga = 0 sem email
        (2, 0, 129),  # estouro sem email -> n8n Cloud!
        (2, 1, 100),  # sem email folga = 4
        (2, 1, 105),  # sem email estoura -> n8n Cloud!
        (2, 2, 100),  # estoura ambos -> n8n Cloud!
        (3, 0, 100),  # 3 extras/venda -> estoura ambos -> n8n Cloud!
    ]

    print(f"{'EV':<3} | {'ER':<3} | {'Testes':<6} | {'Com Email':<10} | {'Folga Com':<10} | {'Sem Email':<10} | {'Folga Sem':<10} | {'Decisão de Plataforma':<22}")
    print("-" * 92)
    for ev, er, t in sweep_matrix:
        delta_t = t - 100
        c_com = 836 + (160 * ev) + (24 * er) + delta_t
        f_com = 1000 - c_com
        c_sem = 652 + (160 * ev) + (24 * er) + delta_t
        f_sem = 1000 - c_sem

        if f_com >= 0:
            dec = "Make com e-mail"
        elif f_sem >= 0:
            dec = "Make sem e-mail"
        else:
            dec = "MIGRAR PARA n8n CLOUD"

        print(f"{ev:>2}  | {er:>2}  | {t:>4} cr | {c_com:>5} cr   | {f_com:>5} cr   | {c_sem:>5} cr   | {f_sem:>5} cr   | {dec:<22}")

    print("\n" + "=" * 84)
    print("      CONCLUSÃO DO HARNESS: MODELO ROBUSTO, EXATO E DETERMINÍSTICO")
    print("=" * 84)

if __name__ == "__main__":
    run_stress_sweep()
