# Taliya CRM - Contratos De Estados Das Configuracoes Pos-Go-Live

Status: contrato v1.
Data: 2026-05-24.

## Objetivo

Definir todos os estados visuais e operacionais que as paginas de Configuracoes Pos-Go-Live precisam suportar.

Este documento cobre:

- estado publicado;
- alteracao pendente;
- bloqueio por permissao;
- bloqueio por integracao;
- bloqueio por plano/entitlement;
- erro de validacao;
- recurso pausado/inativo;
- revisao necessaria;
- fallback quando a pagina aponta para outra area.

## Estados Globais

| Estado | Significado | UI Esperada | CTA Principal |
|---|---|---|---|
| `published` | Configuracao salva e ativa | chip `Publicado` ou `Pronto` | Nenhum ou `Salvar alteracoes` se editar |
| `dirty` | Usuario alterou algo e nao salvou | aviso discreto `Alteracoes nao salvas` | `Salvar alteracoes` |
| `saving` | Salvando | botao com loading | nenhum extra |
| `saved` | Salvou agora | toast curto | continuar |
| `validationError` | Campo invalido | erro no campo e resumo curto | corrigir |
| `reviewNeeded` | Algo precisa revisao humana | chip `Revisar` | abrir item |
| `pending` | Configuracao incompleta | chip `Pendente` | completar |
| `blockedPermission` | Usuario nao pode editar | campos read-only | pedir acesso ou voltar |
| `blockedIntegration` | Depende de integracao tecnica | chip `Integracao pendente` | abrir detalhe tecnico na configuracao especifica |
| `blockedEntitlement` | Plano Taliya nao inclui recurso | chip `Nao contratado` | `Ver plano` |
| `systemError` | Falha inesperada | alerta recuperavel | tentar novamente |

## Regras De Exibicao

- Estado nao pode depender apenas de cor.
- Todo bloqueio deve explicar motivo e proximo destino.
- Pagina bloqueada por permissao continua visivel em leitura quando possivel.
- Erro tecnico de provedor nunca abre payload bruto. A propria Configuracao mostra status, impacto, teste/reconexao e logs compactos quando necessario.
- Billing nao aparece como configuracao financeira dos alunos.

## 1. Hub `/app/configuracoes`

| Estado | Quando Acontece | Como Mostra | Acao |
|---|---|---|---|
| `allReady` | todos os cards sem pendencia | cards `Pronto`/`Conectado` | abrir pagina |
| `hasReview` | algum card precisa atencao | chip `Revisar` no card | abrir pagina |
| `hasPending` | configuracao incompleta | chip `Pendente` | abrir pagina |
| `readOnly` | usuario sem permissao de editar | cards visiveis, sem acao sensivel | abrir em leitura |
| `entitlementBlocked` | pagina/recurso nao contratado | chip `Nao contratado` no card, quando aplicavel | `Ver plano` ou abrir leitura |

Nao tem Agente de Configuracao.

## 2. Studio

| Estado | Quando Acontece | Como Mostra | Acao |
|---|---|---|---|
| `published` | dados salvos | chip `Publicado` | editar/salvar |
| `dirty` | campo alterado | chip `Alteracao manual` | salvar/cancelar |
| `validationError` | horario invalido, campo obrigatorio vazio | erro no campo | corrigir |
| `reviewAgendaImpact` | horario pode conflitar com aulas | aviso no Agente de Configuracao | abrir Agenda |
| `blockedPermission` | nao Dono/Admin | campos leitura | pedir acesso |

Nao move aulas automaticamente.

## 3. Equipe

| Estado | Quando Acontece | Como Mostra | Acao |
|---|---|---|---|
| `activeMember` | usuario ativo | chip `Ativo` | editar/desativar |
| `inactiveMember` | usuario desativado | chip `Inativo` | reativar |
| `invitePending` | convite enviado nao aceito | chip `Convite pendente` | reenviar/cancelar |
| `ownerTransferPending` | troca de dono em andamento | confirmacao forte | concluir/cancelar |
| `blockedLastAdmin` | tentativa de remover ultimo admin | erro bloqueante | manter admin |
| `blockedPermission` | usuario sem acesso | leitura | pedir acesso |

Equipe nao altera permissao fina; aponta para Permissoes.

## 4. Permissoes

| Estado | Quando Acontece | Como Mostra | Acao |
|---|---|---|---|
| `published` | matriz salva | chip `Publicado` | editar/salvar |
| `reviewPermissions` | regra sensivel recomenda revisao | chip `Revisar permissoes` | revisar ajuste |
| `dirty` | ajuste alterado | botoes salvar/cancelar ativos | salvar/cancelar |
| `requiresApproval` | aumento de permissao sensivel | aviso antes de salvar | confirmar como Dono/Admin |
| `blockedPermission` | nao Dono/Admin | read-only | pedir acesso |
| `validationError` | desconto fora do permitido | erro no campo | corrigir |

Nao configura agente, fluxo ou cota.

## 5. Canais

| Estado | Quando Acontece | Como Mostra | Acao |
|---|---|---|---|
| `connected` | WhatsApp/e-mail conectado | chip `Conectado` | salvar canais |
| `pendingConnection` | canal informado mas nao conectado | chip `Pendente` | conectar/testar |
| `disconnected` | canal tecnico desconectado | chip `Desconectado` | testar/reconectar |
| `dirty` | canal editado | salvar/cancelar | salvar |
| `invalidUrlOrEmail` | campo invalido | erro no campo | corrigir |
| `blockedPermission` | sem acesso | leitura | pedir acesso |

Logs tecnicos ficam em Integracoes.

## 6. Planos E Modelos

| Estado | Quando Acontece | Como Mostra | Acao |
|---|---|---|---|
| `activePlan` | plano em uso | chip `Ativo` | editar/duplicar |
| `inactivePlan` | plano desligado | chip `Inativo` | reativar/duplicar |
| `draftPlan` | plano criado nao publicado | chip `Rascunho` | publicar |
| `planInUse` | alunos usando plano | contador | revisar impacto antes de salvar |
| `cannotDelete` | plano com alunos/historico | acao bloqueada | inativar |
| `reviewConsumption` | reposicao/falta exige revisao | chip `Revisar` | ajustar |
| `blockedPermission` | sem acesso | leitura | pedir acesso |

Meios de pagamento nao ficam aqui.

## 7. Pagamentos E Financeiro

| Estado | Quando Acontece | Como Mostra | Acao |
|---|---|---|---|
| `manualActive` | meios manuais ativos | chip `Manual ativo` | salvar regras |
| `taliyaPaymentsPending` | online nao ativado | chip `Pagamentos Taliya pendente` | ativar |
| `taliyaPaymentsActive` | online ativo | chip `Pagamentos Taliya ativo` | salvar preferencias |
| `providerBlocked` | provedor bloqueou/nao validou | chip `Revisar ativacao` | revisar ativacao |
| `integrationError` | webhook/provedor falhando | chip `Falha tecnica` | ver detalhe tecnico |
| `dirty` | regra editada | salvar/cancelar | salvar |
| `blockedPermission` | sem acesso financeiro | leitura | pedir acesso |
| `blockedEntitlement` | Pagamentos Taliya nao contratado | online bloqueado | ver plano |

Comprovante e evidencia de baixa manual, nao meio.

## 8. Agenda

| Estado | Quando Acontece | Como Mostra | Acao |
|---|---|---|---|
| `published` | regras salvas | chip `Publicado` | salvar alteracoes |
| `activeBlocks` | existe bloqueio ativo | chip `2 bloqueios ativos` | abrir item |
| `reviewFutureClass` | excecao/bloqueio afeta aula futura | chip local no item | abrir item ou Agenda |
| `dirty` | regra editada | salvar/cancelar | salvar |
| `invalidPeriod` | data/hora invalida | erro no campo | corrigir |
| `blockedPermission` | sem acesso | leitura | pedir acesso |

Nao tem resumo de impacto separado. Impacto aparece dentro do item afetado.

## 9. Notificacoes

| Estado | Quando Acontece | Como Mostra | Acao |
|---|---|---|---|
| `published` | preferencias salvas | chip `Publicado` | salvar alteracoes |
| `rolesConfigured` | papeis configurados | chip `3 papeis configurados` | revisar |
| `reviewAlert` | algum alerta precisa revisao | chip `Revisar 1 alerta` | abrir ajuste |
| `dirty` | ajuste editado | salvar/cancelar | salvar |
| `blockedPermission` | sem acesso | leitura | pedir acesso |
| `channelUnavailable` | canal interno indisponivel | aviso no campo | ajustar canal |

`Nao critico` pode estar ligado e silenciado fora do horario.

WhatsApp interno e sempre WhatsApp da equipe.

## Estados Que Nao Geram Imagem Propria

Nao gerar imagem separada agora para:

- permissao insuficiente;
- erro de integracao;
- recurso nao contratado;
- alteracao pendente;
- configuracao publicada;
- configuracao com item em revisao;
- plano 0/1/3/7 agentes vendo recurso bloqueado.

Essas variacoes devem ser implementadas com chips, mensagens inline, estados disabled/read-only e CTAs contextuais.

## Destinos De Bloqueio

| Bloqueio | Destino |
|---|---|
| permissao insuficiente | `/app/configuracoes/permissoes` ou pedir Dono/Admin |
| integracao tecnica | configuracao especifica que usa a integracao: Canais, Pagamentos, Agenda, Notificacoes ou job contextual |
| Pagamentos Taliya pendente | `/app/configuracoes/financeiro/pagamentos` |
| plano Taliya nao inclui recurso | `/app/billing` |
| cota ou uso | `/app/uso` ou `/app/uso/cotas` |
| falha de agente/fluxo | `/app/operacao/incidentes` ou `/app/fluxos/execucoes/[runId]` |
| auditoria | `/app/auditoria/[eventId]` |
