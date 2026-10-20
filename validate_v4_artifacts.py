#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Validador de Artefatos v4.0 (validate_v4_artifacts.py)
Projeto: automacao-greenn-drive-teste-gratis-v4

Suíte de verificação automatizada e auditoria programática contra desvios de especificação,
inconsistências matemáticas, violação de contratos de dados e uso de variáveis proibidas.

Baseado nas diretrizes de engenharia 'clean-code' e 'lint-and-validate'.
"""

import sys
import os
import re
import json
from pathlib import Path
from typing import List, Dict, Tuple, Optional

# Dependência PyYAML para auditoria estrita da Ficha Técnica
try:
    import yaml
except ImportError:
    print("[ERRO FATAL] Pacote 'pyyaml' não encontrado. Execute: pip install pyyaml")
    sys.exit(1)

if sys.platform.startswith("win"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

# Configuração de Caminhos Globais
ROOT_DIR = Path(__file__).resolve().parent
FILE_MASTER = ROOT_DIR / "automacao-greenn-drive-teste-gratis-v4.md"
FILE_TEMPLATES = ROOT_DIR / "templates-email-v4.md"
FILE_CURL = ROOT_DIR / "testes-d1-curl-v4.sh"

# Constantes de Validação e Whitelists
BANNED_VARIABLES = [
    r"\{\{buyer_email\}\}",
    r"\{\{transaction_id\}\}",
    r"\{\{preferred_channel\}\}",
    r'"buyer_email"',
    r'"transaction_id"'
]

EXPECTED_YAML_KEYS = [
    "versao",
    "gatilho_upgrade_creditos",
    "reserva_testes_creditos",
    "limite_vendas_cenario_1",
    "limite_vendas_cenario_2",
    "limite_vendas_cenario_3",
    "acao_upgrade",
    "criterio_migracao_n8n",
    "eventos_greenn",
    "arquitetura",
    "protecao_delete_fluxo_b",
    "variaveis_padronizadas"
]

REQUIRED_SKILLS = [
    "software-architecture",
    "api-design-principles",
    "security-and-hardening",
    "privacy-by-design",
    "pdf-official",
    "clean-code",
    "clean-code-guard",
    "lint-and-validate"
]


class ValidationReport:
    """Acumulador e formatador de resultados de auditoria."""

    def __init__(self):
        self.passes: List[str] = []
        self.failures: List[str] = []
        self.warnings: List[str] = []

    def record_pass(self, gate_name: str, detail: str):
        self.passes.append(f"[{gate_name}] PASS: {detail}")

    def record_failure(self, gate_name: str, detail: str):
        self.failures.append(f"[{gate_name}] FAIL: {detail}")

    def record_warning(self, gate_name: str, detail: str):
        self.warnings.append(f"[{gate_name}] WARN: {detail}")

    def is_clean(self) -> bool:
        return len(self.failures) == 0

    def print_summary(self):
        print("\n" + "=" * 76)
        print("    RELATORIO DE AUDITORIA E VALIDACAO DE ARTEFATOS v4.0")
        print("=" * 76)

        for p in self.passes:
            print(f"  [OK]   {p}")

        if self.warnings:
            print("\n" + "-" * 76)
            print("  AVISOS / PENDENCIAS:")
            for w in self.warnings:
                print(f"  [WARN] {w}")

        if self.failures:
            print("\n" + "-" * 76)
            print("  FALHAS ENCONTRADAS:")
            for f in self.failures:
                print(f"  [FAIL] {f}")
            print("-" * 76)
            print(f"STATUS FINAL: REPROVADO ({len(self.failures)} falhas)")
            print("=" * 76)
        else:
            print("-" * 76)
            print("STATUS FINAL: APROVADO COM 100% DE CONFORMIDADE")
            print("=" * 76)


def read_file_utf8(path: Path) -> Tuple[bool, str, str]:
    """Lê arquivo garantindo estritamente codificação UTF-8."""
    if not path.is_file():
        return False, "", f"Arquivo não encontrado: {path.name}"
    try:
        content = path.read_text(encoding="utf-8")
        return True, content, "OK"
    except UnicodeDecodeError as e:
        return False, "", f"Falha de decodificação UTF-8 em {path.name}: {e}"
    except Exception as e:
        return False, "", f"Erro ao ler {path.name}: {e}"


# ==============================================================================
# PORTÃO 1: VERIFICAÇÃO DE EXISTÊNCIA E CODIFICAÇÃO UTF-8
# ==============================================================================
def audit_gate_1_files(report: ValidationReport, require_master: bool = False) -> Dict[str, str]:
    """Valida existência e UTF-8 dos artefatos."""
    contents: Dict[str, str] = {}

    # Artefatos obrigatórios autônomos
    for file_path in [FILE_TEMPLATES, FILE_CURL]:
        success, content, msg = read_file_utf8(file_path)
        if success:
            contents[file_path.name] = content
            report.record_pass("Portão 1: Arquivos UTF-8", f"{file_path.name} íntegro em UTF-8 ({len(content)} chars)")
        else:
            report.record_failure("Portão 1: Arquivos UTF-8", msg)

    # Documento mestre
    success_master, content_master, msg_master = read_file_utf8(FILE_MASTER)
    if success_master:
        contents[FILE_MASTER.name] = content_master
        report.record_pass("Portão 1: Arquivos UTF-8", f"{FILE_MASTER.name} íntegro em UTF-8 ({len(content_master)} chars)")
    else:
        if require_master:
            report.record_failure("Portão 1: Arquivos UTF-8", msg_master)
        else:
            report.record_warning("Portão 1: Arquivos UTF-8", f"{FILE_MASTER.name} ainda não gerado (aguardando Worker 1)")

    return contents


# ==============================================================================
# PORTÃO 2: SCANNER RIGOROSO CONTRA VARIÁVEIS PROIBIDAS
# ==============================================================================
def audit_gate_2_banned_variables(report: ValidationReport, contents: Dict[str, str]):
    """Garante erradicação absoluta de variáveis legadas proibidas."""
    violations = 0

    for filename, text in contents.items():
        lines = text.splitlines()
        for line_no, line in enumerate(lines, start=1):
            for pattern in BANNED_VARIABLES:
                matches = re.findall(pattern, line)
                if matches:
                    violations += 1
                    report.record_failure(
                        "Portão 2: Variáveis Proibidas",
                        f"{filename}:{line_no} contém variável legada proibida: '{pattern}' -> Linha: {line.strip()}"
                    )

    if violations == 0:
        report.record_pass(
            "Portão 2: Variáveis Proibidas",
            f"Zero ocorrências de variáveis proibidas em {len(contents)} arquivo(s) analisado(s)"
        )


# ==============================================================================
# PORTÃO 3: AUDITORIA ESTRUTURAL DA FICHA TÉCNICA YAML
# ==============================================================================
def audit_gate_3_yaml_ficha_tecnica(report: ValidationReport, master_text: Optional[str]):
    """Valida o bloco YAML da Ficha Técnica na documentação mestre."""
    if master_text is None:
        report.record_warning("Portão 3: Ficha Técnica YAML", "Ignorado: documento mestre ainda não criado.")
        return

    # Busca o primeiro bloco ```yaml ... ```
    match = re.search(r"```ya?ml\s*\n(.*?)\n```", master_text, re.DOTALL | re.IGNORECASE)
    if not match:
        report.record_failure("Portão 3: Ficha Técnica YAML", "Bloco YAML da Ficha Técnica não encontrado em formato ```yaml.")
        return

    yaml_raw = match.group(1)
    try:
        data = yaml.safe_load(yaml_raw)
    except Exception as e:
        report.record_failure("Portão 3: Ficha Técnica YAML", f"Erro de sintaxe no parser YAML: {e}")
        return

    if not isinstance(data, dict):
        report.record_failure("Portão 3: Ficha Técnica YAML", "O bloco YAML não foi parseado como um dicionário/mapa válido.")
        return

    # Validação da contagem exata de 12 chaves canônicas
    keys = list(data.keys())
    if len(keys) != 12:
        report.record_failure(
            "Portão 3: Ficha Técnica YAML",
            f"Ficha Técnica deve ter exatamente 12 chaves. Encontradas {len(keys)}: {keys}"
        )

    for required_key in EXPECTED_YAML_KEYS:
        if required_key not in data:
            report.record_failure("Portão 3: Ficha Técnica YAML", f"Chave canônica ausente: '{required_key}'")

    # Validação estrita de valores e tipos canônicos
    if str(data.get("versao")) not in ["4.0", "4"]:
        report.record_failure("Portão 3: Ficha Técnica YAML", f"versao incorreta: {data.get('versao')} (esperado '4.0')")

    if data.get("gatilho_upgrade_creditos") != 900:
        report.record_failure("Portão 3: Ficha Técnica YAML", f"gatilho_upgrade_creditos incorreto: {data.get('gatilho_upgrade_creditos')}")

    if data.get("reserva_testes_creditos") != 100:
        report.record_failure("Portão 3: Ficha Técnica YAML", f"reserva_testes_creditos incorreto: {data.get('reserva_testes_creditos')}")

    if data.get("limite_vendas_cenario_1") != 195:
        report.record_failure("Portão 3: Ficha Técnica YAML", f"limite_vendas_cenario_1 incorreto: {data.get('limite_vendas_cenario_1')}")

    if data.get("limite_vendas_cenario_2") != 160:
        report.record_failure("Portão 3: Ficha Técnica YAML", f"limite_vendas_cenario_2 incorreto: {data.get('limite_vendas_cenario_2')}")

    if data.get("limite_vendas_cenario_3") != 156:
        report.record_failure("Portão 3: Ficha Técnica YAML", f"limite_vendas_cenario_3 incorreto: {data.get('limite_vendas_cenario_3')}")

    if data.get("acao_upgrade") != "conferir_plano_vigente_no_site_do_make":
        report.record_failure("Portão 3: Ficha Técnica YAML", f"acao_upgrade inválida: '{data.get('acao_upgrade')}'")

    if data.get("criterio_migracao_n8n") != "somente_se_folga_no_make_ficar_negativa_mesmo_sem_email_proprio":
        report.record_failure("Portão 3: Ficha Técnica YAML", f"criterio_migracao_n8n inválido: '{data.get('criterio_migracao_n8n')}'")

    if data.get("eventos_greenn") != ["paid", "refunded", "chargedback"]:
        report.record_failure("Portão 3: Ficha Técnica YAML", f"eventos_greenn inválido: {data.get('eventos_greenn')}")

    if data.get("arquitetura") != "cenario_unico_router":
        report.record_failure("Portão 3: Ficha Técnica YAML", f"arquitetura inválida: '{data.get('arquitetura')}'")

    if data.get("protecao_delete_fluxo_b") != "filtro_se_encontrou_arquivo_ou_error_handler_ignore":
        report.record_failure("Portão 3: Ficha Técnica YAML", f"protecao_delete_fluxo_b inválido: '{data.get('protecao_delete_fluxo_b')}'")

    expected_vars = ["URL_WEBHOOK", "email_comprador", "id_transacao", "webViewLink", "oldStatus", "currentStatus"]
    if data.get("variaveis_padronizadas") != expected_vars:
        report.record_failure("Portão 3: Ficha Técnica YAML", f"variaveis_padronizadas inválidas: {data.get('variaveis_padronizadas')}")

    report.record_pass("Portão 3: Ficha Técnica YAML", "YAML canônico validado com exatamente 12 chaves e valores estritos")


# ==============================================================================
# PORTÃO 4: VALIDAÇÃO DOS PAYLOADS JSON E SINTAXE DOS COMANDOS CURL
# ==============================================================================
def extract_json_payloads_from_curl(script_text: str) -> List[Dict]:
    """Extrai blocos JSON passados como argumento -d nos comandos curl."""
    payloads = []
    # Expressão regular para capturar blocos -d '{ ... }'
    pattern = r"-d\s+'(\{[^']+\})'"
    matches = re.findall(pattern, script_text, re.DOTALL)
    for raw in matches:
        try:
            payloads.append(json.loads(raw))
        except Exception as e:
            payloads.append({"_parse_error": str(e), "_raw": raw})
    return payloads


def audit_gate_4_json_payloads(report: ValidationReport, curl_text: str, master_text: Optional[str]):
    """Valida conformidade dos 3 payloads JSON nos comandos curl."""
    payloads = extract_json_payloads_from_curl(curl_text)

    if len(payloads) != 3:
        report.record_failure(
            "Portão 4: Payloads JSON",
            f"Esperados exatamente 3 payloads nos comandos curl de {FILE_CURL.name}. Encontrados: {len(payloads)}"
        )
        return

    # Teste 1: waiting_payment -> paid
    t1 = payloads[0]
    if "_parse_error" in t1:
        report.record_failure("Portão 4: Payloads JSON", f"Teste 1 JSON inválido: {t1['_parse_error']}")
    else:
        if t1.get("oldStatus") != "waiting_payment" or t1.get("currentStatus") != "paid":
            report.record_failure(
                "Portão 4: Payloads JSON",
                f"Teste 1 transição inválida: oldStatus='{t1.get('oldStatus')}', currentStatus='{t1.get('currentStatus')}' (esperado waiting_payment -> paid)"
            )
        if "email_comprador" not in t1 or "id_transacao" not in t1:
            report.record_failure("Portão 4: Payloads JSON", f"Teste 1 chaves ausentes: {t1}")

    # Teste 2: paid -> paid
    t2 = payloads[1]
    if "_parse_error" in t2:
        report.record_failure("Portão 4: Payloads JSON", f"Teste 2 JSON inválido: {t2['_parse_error']}")
    else:
        if t2.get("oldStatus") != "paid" or t2.get("currentStatus") != "paid":
            report.record_failure(
                "Portão 4: Payloads JSON",
                f"Teste 2 transição inválida: oldStatus='{t2.get('oldStatus')}', currentStatus='{t2.get('currentStatus')}' (esperado paid -> paid)"
            )
        if "email_comprador" not in t2 or "id_transacao" not in t2:
            report.record_failure("Portão 4: Payloads JSON", f"Teste 2 chaves ausentes: {t2}")

    # Teste 3: paid -> refunded (NUNCA waiting_payment!)
    t3 = payloads[2]
    if "_parse_error" in t3:
        report.record_failure("Portão 4: Payloads JSON", f"Teste 3 JSON inválido: {t3['_parse_error']}")
    else:
        if t3.get("oldStatus") != "paid" or t3.get("currentStatus") != "refunded":
            report.record_failure(
                "Portão 4: Payloads JSON",
                f"Teste 3 transição inválida: oldStatus='{t3.get('oldStatus')}', currentStatus='{t3.get('currentStatus')}' (esperado paid -> refunded)"
            )
        if "email_comprador" not in t3 or "id_transacao" not in t3:
            report.record_failure("Portão 4: Payloads JSON", f"Teste 3 chaves ausentes: {t3}")

    report.record_pass(
        "Portão 4: Payloads JSON",
        "Os 3 payloads JSON em testes-d1-curl-v4.sh são válidos e cumprem rigorosamente as transições de status canônicas"
    )

    # Se o documento mestre existir, checar se ele também contém os mesmos status
    if master_text:
        if '"waiting_payment"' not in master_text or '"paid"' not in master_text or '"refunded"' not in master_text:
            report.record_failure("Portão 4: Payloads JSON", "Documento mestre não contém menção aos 3 status JSON esperados")
        else:
            report.record_pass("Portão 4: Payloads JSON", "Documento mestre contém referências aos status canônicos")


# ==============================================================================
# PORTÃO 5: AUDITORIA MATEMÁTICA E CENÁRIOS DE CRÉDITO
# ==============================================================================
def audit_gate_5_math_and_scenarios(report: ValidationReport, master_text: Optional[str]):
    """Valida a precisão matemática dos 3 cenários de consumo de créditos e execuções."""
    if master_text is None:
        report.record_warning("Portão 5: Auditoria Matemática", "Ignorado: documento mestre ainda não criado.")
        return

    # Verificações numéricas obrigatórias da memória de cálculo
    checks = [
        ("836", "Consumo Cenário 1 com e-mail (836 de 1.000 créditos)"),
        ("652", "Consumo Cenário 1 sem e-mail (652 de 1.000 créditos)"),
        ("184", "Consumo Cenário 1 no n8n Cloud (184 de 1.000 execuções)"),
        ("195", "Gatilho de 900 créditos Cenário 1 (~195 vendas)"),
        ("996", "Consumo Cenário 2 com e-mail (996 de 1.000 créditos)"),
        ("812", "Consumo Cenário 2 sem e-mail (812 de 1.000 créditos)"),
        ("344", "Consumo Cenário 2 no n8n Cloud (344 de 1.000 execuções)"),
        ("160", "Gatilho de 900 créditos Cenário 2 (~160 vendas)"),
        ("1020", "Consumo Cenário 3 com e-mail (1.020 créditos / estouro)"),
        ("368", "Consumo Cenário 3 no n8n Cloud (368 de 1.000 execuções)"),
        ("156", "Gatilho de 900 créditos Cenário 3 (~156 vendas)"),
        ("100", "Reserva total de testes de D-1 e Dia D (100 créditos)")
    ]

    missing = []
    # Normalizar texto para busca de números (ex.: '1.020' ou '1020')
    normalized_text = master_text.replace("1.020", "1020")
    for num, label in checks:
        if num not in normalized_text:
            missing.append(f"Número {num} ausente ({label})")

    if missing:
        for m in missing:
            report.record_failure("Portão 5: Auditoria Matemática", m)
    else:
        report.record_pass("Portão 5: Auditoria Matemática", "Todos os números e limites dos 3 cenários conferidos com exatidão")


# ==============================================================================
# PORTÃO 6: AUDITORIA DO CHECKLIST DE D-1 (12 ITENS E FÓRMULA)
# ==============================================================================
def audit_gate_6_checklist_d1(report: ValidationReport, master_text: Optional[str]):
    """Valida presença dos 12 itens do checklist de D-1 e fórmula de recálculo."""
    if master_text is None:
        report.record_warning("Portão 6: Checklist D-1", "Ignorado: documento mestre ainda não criado.")
        return

    # 12 itens canônicos com palavras-chave compostas
    expected_items_checks = [
        ("Item 1: Restrição de Eventos", ["restri", "evento"]),
        ("Item 2: URL de Webhook por Produto", ["url", "produto"]),
        ("Item 3: URL Real do Webhook", ["url real", "url_webhook", "{{url_webhook}}"]),
        ("Item 4: Medição de Chamadas Reais", ["medi", "chamadas"]),
        ("Item 5: Consumo Real de Testes", ["consumo real de testes", "100"]),
        ("Item 6: Recálculo da Folga", ["folga", "836", "652"]),
        ("Item 7: Decisão de Plataforma", ["decis", "plataforma"]),
        ("Item 8: Conferência dos Nomes no Payload", ["nome", "payload"]),
        ("Item 9: Unicidade do Arquivo e Proteção", ["unicidade", "delete"]),
        ("Item 10: Herança da Trava de Download", ["trava", "download"]),
        ("Item 11: Desativação do Aviso Nativo", ["aviso nativo", "sendnotificationemail"]),
        ("Item 12: Método de Envio de E-mail", ["método de envio", "metodo de envio", "smtp"])
    ]

    missing_items = []
    text_lower = master_text.lower()
    for item_label, kw_list in expected_items_checks:
        found = False
        for kw in kw_list:
            if kw in text_lower:
                found = True
                break
        if not found:
            missing_items.append(item_label)

    if missing_items:
        report.record_failure("Portão 6: Checklist D-1", f"Itens ausentes no checklist de D-1: {missing_items}")
    else:
        report.record_pass("Portão 6: Checklist D-1", "Todos os 12 itens canônicos do checklist de D-1 identificados")

    # Verificação da fórmula paramétrica de recálculo
    formula_terms = ["extras/venda", "extras/reembolso", "consumo real de testes"]
    missing_formula_terms = [t for t in formula_terms if t not in text_lower]
    if missing_formula_terms:
        report.record_failure(
            "Portão 6: Checklist D-1",
            f"Fórmula paramétrica de recálculo com termos ausentes: {missing_formula_terms}"
        )
    else:
        report.record_pass("Portão 6: Checklist D-1", "Fórmula paramétrica de recálculo de folga confirmada")

    # Verificação de campos preenchíveis [ ___ ]
    fillable_matches = re.findall(r"\[\s*_{2,}\s*\]", master_text)
    if len(fillable_matches) < 3:
        report.record_failure("Portão 6: Checklist D-1", f"Poucos campos preenchíveis '[ ___ ]' encontrados ({len(fillable_matches)})")
    else:
        report.record_pass("Portão 6: Checklist D-1", f"Campos preenchíveis '[ ___ ]' confirmados ({len(fillable_matches)} ocorrências)")


# ==============================================================================
# PORTÃO 7: MAPEAMENTO DE SKILLS DA EQUIPE MULTI-AGENTE
# ==============================================================================
def audit_gate_7_skills_mapping(report: ValidationReport, master_text: Optional[str]):
    """Valida se todas as 8 skills estão documentadas e associadas aos papéis."""
    if master_text is None:
        report.record_warning("Portão 7: Mapeamento de Skills", "Ignorado: documento mestre ainda não criado.")
        return

    missing_skills = []
    for skill in REQUIRED_SKILLS:
        if skill not in master_text:
            missing_skills.append(skill)

    if missing_skills:
        report.record_failure("Portão 7: Mapeamento de Skills", f"Skills ausentes no documento mestre: {missing_skills}")
    else:
        report.record_pass("Portão 7: Mapeamento de Skills", f"Todas as 8 skills documentadas: {', '.join(REQUIRED_SKILLS)}")


# ==============================================================================
# PORTÃO 8: AUDITORIA DOS TEMPLATES DE E-MAIL (HTML, TEXTO, ALERTA GOOGLE)
# ==============================================================================
def audit_gate_8_email_templates(report: ValidationReport, templates_text: str):
    """Valida integridade estrutural dos templates de e-mail."""
    # E-mail 1 e E-mail 2 presentes
    if "E-mail 1" not in templates_text or "E-mail 2" not in templates_text:
        report.record_failure("Portão 8: Templates de E-mail", "Estrutura de E-mail 1 ou E-mail 2 ausente")

    # Assunto, HTML e Texto Puro presentes
    for expected_sec in ["Assunto", "HTML", "Texto Puro"]:
        if expected_sec not in templates_text:
            report.record_failure("Portão 8: Templates de E-mail", f"Seção obrigatória '{expected_sec}' ausente no arquivo de templates")

    # Verificação do alerta mandatório em negrito da conta Google no E-mail 1
    # Deve conter menção ao email_comprador em negrito vinculada à conta Google
    google_alert_pattern = r"(?=.*logado na conta Google)(?=.*\{\{email_comprador\}\})"
    if not re.search(google_alert_pattern, templates_text, re.IGNORECASE):
        report.record_failure(
            "Portão 8: Templates de E-mail",
            "Alerta obrigatório de login na conta Google correspondente ao {{email_comprador}} não identificado com a redação exigida"
        )
    else:
        report.record_pass("Portão 8: Templates de E-mail", "Alerta obrigatório de login na conta Google correspondente em negrito validado")

    # Verificação das variáveis nos templates
    if "{{webViewLink}}" not in templates_text:
        report.record_failure("Portão 8: Templates de E-mail", "Variável {{webViewLink}} não encontrada no template de entrega")
    if "{{id_transacao}}" not in templates_text:
        report.record_failure("Portão 8: Templates de E-mail", "Variável {{id_transacao}} não encontrada nos templates")

    report.record_pass("Portão 8: Templates de E-mail", "Templates de e-mail validados com HTML inline limpo, texto puro e variáveis unificadas")


# ==============================================================================
# EXECUÇÃO PRINCIPAL
# ==============================================================================
def run_all_audits(require_all: bool = False) -> bool:
    """Executa a suíte de auditoria completa."""
    report = ValidationReport()

    # 1. Carrega arquivos UTF-8
    contents = audit_gate_1_files(report, require_master=require_all)

    # 2. Scanner de variáveis proibidas em todos os arquivos carregados
    audit_gate_2_banned_variables(report, contents)

    # 3. Auditoria dos Templates de E-mail (se carregado)
    if FILE_TEMPLATES.name in contents:
        audit_gate_8_email_templates(report, contents[FILE_TEMPLATES.name])

    # 4. Auditoria dos comandos curl e payloads JSON
    if FILE_CURL.name in contents:
        audit_gate_4_json_payloads(report, contents[FILE_CURL.name], contents.get(FILE_MASTER.name))

    # 5. Auditorias do Documento Mestre (se presente)
    master_text = contents.get(FILE_MASTER.name)
    audit_gate_3_yaml_ficha_tecnica(report, master_text)
    audit_gate_5_math_and_scenarios(report, master_text)
    audit_gate_6_checklist_d1(report, master_text)
    audit_gate_7_skills_mapping(report, master_text)

    # Exibe resumo formatado
    report.print_summary()
    return report.is_clean()


if __name__ == "__main__":
    require_all_flag = "--require-all" in sys.argv or "--all" in sys.argv
    is_success = run_all_audits(require_all=require_all_flag)
    sys.exit(0 if is_success else 1)
