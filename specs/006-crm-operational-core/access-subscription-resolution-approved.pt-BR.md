# Acesso E Assinatura - Resolver Assinatura Aprovada - PT-BR

> Status: imagem 76 aprovada. Este documento registra o contrato visual-funcional da tela `Nao conseguimos confirmar sua assinatura`.

## Imagem Aprovada

Arquivo:

`76_round-4.1Q_acesso-assinatura_resolver-assinatura-aprovado.png`

Local:

`D:\Downloads\taliya-crm-chatgpt-images-named-20260511-082508\76_round-4.1Q_acesso-assinatura_resolver-assinatura-aprovado.png`

## Papel Da Tela

Esta tela aparece quando a Taliya ja sabe que a tentativa de assinatura nao confirmou e o usuario precisa resolver.

Ela nao e um estado de espera. Casos ainda pendentes ficam na imagem 75. A imagem 76 e uma tela de recuperacao: explica o que pode ter acontecido, mostra a assinatura tentada e oferece caminhos claros para tentar novamente, trocar plano ou falar com suporte.

Fluxo aprovado:

```text
Landing / Planos
-> criar conta ou entrar
-> 74 Revisar assinatura
-> 75 Estamos confirmando sua assinatura
-> 76 Nao conseguimos confirmar sua assinatura, se a tentativa falhar/expirar/cancelar
```

## Formas De Entrada

| Entrada | Quando cai na 76 |
| --- | --- |
| Vindo da 75 | A verificacao automatica conclui que a tentativa falhou, expirou, foi cancelada ou excedeu o tempo maximo. |
| Retorno do provedor | O checkout externo retorna cancelado, expirado, recusado ou sem confirmacao confiavel. |
| Login futuro | A pessoa entra numa conta ja criada, mas com assinatura nao confirmada e tentativa anterior falha/expirada. |
| Link de e-mail ou suporte | A pessoa abre um link para resolver assinatura nao confirmada. |
| Volta manual ao app | A conta existe, mas o CRM continua bloqueado por falta de assinatura ativa. |

## Estados Que Levam Para 76

| Estado interno Taliya | Tela |
| --- | --- |
| `checkout_canceled` | 76 |
| `checkout_expired` | 76 |
| `payment_failed` | 76 |
| `payment_declined` | 76 |
| `confirmation_timeout` | 76 |
| `payment_abandoned_expired` | 76 |

Estados `payment_started`, `checking_confirmation` e `payment_pending` continuam na 75.

## Conteudo Aprovado

| Elemento | Conteudo |
| --- | --- |
| Titulo | `Nao conseguimos confirmar sua assinatura` |
| Subtexto | `Sua assinatura ainda nao foi ativada. Voce pode tentar novamente com seguranca.` |
| Bloco explicativo | `O que aconteceu` |
| Texto do bloco | `O pagamento pode ter sido cancelado, expirado ou recusado pelo provedor.` |
| Status | `Status da assinatura` com badge `Nao confirmada` |
| Secao | `Sua assinatura` |
| Plano | `Plano` - `Avance` |
| Conta | `Conta` - e-mail da conta autenticada |
| Seguranca | `Pagamento seguro` |
| Nota | `A Taliya nao coleta dados de cartao. A nova tentativa acontece pelo ambiente seguro do provedor.` |
| CTA principal | `Tentar pagamento novamente` |
| Link secundario 1 | `Voltar aos planos` |
| Link secundario 2 | `Falar com suporte` |
| Microcopy final | `O CRM sera liberado assim que a assinatura for confirmada.` |

## Regras Das Acoes

| Acao | Comportamento esperado |
| --- | --- |
| `Tentar pagamento novamente` | Cria ou reabre uma nova tentativa de checkout seguro no provedor externo. Depois de iniciar, o usuario volta para a 75. |
| `Voltar aos planos` | Retorna para escolha/revisao de plano antes de uma nova tentativa. |
| `Falar com suporte` | Abre suporte pre-CRM para duvida, erro persistente ou caso sensivel, sem liberar o app. |

Se uma nova tentativa for confirmada, a continuidade aprovada e a imagem 77 de assinatura confirmada e setup guiado.

## Variacao De Motivo

A tela pode trocar apenas o motivo curto do bloco `O que aconteceu`, sem criar novas telas:

- `O pagamento foi cancelado antes da conclusao.`
- `A sessao de pagamento expirou.`
- `O pagamento foi recusado pelo provedor.`
- `Nao recebemos a confirmacao dentro do tempo esperado.`

A estrutura, status, CTA e bloqueio de CRM continuam iguais.

## Nao Incluir

- linha de progresso ou steps;
- estado de verificacao em andamento;
- formulario de cartao;
- Pix;
- boleto;
- QR Code;
- campo de cupom;
- comparativo de planos;
- upsell;
- configuracao do studio;
- importacao de dados;
- convite de equipe;
- agentes;
- sidebar ou menu do CRM;
- CTA para entrar no app antes da confirmacao.

## Criterio De Aceite

A tela esta correta quando o usuario entende que:

- a assinatura ainda nao foi ativada;
- o problema pode ter sido cancelamento, expiracao, recusa ou falta de confirmacao;
- o CRM continua bloqueado;
- ele pode tentar pagar novamente, voltar aos planos ou falar com suporte;
- a Taliya nao coleta dados de cartao nesta tela.
