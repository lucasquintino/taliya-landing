# Acesso E Assinatura - Shell Base Aprovado - PT-BR

> Status: imagem 71 aprovada. Este documento registra o contrato visual do shell pre-CRM de Acesso e Assinatura.

## Imagem Aprovada

Arquivo:

`71_round-4.1Q_acesso-assinatura_shell-base-aprovado.png`

Local:

`D:\Downloads\taliya-crm-chatgpt-images-named-20260511-082508\71_round-4.1Q_acesso-assinatura_shell-base-aprovado.png`

Referencias:

- Deriva visualmente da imagem `16_round-4.1S_app-shell_01_base-web.png`.
- Usa o mesmo DNA visual da Taliya.
- Nao usa o app shell do CRM.
- Nao usa o shell do onboarding.

## Objetivo

Servir como moldura neutra para telas antes do CRM:

- criar conta;
- entrar;
- revisar assinatura;
- aguardar confirmacao;
- resolver assinatura/bloqueio;
- confirmar assinatura e seguir para onboarding.

## Decisao Visual

O shell aprovado tem:

- fundo cinza suave/frosted;
- janela central grande, arredondada e premium;
- barra de navegador visual no topo, mantendo continuidade com a imagem 16;
- header interno simples com logo Taliya;
- dois icones no canto direito para ajuda e conta;
- area principal ampla como slot de conteudo;
- coluna lateral com tres cards neutros;
- rodape com `Termos`, `Privacidade` e `Ajuda`;
- ausencia total de sidebar, menu operacional e navegacao do CRM.

## O Que Deve Ser Herdado Nas Proximas Telas

| Elemento | Regra |
| --- | --- |
| Fundo | Manter cinza suave/frosted. |
| Janela | Manter container central arredondado e premium. |
| Header | Logo Taliya a esquerda, icones simples a direita. |
| Area principal | Substituir o slot pelo conteudo especifico da etapa. |
| Coluna lateral | Usar para contexto da etapa, sem virar dashboard. |
| Rodape | Manter termos, privacidade e ajuda/suporte. |
| Botao principal | Quando houver, usar pill preto do design system. |
| Botao secundario | Discreto, leve, sem competir com a acao principal. |

## O Que Nao Pode Entrar No Shell

- sidebar;
- topbar interna do CRM;
- menu operacional;
- dashboard;
- avatar de CRM logado;
- cards de Hoje, Inbox, Agenda, Financeiro ou Alunos;
- stepper do onboarding;
- chat lateral de configuracao;
- dados reais de pagamento;
- formulario de cartao;
- Pix ou boleto dentro da Taliya;
- checkout completo dentro da Taliya.

## Telas Que Devem Usar Este Shell

| Proxima imagem | Tela | Status |
| --- | --- | --- |
| 72 | Criar conta | Salva; ajustes finos documentados em `access-subscription-auth-screens-review.pt-BR.md` |
| 73 | Entrar | Salva; ajustes finos documentados em `access-subscription-auth-screens-review.pt-BR.md` |
| 74 | Revisar assinatura | Aprovada em `access-subscription-review-checkout-approved.pt-BR.md` |
| 75 | Aguardando confirmacao | Aprovada em `access-subscription-pending-confirmation-approved.pt-BR.md` |
| 76 | Resolver assinatura / bloqueado | Aprovada em `access-subscription-resolution-approved.pt-BR.md` |
| 77 | Assinatura confirmada / ir para onboarding | Aprovada em `access-subscription-confirmed-setup-approved.pt-BR.md` |

## Criterio De Aceite

As proximas imagens estao corretas quando parecem pertencer ao mesmo shell 71, mas cada uma preenche somente o conteudo necessario da etapa. Nenhuma delas deve dar a sensacao de que o usuario ja entrou no CRM antes da assinatura confirmada.
