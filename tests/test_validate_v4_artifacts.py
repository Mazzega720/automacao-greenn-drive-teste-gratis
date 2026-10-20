#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Testes Unitários da Suíte de Validação (test_validate_v4_artifacts.py)
Garante a integridade dos validadores, checagem de variáveis banidas e lógica de auditoria.
"""

import unittest
import sys
import shutil
import subprocess
from pathlib import Path

# Adiciona o diretório raiz ao sys.path para importar o validador
ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

import validate_v4_artifacts as val


class TestValidateV4Artifacts(unittest.TestCase):
    """Bateria de testes unitários para validate_v4_artifacts.py."""

    def test_standalone_files_exist_and_valid_utf8(self):
        """Verifica se templates-email-v4.md e testes-d1-curl-v4.sh existem e abrem em UTF-8."""
        for file_path in [val.FILE_TEMPLATES, val.FILE_CURL]:
            success, content, msg = val.read_file_utf8(file_path)
            self.assertTrue(success, f"Falha ao ler {file_path.name}: {msg}")
            self.assertGreater(len(content), 100, f"Conteúdo muito curto em {file_path.name}")

    def test_banned_variables_scanner_detects_prohibited_tokens(self):
        """Comprova que o scanner de variáveis detecta tokens proibidos quando presentes."""
        report = val.ValidationReport()
        mock_content = {
            "dummy_bad.md": 'Aqui usamos {{buyer_email}} e "transaction_id" proibidos.'
        }
        val.audit_gate_2_banned_variables(report, mock_content)
        self.assertFalse(report.is_clean())
        self.assertEqual(len(report.failures), 2)

    def test_banned_variables_scanner_passes_clean_content(self):
        """Comprova que o scanner de variáveis aprova conteúdo limpo com variáveis homologadas."""
        report = val.ValidationReport()
        mock_content = {
            "clean.md": "Olá {{email_comprador}}, sua transação {{id_transacao}} tem link {{webViewLink}}."
        }
        val.audit_gate_2_banned_variables(report, mock_content)
        self.assertTrue(report.is_clean())
        self.assertEqual(len(report.failures), 0)

    def test_production_templates_contain_no_banned_variables(self):
        """Comprova que templates-email-v4.md tem ZERO variáveis proibidas."""
        report = val.ValidationReport()
        _, content, _ = val.read_file_utf8(val.FILE_TEMPLATES)
        val.audit_gate_2_banned_variables(report, {val.FILE_TEMPLATES.name: content})
        self.assertTrue(report.is_clean(), f"Variáveis proibidas em templates: {report.failures}")

    def test_production_curl_contains_no_banned_variables(self):
        """Comprova que testes-d1-curl-v4.sh tem ZERO variáveis proibidas."""
        report = val.ValidationReport()
        _, content, _ = val.read_file_utf8(val.FILE_CURL)
        val.audit_gate_2_banned_variables(report, {val.FILE_CURL.name: content})
        self.assertTrue(report.is_clean(), f"Variáveis proibidas em curl: {report.failures}")

    def test_curl_payloads_extraction_and_transitions(self):
        """Valida se os 3 payloads do script curl cumprem as regras de transição."""
        report = val.ValidationReport()
        _, content, _ = val.read_file_utf8(val.FILE_CURL)
        val.audit_gate_4_json_payloads(report, content, None)
        self.assertTrue(report.is_clean(), f"Falha na validação dos payloads: {report.failures}")

        payloads = val.extract_json_payloads_from_curl(content)
        self.assertEqual(len(payloads), 3)

        # Teste 1: waiting_payment -> paid
        self.assertEqual(payloads[0]["oldStatus"], "waiting_payment")
        self.assertEqual(payloads[0]["currentStatus"], "paid")
        self.assertEqual(payloads[0]["email_comprador"], "comprador.teste.v4@gmail.com")
        self.assertEqual(payloads[0]["id_transacao"], "TRX-TESTE-4001")

        # Teste 2: paid -> paid
        self.assertEqual(payloads[1]["oldStatus"], "paid")
        self.assertEqual(payloads[1]["currentStatus"], "paid")

        # Teste 3: paid -> refunded
        self.assertEqual(payloads[2]["oldStatus"], "paid")
        self.assertEqual(payloads[2]["currentStatus"], "refunded")

    def test_email_templates_structural_integrity(self):
        """Valida que templates-email-v4.md possui HTML, texto puro e aviso Google em negrito."""
        report = val.ValidationReport()
        _, content, _ = val.read_file_utf8(val.FILE_TEMPLATES)
        val.audit_gate_8_email_templates(report, content)
        self.assertTrue(report.is_clean(), f"Falha nos templates de e-mail: {report.failures}")

    def test_yaml_ficha_tecnica_validator_with_valid_mock(self):
        """Comprova que o validador aceita um bloco YAML canônico com 12 chaves exatas."""
        mock_yaml_doc = """
# Documento
```yaml
versao: 4.0
gatilho_upgrade_creditos: 900
reserva_testes_creditos: 100
limite_vendas_cenario_1: 195
limite_vendas_cenario_2: 160
limite_vendas_cenario_3: 156
acao_upgrade: conferir_plano_vigente_no_site_do_make
criterio_migracao_n8n: somente_se_folga_no_make_ficar_negativa_mesmo_sem_email_proprio
eventos_greenn: [paid, refunded, chargedback]
arquitetura: cenario_unico_router
protecao_delete_fluxo_b: filtro_se_encontrou_arquivo_ou_error_handler_ignore
variaveis_padronizadas: [URL_WEBHOOK, email_comprador, id_transacao, webViewLink, oldStatus, currentStatus]
```
        """
        report = val.ValidationReport()
        val.audit_gate_3_yaml_ficha_tecnica(report, mock_yaml_doc)
        self.assertTrue(report.is_clean(), f"Falha inesperada no YAML válido: {report.failures}")

    def test_yaml_ficha_tecnica_rejects_missing_key(self):
        """Comprova que o validador rejeita bloco YAML com chaves a menos."""
        mock_bad_yaml = """
```yaml
versao: 4.0
gatilho_upgrade_creditos: 900
```
        """
        report = val.ValidationReport()
        val.audit_gate_3_yaml_ficha_tecnica(report, mock_bad_yaml)
        self.assertFalse(report.is_clean())

    def test_math_and_scenarios_validation(self):
        """Valida que a memória de cálculo aceita texto com todos os números exigidos."""
        mock_text = """
        Cenário 1: 836 créditos com e-mail, 652 créditos sem e-mail, 184 execuções n8n, gatilho 195 vendas.
        Cenário 2: 996 créditos com e-mail, 812 créditos sem e-mail, 344 execuções n8n, gatilho 160 vendas.
        Cenário 3: 1020 créditos com e-mail (estouro), 836 créditos sem e-mail, 368 execuções n8n, gatilho 156 vendas.
        Reserva de testes de 100 créditos.
        """
        report = val.ValidationReport()
        val.audit_gate_5_math_and_scenarios(report, mock_text)
        self.assertTrue(report.is_clean(), f"Falha na validação matemática: {report.failures}")

    def test_checklist_d1_and_formula_validation(self):
        """Valida se o checklist de D-1 e a fórmula paramétrica são reconhecidos."""
        mock_text = """
        Item 1: Restrição de Eventos no Painel Greenn [ SIM / NÃO ]
        Item 2: URL de Webhook por Produto [ 1 URL (Router) / 2 URLs ]
        Item 3: URL Real do Webhook Gerada {{URL_WEBHOOK}} = [ ______________________ ]
        Item 4: Medição de Chamadas Reais: Chamadas/venda: [ ___ ] | Chamadas/reembolso: [ ___ ]
        Item 5: Consumo Real de Testes em D-1: consumo real de testes: [ ___ ] créditos (reserva total = 100)
        Item 6: Recálculo da Folga de Créditos em D-1: Com e-mail: 836 + (160 × [extras/venda]) + (24 × [extras/reembolso]) + ([consumo real de testes] - 100) = [ ___ ] créditos | Sem e-mail: 652 + (160 × [extras/venda]) + (24 × [extras/reembolso]) + ([consumo real de testes] - 100) = [ ___ ] créditos | Folga real: [ ___ ]
        Item 7: Decisão de Plataforma em D-1: [ Make com e-mail / Make sem e-mail / Migrar para n8n Cloud ]
        Item 8: Conferência dos Nomes no Payload: Mapeamento ajustado: [ ___ ]
        Item 9: Unicidade do Arquivo na Busca e proteção no delete [ SIM / NÃO ]
        Item 10: Herança da Trava de Download no Drive [ SIM / NÃO — Risco aceito ]
        Item 11: Desativação do Aviso Nativo do Drive (sendNotificationEmail = false) [ SIM / NÃO ]
        Item 12: Método de Envio de E-mail Configurado: SMTP com Senha de App
        """
        report = val.ValidationReport()
        val.audit_gate_6_checklist_d1(report, mock_text)
        self.assertTrue(report.is_clean(), f"Falha no checklist D-1: {report.failures}")

    def test_skills_mapping_validation(self):
        """Valida que todas as 8 skills obrigatórias são identificadas."""
        mock_text = """
        Skills da Equipe:
        - software-architecture
        - api-design-principles
        - security-and-hardening
        - privacy-by-design
        - pdf-official
        - clean-code
        - clean-code-guard
        - lint-and-validate
        """
        report = val.ValidationReport()
        val.audit_gate_7_skills_mapping(report, mock_text)
        self.assertTrue(report.is_clean(), f"Falha nas skills: {report.failures}")

    @unittest.skipUnless(shutil.which("bash"), "Interpretador bash não encontrado no PATH")
    def test_curl_script_bash_syntax_valid(self):
        """Valida que testes-d1-curl-v4.sh passa na verificação estática de sintaxe bash -n."""
        res = subprocess.run(
            ["bash", "-n", "testes-d1-curl-v4.sh"],
            cwd=str(ROOT_DIR),
            capture_output=True,
            text=True
        )
        self.assertEqual(res.returncode, 0, f"bash -n falhou: {res.stderr}")

    @unittest.skipUnless(shutil.which("bash"), "Interpretador bash não encontrado no PATH")
    def test_curl_script_parameter_expansion_resolution(self):
        """Garante que a passagem de URL como $1 não anexa '}}' ao endpoint alvo."""
        test_url = "http://example.com"
        res = subprocess.run(
            ["bash", "testes-d1-curl-v4.sh", test_url],
            cwd=str(ROOT_DIR),
            capture_output=True,
            encoding="utf-8",
            errors="replace"
        )
        self.assertEqual(res.returncode, 0, f"Script falhou ao rodar com URL: {res.stderr}")
        self.assertIn("Endpoint Alvo : http://example.com", res.stdout)
        self.assertNotIn("http://example.com}}", res.stdout)

    @unittest.skipUnless(shutil.which("bash"), "Interpretador bash não encontrado no PATH")
    def test_curl_script_inspection_mode_on_placeholder(self):
        """Garante que execução sem argumentos exibe aviso e encerra sem falha (exit 0)."""
        res = subprocess.run(
            ["bash", "testes-d1-curl-v4.sh"],
            cwd=str(ROOT_DIR),
            capture_output=True,
            encoding="utf-8",
            errors="replace"
        )
        self.assertEqual(res.returncode, 0, f"Script falhou ao rodar sem argumentos: {res.stderr}")
        self.assertIn("Endpoint Alvo : {{URL_WEBHOOK}}", res.stdout)
        self.assertIn("AVISO: Endpoint com placeholder {{URL_WEBHOOK}}", res.stdout)
        self.assertIn("Modo de inspeção", res.stdout)

    @unittest.skipUnless(shutil.which("bash"), "Interpretador bash não encontrado no PATH")
    def test_curl_script_env_var_expansion(self):
        """Garante que a variável de ambiente URL_WEBHOOK é respeitada sem caracteres espúrios."""
        env_url = "https://hook.make.com/teste-env-homolog"
        # Executa no bash com exportação explícita
        cmd = f'export URL_WEBHOOK="{env_url}"; bash testes-d1-curl-v4.sh'
        res = subprocess.run(
            ["bash", "-c", cmd],
            cwd=str(ROOT_DIR),
            capture_output=True,
            encoding="utf-8",
            errors="replace"
        )
        self.assertIn(f"Endpoint Alvo : {env_url}", res.stdout)
        self.assertNotIn(env_url + "}}", res.stdout)


if __name__ == "__main__":
    unittest.main()
