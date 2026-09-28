# Acesso E Assinatura - Revisar Assinatura Aprovada - PT-BR

> Status: imagem 74 aprovada. Este documento registra o contrato visual-funcional da tela `Revisar assinatura`.

## Imagem Aprovada

Arquivo:

`74_round-4.1Q_acesso-assinatura_revisar-assinatura-aprovado.png`

Local:

`D:\Downloads\taliya-crm-chatgpt-images-named-20260511-082508\74_round-4.1Q_acesso-assinatura_revisar-assinatura-aprovado.png`

## Papel Da Tela

Esta tela aparece depois que o usuario:

```text
escolhe um plano
→ cria conta ou entra
-> revisa a assinatura
-> continua para pagamento seguro externo
-> entra na tela 75 de confirmacao automatica
```

Ela nao coleta pagamento. Ela confirma o plano, mostra o que esta incluso, permite cupom e leva o usuario para o checkout hospedado do provedor.

## Decisao De Estrutura

Usar o shell 71 e dois cards separados:

| Card | Funcao |
| --- | --- |
| Esquerdo | Dados do plano, agentes, inclusoes, limites e conta. |
| Direito | Resumo de pagamento, cupom, total, seguranca e CTA para provedor. |

Nao usar card unico dividido por linha vertical. Nao usar sidebar, CRM shell ou onboarding shell.

## Conteudo Aprovado

### Card Esquerdo

| Elemento | Conteudo |
| --- | --- |
| Plano | `Plano Avance` |
| Badge | `3 agentes incluidos` |
| Secao | `Incluso no plano` |
| Inclusos | Painel Taliya + app; Sistema do studio; WhatsApp Business; Atendimento; Agenda; Vendas; Mensagens de IA. |
| Nao inclusos | Financeiro; Retencao; Gestao; Historico/Evolucao. |
| Limite | `5.000 mensagens/mes` abaixo de Mensagens de IA. |
| Conta | `ana@studiolume.com` com link `Trocar`. |

### Card Direito

| Elemento | Conteudo |
| --- | --- |
| Titulo | `Pagamento` |
| Item | `Plano Avance` - `R$ 497,00` |
| Cupom | Input `Codigo promocional` + botao `Aplicar`. |
| Total | `Total hoje` - `R$ 497,00` |
| Recorrencia | `Renovacao mensal` |
| Seguranca | Badge `Pagamento seguro` |
| Nota | `A Taliya nao coleta dados de cartao nesta tela.` |
| CTA | `Continuar para pagamento seguro` |
| Link secundario | `Voltar aos planos` |

## Regras Funcionais

- O plano mostrado vem da pagina de planos.
- O usuario deve estar autenticado antes desta tela.
- O ciclo e mensal sempre; nao mostrar seletor de ciclo.
- Cupom pode ser informado nesta tela antes do provedor.
- O pagamento real acontece em provedor externo/hospedado.
- A Taliya nao coleta cartao, Pix, boleto, CVC ou dados bancarios nesta tela.
- CRM e onboarding so podem ser liberados depois da confirmacao confiavel da assinatura.

## Nao Incluir

- campo de cartao;
- Pix;
- boleto;
- QR Code;
- CVC;
- checkout embutido;
- provedor especifico;
- seletor mensal/anual;
- comparativo de todos os planos;
- CRM operacional;
- onboarding;
- sidebar;
- menu operacional.

## Proximas Telas

| Imagem | Tela | Status |
| --- | --- | --- |
| 75 | Aguardando confirmacao | Aprovada em `access-subscription-pending-confirmation-approved.pt-BR.md` |
| 76 | Resolver assinatura / bloqueado | Aprovada em `access-subscription-resolution-approved.pt-BR.md` |
| 77 | Assinatura confirmada / ir para onboarding | Aprovada em `access-subscription-confirmed-setup-approved.pt-BR.md` |
