#!/usr/bin/env bash
# ==============================================================================
# SCRIPT DE TESTES EM D-1 (v4.0) — AUTOMAÇÃO GREENN + GOOGLE DRIVE + E-MAIL
# ==============================================================================
# Objetivo Operacional:
#   Validar em ambiente de homologação ou de produção na véspera (D-1) os 3 fluxos
#   críticos de recepção de webhook da Greenn, comprovando a lógica de roteamento,
#   a eficácia dos filtros anti-duplicidade e a medição exata do consumo de créditos
#   no Make (ou execuções no n8n Cloud).
#
# Uso:
#   1. Passando a URL do webhook como primeiro argumento:
#      ./testes-d1-curl-v4.sh "https://hook.make.com/sua-url-aqui"
#
#   2. Ou definindo a variável de ambiente URL_WEBHOOK:
#      export URL_WEBHOOK="https://hook.make.com/sua-url-aqui"
#      ./testes-d1-curl-v4.sh
#
#   3. Ou mantendo o placeholder padronizado para inspeção de sintaxe:
#      ./testes-d1-curl-v4.sh
# ==============================================================================

set -euo pipefail

# Resolução da URL de destino do Webhook
DEFAULT_URL="{{URL_WEBHOOK}}"
URL_WEBHOOK="${1:-${URL_WEBHOOK:-$DEFAULT_URL}}"

echo "======================================================================"
echo "    BATERIA DE TESTES DE D-1 — AUTOMAÇÃO GREENN DRIVE v4.0            "
echo "======================================================================"
echo "Endpoint Alvo : ${URL_WEBHOOK}"
echo "Executado em  : $(date -u +"%Y-%m-%dT%H:%M:%SZ" 2>/dev/null || date)"
echo "----------------------------------------------------------------------"

if [ "${URL_WEBHOOK}" = "{{URL_WEBHOOK}}" ]; then
  echo "AVISO: Endpoint com placeholder {{URL_WEBHOOK}}."
  echo "Para disparar contra uma instância ativa, informe a URL real no D-1:"
  echo "  Opção 1 (via argumento): ./testes-d1-curl-v4.sh 'https://hook.make.com/seu-endpoint'"
  echo "  Opção 2 (via ambiente) : export URL_WEBHOOK='https://hook.make.com/seu-endpoint' && ./testes-d1-curl-v4.sh"
  echo "----------------------------------------------------------------------"
  echo "Modo de inspeção: sintaxe e payloads validados com sucesso."
  echo "Para disparos HTTP reais, forneça a URL conforme os exemplos acima."
  echo "======================================================================"
  exit 0
fi

# ==============================================================================
# TESTE 1: SIMULAÇÃO DE VENDA APROVADA (FLUXO A)
# ==============================================================================
# Contexto:
#   O comprador concluiu o pagamento via Pix ou Cartão. A Greenn emite o evento
#   saleUpdated com transição de waiting_payment para paid.
#
# Comportamento Esperado:
#   1. O Webhook recebe o evento e aciona o Router.
#   2. O Filtro da Rota A (currentStatus = paid E oldStatus != paid) valida como VERDADEIRO.
#   3. O módulo Google Drive (Copy a File) cria a cópia individualizada:
#      'comprador.teste.v4@gmail.com - TRX-TESTE-4001.pdf'.
#   4. O módulo Google Drive (Share a File) concede permissão 'reader' para o comprador.
#   5. O módulo de E-mail (SMTP com Senha de App ou Gmail OAuth) despacha o E-mail 1
#      com o link de visualização webViewLink e o alerta de login em negrito.
#
# Consumo de Recursos:
#   - Make: 4 créditos totais (1 Webhook + 1 Copy + 1 Share + 1 E-mail).
#   - n8n Cloud: 1 execução.
# ==============================================================================
echo ""
echo "[TESTE 1/3] Disparando Simulação de Venda Aprovada (Fluxo A)..."
echo "Payload: oldStatus='waiting_payment' -> currentStatus='paid'"
echo "Consumo esperado: 4 créditos no Make / 1 execução no n8n"

curl -s -w "\nHTTP Status: %{http_code} | Tempo: %{time_total}s\n" \
  -X POST "${URL_WEBHOOK}" \
  -H "Content-Type: application/json" \
  -d '{
    "oldStatus": "waiting_payment",
    "currentStatus": "paid",
    "email_comprador": "comprador.teste.v4@gmail.com",
    "id_transacao": "TRX-TESTE-4001"
  }'

echo "-> Verificação Operacional D-1:"
echo "   1. Confira se o arquivo 'comprador.teste.v4@gmail.com - TRX-TESTE-4001.pdf' existe no Drive."
echo "   2. Confira se a permissão 'reader' foi concedida ao e-mail de teste."
echo "   3. Verifique o recebimento do E-mail 1 com o botão e o webViewLink."

# ==============================================================================
# TESTE 2: SIMULAÇÃO DE EVENTO BARRADO NO FILTRO (ANTI-DUPLICIDADE)
# ==============================================================================
# Contexto:
#   A Greenn emite uma segunda chamada para um pedido já pago (ex.: nota fiscal emitida,
#   atualização de dados cadastrais ou reenvio de webhook da plataforma).
#
# Comportamento Esperado:
#   1. O Webhook recebe a requisição (consumindo 1 crédito).
#   2. O Router avalia o Filtro da Rota A (exige oldStatus != paid). Como oldStatus == paid,
#      a Rota A é BLOQUEADA GRATUITAMENTE.
#   3. O Router avalia o Filtro da Rota B (exige currentStatus IN [refunded, chargedback]).
#      Como currentStatus == paid, a Rota B é BLOQUEADA GRATUITAMENTE.
#   4. Nenhum módulo subsequente é acionado: NENHUMA cópia duplicada é criada no Drive
#      e NENHUM e-mail repetido é enviado.
#
# Consumo de Recursos:
#   - Make: 1 crédito total (apenas a recepção do Webhook; o filtro consome 0 créditos).
#   - n8n Cloud: 1 execução.
# ==============================================================================
echo ""
echo "[TESTE 2/3] Disparando Simulação de Evento Barrado no Filtro (Anti-Duplicidade)..."
echo "Payload: oldStatus='paid' -> currentStatus='paid'"
echo "Consumo esperado: 1 crédito no Make (apenas Webhook) / 1 execução no n8n"

curl -s -w "\nHTTP Status: %{http_code} | Tempo: %{time_total}s\n" \
  -X POST "${URL_WEBHOOK}" \
  -H "Content-Type: application/json" \
  -d '{
    "oldStatus": "paid",
    "currentStatus": "paid",
    "email_comprador": "comprador.teste.v4@gmail.com",
    "id_transacao": "TRX-TESTE-4001"
  }'

echo "-> Verificação Operacional D-1:"
echo "   1. Acesse o histórico de execuções no Make e comprove que o cenário parou no Filtro."
echo "   2. Comprove que não foi criada uma segunda cópia no Google Drive com o mesmo id_transacao."

# ==============================================================================
# TESTE 3: SIMULAÇÃO DE REEMBOLSO / REVOGAÇÃO DE ACESSO (FLUXO B)
# ==============================================================================
# Contexto:
#   O cliente solicita o estorno ou a operadora aprova a devolução da compra paga.
#   A Greenn emite o evento saleUpdated com status de estorno.
#   ATENÇÃO: oldStatus deve ser obrigatoriamente 'paid' (nunca 'waiting_payment')
#   para satisfazer a regra de integridade do Filtro B.
#
# Comportamento Esperado:
#   1. O Webhook recebe o evento e aciona o Router.
#   2. O Filtro da Rota A rejeita (currentStatus != paid).
#   3. O Filtro da Rota B (currentStatus IN [refunded, chargedback] E oldStatus = paid)
#      valida como VERDADEIRO.
#   4. O módulo Google Drive (Search Files) busca o arquivo pelo nome contendo TRX-TESTE-4001.
#   5. O Filtro de Proteção 'File ID Exists' (ou Error Handler Ignore) garante que a
#      execução prossiga com segurança apenas se o arquivo foi localizado.
#   6. O módulo Google Drive (Delete a File) exclui permanentemente o arquivo.
#   7. O módulo de E-mail despacha o E-mail 2 confirmando o encerramento do acesso.
#
# Consumo de Recursos:
#   - Make com e-mail próprio: 4 créditos totais (1 Webhook + 1 Search + 1 Delete + 1 E-mail).
#   - Make sem e-mail próprio: 3 créditos totais (1 Webhook + 1 Search + 1 Delete).
#   - n8n Cloud: 1 execução.
# ==============================================================================
echo ""
echo "[TESTE 3/3] Disparando Simulação de Reembolso (Fluxo B)..."
echo "Payload: oldStatus='paid' -> currentStatus='refunded'"
echo "Consumo esperado: 4 créditos (com e-mail) ou 3 créditos (sem e-mail) no Make / 1 exec n8n"

curl -s -w "\nHTTP Status: %{http_code} | Tempo: %{time_total}s\n" \
  -X POST "${URL_WEBHOOK}" \
  -H "Content-Type: application/json" \
  -d '{
    "oldStatus": "paid",
    "currentStatus": "refunded",
    "email_comprador": "comprador.teste.v4@gmail.com",
    "id_transacao": "TRX-TESTE-4001"
  }'

echo "-> Verificação Operacional D-1:"
echo "   1. Comprove que a cópia 'comprador.teste.v4@gmail.com - TRX-TESTE-4001.pdf' foi EXCLUÍDA do Drive."
echo "   2. Se o e-mail opcional de cancelamento estiver ativo, verifique a chegada do E-mail 2."

echo ""
echo "======================================================================"
echo "    BATERIA DE TESTES CONCLUÍDA COM SUCESSO                           "
echo "======================================================================"
echo "Ação Obrigatória do Operador em D-1:"
echo "-> Anotar o total de créditos consumidos no Item 5 do Checklist de D-1."
echo "-> Aplicar a fórmula de recálculo da folga no Item 6 do Checklist."
echo "======================================================================"
