# Automação Greenn + Google Drive + E-mail (Teste Grátis — v4.0)

Especificação técnica final de **D-1** e artefatos operacionais para entrega automatizada e revogação de acesso de PDF via **Greenn**, **Google Drive** e **E-mail**, projetada para rodar a **custo US$ 0** no plano gratuito do **Make** (1.000 créditos/mês, 1 cenário único com Router) ou no trial de 14 dias do **n8n Cloud** (1.000 execuções).

---

## 📂 Estrutura do Repositório

| Arquivo | Descrição |
| :--- | :--- |
| [`automacao-greenn-drive-teste-gratis-v4.md`](./automacao-greenn-drive-teste-gratis-v4.md) | **Especificação Técnica Completa (v4.0)**: Resumo Executivo (Cenários 1, 2 e 3), Histórico v3.0 → v4.0, Ficha Técnica YAML, Arquitetura com Router (Fluxos A e B), Checklist de Execução de D-1 (`[ ___ ]`), Cronograma Operacional, Matriz de Contingência, Matriz de 12 Riscos e Mapeamento de Skills Multi-Agente. |
| [`templates-email-v4.md`](./templates-email-v4.md) | **Templates de E-mail (Português)**: Assunto, HTML Simples e Texto Puro para o **E-mail 1 (Entrega — Fluxo A)** e **E-mail 2 (Reembolso/Cancelamento — Fluxo B)** com variáveis padronizadas (`{{email_comprador}}`, `{{id_transacao}}`, `{{webViewLink}}`). |
| [`testes-d1-curl-v4.sh`](./testes-d1-curl-v4.sh) | **Bateria de Testes `curl` para D-1**: Comandos e payloads JSON para simulação de Venda Aprovada (`waiting_payment` → `paid`), Evento Duplicado Barrado (`paid` → `paid`) e Reembolso (`paid` → `refunded`). |
| [`validate_v4_artifacts.py`](./validate_v4_artifacts.py) | **Validador Automatizado (8 Portões)**: Auditoria programática do bloco YAML, cálculos matemáticos dos 3 cenários, ausência de variáveis legadas e validação de sintaxe JSON dos comandos `curl`. |
| [`tests/`](./tests/) | **Suíte de Testes Unitários e de Estresse**: 25 testes automatizados (`unittest`) validando a especificação e as fórmulas paramétricas de créditos. |

---

## 📊 Resumo dos Cenários (160 Vendas + 24 Reembolsos + 100 Créditos de Reserva)

| Cenário | Premissa de Chamadas | Make (Com E-mail) | Make (Sem E-mail) | Gatilho de 900 Créditos (Com E-mail) | n8n Cloud (Fora Testes) |
| :--- | :--- | :---: | :---: | :---: | :---: |
| **Cenário 1 (Base)** | 1 chamada/venda + 1 chamada/reembolso | **836 / 1.000** *(folga: 164)* | **652 / 1.000** *(folga: 348)* | **~195 vendas** *(4,6 cr/venda)* | **184 / 1.000 execuções** |
| **Cenário 2 (Extra na Venda)** | 2 chamadas/venda (+160) + 1 chamada/reembolso | **996 / 1.000** *(folga: 4)* | **812 / 1.000** *(folga: 188)* | **~160 vendas** *(5,6 cr/venda)* | **344 / 1.000 execuções** |
| **Cenário 3 (Extra Venda + Reembolso)** | 2 chamadas/venda (+160) + 2 chamadas/reembolso (+24) | **1.020 / 1.000** *(estouro: -20)* | **836 / 1.000** *(folga: 164)* | **~156 vendas** *(5,75 cr/venda)* | **368 / 1.000 execuções** |

---

## 🚀 Como Executar a Validação e os Testes de D-1

### 1. Validar todos os artefatos da v4.0
```bash
python validate_v4_artifacts.py --require-all
python -m unittest discover -s tests -v
```

### 2. Inspecionar ou disparar os testes `curl` em D-1
```bash
# Modo de inspeção segura (Dry-Run — exibe os comandos sem disparar requisições)
bash testes-d1-curl-v4.sh

# Disparo real contra o Webhook configurado no Make ou n8n
bash testes-d1-curl-v4.sh "https://hook.us1.make.com/SEU_ENDPOINT_REAL"
```
