# Acesso E Assinatura - Aguardando Confirmacao Aprovada - PT-BR

> Status: imagem 75 aprovada. Este documento registra o contrato visual-funcional da tela `Estamos confirmando sua assinatura`.

## Imagem Aprovada

Arquivo:

`75_round-4.1Q_acesso-assinatura_aguardando-confirmacao-aprovado.png`

Local:

`D:\Downloads\taliya-crm-chatgpt-images-named-20260511-082508\75_round-4.1Q_acesso-assinatura_aguardando-confirmacao-aprovado.png`

## Papel Da Tela

Esta tela aparece imediatamente depois que o usuario clica em `Continuar para pagamento seguro` na tela 74.

Ela cumpre um papel unico: manter o studio em um estado confiavel enquanto a assinatura e confirmada pelo provedor externo. Ela nao vende plano, nao coleta pagamento, nao configura o CRM e nao libera onboarding.

Fluxo aprovado:

```text
Landing / Planos
-> criar conta ou entrar
-> 74 Revisar assinatura
-> 75 Estamos confirmando sua assinatura
-> 76 Resolver assinatura / bloqueio, se falhar ou ficar pendente demais
-> 77 Assinatura confirmada / seguir para onboarding, se confirmar
```

## Decisao De Produto

- Ao clicar no CTA da 74, o usuario vai para a 75.
- A 75 pode abrir, reabrir ou acompanhar o checkout seguro externo conforme a etapa real do pagamento.
- Depois do retorno do provedor, a 75 continua sendo o estado de verificacao ate receber confirmacao confiavel.
- A verificacao deve ser automatica; o usuario nao precisa atualizar a pagina.
- Antes da confirmacao, o CRM, o onboarding, equipe, importacao e agentes continuam bloqueados.

## Conteudo Aprovado

| Elemento | Conteudo |
| --- | --- |
| Titulo | `Estamos confirmando sua assinatura` |
| Subtexto | `Seu pagamento foi iniciado. Assim que a confirmacao chegar, voce podera configurar o Taliya para o seu studio.` |
| Status | `Status da assinatura` com badge `Verificando confirmacao` |
| Progresso | `Pagamento iniciado`, `Confirmacao em andamento`, `Configuracao liberada` |
| Plano | `Plano escolhido` - `Avance` |
| Conta | `Conta` - e-mail da conta autenticada |
| Seguranca | `Pagamento seguro` |
| Nota | `A Taliya nao coleta dados de cartao. A confirmacao vem pelo ambiente seguro de pagamento.` |
| Estado principal | Botao/area em loading desabilitada com `Verificando...` |
| Microcopy | `A verificacao acontece automaticamente. Voce nao precisa atualizar a pagina.` |
| Fallback 1 | `Reabrir pagamento seguro` |
| Fallback 2 | `Falar com suporte` |

## Regras Dos Botoes E Links

| Acao | Comportamento esperado |
| --- | --- |
| `Verificando...` | Nao e acao manual. E estado de loading/desabilitado enquanto a verificacao automatica roda. |
| `Reabrir pagamento seguro` | Fallback para quando o checkout externo foi fechado, expirou ou o usuario precisa retomar o pagamento. Nao deve competir com o estado automatico. |
| `Falar com suporte` | Fallback para duvida, erro, demora incomum ou bloqueio. Deve abrir suporte pre-CRM, sem liberar o app. |

## Estados Possiveis

| Estado | O que a tela comunica | Proximo passo |
| --- | --- | --- |
| Pagamento iniciado | O checkout seguro foi iniciado. | Aguardar confirmacao. |
| Confirmacao em andamento | A Taliya ainda nao recebeu confirmacao confiavel. | Continuar verificacao automatica. |
| Confirmado | Assinatura ativa. | Ir para imagem 77 e setup guiado. |
| Falhou, expirou, foi recusado ou cancelado | Pagamento nao confirmado. | Ir para imagem 76. |

## Nao Incluir

- formulario de cartao;
- Pix;
- boleto;
- QR Code;
- cupom;
- comparativo de planos;
- upsell;
- configuracao do studio;
- importacao de dados;
- convite de equipe;
- agentes;
- sidebar ou menu do CRM;
- CTA para entrar no app antes da confirmacao.

## Ajustes Finos Aceitos Para Implementacao Visual

A imagem esta aprovada como contrato. Na implementacao visual futura, manter a estrutura e apenas refinar:

- o estado `Verificando...` deve parecer claramente desabilitado/loading, sem competir com CTA primario;
- os links de fallback devem ficar discretos;
- a microcopy final nao deve duplicar a mensagem de verificacao automatica;
- o icone de seguranca pode ganhar leve presenca, sem virar elemento decorativo dominante.

## Criterio De Aceite

A tela esta correta quando o usuario entende que:

- o pagamento foi iniciado;
- a Taliya esta aguardando confirmacao segura;
- ele nao precisa atualizar a pagina;
- ainda nao tem acesso ao CRM;
- pode retomar o pagamento ou falar com suporte se algo sair do fluxo normal.

## Proxima Tela De Falha

Quando a verificacao automatica concluir que a tentativa nao confirmou, a continuidade aprovada e a imagem 76:

`76_round-4.1Q_acesso-assinatura_resolver-assinatura-aprovado.png`

Quando a verificacao automatica confirmar a assinatura, a continuidade aprovada e a imagem 77:

`77_round-4.1Q_acesso-assinatura_assinatura-confirmada-setup-guiado-aprovado.png`
