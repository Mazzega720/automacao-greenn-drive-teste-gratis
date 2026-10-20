# Templates de E-mail de Produção (v4.0)
## Automação Greenn + Google Drive + E-mail
**Versão:** 4.0  
**Data de Emissão:** 2026-10-20  
**Padrão de Variáveis:** Unificadas e Padronizadas  
**Codificação:** UTF-8  

---

## 1. Diretrizes Técnicas e Princípios de Clean Code

Os templates de e-mail abaixo foram desenvolvidos seguindo as melhores práticas de entregabilidade, acessibilidade e compatibilidade entre os principais clientes de e-mail (Gmail, Outlook, Apple Mail, navegadores móveis e webmail):

1. **Estrutura e Estilização Inline:** Utilização de tabelas HTML 4.01 limpas com estilos CSS estritamente *inline*, garantindo renderização idêntica em desktops e smartphones sem depender de stylesheets externos bloqueados por clientes de correio.
2. **Largura e Tipografia Seguras:** Largura máxima de 600px centralizada, com tipografia universal legível (`Arial, Helvetica, sans-serif`), contraste elevado em conformidade com WCAG AA e espaçamentos adequados para leitura confortável.
3. **Variáveis Canônicas Homologadas:** Uso estrito e exclusivo dos identificadores:
   - `{{email_comprador}}`: Endereço de e-mail do comprador cadastrado na Greenn (vinculado à conta Google).
   - `{{id_transacao}}`: Código alfanumérico exclusivo da transação/pedido.
   - `{{webViewLink}}`: URL segura gerada pelo Google Drive para visualização do PDF no navegador.
4. **Erradicação Absoluta de Nomes Legados:** É estritamente proibido o uso de variáveis legadas em língua inglesa ou identificadores fora do padrão canônico da especificação v4.0.
5. **Alerta de Conta Google em Destaque:** O material é compartilhado individualmente com a conta Google informada no momento da compra. Por isso, a instrução de login obrigatório no Google com o e-mail correspondente está destacada em **negrito** e em bloco de aviso de alta visibilidade.

---

## 2. E-mail 1 — Entrega do PDF (Fluxo A: Venda Aprovada)

Disparado automaticamente pelo módulo de envio de e-mail após a confirmação de pagamento pela Greenn, criação da cópia individual e concessão de permissão `reader` no Google Drive.

### 2.1 Assunto
```text
Seu material exclusivo está liberado! (Transação: {{id_transacao}})
```

### 2.2 Versão HTML Simples (Clean HTML Inline)
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

### 2.3 Versão Texto Puro
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

## 3. E-mail 2 — Confirmação de Reembolso/Cancelamento (Fluxo B: Reembolso)

Disparado pelo módulo opcional de e-mail após a confirmação de estorno (`refunded` ou `chargedback`), localização do arquivo correspondente no Google Drive e sua exclusão definitiva.

### 3.1 Assunto
```text
Confirmação de Reembolso e Encerramento de Acesso (Transação: {{id_transacao}})
```

### 3.2 Versão HTML Simples (Clean HTML Inline)
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

### 3.3 Versão Texto Puro
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
