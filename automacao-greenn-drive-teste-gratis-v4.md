# Especificação Técnica de Produção e Arquitetura de Automação (v4.0)
## Entrega Segura de Infoproduto via Greenn + Google Drive + E-mail
**Projeto:** `automacao-greenn-drive-teste-gratis`  
**Versão:** 4.0  
**Data de Emissão:** 2026-10-20  
**Status:** Oficial / Homologado para D-1 e Produção  
**Padrão de Variáveis:** Canônicas e Unificadas  
**Codificação:** UTF-8  

---

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

---

## 1. Resumo Executivo & Tabela Comparativa de Cenários

### 1.1 Contexto e Premissas do Lançamento
O presente documento estabelece a especificação técnica definitiva para a automação de entrega e revogação de infoproduto digital em PDF sob o modelo de **Lançamento de 1 Dia**, atendendo às seguintes premissas operacionais:
- **Volume Esperado de Compradores:** 160 vendas aprovadas.
- **Taxa Estimada de Reembolsos/Chargebacks:** 15% das vendas = 24 transações de estorno.
- **Orçamento Operacional:** Custo US$ 0 utilizando a camada gratuita do **Make** (1.000 créditos/mês, 2 cenários ativos) com retaguarda arquitetada no **n8n Cloud Trial de 14 dias** (1.000 execuções de workflows).
- **Reserva Técnica Obrigatória de Testes:** **100 créditos** alocados estritamente para homologação na véspera (D-1) e testes pontuais no Dia D.
- **Entrega e Segurança:** 1 arquivo PDF mestre original replicado em cópias exclusivas por transação no Google Drive com papel `reader` e travas de proteção contra cópia/impressão/download vinculadas à conta Google do comprador (`{{email_comprador}}`).

---

### 1.2 Tabela Comparativa Lado a Lado dos 3 Cenários Operacionais

A tabela abaixo compara o comportamento de consumo, folga e limites nos três cenários operacionais, destacando o impacto de chamadas intermediárias de webhook emitidas pela Greenn:

| Dimensão / Parâmetro Operacional | Cenário 1: Base (1 chamada / venda, 1 chamada / reembolso) | Cenário 2: Chamada Extra na Venda (2 chamadas / venda, 1 / reembolso) | Cenário 3: Extra na Venda E no Reembolso (2 chamadas / venda, 2 / reembolso) |
|---|:---:|:---:|:---:|
| **Chamadas de Webhook por Venda** | 1 chamada (`waiting_payment` → `paid`) | 2 chamadas (+1 barrada no Filtro A) | 2 chamadas (+1 barrada no Filtro A) |
| **Chamadas de Webhook por Reembolso** | 1 chamada (`paid` → `refunded`) | 1 chamada (`paid` → `refunded`) | 2 chamadas (+1 barrada no Filtro B) |
| **Consumo em 160 Vendas (com E-mail)** | 160 × 4 = **640 créditos** | 160 × (4 + 1) = **800 créditos** | 160 × (4 + 1) = **800 créditos** |
| **Consumo em 160 Vendas (sem E-mail)** | 160 × 3 = **480 créditos** | 160 × (3 + 1) = **640 créditos** | 160 × (3 + 1) = **640 créditos** |
| **Consumo em 24 Reembolsos (com E-mail)** | 24 × 4 = **96 créditos** | 24 × 4 = **96 créditos** | 24 × (4 + 1) = **120 créditos** |
| **Consumo em 24 Reembolsos (sem E-mail)** | 24 × 3 = **72 créditos** | 24 × 3 = **72 créditos** | 24 × (3 + 1) = **96 créditos** |
| **Reserva Obrigatória de Testes (D-1 + Dia D)** | **100 créditos** | **100 créditos** | **100 créditos** |
| **Total Consumido Make com E-mail Próprio** | **836 de 1.000 créditos** | **996 de 1.000 créditos** | **1.020 de 1.000 créditos** |
| **Folga Operacional no Make (com E-mail)** | **+164 créditos** (Folga Segura) | **+4 créditos** (Folga Crítica) | **-20 créditos (ESTOURO DE COTA!)** |
| **Total Consumido Make sem E-mail Próprio** | **652 de 1.000 créditos** | **812 de 1.000 créditos** | **836 de 1.000 créditos** |
| **Folga Operacional no Make (sem E-mail)** | **+348 créditos** (Folga Ampla) | **+188 créditos** (Folga Confortável) | **+164 créditos** (Folga Segura) |
| **Consumo Médio Ponderado por Venda** | (1 × 4) + (0,15 × 4) = **4,6 créditos/venda** | (1 × 5) + (0,15 × 4) = **5,6 créditos/venda** | (1 × 5) + (0,15 × 5) = **5,75 créditos/venda** |
| **Gatilho de Upgrade aos 900 Créditos** | 900 ÷ 4,6 ≈ **~195 vendas** | 900 ÷ 5,6 ≈ **~160 vendas** | 900 ÷ 5,75 ≈ **~156 vendas** |
| **Consumo de Execuções no n8n Cloud** | 160 + 24 = **184 de 1.000 execuções** | 320 + 24 = **344 de 1.000 execuções** | 320 + 48 = **368 de 1.000 execuções** |
| **Folga de Execuções no n8n Cloud** | **+816 execuções** restantes | **+656 execuções** restantes | **+632 execuções** restantes |

---

### 1.3 Conclusões Estratégicas do Resumo Executivo
1. **Cenário 1 (Base Ideal):** Opera com folga de 164 créditos com envio de e-mail próprio ativo. Permite absorver os 160 compradores e 24 reembolsos sem necessidade de intervenção manual ou corte de recursos.
2. **Cenário 2 (Pico de Webhooks em Pix/Boleto):** A emissão de chamadas intermediárias de status (geração de Pix/boleto antes do pagamento) consome 160 créditos adicionais na recepção do Webhook. Com e-mail próprio, a folga cai para míseros 4 créditos. **Mitigação imediata em D-1:** Ao constatar 2 chamadas/venda nos testes, corta-se preventivamente o módulo de e-mail próprio, recuperando 188 créditos de folga segura (812/1.000 créditos consumidos).
3. **Cenário 3 (Chamadas Múltiplas em Vendas e Reembolsos):** Se ocorrerem 2 chamadas por venda e 2 chamadas por reembolso (ex.: status intermediário de contestação antes do estorno definitivo), o consumo atinge 1.020 créditos com e-mail próprio, resultando em **estouro imediato do plano gratuito em 20 créditos**. **Diretriz Mandatória:** Desligar o módulo de e-mail próprio no Make reduz o consumo para 836 créditos (folga de 164 créditos), mantendo o lançamento 100% no plano gratuito.
4. **Critério Rígido para n8n Cloud:** O chaveamento para o n8n Cloud Trial (14 dias) só deve ser executado se as medições em D-1 apontarem consumo no Make superior a 1.000 créditos **mesmo com o módulo de e-mail próprio totalmente desligado** (exemplo: se a Greenn emitir 3 ou mais chamadas por venda).

---

## 2. Histórico de Alterações Estruturais (v3.0 → v4.0)

A evolução da versão 3.0 para a versão 4.0 reflete um processo cirúrgico de simplificação arquitetural, eliminação de pontos únicos de falha e blindagem de segurança:

### 2.1 Ponto 1: Exclusividade Greenn e Remoção de Canais Externos
- **Eliminação de Canais Fragmentados:** Foram removidas completamente as integrações com WhatsApp (Z-API, Evolution, Baileys), Telegram Bot API e gateways de SMS. Esses canais adicionavam custos de mensalidade, fragilidade operacional por bloqueio de chips e risco de entrega desincronizada.
- **Remoção de Campos Fictícios:** O campo inexistente na API da Greenn para canal preferencial foi definitivamente extinto.
- **Entrega Centralizada e Determinística:** Toda a governança de acesso e notificação foi unificada no **Google Drive com Notificação por E-mail**. Como o arquivo físico reside no Drive e a permissão de leitura (`reader`) é concedida exclusivamente ao endereço de e-mail informado no checkout da Greenn (`{{email_comprador}}`), o e-mail passa a ser o canal canônico de entrega e suporte ao aluno.

### 2.2 Ponto 2: Filtros Anti-Duplicidade para o Evento `saleUpdated` da Greenn
- **Idempotência no Topo do Fluxo:** O gateway da Greenn trabalha preferencialmente com o evento abrangente `saleUpdated`, notificando alterações de status da transação. Sem filtros rígidos, atualizações cadastrais ou disparos duplicados poderiam recriar cópias no Drive e reenviar mensagens.
- **Regras Matemáticas dos Filtros:**
  - **Fluxo A (Venda Aprovada):** `currentStatus = paid` E `oldStatus != paid` (impede reprocessamento de vendas já pagas).
  - **Fluxo B (Reembolso/Chargeback):** `currentStatus IN [refunded, chargedback]` E `oldStatus = paid` (impede cancelamentos de pedidos nunca pagos ou múltiplos disparos para a mesma devolução).
- **Gratuidade dos Filtros no Make:** O módulo de filtro entre nós no Make consome **0 créditos**.
- **Custo Operacional Efetivo:**
  - Com envio de e-mail ativo: 1 crédito de Webhook + 3 créditos pós-filtro (Copy + Share + Email no Fluxo A; Search + Delete + Email no Fluxo B) = **4 créditos por execução completa**.
  - Sem envio de e-mail próprio: 1 crédito de Webhook + 2 créditos pós-filtro (Copy + Share no Fluxo A; Search + Delete no Fluxo B) = **3 créditos por execução completa**.
  - Chamada barrada pelo filtro: consome estritamente **1 crédito** da requisição HTTP do Webhook, interrompendo a cadeia a custo zero subsequente.

### 2.3 Ponto 3: Impacto de Chamadas Filtradas no Webhook e Arquitetura com Router
- **Regra de Faturamento do Webhook:** No Make, qualquer requisição HTTP recebida por um endpoint Custom Webhook ativo consome **1 crédito**, mesmo que a execução seja interrompida no primeiro filtro. No n8n Cloud, qualquer disparo de Webhook consome **1 execução**, independentemente do número de nós subsequentes executados.
- **Origem das Chamadas Extras:** Vendas geradas por Pix ou boleto frequentemente emitem uma chamada preliminar no checkout (ex.: `waiting_payment`), gerando 1 chamada adicional antes do pagamento aprovado (+160 créditos no Cenário 2). Da mesma forma, disputas ou status intermediários em reembolsos podem gerar chamadas prévias (+24 créditos no Cenário 3).
- **Restrição na Origem (Painel Greenn):** É mandatório configurar as regras do Webhook na Greenn para selecionar exclusivamente os eventos: `paid`, `refunded` e `chargedback`. Jamais selecionar a opção "todos os eventos".
- **Topologia de Cenário Único com Router:** Em vez de manter 2 cenários distintos (um para vendas e outro para estornos), a v4.0 unifica toda a automação em **1 único cenário ativo** utilizando o módulo **Router** logo após o Webhook.
  - O Router consome **0 créditos** no Make.
  - A automação consome apenas 1 dos 2 slots de cenários ativos permitidos no plano gratuito do Make, preservando 1 slot livre para testes ou contingência.
  - Contorna a limitação frequente da Greenn de permitir apenas 1 URL de webhook registrada por produto.

### 2.4 Ponto 4: Regras Práticas de D-1 e Robustez Operacional (Google Drive, E-mail e Reserva Técnica)
- **Restrição de Download/Impressão no Google Drive:** No arquivo original (PDF mestre), o produtor desmarca a opção *"Os visualizadores e comentadores podem ver a opção de transferir por download, imprimir e copiar"* (`copyRequiresWriterPermission: true`). Em D-1, valida-se se a cópia gerada herda essa configuração. Se a API não propagar a herança automaticamente, a diretriz é **aceitar o risco formalmente para o lançamento de 1 dia**, evitando adicionar chamadas de API extras que consumiriam +160 créditos no Make.
- **Supressão do Aviso Nativo do Drive (`sendNotificationEmail = false`):** Se o conector do Make não suportar a desativação do aviso nativo do Google Drive, a equipe decide entre aceitar o envio de 2 e-mails (aviso nativo + e-mail próprio) ou desativar o e-mail próprio no Make, reduzindo o consumo de 836 para 652 créditos no Cenário 1.
- **Fallback Seguro de E-mail via SMTP com Senha de App:** O conector nativo do Gmail via OAuth 2.0 frequentemente apresenta telas de alerta de "Aplicativo Não Verificado" (*Google hasn't verified this app*) ou revoga credenciais de teste em 7 dias no Google Cloud Console. A v4.0 padroniza o uso do módulo **Email (SMTP)** apontando para `smtp.gmail.com:465` (SSL) ou `587` (TLS) autenticado por uma **Senha de App de 16 caracteres**, garantindo conexão instantânea sem dependências de infraestrutura no GCP.
- **Proteção Anti-Falha no Fluxo B (File ID Exists / Error Handler):** Se um reembolso ocorrer antes da cópia existir ou o `Search Files` não localizar o PDF, a tentativa de excluir um ID nulo gera erro HTTP 404. É obrigatório configurar o **Filtro Gratuito `"File ID Exists"`** antes do módulo `Delete a File` OU configurar uma diretiva **Error Handler → Ignore / Resume** no `Delete a File`. Em caso de arquivo não localizado, a transação é registrada na planilha de controle e o fluxo é encerrado com sucesso.
- **Unicidade na Busca e Exclusão:** As cópias são criadas com nome padronizado `{{email_comprador}} - {{id_transacao}}.pdf`. A busca no `Search Files` utiliza estritamente o identificador único `{{id_transacao}}`.
- **Reserva Obrigatória de 100 Créditos:** Estabelece um teto de 100 créditos para os testes de homologação em D-1 e testes do Dia D, registrando o valor real no Checklist de D-1.

### 2.5 Ponto 5: Padronização Estrita de Variáveis e Regra Pós-D-1
- **Whitelist Fechada de 6 Variáveis:** Toda a especificação, os templates de e-mail e os comandos de teste adotam estritamente:
  1. `{{URL_WEBHOOK}}`: URL de entrada do webhook no Make / n8n.
  2. `{{email_comprador}}`: E-mail do comprador (conta Google).
  3. `{{id_transacao}}`: Identificador exclusivo da compra na Greenn.
  4. `{{webViewLink}}`: URL direta de leitura online gerada pelo Google Drive.
  5. `{{oldStatus}}`: Status anterior da transação no webhook.
  6. `{{currentStatus}}`: Status atual da transação no webhook.
- **Regra Pós-D-1 para Mapeamento de Payloads:** Os campos mapeados na documentação são marcados como `[CONFIRMAR COM PAYLOAD REAL]`. Durante a compra-teste de D-1, aciona-se o recurso *"Redetermine data structure"* no Make. Caso as chaves do payload real da Greenn apresentem estrutura aninhada (ex.: `data.buyer.email`), ajusta-se o mapeamento interno dos módulos no Make e os comandos `curl`, mantendo rigorosamente os nomes canônicos e a semântica na documentação.

### 2.6 Ponto 6: Memória de Cálculo Quantificada e Gatilho aos 900 Créditos
- Formalização detalhada dos cálculos matemáticos de consumo, limites de segurança e folgas para os 3 cenários operacionais, definindo com exatidão os pontos de corte de vendas para atingimento do patamar de alerta aos 900 créditos (~195 vendas no Cenário 1, ~160 vendas no Cenário 2 e ~156 vendas no Cenário 3).

---

## 3. Ficha Técnica Canônica em YAML (v4.0)

Abaixo encontra-se a Ficha Técnica em YAML 1.2 canônica contendo rigorosamente as 12 chaves exigidas para parametrização legível por máquina:

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

---

## 4. Arquitetura e Engenharia de Integração dos Fluxos A e B

### 4.1 Topologia de Cenário Único com Router no Make

A arquitetura do Make é estruturada em um único cenário que recebe todas as requisições através de um único endpoint e delega o processamento lógico via Router:

```
                               ┌────────────────────────────────┐
                               │   Greenn Webhook: saleUpdated  │
                               │  (Consumo: 1 crédito no Make)  │
                               └───────────────┬────────────────┘
                                               │
                                               ▼
                               ┌────────────────────────────────┐
                               │     Router Lógico do Make      │
                               │  (Consumo: 0 créditos no Make) │
                               └───────┬────────────────┬───────┘
                                       │                │
            ┌──────────────────────────┘                └──────────────────────────┐
            ▼                                                                      ▼
  [ ROTA A: Venda Aprovada ]                                             [ ROTA B: Reembolso / Estorno ]
  Filtro Anti-Duplicidade A (0 cr):                                      Filtro Anti-Duplicidade B (0 cr):
  currentStatus = paid AND oldStatus != paid                             currentStatus IN [refunded, chargedback]
            │                                                            AND oldStatus = paid
            ▼                                                                      │
  Google Drive: Copy a File (1 cr)                                                 ▼
  (Cria {{email_comprador}} - {{id_transacao}}.pdf)                      Google Drive: Search Files (1 cr)
            │                                                            (Busca arquivo pelo {{id_transacao}})
            ▼                                                                      │
  Google Drive: Share a File (1 cr)                                                ▼
  (Papel: reader para {{email_comprador}})                               Filtro: File ID Exists (0 cr)
            │                                                            (ou Error Handler: Ignore/Resume)
            ▼                                                                      │
  Email: Envio de Entrega (1 cr)                                                   ▼
  (Template E-mail 1 com {{webViewLink}})                                Google Drive: Delete a File (1 cr)
                                                                         (Exclusão física da cópia no Drive)
                                                                                   │
                                                                                   ▼
                                                                         Email: Confirmação de Estorno (1 cr - Opcional)
                                                                         (Template E-mail 2 de Encerramento)
```

---

### 4.2 Detalhamento Passo a Passo do Fluxo A (Venda Aprovada)

O Fluxo A é responsável pelo provisionamento seguro do PDF exclusivo e despacho das credenciais de acesso para o comprador:

1. **Recepção do Webhook (1 crédito no Make / 1 execução no n8n):**
   - O nó Webhook escuta em `{{URL_WEBHOOK}}` o evento `saleUpdated` disparado pelo checkout da Greenn.
   - O payload recebido contém os campos `oldStatus`, `currentStatus`, `email_comprador` e `id_transacao` `[CONFIRMAR COM PAYLOAD REAL]`.
2. **Avaliação do Filtro da Rota A (0 créditos no Make):**
   - **Expressão Lógica:** `currentStatus = "paid"` E `oldStatus != "paid"`.
   - Se a transição for verdadeira (ex.: `waiting_payment` → `paid` ou compra direta no cartão): a execução prossegue para a Rota A.
   - Se for um webhook de atualização de pedido já pago (`paid` → `paid`): o filtro bloqueia a execução. O cenário encerra com consumo de apenas 1 crédito (do Webhook), impedindo duplicidade no Drive.
3. **Google Drive — `Copy a File` (1 crédito no Make):**
   - **Arquivo Origem:** ID fixo do PDF mestre original armazenado no Drive do produtor.
   - **Pasta Destino:** Pasta dedicada do lançamento no Google Drive.
   - **Nome da Cópia:** `{{email_comprador}} - {{id_transacao}}.pdf`.
   - **Saídas Produzidas:** `fileId` (ID do arquivo gerado) e `webViewLink` (URL segura de visualização no navegador).
4. **Google Drive — `Share a File with Anyone / Add a Permission` (1 crédito no Make):**
   - **Parâmetro de Entrada:** `fileId` gerado no passo anterior.
   - **Tipo (`type`):** `user`.
   - **Papel (`role`):** `reader` (Leitor).
   - **E-mail do Destinatário (`emailAddress`):** `{{email_comprador}}`.
   - **Notificação Nativa:** Configurar `sendNotificationEmail = false` se suportado pelo módulo; caso contrário, aceitar o aviso nativo ou aplicar a decisão de D-1.
5. **Envio de E-mail Transacional de Entrega (1 crédito no Make — Opcional se usar aviso nativo):**
   - **Conector:** Módulo **Email (SMTP)** via `smtp.gmail.com:465` (com Senha de App de 16 caracteres) ou conector nativo do Gmail via OAuth.
   - **Destinatário:** `{{email_comprador}}`.
   - **Assunto:** `Seu material exclusivo está liberado! (Transação: {{id_transacao}})`.
   - **Corpo:** Template oficial do E-mail 1 com o botão apontando para `{{webViewLink}}` e aviso em negrito exigindo login na conta Google correspondente a `{{email_comprador}}`.

**Consumo Total do Fluxo A:**
- **Com E-mail Próprio:** 1 (Webhook) + 1 (Copy) + 1 (Share) + 1 (Email) = **4 créditos no Make** (1 execução no n8n).
- **Sem E-mail Próprio:** 1 (Webhook) + 1 (Copy) + 1 (Share) = **3 créditos no Make** (1 execução no n8n).

---

### 4.3 Detalhamento Passo a Passo do Fluxo B (Reembolso / Chargeback)

O Fluxo B é acionado em caso de cancelamento, devolução ou estorno pelo titular do cartão:

1. **Recepção do Webhook (1 crédito no Make / 1 execução no n8n):**
   - O nó Webhook recebe a requisição com status atualizado.
2. **Avaliação do Filtro da Rota B (0 créditos no Make):**
   - **Expressão Lógica:** `currentStatus IN ["refunded", "chargedback"]` E `oldStatus = "paid"`.
   - Se verdadeira: o comprador possuía acesso legítimo que agora deve ser revogado. O fluxo avança para a Rota B.
   - Se o cancelamento for de uma transação pendente que nunca foi paga (`waiting_payment` → `refunded`): o filtro bloqueia o fluxo a custo zero, pois nenhuma cópia foi criada no Drive.
3. **Google Drive — `Search Files` (1 crédito no Make):**
   - **Query de Busca:** `name contains '{{id_transacao}}' and trashed = false` (ou busca estrita pelo nome `{{email_comprador}} - {{id_transacao}}.pdf`).
   - **Retorno:** Lista de arquivos correspondentes contendo o `fileId` da cópia individual do aluno.
4. **Filtro de Proteção Pré-Exclusão e Tratamento de Erro (0 créditos no Make):**
   - **Filtro Pré-Delete (`File ID Exists`):** Verifica se `Search Files` retornou pelo menos 1 arquivo (`length(files[]) > 0` ou `fileId Exists`). Se nenhum arquivo for localizado, o filtro barra o fluxo a custo zero, impedindo erro de chamada com parâmetro nulo.
   - **Error Handler no `Delete a File`:** Caso ocorra erro na chamada de exclusão (ex.: erro 404 da API do Drive), configura-se uma diretiva **Error Handler → Ignore** (ou **Resume**), garantindo que o cenário não aborte de forma fatal.
   - **Auditoria:** Em caso de arquivo ausente, registrar o evento com `{{id_transacao}}` na planilha de controle do lançamento.
5. **Google Drive — `Delete a File` (1 crédito no Make):**
   - **Parâmetro de Entrada:** `fileId` localizado na busca.
   - **Ação:** Exclusão definitiva ou envio para a lixeira do Google Drive, revogando instantaneamente o acesso do aluno ao material.
6. **Envio de E-mail de Confirmação de Cancelamento (1 crédito no Make — Opcional):**
   - **Destinatário:** `{{email_comprador}}`.
   - **Assunto:** `Confirmação de Reembolso e Encerramento de Acesso (Transação: {{id_transacao}})`.
   - **Corpo:** Template oficial do E-mail 2 informando que o reembolso foi concluído e o acesso ao Drive foi encerrado.
   - *Nota de Economia:* Se este módulo de e-mail de reembolso for omitido, a operação economiza 24 créditos sobre o volume estimado de estornos.

**Consumo Total do Fluxo B:**
- **Com E-mail de Cancelamento:** 1 (Webhook) + 1 (Search) + 1 (Delete) + 1 (Email) = **4 créditos no Make** (1 execução no n8n).
- **Sem E-mail de Cancelamento:** 1 (Webhook) + 1 (Search) + 1 (Delete) = **3 créditos no Make** (1 execução no n8n).

---

## 5. Checklist de Execução e Registro de D-1 (Tabela Preenchível)

O Checklist de D-1 deve ser impresso ou preenchido digitalmente pelo responsável técnico na véspera do lançamento durante a bateria de testes práticos:

| # | Item de Verificação Operacional | Ação de Auditoria e Teste em D-1 | Campo Preenchível / Resultado Obtido |
|---|----------------------------------|----------------------------------|--------------------------------------|
| 1 | **Restrição de Eventos no Painel Greenn** | Acessar o painel da Greenn e confirmar que foram marcados estritamente os eventos `paid`, `refunded` e `chargedback`, sem selecionar eventos intermediários de checkout. | `Resultado: [ SIM / NÃO ]` |
| 2 | **URL de Webhook por Produto na Greenn** | Testar se o painel da Greenn aceita duas URLs de webhook distintas por produto ou se exige apenas uma URL unificada direcionada ao Router. | `Resultado: [ 1 URL (Router) / 2 URLs ]` |
| 3 | **URL Real do Webhook Gerada** | Inserir a URL de produção final gerada pelo módulo Custom Webhook do Make ou n8n Cloud. | `{{URL_WEBHOOK}} = [ ______________________ ]` |
| 4 | **Medição de Chamadas Reais** | Executar 1 compra-teste via Pix/Boleto e 1 estorno-teste na Greenn. Registrar o número de requisições que atingiram o log do webhook. | `Chamadas/venda: [ ___ ] \| Chamadas/reembolso: [ ___ ]` |
| 5 | **Consumo Real de Testes em D-1** | Registrar o total exato de créditos consumidos no painel do Make durante toda a bateria de testes de véspera (reserva total de testes = 100 créditos para D-1 + Dia D). | `consumo real de testes: [ ___ ] créditos (Se > 100 créditos, descontar o excedente da folga abaixo)` |
| 6 | **Recálculo da Folga de Créditos em D-1** | Aplicar a fórmula de projeção abaixo utilizando o número de chamadas extras medidas no item 4 (`extras/venda = chamadas/venda - 1`; `extras/reembolso = chamadas/reembolso - 1`) e o consumo real de testes do item 5: | `Com e-mail: 836 + (160 × [extras/venda]) + (24 × [extras/reembolso]) + ([consumo real de testes] - 100) = [ ___ ] créditos \| Sem e-mail: 652 + (160 × [extras/venda]) + (24 × [extras/reembolso]) + ([consumo real de testes] - 100) = [ ___ ] créditos \| Folga real: [ ___ ]` |
| 7 | **Decisão de Plataforma em D-1** | Avaliar se a folga recalculada no Make permaneceu positiva. *(Regra Inegociável: Migrar para o n8n Cloud Trial apenas se a folga no Make ficar negativa mesmo sem e-mail próprio).* | `Decisão: [ Make com e-mail / Make sem e-mail / Migrar para n8n Cloud ]` |
| 8 | **Conferência dos Nomes Reais no Payload** | Comparar o JSON capturado via "Redetermine data structure" com os identificadores canônicos `currentStatus`, `oldStatus`, `email_comprador`, `id_transacao`. | `Mapeamento ajustado: [ ___ ]` |
| 9 | **Unicidade do Arquivo na Busca e Proteção do `Delete a File` (Fluxo B)** | Confirmar que a cópia foi gerada como `{{email_comprador}} - {{id_transacao}}.pdf`, que o `Search Files` localiza apenas ela e que o filtro `File ID Exists` (ou Error Handler) está ativo no Delete com registro na planilha. | `Resultado: [ SIM / NÃO ]` |
| 10 | **Herança da Trava de Download** | Abrir a cópia de teste compartilhada com um perfil leitor e verificar se as opções de download, impressão e cópia de texto estão bloqueadas. | `Resultado: [ SIM / NÃO — Risco aceito ]` |
| 11 | **Desativação do Aviso Nativo do Drive** | Checar se a opção `sendNotificationEmail = false` suprimiu o e-mail automático do Google Drive. Caso não tenha suprimido, decidir o caminho. | `Resultado: [ SIM / NÃO — Decisão: Manter 2 e-mails / Cortar e-mail próprio ]` |
| 12 | **Método de Envio de E-mail Configurado** | Validar se o e-mail foi autenticado via SMTP com Senha de App de 16 caracteres em `smtp.gmail.com:465/587` sem telas de bloqueio de aplicativo não verificado. | `Resultado: [ SMTP com Senha de App / Gmail OAuth ]` |

---

## 6. Cronograma Operacional em 3 Fases (D-1, Dia D, Pós-Garantia)

O ciclo de vida operacional do lançamento é estruturado em três fases temporais bem delimitadas:

```
+----------------------------------------------------------------------------------------------------+
|                                    CRONOGRAMA OPERACIONAL v4.0                                     |
+------------------------------------+-----------------------------------+---------------------------+
|          FASE 1: D-1               |          FASE 2: DIA D            |   FASE 3: PÓS-GARANTIA    |
|   (Véspera / Testes / Validação)   |   (Lançamento / Monitoramento)    |   (D+7 a D+30 / Auditoria)|
+------------------------------------+-----------------------------------+---------------------------+
| 1. Configurar Cenário Único Router | 1. Ativar Cenário (Status: ON)    | 1. Manter cenário ON para |
| 2. Restringir eventos na Greenn    | 2. Monitorar consumo horário      |    reembolsos tardios     |
| 3. Upload PDF mestre com trava     | 3. Acompanhar gatilho 900 créditos| 2. Confirmar exclusão de  |
| 4. Executar Testes 1, 2 e 3 (curl) |    (~195 / ~160 / ~156 vendas)    |    arquivos no Drive      |
| 5. Teste de rajada (5 disparos)    | 4. Se 900 créditos: desligar      | 3. Exportar logs do Make  |
| 6. Medir chamadas e testes reais   |    e-mail próprio ou upgrade      |    (prazo limite: 7 dias!)|
| 7. Preencher Checklist D-1         | 5. Se estouro (1.000 créditos):   | 4. Reconciliar planilha   |
| 8. Calcular folga e definir stack  |    liberar acessos manualmente via|    vs Greenn vs Drive     |
| 9. Setup SMTP com Senha de App     |    exportação CSV da Greenn       | 5. Desativar Webhook      |
+------------------------------------+-----------------------------------+---------------------------+
```

### 6.1 Fase 1: D-1 (Véspera do Lançamento — Testes e Homologação)
1. **Montagem do Cenário no Make:** Criar o cenário único com Webhook Customizado, Router, Filtro A, Google Drive Copy, Google Drive Share, Envio de E-mail (Rota A) e Filtro B, Google Drive Search, Filtro File ID Exists, Google Drive Delete, Envio de E-mail de Cancelamento (Rota B).
2. **Configuração de Segurança no Google Drive:** Fazer upload do PDF mestre, acessar configurações avançadas de compartilhamento e desmarcar a opção para fazer download, imprimir e copiar.
3. **Execução dos Testes Canônicos:** Disparar os Testes 1, 2 e 3 via script `testes-d1-curl-v4.sh` contra a URL de webhook real.
4. **Teste de Rajada (Burst Stress Test):** Disparar 5 requisições simuladas sequenciais rápidas (< 1 segundo) para assegurar que a fila assíncrona do Make absorve o tráfego sem retornar erro HTTP 429 ou 500.
5. **Medição e Decisão Técnica:** Contar o consumo real de créditos na interface do Make, preencher todos os 12 itens do Checklist de D-1, aplicar a fórmula de recálculo da folga e oficializar a stack operacional.

### 6.2 Fase 2: Dia D (Abertura do Carrinho e Monitoramento Ativo)
1. **Ativação da Operação:** Colocar o cenário em modo `ON` (Execução Imediata via Webhook).
2. **Plantão de Monitoramento Horário:** O operador técnico acessa o painel do Make a cada 60 minutos e anota o volume de operações consumidas.
3. **Ponto de Corte aos 900 Créditos:**
   - Ao atingir 900 créditos consumidos (~195 vendas no Cenário 1, ~160 vendas no Cenário 2 ou ~156 vendas no Cenário 3):
   - Executar a contingência imediata: desativar o módulo de e-mail próprio em ambas as rotas do cenário ativo (passando a usar a notificação nativa do Google Drive e economizando 1 crédito por venda/reembolso restante) OU efetuar upgrade para o plano pago vigente no site do Make.
4. **Contingência em Caso de Estouro de Cota (1.000 créditos atingidos):**
   - Executar o protocolo de contingência imediata: upgrade no Make ou desativação de e-mails.
   - Exportar o relatório de vendas aprovadas no painel da Greenn.
   - Cruzar com a planilha de controle e conceder acesso manual no Google Drive para os clientes represados.

### 6.3 Fase 3: Pós-Garantia (D+7 a D+30 — Auditoria e Encerramento)
1. **Acompanhamento da Garantia Legal (Art. 49 do CDC — 7 dias):** O cenário permanece ativo durante os 7 dias seguintes para processar cancelamentos automáticos e revogar permissões no Google Drive.
2. **Auditoria Forense de Revogações:** Validar que cada pedido com status `refunded` ou `chargedback` na Greenn teve a sua respectiva cópia excluída no Google Drive.
3. **Exportação Mandatória de Logs:** O plano gratuito do Make retém logs por apenas **7 dias**. No dia D+6, o operador deve baixar o histórico completo de execuções em formato CSV para guarda e conformidade fiscal/operacional.
4. **Desativação Final:** Decorrido o período de garantia contratual, desativar o cenário para preservar a cota do mês seguinte.

---

## 7. Tabela de Gatilhos e Procedimentos de Contingência Operacional

Esta tabela define ações de resposta rápida para as 5 situações operacionais críticas:

| Gatilho / Evento Crítico | Condição de Disparo | Ação Operacional Imediata | Responsável Técnico |
|---|---|---|---|
| **1. Detecção de 2 Chamadas por Venda/Reembolso em D-1 ou Testes > 100 Créditos** | A medição de D-1 apontou 2 chamadas/venda (Cenário 2 = 996 créditos) ou 2 chamadas/reembolso (Cenário 3 = 1.020 créditos) ou consumo de testes consumiu a folga. | 1. Cortar preventivamente o módulo de e-mail próprio no Make (reduz consumo para 812 créditos no Cenário 2 ou 836 créditos no Cenário 3).<br>2. Se a folga calculada no Make permanecer negativa **mesmo sem e-mail próprio**, migrar a operação para o **n8n Cloud Trial de 14 dias** (1.000 execuções). | Arquiteto de Integração / Lead Spec Writer |
| **2. Consumo Atingiu 900 Créditos no Dia D** | Contador do Make registra 900 operações consumidas no painel da organização (~195 vendas no Cenário 1, ~160 vendas no Cenário 2 ou ~156 vendas no Cenário 3). | 1. **Opção Custo US$ 0:** Acessar o cenário ativo no Make, desconectar os nós de E-mail Próprio e salvar. O fluxo passa a gastar 3 créditos/transação usando o e-mail automático do Drive.<br>2. **Opção de Escala:** Acessar o site do Make e assinar o plano pago vigente para liberar 10.000 créditos imediatos. | Operador Técnico do Dia D |
| **3. Estouro de Cota Durante o Dia D (1.000 Créditos Atingidos)** | Make interrompe execuções com alerta de 100% da cota consumida (ex.: Cenário 3 não mitigado com 20 créditos excedentes) e compradores pagos ficam na fila. | 1. Fazer upgrade imediato para o plano pago no Make ou desligar nós de e-mail.<br>2. Exportar o CSV de vendas `paid` do painel da Greenn.<br>3. Identificar na planilha de controle os compradores sem arquivo correspondente.<br>4. Duplicar o PDF mestre no Google Drive e compartilhar manualmente com papel `reader` para os clientes retidos (ou reprocessar a fila de webhooks no Make). | DevOps / Operador do Dia D |
| **4. Reembolso no Fluxo B sem Arquivo Correspondente no Drive** | Webhook de estorno acionado, mas o módulo `Search Files` retorna 0 arquivos (compra sem arquivo gerado ou deletado previamente). | 1. O filtro gratuito `File ID Exists` (ou a diretiva Error Handler Ignore/Resume no Delete) barra a execução a custo zero, impedindo erro fatal no cenário.<br>2. O sistema registra a transação `{{id_transacao}}` na planilha de controle com status `ARQUIVO_NAO_ENCONTRADO_NA_EXCLUSAO` para auditoria manual. | Especialista de Segurança e Drive |
| **5. Falha ou Erro Técnico em Módulo do Cenário** | Erro de conexão de rede, instabilidade na API do Google Drive ou falha de autenticação SMTP. | 1. O Make emite notificação automática de erro por e-mail para o administrador.<br>2. Registrar a transação na planilha de controle.<br>3. Sanar a credencial/parâmetro e reprocessar as execuções incompletas diretamente pela fila do histórico do Make. | Arquiteto de Integração / QA |

---

## 8. Matriz Completa de Riscos e Mitigações Arquiteturais (12 Riscos)

Mapeamento exaustivo de todos os 12 riscos operacionais do projeto, detalhando a severidade, probabilidade e estratégias de mitigação preventiva em D-1 e corretiva no Dia D:

| # | Risco Identificado | Severidade | Probabilidade | Mitigação Preventiva em D-1 | Mitigação Corretiva no Dia D |
|---|---|:---:|:---:|---|---|
| **1** | **Chamadas extras de webhook em vendas (Cenário 2)** | Média | Alta | Configurar Filtro Anti-Duplicidade A (`currentStatus = paid AND oldStatus != paid`). Se a medição em D-1 registrar 2 chamadas/venda, desativar o módulo de e-mail próprio, garantindo folga de 188 créditos. | Monitorar o gatilho de 900 créditos aos ~160 compradores e cortar o e-mail próprio se ainda estiver ativo. |
| **2** | **Chamadas extras de webhook em vendas E reembolsos (Cenário 3)** | Alta | Média | Se a medição em D-1 acusar 2 chamadas por venda e por estorno, desligar obrigatoriamente o e-mail próprio no Make, reduzindo o consumo de 1.020 para 836 créditos (evitando estouro em 20 créditos). | Atingindo 900 créditos (~156 vendas), realizar upgrade imediato para o plano pago vigente no site do Make. |
| **3** | **Falha no Fluxo B se a cópia não existir** | Alta | Média | Adicionar filtro pré-exclusão `File ID Exists` (0 créditos) ou diretiva *Error Handler → Ignore / Resume* no módulo `Delete a File`. Registrar ocorrência na planilha de controle. | Auditoria na planilha de controle para inspecionar reembolsos registrados sem arquivo excluído. |
| **4** | **Busca no Fluxo B trazendo mais de um arquivo** | Média | Baixa | Padronizar a nomenclatura das cópias incluindo o identificador global único: `{{email_comprador}} - {{id_transacao}}.pdf` e buscar estritamente por `{{id_transacao}}`. | Se o Make iterar sobre mais de um arquivo com o mesmo ID, o cenário excluirá ambos sem falha técnica. |
| **5** | **Consumo de testes ultrapassando a reserva de 100 créditos** | Média | Média | Limitar os testes de D-1 a no máximo 10 a 15 disparos de webhook controlados. Inserir o consumo real no checklist e aplicar a fórmula de recálculo da folga. | Descontar o excesso de testes da folga operacional líquida ou cortar o módulo de e-mail próprio se a folga ficar comprimida. |
| **6** | **Divergência nos nomes dos campos do payload real da Greenn (documentação de 2021)** | Alta | Alta | Executar compra-teste real no D-1 e acionar *"Redetermine data structure"* no módulo Webhook. Ajustar os mapeamentos de nós e do script `curl`, preservando a nomenclatura padronizada na documentação. | Ajuste imediato do mapeamento do módulo Webhook no Make em menos de 3 minutos. |
| **7** | **Limite de 1 URL de webhook na Greenn** | Alta | Alta | Adoção da arquitetura de **Cenário Único com Router**, permitindo que uma única URL atenda simultaneamente aos fluxos de venda e reembolso. | Inexistente no Dia D, pois a URL única já estará vinculada ao produto no painel da Greenn. |
| **8** | **Rajada de vendas simultâneas na abertura do carrinho (pico inicial)** | Média | Alta | Executar teste de estresse disparando 5 requisições `curl` consecutivas em D-1 para validar a retenção no buffer da fila HTTP 200 do Make. | A fila do Make processa as execuções de forma sequencial sem perda de webhooks. |
| **9** | **Limite de 5 MB no Make gratuito** | Baixa | Baixa | A automação manipula apenas mensagens JSON textuais (< 5 KB). Nenhum binário de PDF trafega pelo Make — o arquivo mestre é duplicado diretamente na nuvem do Google Drive. | Risco nulo durante a operação. |
| **10** | **Intervalo mínimo de agendamento de 15 min no Make gratuito** | Baixa | Nula | O gatilho utilizado é do tipo **Instant Webhook** (orientado a eventos assíncronos em tempo real), imune às limitações de agendamento de polling do plano gratuito. | Nenhuma ação necessária, pois o disparo é instantâneo. |
| **11** | **Retenção de logs de apenas 7 dias no Make gratuito** | Baixa | Alta | Programar lembrete operacional para o dia D+6 para exportar todos os logs de execução em arquivo CSV para arquivo local e auditoria fiscal. | Exportar o histórico de execuções antes do sétimo dia pós-lançamento. |
| **12** | **Herança de trava de download, aviso duplicado do Drive e bloqueio OAuth do Gmail** | Alta | Alta | Validar herança no D-1 (se não herdar, aceitar o risco formalmente); decidir sobre aviso nativo do Drive; e utilizar conexão de e-mail **SMTP com Senha de App** para evitar bloqueios do Google Cloud. | Se a conta Gmail bloquear envio diário (limite de 500 envios), chavear para envio nativo do Google Drive. |

---

## 9. Alocação de Skills por Papel de Agente (Multi-Agent Skill Mapping)

Para assegurar governança, rigor metodológico e conformidade com as melhores práticas de engenharia de software, a execução deste projeto envolve 4 papéis especializados e a aplicação estrita de 8 skills:

```
+----------------------------------------------------------------------------------------------------+
|                         MAPEAMENTO DE SKILLS DA EQUIPE MULTI-AGENTE                                |
+----------------------------------------------------+-----------------------------------------------+
| Papel Especializado do Agente                      | Skills Carregadas e Metodologia Aplicada      |
+----------------------------------------------------+-----------------------------------------------+
| 1. Agente Arquiteto de Integração & Automação      | • software-architecture: Cenário único com     |
|    (Lead Spec Writer)                              |   Router, idempotência, modelagem de estados. |
|                                                    | • api-design-principles: Contrato de webhook, |
|                                                    |   restrição na origem, payloads padronizados. |
+----------------------------------------------------+-----------------------------------------------+
| 2. Agente de Segurança, Privacidade & Controle     | • security-and-hardening: Permissão reader,   |
|    de Acesso (Drive & Auth Specialist)             |   trava de download, isolamento e SMTP AppPwd.|
|                                                    | • privacy-by-design: Cópias individuais, LGPD,|
|                                                    |   revogação determinística no estorno.        |
|                                                    | • pdf-official: Entrega por link protegido    |
|                                                    |   (webViewLink) sem anexo perigoso.           |
+----------------------------------------------------+-----------------------------------------------+
| 3. Agente Engenheiro de Templates & Payloads       | • clean-code: Construção de templates HTML    |
|    (DevOps / QA Spec Miner)                        |   inline seguros, texto puro e scripts curl.  |
+----------------------------------------------------+-----------------------------------------------+
| 4. Agente Auditor & Verificador de Qualidade       | • clean-code-guard: Auditoria contra desvios,  |
|    (Independent Verifier / Judge)                  |   omissões de escopo e variáveis banidas.     |
|                                                    | • lint-and-validate: Validação automatizada   |
|                                                    |   de sintaxe YAML, JSON, matemática e portas. |
+----------------------------------------------------+-----------------------------------------------+
```

### Detalhamento das Atribuições por Agente:
1. **Agente Arquiteto de Integração & Automação (Lead Spec Writer):**
   - `software-architecture`: Projeta a topologia de cenário único com Router (0 créditos), assegura idempotência via filtros `oldStatus` e `currentStatus`, planeja o isolamento de falhas (*Error Handler Ignore/Resume*) e estrutura a governança de estados da venda.
   - `api-design-principles`: Define o contrato formal do evento `saleUpdated`, estabelece a restrição de eventos na origem do gateway (`paid`, `refunded`, `chargedback`) e padroniza as variáveis de payload.
2. **Agente de Segurança, Privacidade & Controle de Acesso (Drive & Auth Specialist):**
   - `security-and-hardening`: Modela as permissões do Google Drive com privilégio mínimo (`role: reader`), restringe o download/impressão via metadados `copyRequiresWriterPermission`, configura a autenticação SMTP com Senha de App de 16 caracteres e blinda a deleção no Fluxo B.
   - `privacy-by-design`: Garante isolamento estrito entre compradores criando arquivos individuais (`{{email_comprador}} - {{id_transacao}}.pdf`), cumpre o princípio da minimização de dados da LGPD/GDPR e garante o direito de revogação/eliminação instantânea de acesso em reembolsos.
   - `pdf-official`: Estabelece a entrega controlada via streaming/leitura online no navegador (`webViewLink`) sem envio de binários brutos por anexo de e-mail (o que violaria o DRM e consumiria banda).
3. **Agente Engenheiro de Templates & Payloads de Teste (DevOps / QA Spec Miner):**
   - `clean-code`: Desenvolve templates de e-mail em HTML 4.01 transicional inline de alta entregabilidade, versões em texto puro e scripts de teste executáveis em bash/curl para os testes de homologação em D-1.
4. **Agente Auditor & Verificador de Qualidade (Independent Verifier / Judge):**
   - `clean-code-guard`: Realiza varreduras estáticas de código e documentação contra desvios de variáveis, erros de mapeamento e omissões de requisitos.
   - `lint-and-validate`: Executa a suíte de verificação programática (`validate_v4_artifacts.py`), auditando sintaxe YAML da Ficha Técnica, formatação JSON dos payloads curl, precisão aritmética dos 3 cenários e conformidade de todos os 12 itens do checklist de D-1.

---

## 10. Templates Oficiais de E-mail (R2 Consolidado)

Os textos abaixo constituem a redação oficial homologada para os e-mails transacionais do lançamento, estruturados com estilos inline de alta entregabilidade e alertas visuais proeminentes:

### 10.1 E-mail 1 — Entrega do PDF (Fluxo A: Venda Aprovada)

#### Assunto:
```text
Seu material exclusivo está liberado! (Transação: {{id_transacao}})
```

#### Versão HTML Simples (Clean HTML Inline):
```html
<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <title>Acesso ao seu Material Exclusivo</title>
</head>
<body style="margin: 0; padding: 20px; font-family: Arial, Helvetica, sans-serif; background-color: #f4f6f8; color: #333333;">
  <table align="center" border="0" cellpadding="0" cellspacing="0" width="100%" style="max-width: 600px; background-color: #ffffff; border-radius: 8px; overflow: hidden; box-shadow: 0 2px 8px rgba(0,0,0,0.06);">
    <!-- Cabeçalho -->
    <tr>
      <td style="background-color: #1a73e8; padding: 24px; text-align: center; color: #ffffff;">
        <h1 style="margin: 0; font-size: 22px; font-weight: bold;">Seu Material está Liberado!</h1>
      </td>
    </tr>
    <!-- Conteúdo Principal -->
    <tr>
      <td style="padding: 30px 24px;">
        <p style="font-size: 16px; line-height: 1.5; margin-top: 0;">Olá,</p>
        <p style="font-size: 15px; line-height: 1.5;">Obrigado pela sua compra! O pagamento referente à transação <strong>{{id_transacao}}</strong> foi confirmado com sucesso.</p>
        <p style="font-size: 15px; line-height: 1.5;">Sua cópia exclusiva e individual do material já está disponível para leitura no Google Drive através do link seguro abaixo:</p>
        
        <!-- Botão CTA -->
        <table align="center" border="0" cellpadding="0" cellspacing="0" style="margin: 28px auto;">
          <tr>
            <td align="center" style="border-radius: 6px; background-color: #1a73e8;">
              <a href="{{webViewLink}}" target="_blank" style="font-size: 16px; font-weight: bold; color: #ffffff; text-decoration: none; padding: 14px 28px; display: inline-block;">Acessar Meu Material Online</a>
            </td>
          </tr>
        </table>

        <!-- Bloco de Alerta Mandatório -->
        <div style="background-color: #fff3cd; border-left: 4px solid #ffc107; padding: 14px 16px; margin: 24px 0; border-radius: 4px;">
          <p style="margin: 0; font-size: 14px; line-height: 1.5; color: #856404;">
            <strong>ATENÇÃO OBRIGATÓRIA:</strong> Este documento é protegido contra download e cópia para leitura exclusiva online. Para conseguir visualizar o arquivo, <strong>é obrigatório estar logado na conta Google correspondente ao e-mail {{email_comprador}}</strong>. Se estiver conectado a outro perfil, o Google Drive exibirá erro de permissão.
          </p>
        </div>

        <p style="font-size: 14px; line-height: 1.5; color: #555555;">Se você não conseguir abrir o botão acima, copie e cole o link direto em seu navegador:<br>
          <a href="{{webViewLink}}" style="color: #1a73e8; word-break: break-all;">{{webViewLink}}</a>
        </p>
      </td>
    </tr>
    <!-- Rodapé Transacional -->
    <tr>
      <td style="background-color: #f8f9fa; padding: 16px 24px; text-align: center; font-size: 12px; color: #888888; border-top: 1px solid #eeeeee;">
        Este e-mail é transacional e foi enviado para <strong>{{email_comprador}}</strong> referente à transação <strong>{{id_transacao}}</strong>.
      </td>
    </tr>
  </table>
</body>
</html>
```

#### Versão Texto Puro:
```text
Olá,

Obrigado pela sua compra! O pagamento referente à transação {{id_transacao}} foi confirmado com sucesso.

Sua cópia exclusiva e individual do material já está disponível para leitura online no Google Drive através do link seguro abaixo:
{{webViewLink}}

ATENÇÃO OBRIGATÓRIA:
Este documento é protegido contra download, impressão e cópia para leitura exclusiva online. Para abrir e visualizar o arquivo, é obrigatório estar logado na conta Google correspondente ao e-mail {{email_comprador}}. Caso você acesse por outra conta Google, o Drive exibirá aviso de acesso não autorizado.

Atenciosamente,
Equipe de Suporte
Transação: {{id_transacao}}
Destinatário: {{email_comprador}}
```

---

### 10.2 E-mail 2 — Confirmação de Reembolso/Cancelamento (Fluxo B: Reembolso)

#### Assunto:
```text
Confirmação de Reembolso e Encerramento de Acesso (Transação: {{id_transacao}})
```

#### Versão HTML Simples (Clean HTML Inline):
```html
<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <title>Confirmação de Reembolso</title>
</head>
<body style="margin: 0; padding: 20px; font-family: Arial, Helvetica, sans-serif; background-color: #f4f6f8; color: #333333;">
  <table align="center" border="0" cellpadding="0" cellspacing="0" width="100%" style="max-width: 600px; background-color: #ffffff; border-radius: 8px; overflow: hidden; box-shadow: 0 2px 8px rgba(0,0,0,0.06);">
    <!-- Cabeçalho -->
    <tr>
      <td style="background-color: #d93025; padding: 24px; text-align: center; color: #ffffff;">
        <h1 style="margin: 0; font-size: 22px; font-weight: bold;">Acesso Encerrado / Reembolso Concluído</h1>
      </td>
    </tr>
    <!-- Conteúdo Principal -->
    <tr>
      <td style="padding: 30px 24px;">
        <p style="font-size: 16px; line-height: 1.5; margin-top: 0;">Olá,</p>
        <p style="font-size: 15px; line-height: 1.5;">Informamos ao titular do e-mail <strong>{{email_comprador}}</strong> que o reembolso ou cancelamento referente à transação <strong>{{id_transacao}}</strong> foi processado e concluído com sucesso.</p>
        
        <!-- Bloco Informativo de Revogação -->
        <div style="background-color: #fce8e6; border-left: 4px solid #d93025; padding: 14px 16px; margin: 24px 0; border-radius: 4px;">
          <p style="margin: 0; font-size: 14px; line-height: 1.5; color: #a51d24;">
            <strong>REVOGAÇÃO DE ACESSO:</strong> Em conformidade com as regras do produto, a sua permissão individual de leitura foi revogada e a cópia exclusiva do PDF associada à sua conta foi <strong>removida permanentemente do Google Drive</strong>.
          </p>
        </div>

        <p style="font-size: 14px; line-height: 1.5; color: #555555;">Caso o estorno tenha sido solicitado por cartão de crédito ou Pix, consulte a sua operadora financeira ou extrato bancário para verificar o prazo de lançamento do crédito.</p>
        <p style="font-size: 14px; line-height: 1.5; color: #555555;">Se você acredita que este cancelamento ocorreu por engano, entre em contato imediatamente com o nosso time de suporte.</p>
      </td>
    </tr>
    <!-- Rodapé Transacional -->
    <tr>
      <td style="background-color: #f8f9fa; padding: 16px 24px; text-align: center; font-size: 12px; color: #888888; border-top: 1px solid #eeeeee;">
        Notificação automática de encerramento enviada para <strong>{{email_comprador}}</strong> | Transação: <strong>{{id_transacao}}</strong>.
      </td>
    </tr>
  </table>
</body>
</html>
```

#### Versão Texto Puro:
```text
Olá,

Informamos ao titular do e-mail {{email_comprador}} que o reembolso ou cancelamento referente à transação {{id_transacao}} foi processado e concluído com sucesso.

REVOGAÇÃO DE ACESSO:
Em virtude do reembolso/cancelamento, a sua permissão individual de leitor foi revogada e a cópia exclusiva do PDF associada à sua conta foi removida permanentemente do Google Drive.

Caso tenha dúvidas sobre prazos de estorno junto à sua instituição financeira ou se este cancelamento ocorreu por engano, responda a este e-mail para suporte.

Atenciosamente,
Equipe de Atendimento
Transação: {{id_transacao}}
Titular: {{email_comprador}}
```

---

## 11. Payloads JSON e Comandos curl de Teste em D-1 (R3 Consolidado)

Os comandos abaixo representam os testes padronizados a serem disparados em D-1 apontando para `"{{URL_WEBHOOK}}"`. Todos os payloads utilizam estritamente as chaves padronizadas `email_comprador`, `id_transacao`, `oldStatus` e `currentStatus` `[CONFIRMAR COM PAYLOAD REAL]`:

### 11.1 Teste 1: Simulação de Venda Aprovada (Fluxo A)
- **Cenário de Teste:** Simula um pagamento aprovado via Pix ou cartão. O webhook da Greenn emite a transição de aguardando pagamento para aprovado.
- **Transição de Status:** `"oldStatus": "waiting_payment"` → `"currentStatus": "paid"`.
- **Comportamento Esperado:** Passa pelo Filtro da Rota A, cria a cópia única `comprador.teste.v4@gmail.com - TRX-TESTE-4001.pdf` no Google Drive, concede permissão de leitura (`reader`) e despacha o E-mail 1 com o `{{webViewLink}}`.
- **Consumo:** **4 créditos no Make** (1 no Webhook + 3 pós-filtro: Copy + Share + E-mail) / **1 execução no n8n Cloud**.

```bash
curl -s -X POST "{{URL_WEBHOOK}}" \
  -H "Content-Type: application/json" \
  -d '{
    "oldStatus": "waiting_payment",
    "currentStatus": "paid",
    "email_comprador": "comprador.teste.v4@gmail.com",
    "id_transacao": "TRX-TESTE-4001"
  }'
```

---

### 11.2 Teste 2: Simulação de Evento Barrado no Filtro (Anti-Duplicidade)
- **Cenário de Teste:** Simula o reenvio de um webhook para um pedido já aprovado (ex.: atualização cadastral ou emissão de nota fiscal pela Greenn).
- **Transição de Status:** `"oldStatus": "paid"` → `"currentStatus": "paid"`.
- **Comportamento Esperado:** O Webhook recebe a chamada, mas a Rota A bloqueia gratuitamente no Filtro A (pois exige `oldStatus != paid`) e a Rota B bloqueia no Filtro B (pois exige `currentStatus IN [refunded, chargedback]`). Nenhuma cópia duplicada é criada no Drive e nenhum e-mail é disparado.
- **Consumo:** **1 crédito no Make** (apenas a ingestão do Webhook) / **1 execução no n8n Cloud**.

```bash
curl -s -X POST "{{URL_WEBHOOK}}" \
  -H "Content-Type: application/json" \
  -d '{
    "oldStatus": "paid",
    "currentStatus": "paid",
    "email_comprador": "comprador.teste.v4@gmail.com",
    "id_transacao": "TRX-TESTE-4001"
  }'
```

---

### 11.3 Teste 3: Simulação de Reembolso / Revogação de Acesso (Fluxo B)
- **Cenário de Teste:** Simula o estorno ou devolução de uma compra previamente aprovada.
- **Transição de Status:** `"oldStatus": "paid"` → `"currentStatus": "refunded"` *(Atenção Mandatória: `oldStatus` deve ser estritamente `"paid"`, nunca `"waiting_payment"`, para satisfazer a regra de integridade do Filtro B).*
- **Comportamento Esperado:** Passa pelo Filtro da Rota B, pesquisa o arquivo contendo `TRX-TESTE-4001` no Google Drive, valida sua existência no filtro `File ID Exists` (ou Error Handler Ignore), exclui permanentemente o arquivo do Drive (revogando o acesso) e envia o E-mail 2 de confirmação de cancelamento.
- **Consumo:** **4 créditos no Make com e-mail próprio** (1 Webhook + 3 pós-filtro: Search + Delete + E-mail) ou **3 créditos no Make sem e-mail próprio** (1 Webhook + 2 pós-filtro: Search + Delete) / **1 execução no n8n Cloud**.

```bash
curl -s -X POST "{{URL_WEBHOOK}}" \
  -H "Content-Type: application/json" \
  -d '{
    "oldStatus": "paid",
    "currentStatus": "refunded",
    "email_comprador": "comprador.teste.v4@gmail.com",
    "id_transacao": "TRX-TESTE-4001"
  }'
```

---

## 12. Considerações Finais de Homologação

A especificação v4.0 conclui a blindagem completa da infraestrutura de entrega e revogação do infoproduto. A equipe operacional deve estritamente:
1. Executar os procedimentos descritos nesta especificação e preencher o Checklist de D-1 na íntegra.
2. Manter a disciplina orçamentária de custo US$ 0 priorizando o Make e acionando o n8n Cloud Trial unicamente sob o critério mandatório homologado.
3. Garantir a guarda e exportação dos logs operacionais em D+6 para conformidade fiscal e jurídica.
