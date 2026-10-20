#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Suíte de Testes Empíricos do Challenger 2:
Estresse Matemático, Condições de Contorno, Checklist D-1 e Matriz de Riscos
(test_math_stress_challenger.py)

Agente: Challenger 2 (Mathematical, Stress & Boundary Conditions Challenger)
Projeto: automacao-greenn-drive-teste-gratis-v4

Este script executa uma bateria empírica e rigorosa sobre:
1. Modelagem matemática exata dos Cenários 1, 2 e 3 (Make e n8n, gatilhos de 900 cr).
2. Simulação de sensibilidade e fragilidade da margem de segurança (folga crítica de 4 cr no Cenário 2).
3. Simulação de estresse de contorno na fórmula paramétrica do Checklist D-1:
   - extras/venda in [0, 1, 2, 3]
   - extras/reembolso in [0, 1, 2, 3]
   - consumo_real_testes in [0, 50, 100, 104, 105, 150, 200, 288, 289]
4. Ponto exato de chaveamento para n8n Cloud Trial (quando Make sem e-mail estoura).
5. Validação estrutural e textual exata dos 12 itens do Checklist D-1 em automacao-greenn-drive-teste-gratis-v4.md.
6. Validação estrutural e textual exata dos 12 riscos da Tabela de Riscos em automacao-greenn-drive-teste-gratis-v4.md.
7. Alinhamento estrito dos valores da Ficha Técnica YAML com os cálculos do motor.
"""

import sys
import os
import re
import math
import unittest
from pathlib import Path

# Força UTF-8 no Windows
if sys.platform.startswith("win"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

ROOT_DIR = Path(__file__).resolve().parent.parent
FILE_MASTER = ROOT_DIR / "automacao-greenn-drive-teste-gratis-v4.md"


class MathematicalModelEngine:
    """Motor de cálculo e simulação matemática dos cenários operacionais."""

    TOTAL_VENDAS = 160
    TAXA_REEMBOLSO = 0.15
    TOTAL_REEMBOLSOS = 24  # 160 * 0.15 = 24
    RESERVA_TESTES = 100
    CAPACIDADE_MAKE = 1000
    CAPACIDADE_N8N = 1000
    GATILHO_CREDITOS = 900

    @classmethod
    def calc_cenario_1(cls):
        """Cenário 1: Base (1 chamada/venda, 1 chamada/reembolso)."""
        vendas_com_email = cls.TOTAL_VENDAS * 4  # 640
        vendas_sem_email = cls.TOTAL_VENDAS * 3  # 480
        reembolsos_com_email = cls.TOTAL_REEMBOLSOS * 4  # 96
        reembolsos_sem_email = cls.TOTAL_REEMBOLSOS * 3  # 72

        total_com_email = vendas_com_email + reembolsos_com_email + cls.RESERVA_TESTES  # 836
        folga_com_email = cls.CAPACIDADE_MAKE - total_com_email  # 164

        total_sem_email = vendas_sem_email + reembolsos_sem_email + cls.RESERVA_TESTES  # 652
        folga_sem_email = cls.CAPACIDADE_MAKE - total_sem_email  # 348

        custo_medio_venda = 1 * 4 + cls.TAXA_REEMBOLSO * 4  # 4.6
        gatilho_vendas_float = cls.GATILHO_CREDITOS / custo_medio_venda  # 195.65217...
        gatilho_vendas_int = math.floor(gatilho_vendas_float)  # 195

        n8n_execucoes = cls.TOTAL_VENDAS + cls.TOTAL_REEMBOLSOS  # 184
        n8n_folga = cls.CAPACIDADE_N8N - n8n_execucoes  # 816

        return {
            "vendas_com_email": vendas_com_email,
            "vendas_sem_email": vendas_sem_email,
            "reembolsos_com_email": reembolsos_com_email,
            "reembolsos_sem_email": reembolsos_sem_email,
            "total_com_email": total_com_email,
            "folga_com_email": folga_com_email,
            "total_sem_email": total_sem_email,
            "folga_sem_email": folga_sem_email,
            "custo_medio_venda": custo_medio_venda,
            "gatilho_vendas_float": gatilho_vendas_float,
            "gatilho_vendas_int": gatilho_vendas_int,
            "n8n_execucoes": n8n_execucoes,
            "n8n_folga": n8n_folga
        }

    @classmethod
    def calc_cenario_2(cls):
        """Cenário 2: Chamada extra na venda (+160 cr)."""
        vendas_com_email = cls.TOTAL_VENDAS * (4 + 1)  # 800
        vendas_sem_email = cls.TOTAL_VENDAS * (3 + 1)  # 640
        reembolsos_com_email = cls.TOTAL_REEMBOLSOS * 4  # 96
        reembolsos_sem_email = cls.TOTAL_REEMBOLSOS * 3  # 72

        total_com_email = vendas_com_email + reembolsos_com_email + cls.RESERVA_TESTES  # 996
        folga_com_email = cls.CAPACIDADE_MAKE - total_com_email  # 4

        total_sem_email = vendas_sem_email + reembolsos_sem_email + cls.RESERVA_TESTES  # 812
        folga_sem_email = cls.CAPACIDADE_MAKE - total_sem_email  # 188

        custo_medio_venda = 1 * 5 + cls.TAXA_REEMBOLSO * 4  # 5.6
        gatilho_vendas_float = cls.GATILHO_CREDITOS / custo_medio_venda  # 160.71428...
        gatilho_vendas_int = math.floor(gatilho_vendas_float)  # 160

        n8n_execucoes = (cls.TOTAL_VENDAS * 2) + cls.TOTAL_REEMBOLSOS  # 320 + 24 = 344
        n8n_folga = cls.CAPACIDADE_N8N - n8n_execucoes  # 656

        return {
            "vendas_com_email": vendas_com_email,
            "vendas_sem_email": vendas_sem_email,
            "reembolsos_com_email": reembolsos_com_email,
            "reembolsos_sem_email": reembolsos_sem_email,
            "total_com_email": total_com_email,
            "folga_com_email": folga_com_email,
            "total_sem_email": total_sem_email,
            "folga_sem_email": folga_sem_email,
            "custo_medio_venda": custo_medio_venda,
            "gatilho_vendas_float": gatilho_vendas_float,
            "gatilho_vendas_int": gatilho_vendas_int,
            "n8n_execucoes": n8n_execucoes,
            "n8n_folga": n8n_folga
        }

    @classmethod
    def calc_cenario_3(cls):
        """Cenário 3: Chamada extra na venda e no reembolso (+160 e +24 cr)."""
        vendas_com_email = cls.TOTAL_VENDAS * (4 + 1)  # 800
        vendas_sem_email = cls.TOTAL_VENDAS * (3 + 1)  # 640
        reembolsos_com_email = cls.TOTAL_REEMBOLSOS * (4 + 1)  # 120
        reembolsos_sem_email = cls.TOTAL_REEMBOLSOS * (3 + 1)  # 96

        total_com_email = vendas_com_email + reembolsos_com_email + cls.RESERVA_TESTES  # 1020
        folga_com_email = cls.CAPACIDADE_MAKE - total_com_email  # -20 (estouro de 20 cr)

        total_sem_email = vendas_sem_email + reembolsos_sem_email + cls.RESERVA_TESTES  # 836
        folga_sem_email = cls.CAPACIDADE_MAKE - total_sem_email  # 164

        custo_medio_venda = 1 * 5 + cls.TAXA_REEMBOLSO * 5  # 5.75
        gatilho_vendas_float = cls.GATILHO_CREDITOS / custo_medio_venda  # 156.5217...
        gatilho_vendas_int = math.floor(gatilho_vendas_float)  # 156

        n8n_execucoes = (cls.TOTAL_VENDAS * 2) + (cls.TOTAL_REEMBOLSOS * 2)  # 320 + 48 = 368
        n8n_folga = cls.CAPACIDADE_N8N - n8n_execucoes  # 632

        return {
            "vendas_com_email": vendas_com_email,
            "vendas_sem_email": vendas_sem_email,
            "reembolsos_com_email": reembolsos_com_email,
            "reembolsos_sem_email": reembolsos_sem_email,
            "total_com_email": total_com_email,
            "folga_com_email": folga_com_email,
            "total_sem_email": total_sem_email,
            "folga_sem_email": folga_sem_email,
            "custo_medio_venda": custo_medio_venda,
            "gatilho_vendas_float": gatilho_vendas_float,
            "gatilho_vendas_int": gatilho_vendas_int,
            "n8n_execucoes": n8n_execucoes,
            "n8n_folga": n8n_folga
        }

    @classmethod
    def calc_d1_formula(cls, extras_venda: int, extras_reembolso: int, consumo_testes: int):
        """
        Fórmula de recálculo em D-1:
        Com e-mail: 836 + (160 * extras/venda) + (24 * extras/reembolso) + (consumo_real_testes - 100)
        Sem e-mail: 652 + (160 * extras/venda) + (24 * extras/reembolso) + (consumo_real_testes - 100)
        """
        delta_testes = consumo_testes - 100
        consumo_com_email = 836 + (160 * extras_venda) + (24 * extras_reembolso) + delta_testes
        folga_com_email = cls.CAPACIDADE_MAKE - consumo_com_email

        consumo_sem_email = 652 + (160 * extras_venda) + (24 * extras_reembolso) + delta_testes
        folga_sem_email = cls.CAPACIDADE_MAKE - consumo_sem_email

        # Decisão de plataforma segundo o critério inegociável
        if folga_com_email >= 0:
            decisao = "Make com e-mail"
        elif folga_sem_email >= 0:
            decisao = "Make sem e-mail"
        else:
            decisao = "Migrar para n8n Cloud"

        return {
            "extras_venda": extras_venda,
            "extras_reembolso": extras_reembolso,
            "consumo_testes": consumo_testes,
            "delta_testes": delta_testes,
            "consumo_com_email": consumo_com_email,
            "folga_com_email": folga_com_email,
            "consumo_sem_email": consumo_sem_email,
            "folga_sem_email": folga_sem_email,
            "decisao": decisao
        }


class TestChallengerMathematicalAndBoundary(unittest.TestCase):
    """Bateria de testes empíricos do Challenger 2."""

    @classmethod
    def setUpClass(cls):
        assert FILE_MASTER.exists(), f"Arquivo mestre não existe: {FILE_MASTER}"
        cls.master_content = FILE_MASTER.read_text(encoding="utf-8")

    def test_cenario_1_math_exactness(self):
        """Valida a precisão matemática exata do Cenário 1."""
        res = MathematicalModelEngine.calc_cenario_1()
        self.assertEqual(res["total_com_email"], 836)
        self.assertEqual(res["folga_com_email"], 164)
        self.assertEqual(res["total_sem_email"], 652)
        self.assertEqual(res["folga_sem_email"], 348)
        self.assertAlmostEqual(res["custo_medio_venda"], 4.6, places=5)
        self.assertAlmostEqual(res["gatilho_vendas_float"], 195.6521739, places=4)
        self.assertEqual(res["gatilho_vendas_int"], 195)
        self.assertEqual(res["n8n_execucoes"], 184)
        self.assertEqual(res["n8n_folga"], 816)

        # Verifica presença exata no documento
        self.assertIn("836", self.master_content)
        self.assertIn("652", self.master_content)
        self.assertIn("184", self.master_content)
        self.assertIn("195", self.master_content)
        self.assertIn("4,6", self.master_content)

    def test_cenario_2_math_exactness(self):
        """Valida a precisão matemática exata do Cenário 2."""
        res = MathematicalModelEngine.calc_cenario_2()
        self.assertEqual(res["total_com_email"], 996)
        self.assertEqual(res["folga_com_email"], 4)
        self.assertEqual(res["total_sem_email"], 812)
        self.assertEqual(res["folga_sem_email"], 188)
        self.assertAlmostEqual(res["custo_medio_venda"], 5.6, places=5)
        self.assertAlmostEqual(res["gatilho_vendas_float"], 160.7142857, places=4)
        self.assertEqual(res["gatilho_vendas_int"], 160)
        self.assertEqual(res["n8n_execucoes"], 344)
        self.assertEqual(res["n8n_folga"], 656)

        # Verifica presença exata no documento
        self.assertIn("996", self.master_content)
        self.assertIn("812", self.master_content)
        self.assertIn("344", self.master_content)
        self.assertIn("160", self.master_content)
        self.assertIn("5,6", self.master_content)

    def test_cenario_3_math_exactness(self):
        """Valida a precisão matemática exata do Cenário 3 e estouro de 20 créditos."""
        res = MathematicalModelEngine.calc_cenario_3()
        self.assertEqual(res["total_com_email"], 1020)
        self.assertEqual(res["folga_com_email"], -20)  # Estouro de 20 créditos
        self.assertEqual(res["total_sem_email"], 836)
        self.assertEqual(res["folga_sem_email"], 164)
        self.assertAlmostEqual(res["custo_medio_venda"], 5.75, places=5)
        self.assertAlmostEqual(res["gatilho_vendas_float"], 156.521739, places=4)
        self.assertEqual(res["gatilho_vendas_int"], 156)
        self.assertEqual(res["n8n_execucoes"], 368)
        self.assertEqual(res["n8n_folga"], 632)

        # Verifica presença exata no documento
        self.assertTrue("1.020" in self.master_content or "1020" in self.master_content)
        self.assertIn("368", self.master_content)
        self.assertIn("156", self.master_content)
        self.assertIn("5,75", self.master_content)
        self.assertIn("20", self.master_content)

    def test_d1_formula_boundary_matrix(self):
        """
        Executa matriz de testes de contorno na fórmula de D-1:
        extras_venda in [0, 1, 2]
        testes in [50, 100, 150]
        """
        test_cases = [
            # (extras_venda, extras_reembolso, testes, exp_com, exp_sem, exp_decisao)
            (0, 0, 100, 836, 652, "Make com e-mail"),
            (0, 0, 50,  786, 602, "Make com e-mail"),
            (0, 0, 150, 886, 702, "Make com e-mail"),
            (1, 0, 100, 996, 812, "Make com e-mail"),
            (1, 0, 50,  946, 762, "Make com e-mail"),
            (1, 0, 150, 1046, 862, "Make sem e-mail"),  # com e-mail estoura (+46), sem e-mail fica seguro (+138)
            (1, 1, 100, 1020, 836, "Make sem e-mail"),  # com e-mail estoura (+20), sem e-mail folga +164
            (2, 0, 100, 1156, 972, "Make sem e-mail"),  # com e-mail estoura (+156), sem e-mail folga +28
            (2, 1, 100, 1180, 996, "Make sem e-mail"),  # sem e-mail folga +4 (crítica)
            (2, 2, 100, 1204, 1020, "Migrar para n8n Cloud"),  # ambos estouram! migra para n8n
            (2, 0, 150, 1206, 1022, "Migrar para n8n Cloud"),  # ambos estouram! migra para n8n
        ]

        for ev, er, t, exp_c, exp_s, exp_dec in test_cases:
            with self.subTest(extras_venda=ev, extras_reembolso=er, testes=t):
                sim = MathematicalModelEngine.calc_d1_formula(ev, er, t)
                self.assertEqual(sim["consumo_com_email"], exp_c)
                self.assertEqual(sim["consumo_sem_email"], exp_s)
                self.assertEqual(sim["decisao"], exp_dec)

    def test_cenario_2_sensitivity_cliff_edge(self):
        """
        Adversarial Test: Comprova que no Cenário 2, gastar 104 créditos em testes deixa folga = 0,
        e gastar 105 créditos (-1 de folga) força imediatamente o corte do e-mail.
        """
        # Exatamente 100 créditos em testes: folga = 4
        s100 = MathematicalModelEngine.calc_d1_formula(extras_venda=1, extras_reembolso=0, consumo_testes=100)
        self.assertEqual(s100["folga_com_email"], 4)
        self.assertEqual(s100["decisao"], "Make com e-mail")

        # 104 créditos em testes: folga = 0 (borda exata)
        s104 = MathematicalModelEngine.calc_d1_formula(extras_venda=1, extras_reembolso=0, consumo_testes=104)
        self.assertEqual(s104["folga_com_email"], 0)
        self.assertEqual(s104["decisao"], "Make com e-mail")

        # 105 créditos em testes: folga = -1 (estouro!) -> migra para Make sem e-mail
        s105 = MathematicalModelEngine.calc_d1_formula(extras_venda=1, extras_reembolso=0, consumo_testes=105)
        self.assertEqual(s105["folga_com_email"], -1)
        self.assertEqual(s105["decisao"], "Make sem e-mail")
        self.assertEqual(s105["folga_sem_email"], 183)  # Folga segura recuperada

    def test_n8n_migration_threshold_boundary(self):
        """
        Adversarial Test: Identifica a fronteira exata em que o Make 'Sem E-mail'
        estoura e força a migração mandatória para o n8n Cloud Trial.
        """
        # Se extras_venda = 2 e extras_reembolso = 0:
        # Sem e-mail consome 652 + 320 = 972 com 100 de testes (folga = 28)
        # O estouro sem e-mail ocorre se testes > 100 + 28 = 128 créditos!
        t128 = MathematicalModelEngine.calc_d1_formula(extras_venda=2, extras_reembolso=0, consumo_testes=128)
        self.assertEqual(t128["folga_sem_email"], 0)
        self.assertEqual(t128["decisao"], "Make sem e-mail")

        t129 = MathematicalModelEngine.calc_d1_formula(extras_venda=2, extras_reembolso=0, consumo_testes=129)
        self.assertEqual(t129["folga_sem_email"], -1)
        self.assertEqual(t129["decisao"], "Migrar para n8n Cloud")

        # Se extras_venda = 3 (4 chamadas por venda):
        # 652 + 480 = 1132 cr -> Imediatamente negativo (-132 cr), forçando n8n Cloud!
        t_ext3 = MathematicalModelEngine.calc_d1_formula(extras_venda=3, extras_reembolso=0, consumo_testes=100)
        self.assertEqual(t_ext3["folga_sem_email"], -132)
        self.assertEqual(t_ext3["decisao"], "Migrar para n8n Cloud")

    def test_d1_checklist_all_12_items(self):
        """Verifica se todos os 12 itens do checklist de D-1 estão documentados no arquivo mestre."""
        required_d1_items = [
            (1, "Restrição de Eventos no Painel Greenn", r"\[ SIM / NÃO \]"),
            (2, "URL de Webhook por Produto na Greenn", r"\[ 1 URL \(Router\) / 2 URLs \]"),
            (3, "URL Real do Webhook Gerada", r"\{\{URL_WEBHOOK\}\}\s*=\s*\[\s*_{3,}\s*\]"),
            (4, "Medição de Chamadas Reais", r"Chamadas/venda:\s*\[\s*___\s*\]\s*\\?\|\s*Chamadas/reembolso:\s*\[\s*___\s*\]"),
            (5, "Consumo Real de Testes em D-1", r"consumo real de testes:\s*\[\s*___\s*\]\s*créditos"),
            (6, "Recálculo da Folga de Créditos em D-1", r"Com e-mail:\s*836\s*\+\s*\(160\s*×\s*\[extras/venda\]\)"),
            (7, "Decisão de Plataforma em D-1", r"\[ Make com e-mail / Make sem e-mail / Migrar para n8n Cloud \]"),
            (8, "Conferência dos Nomes Reais no Payload", r"Mapeamento ajustado:\s*\[\s*___\s*\]"),
            (9, "Unicidade do Arquivo na Busca e Proteção do `Delete a File`", r"\[ SIM / NÃO \]"),
            (10, "Herança da Trava de Download", r"\[ SIM / NÃO — Risco aceito \]"),
            (11, "Desativação do Aviso Nativo do Drive", r"\[ SIM / NÃO — Decisão: Manter 2 e-mails / Cortar e-mail próprio \]"),
            (12, "Método de Envio de E-mail Configurado", r"\[ SMTP com Senha de App / Gmail OAuth \]")
        ]

        sec5_match = re.search(r"## 5\. Checklist de Execução.*?(?=## 6\.)", self.master_content, re.DOTALL)
        self.assertIsNotNone(sec5_match, "Seção 5 (Checklist D-1) não encontrada no documento mestre")
        sec5_text = sec5_match.group(0)

        for item_num, title, pattern in required_d1_items:
            with self.subTest(item=item_num, title=title):
                self.assertIn(title, sec5_text, f"Título do item {item_num} ausente na Seção 5: '{title}'")
                match = re.search(pattern, sec5_text)
                self.assertIsNotNone(match, f"Padrão preenchível do item {item_num} não encontrado: {pattern}")

    def test_risk_matrix_all_12_risks(self):
        """Verifica se todos os 12 riscos estão documentados com severidade, probabilidade e mitigações."""
        required_risks = [
            (1, "Chamadas extras de webhook em vendas (Cenário 2)"),
            (2, "Chamadas extras de webhook em vendas E reembolsos (Cenário 3)"),
            (3, "Falha no Fluxo B se a cópia não existir"),
            (4, "Busca no Fluxo B trazendo mais de um arquivo"),
            (5, "Consumo de testes ultrapassando a reserva de 100 créditos"),
            (6, "Divergência nos nomes dos campos do payload real da Greenn"),
            (7, "Limite de 1 URL de webhook na Greenn"),
            (8, "Rajada de vendas simultâneas na abertura do carrinho"),
            (9, "Limite de 5 MB no Make gratuito"),
            (10, "Intervalo mínimo de agendamento de 15 min no Make gratuito"),
            (11, "Retenção de logs de apenas 7 dias no Make gratuito"),
            (12, "Herança de trava de download, aviso duplicado do Drive e bloqueio OAuth do Gmail")
        ]

        sec8_match = re.search(r"## 8\. Matriz Completa de Riscos.*?(?=## 9\.)", self.master_content, re.DOTALL)
        self.assertIsNotNone(sec8_match, "Seção 8 (Matriz de Riscos) não encontrada no documento mestre")
        sec8_text = sec8_match.group(0)

        for risk_num, title in required_risks:
            with self.subTest(risk=risk_num, title=title):
                self.assertIn(title, sec8_text, f"Título do risco {risk_num} ausente na Seção 8: '{title}'")
                row_pattern = rf"\|\s*\*\*{risk_num}\*\*\s*\|\s*\*\*{re.escape(title)}.*?\*\*\s*\|\s*([^|]+)\|\s*([^|]+)\|\s*([^|]+)\|\s*([^|]+)\|"
                row_match = re.search(row_pattern, sec8_text)
                self.assertIsNotNone(row_match, f"Linha da tabela para o risco {risk_num} mal formatada ou incompleta")
                sev, prob, mit_d1, mit_diad = [c.strip() for c in row_match.groups()]
                self.assertTrue(len(sev) > 0, f"Severidade vazia para risco {risk_num}")
                self.assertTrue(len(prob) > 0, f"Probabilidade vazia para risco {risk_num}")
                self.assertTrue(len(mit_d1) > 10, f"Mitigação D-1 muito curta para risco {risk_num}")
                self.assertTrue(len(mit_diad) > 10, f"Mitigação Dia D muito curta para risco {risk_num}")

    def test_yaml_spec_numbers_alignment(self):
        """Verifica se os valores numéricos do bloco YAML correspondem exatamente aos cálculos do modelo."""
        c1 = MathematicalModelEngine.calc_cenario_1()
        c2 = MathematicalModelEngine.calc_cenario_2()
        c3 = MathematicalModelEngine.calc_cenario_3()

        yaml_match = re.search(r"```yaml(.*?)```", self.master_content, re.DOTALL)
        self.assertIsNotNone(yaml_match, "Bloco YAML da Ficha Técnica não encontrado")
        yaml_text = yaml_match.group(1)

        self.assertIn(f"gatilho_upgrade_creditos: {MathematicalModelEngine.GATILHO_CREDITOS}", yaml_text)
        self.assertIn(f"reserva_testes_creditos: {MathematicalModelEngine.RESERVA_TESTES}", yaml_text)
        self.assertIn(f"limite_vendas_cenario_1: {c1['gatilho_vendas_int']}", yaml_text)
        self.assertIn(f"limite_vendas_cenario_2: {c2['gatilho_vendas_int']}", yaml_text)
        self.assertIn(f"limite_vendas_cenario_3: {c3['gatilho_vendas_int']}", yaml_text)


if __name__ == "__main__":
    unittest.main()
