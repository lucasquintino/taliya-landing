# Taliya CRM - Contratos De Campos Das Configuracoes Pos-Go-Live

Status: contrato v1.
Data: 2026-05-24.

## Objetivo

Definir exatamente quais campos cada pagina de Configuracoes Pos-Go-Live pode mostrar, editar, validar e auditar.

Este documento evita tres erros:

1. transformar Configuracoes em painel gigante;
2. duplicar configuracoes que pertencem a Agentes/Fluxos, Integracoes, Billing ou Operacao;
3. deixar campos livres demais para o dono/admin ajustar coisas que devem ser fixas.

## Regras Globais

- Toda pagina tem `tenantId`.
- Toda mudanca gravavel gera auditoria.
- Toda mudanca sensivel mostra consequencia antes de salvar.
- Campos derivados nao sao editaveis.
- Status tecnico de provedor fica em Integracoes.
- Limite de plano Taliya fica em Billing.
- Regra de agente/fluxo fica em Agentes/Fluxos.
- Operacao diaria fica nas paginas operacionais.

## Tipos Padrao

| Tipo | Uso |
|---|---|
| `text` | texto curto |
| `longText` | observacao curta ou explicacao |
| `email` | e-mail |
| `phone` | telefone/WhatsApp |
| `url` | link publico |
| `boolean` | ligado/desligado |
| `enum` | escolha fechada |
| `multiEnum` | multiplas escolhas fechadas |
| `date` | data |
| `dateRange` | intervalo de datas |
| `time` | horario |
| `timeRange` | intervalo de horario |
| `integer` | numero inteiro |
| `money` | valor monetario |
| `percent` | percentual |
| `reference` | referencia a outro objeto do CRM |
| `computed` | derivado, nao editavel |

## Status De Salvamento

Todas as paginas gravaveis usam:

```text
clean
dirty
saving
saved
validationError
blocked
```

## Auditoria Minima

Toda mudanca salva registra:

- `eventId`;
- `tenantId`;
- `surface`;
- `objectType`;
- `objectId`;
- `actorUserId`;
- `actorRole`;
- `changedAt`;
- `before`;
- `after`;
- `reason`, quando obrigatorio;
- `source`: `manual`, `setup-imported`, `support-assisted`, `system-migration`;
- `requiresApproval`: booleano;
- `approvalId`, se houver.

## 1. `/app/configuracoes` - Hub

### Funcao

Entrada para as configuracoes.

### Campos Visiveis

| Campo | Tipo | Editavel | Origem | Observacao |
|---|---|---:|---|---|
| `title` | computed | Nao | sistema | Sempre `Configuracoes` |
| `subtitle` | computed | Nao | sistema | `Ajustes do CRM depois do go-live.` |
| `cards[]` | computed | Nao | configuracoes | 8 cards fixos |
| `cards[].label` | computed | Nao | sistema | Nome da pagina |
| `cards[].description` | computed | Nao | sistema | Descricao curta |
| `cards[].status` | computed | Nao | pagina filha | `Pronto`, `Revisar`, `Pendente`, `Conectado` |
| `cards[].route` | computed | Nao | sistema | Rota interna |
| `cards[].icon` | computed | Nao | design system | Icone fixo |

### Cards Fixos

| Card | Rota | Descricao |
|---|---|---|
| Studio | `/app/configuracoes/studio` | Dados, unidades e horarios. |
| Equipe | `/app/configuracoes/equipe` | Pessoas que acessam o Taliya. |
| Permissoes | `/app/configuracoes/permissoes` | O que cada papel pode fazer. |
| Canais | `/app/configuracoes/canais` | WhatsApp, e-mail e redes. |
| Planos e modelos | `/app/configuracoes/financeiro/modelos` | O que o aluno compra. |
| Pagamentos e financeiro | `/app/configuracoes/financeiro/pagamentos` | Cobranca, baixa e Pagamentos Taliya. |
| Agenda | `/app/configuracoes/agenda` | Feriados, bloqueios e encaixes. |
| Notificacoes | `/app/configuracoes/notificacoes` | Alertas internos por papel. |

### Nao Tem

- busca;
- filtro;
- formulario;
- Agente de Configuracao;
- historico;
- metricas;
- atividade recente.

## 2. `/app/configuracoes/studio` - Studio

### Funcao

Editar identidade basica do studio e janela institucional de funcionamento.

### Objeto Principal

`StudioSettings`

### Campos

| Campo | Tipo | Obrigatorio | Editavel | Validacao | Observacao |
|---|---|---:|---:|---|---|
| `studioName` | text | Sim | Sim | 2-80 chars | Nome interno/contratual do studio |
| `publicName` | text | Sim | Sim | 2-80 chars | Nome exibido para aluno quando necessario |
| `mainUnitId` | reference | Sim | Sim | deve existir | Unidade principal |
| `address.line1` | text | Sim | Sim | 2-120 chars | Rua e numero |
| `address.line2` | text | Nao | Sim | max 80 chars | Complemento |
| `address.neighborhood` | text | Nao | Sim | max 80 chars | Bairro |
| `address.city` | text | Sim | Sim | 2-80 chars | Cidade |
| `address.state` | enum | Sim | Sim | UF valida | Estado |
| `address.postalCode` | text | Nao | Sim | formato CEP | CEP |
| `timezone` | enum | Sim | Sim | timezone valida | Default `America/Sao_Paulo` |
| `businessDays[]` | multiEnum | Sim | Sim | seg-dom | Dias institucionais de funcionamento |
| `opensAt` | time | Sim | Sim | antes de `closesAt` | Hora padrao de abertura |
| `closesAt` | time | Sim | Sim | depois de `opensAt` | Hora padrao de fechamento |
| `breakStart` | time | Nao | Sim | antes de `breakEnd` | Pausa opcional |
| `breakEnd` | time | Nao | Sim | depois de `breakStart` | Pausa opcional |
| `status` | computed | Nao | Nao | - | `Publicado`, `Alteracao manual`, `Revisar` |

### Nao Edita Aqui

- WhatsApp;
- e-mail;
- redes sociais;
- feriados;
- bloqueios;
- turmas;
- aulas;
- reposicoes;
- fluxo de agente.

### Impacto

Mudanca de horario institucional nao move aulas ja criadas automaticamente. Se houver conflito, a pagina aponta para Agenda.

## 3. `/app/configuracoes/equipe` - Equipe

### Funcao

Gerenciar usuarios do CRM.

### Objetos

- `TeamMember`;
- `TeamInvite`;
- `RoleAssignment`.

### Campos De Membro

| Campo | Tipo | Obrigatorio | Editavel | Validacao | Observacao |
|---|---|---:|---:|---|---|
| `userId` | reference | Sim | Nao | usuario existe | Identidade do usuario |
| `displayName` | text | Sim | Sim | 2-80 chars | Nome mostrado na equipe |
| `email` | email | Sim | Sim | e-mail valido/unico | Login e convite |
| `internalWhatsapp` | phone | Nao | Sim | telefone valido | WhatsApp interno da equipe |
| `role` | enum | Sim | Sim | `owner_admin`, `reception`, `teacher` | Papel principal |
| `status` | enum | Sim | Parcial | `active`, `inactive`, `invitePending` | Status de acesso |
| `lastAccessAt` | computed | Nao | Nao | - | Ultimo acesso |
| `invitedAt` | computed | Nao | Nao | - | Data do convite |
| `invitedBy` | reference | Nao | Nao | usuario existe | Quem convidou |

### Acoes

| Acao | Quem Pode | Requer Confirmacao | Auditoria |
|---|---|---:|---:|
| convidar pessoa | Dono/Admin | Nao | Sim |
| reenviar convite | Dono/Admin | Nao | Sim |
| alterar papel | Dono/Admin | Sim | Sim |
| desativar pessoa | Dono/Admin | Sim | Sim |
| reativar pessoa | Dono/Admin | Sim | Sim |
| transferir dono/admin | Dono/Admin atual | Sim forte | Sim |

### Nao Tem

- matriz detalhada de permissoes;
- escala;
- folha de pagamento;
- comissao;
- limite de agente;
- cota.

## 4. `/app/configuracoes/permissoes` - Permissoes

### Funcao

Definir limites simples por papel.

### Objeto

`RolePermissionSettings`

### Papeis Fixos MVP

```text
owner_admin
reception
teacher
```

### Campos De Papel

| Campo | Tipo | Editavel | Default | Observacao |
|---|---|---:|---|---|
| `role` | enum | Nao | - | Papel |
| `summary` | computed | Nao | - | Explicacao curta |
| `baseCapabilities[]` | computed | Nao | por papel | Padrao do produto |
| `sensitiveControls[]` | array | Sim | ver abaixo | Poucos ajustes sensiveis |

### Ajustes Sensiveis

| Chave | Tipo | Papel Afetado | Default | Opcoes | Observacao |
|---|---|---|---|---|---|
| `teacherCanSeeStudentPhone` | boolean | Professor | false | ligado/desligado | Protege contato do aluno |
| `teacherCanAddObservation` | boolean | Professor | true | ligado/desligado | Observacao em aula/turma |
| `receptionCanRegisterPayment` | boolean | Recepcao | true | ligado/desligado | Baixa manual, se permitido |
| `receptionCanEditStudentPlan` | boolean | Recepcao | false | ligado/desligado | Alteracao de plano exige cuidado |
| `receptionDiscountLimitPercent` | percent/enum | Recepcao | 0 | 0, 5, 10 | Acima disso exige Dono/Admin |
| `receptionCanCancelCharge` | enum | Recepcao | `requiresApproval` | `never`, `requiresApproval`, `allowed` | Cancelamento financeiro |

### Campos Derivados

| Campo | Tipo | Observacao |
|---|---|---|
| `impactSummary[]` | computed | Mostra o que muda antes de salvar |
| `requiresApproval` | computed | Quando a mudanca aumenta permissao sensivel |
| `lastChangedAt` | computed | Ultima alteracao |
| `lastChangedBy` | computed | Responsavel |

### Nao Tem

- builder por campo;
- permissao de agente;
- limite de fluxo;
- cota;
- log tecnico.

## 5. `/app/configuracoes/canais` - Canais

### Funcao

Definir canais oficiais e preferencias de comunicacao do studio.

### Objeto

`ChannelSettings`

### Campos

| Campo | Tipo | Obrigatorio | Editavel | Validacao | Observacao |
|---|---|---:|---:|---|---|
| `whatsappBusinessNumber` | phone | Nao | Sim | telefone valido | Numero publico/oficial |
| `whatsappConnectionStatus` | computed | Nao | Nao | - | Status tecnico aparece embutido em Canais |
| `studioEmail` | email | Nao | Sim | e-mail valido | E-mail publico |
| `instagramUrl` | url | Nao | Sim | URL valida | Canal publico |
| `facebookUrl` | url | Nao | Sim | URL valida | Canal publico |
| `tiktokUrl` | url | Nao | Sim | URL valida | Canal publico |
| `xUrl` | url | Nao | Sim | URL valida | Canal publico |
| `websiteUrl` | url | Nao | Sim | URL valida | Site |
| `primaryContactChannel` | enum | Sim | Sim | `whatsapp`, `email`, `phone`, `none` | Canal principal para contato |
| `internalAlertChannel` | enum | Nao | Sim | `inApp`, `email`, `teamWhatsapp` | Preferencia interna simples |
| `integrationLink` | computed | Nao | Nao | - | Abre Integracoes quando tecnico |

### Nao Tem

- texto de mensagem;
- template;
- campanha;
- automacao;
- agente respondendo aluno;
- log tecnico.

## 6. `/app/configuracoes/financeiro/modelos` - Planos E Modelos

### Funcao

Configurar o que o aluno compra e como esse direito de aula funciona.

### Objeto

`StudentPlanModel`

### Campos Da Lista

| Campo | Tipo | Editavel | Observacao |
|---|---|---:|---|
| `planId` | reference | Nao | Identificador |
| `name` | text | Sim | Nome do plano |
| `status` | enum | Sim | `active`, `inactive`, `draft`, `archived` |
| `studentsUsingCount` | computed | Nao | Alunos vinculados |
| `price` | money | Sim | Valor base |
| `billingCycle` | enum | Sim | `monthly`, `package`, `single`, `trial`, `custom` |

### Campos Do Plano

| Campo | Tipo | Obrigatorio | Editavel | Opcoes/Validacao | Observacao |
|---|---|---:|---:|---|---|
| `name` | text | Sim | Sim | 2-80 chars | Nome exibido |
| `type` | enum | Sim | Sim | `weeklyFrequency`, `monthlyQuantity`, `classPackage`, `singleClass`, `trial`, `customReview` | Tipo fechado |
| `price` | money | Sim | Sim | >= 0 | Valor comercial |
| `classQuantity` | integer | Condicional | Sim | >= 1 | Qtde de aulas |
| `weeklyFrequency` | integer | Condicional | Sim | 1-7 | Frequencia semanal |
| `validityDays` | integer | Condicional | Sim | >= 1 | Validade do pacote/credito |
| `commercialRecurrence` | enum | Nao | Sim | `none`, `monthly`, `custom` | Recorrencia comercial |
| `allowsMakeUp` | boolean | Sim | Sim | - | Permite reposicao |
| `makeUpNoticeMinimumHours` | integer | Condicional | Sim | 0-168 | Aviso minimo |
| `makeUpUseDeadlineDays` | integer | Condicional | Sim | 1-365 | Prazo para usar |
| `noShowRule` | enum | Sim | Sim | `consume`, `doNotConsume`, `requiresReview` | Falta sem aviso |
| `manualExceptionAllowed` | enum | Sim | Sim | `no`, `ownerOnly`, `ownerAndReceptionWithApproval` | Excecao manual |

### Campos Derivados

| Campo | Tipo | Observacao |
|---|---|---|
| `impactSummary` | computed | Alunos afetados e futuras cobrancas |
| `cannotDeactivateReason` | computed | Quando ha dependencias |
| `lastChangedAt` | computed | Auditoria resumida |

### Nao Tem

- Pix;
- dinheiro;
- cartao;
- baixa;
- provedor;
- meio de pagamento por plano;
- mensagem de cobranca;
- automacao de agente.

## 7. `/app/configuracoes/financeiro/pagamentos` - Pagamentos E Financeiro

### Funcao

Configurar cobranca, baixa manual, regras financeiras simples e ativacao de Pagamentos Taliya.

### Objetos

- `PaymentFinanceSettings`;
- `TaliyaPaymentsSettings`;
- `ManualPaymentMethodSettings`.

### Meios E Baixa Manual

| Campo | Tipo | Obrigatorio | Editavel | Default | Observacao |
|---|---|---:|---:|---|---|
| `manualPixEnabled` | boolean | Sim | Sim | true | Pix manual registrado pela equipe |
| `cashEnabled` | boolean | Sim | Sim | true | Dinheiro presencial |
| `inPersonCardEnabled` | boolean | Sim | Sim | true | Cartao presencial |
| `manualPaymentAllowed` | boolean | Sim | Sim | true | Baixa manual permitida |
| `receiptEvidenceAllowed` | boolean | Sim | Sim | true | Comprovante como evidencia, nao meio |

### Regras Financeiras Simples

| Campo | Tipo | Obrigatorio | Editavel | Default | Observacao |
|---|---|---:|---:|---|---|
| `defaultDueDay` | integer | Sim | Sim | 10 | Dia 1-28 |
| `lateToleranceDays` | integer | Sim | Sim | 3 | Dias antes de marcar atraso |
| `markOverduePolicy` | enum | Sim | Sim | `afterTolerance` | `onDueDate`, `afterTolerance`, `manualOnly` |
| `simpleDiscountLimitPercent` | percent | Sim | Sim | 10 | Limite basico; papel fica em Permissoes |
| `cancelChargePolicy` | enum | Sim | Sim | `requiresApproval` | `never`, `requiresApproval`, `allowedForOwner` |

### Pagamentos Taliya

| Campo | Tipo | Obrigatorio | Editavel | Estado | Observacao |
|---|---|---:|---:|---|---|
| `taliyaPaymentsStatus` | enum | Sim | Nao | `pending`, `active`, `blocked`, `error` | Status do provedor |
| `pixTaliyaEnabled` | boolean | Condicional | Sim | ativo | Bloqueado ate ativar |
| `onlineCardEnabled` | boolean | Condicional | Sim | ativo | Bloqueado ate ativar |
| `onlineRecurrenceEnabled` | boolean | Condicional | Sim | ativo | Depende de cobranca recorrente |
| `automaticSettlementEnabled` | computed | Nao | Nao | ativo | Para pagamentos online confirmados |
| `reconciliationEnabled` | computed | Nao | Nao | ativo | Resumo de conciliacao |
| `providerIntegrationId` | reference | Condicional | Nao | ativo | Detalhe tecnico aparece embutido em Pagamentos Taliya |

### Nao Tem

- dados bancarios sensiveis;
- escolha livre de provedor;
- webhook;
- payload;
- log tecnico;
- Billing Taliya;
- fatura da Taliya;
- criacao de plano;
- meio de pagamento por plano;
- bloco separado de comprovante;
- bloco final de impacto.

## 8. `/app/configuracoes/agenda` - Agenda

### Funcao

Configurar excecoes e comportamento basico do calendario.

### Objetos

- `CalendarException`;
- `CalendarTemporaryBlock`;
- `AgendaSimpleRules`.

### Dias Fechados E Excecoes

| Campo | Tipo | Obrigatorio | Editavel | Opcoes/Validacao | Observacao |
|---|---|---:|---:|---|---|
| `exceptionId` | reference | Sim | Nao | - | Identificador |
| `type` | enum | Sim | Sim | `holiday`, `recess`, `closedDay`, `specialHours` | Tipo fechado |
| `label` | text | Sim | Sim | 2-80 chars | Nome curto |
| `date` | date | Condicional | Sim | data valida | Para dia unico |
| `dateRange` | dateRange | Condicional | Sim | inicio <= fim | Para recesso |
| `unitId` | reference | Nao | Sim | unidade existe | Se vazio, todas |
| `specialOpensAt` | time | Condicional | Sim | antes de fechar | Horario especial |
| `specialClosesAt` | time | Condicional | Sim | depois de abrir | Horario especial |
| `status` | enum | Sim | Nao | `published`, `reviewFutureClasses`, `draft` | Status local |

### Bloqueios Temporarios

| Campo | Tipo | Obrigatorio | Editavel | Opcoes/Validacao | Observacao |
|---|---|---:|---:|---|---|
| `blockId` | reference | Sim | Nao | - | Identificador |
| `reason` | text | Sim | Sim | 2-80 chars | Motivo |
| `period` | dateRange/timeRange | Sim | Sim | valido | Data/hora bloqueada |
| `scopeType` | enum | Sim | Sim | `unit`, `room`, `classGroup`, `teacher`, `all` | Escopo |
| `scopeId` | reference | Condicional | Sim | existe | Unidade/sala/turma/professor |
| `blocksNewBookings` | boolean | Sim | Sim | true | Bloqueia novas marcacoes |
| `affectedFutureClassesCount` | computed | Nao | Nao | - | Impacto local no item |

### Regras Simples Da Agenda

| Campo | Tipo | Obrigatorio | Editavel | Default | Observacao |
|---|---|---:|---:|---|---|
| `waitlistEnabled` | boolean | Sim | Sim | true | Liga lista de espera |
| `fitInPolicy` | enum | Sim | Sim | `requiresApproval` | `allowed`, `requiresApproval`, `notAllowed` |
| `attendanceToleranceMinutes` | integer | Nao | Sim | 10 | Tolerancia simples de chamada |

### Nao Tem

- agenda diaria;
- calendario operacional completo;
- saldo/reposicao detalhada;
- pagamento;
- mensagem automatica;
- fluxo de agente;
- regra profunda de falta/no-show;
- bloco separado de resumo de impacto.

## 9. `/app/configuracoes/notificacoes` - Notificacoes

### Funcao

Definir quem da equipe recebe alertas internos do CRM.

### Objetos

- `NotificationRoleSettings`;
- `NotificationFrequencySettings`;
- `InternalChannelSettings`.

### Alertas Por Papel

| Campo | Tipo | Obrigatorio | Editavel | Opcoes | Observacao |
|---|---|---:|---:|---|---|
| `role` | enum | Sim | Nao | `owner_admin`, `reception`, `teacher` | Papel |
| `enabledAlertTypes[]` | multiEnum | Sim | Sim | lista abaixo | Tipos permitidos por papel |
| `roleSummary` | computed | Nao | Nao | - | Texto curto |

### Tipos De Alerta

| Tipo | Criticidade Padrao | Papeis Padrao |
|---|---|---|
| `approvalPending` | alta | Dono/Admin, Recepcao quando aplicavel |
| `criticalPayment` | alta | Dono/Admin |
| `integrationFailure` | alta | Dono/Admin |
| `classProblem` | media | Recepcao, Professor quando turma propria |
| `studentMissingContact` | media | Recepcao |
| `manualCharge` | media | Recepcao, Dono/Admin |
| `teamInvitePending` | baixa | Dono/Admin |
| `configurationPending` | media | Dono/Admin |
| `teacherClassAlert` | media | Professor |
| `importantObservation` | media | Professor quando permitido |

### Frequencia

| Campo | Tipo | Obrigatorio | Editavel | Default | Observacao |
|---|---|---:|---:|---|---|
| `criticalFrequency` | enum | Sim | Sim | `immediate` | Critico |
| `operationalFrequency` | enum | Sim | Sim | `daily` | Operacional |
| `informationalFrequency` | enum | Sim | Sim | `weekly` | Informativo |
| `nonCriticalAfterHoursPolicy` | enum | Sim | Sim | `silentAfterHours` | Nao critico fora do horario |

### Canais Internos

| Campo | Tipo | Obrigatorio | Editavel | Default | Observacao |
|---|---|---:|---:|---|---|
| `inAppEnabled` | boolean | Sim | Sim | true | Dentro do Taliya |
| `emailInternalPolicy` | enum | Sim | Sim | `ownerAdminOnly` | E-mail interno |
| `teamWhatsappPolicy` | enum | Sim | Sim | `criticalOnly` | WhatsApp da equipe |
| `afterHoursPolicy` | enum | Sim | Sim | `criticalOnly` | Fora do horario |

### Nao Tem

- mensagem para aluno;
- template;
- campanha;
- automacao;
- agente;
- cota;
- log tecnico;
- WhatsApp de aluno;
- resumo de impacto;
- historico na tela aprovada.

## Dependencias Entre Paginas

| Se a mudanca envolve | Pagina fonte | Pagina relacionada |
|---|---|---|
| Quem pode fazer | Permissoes | Equipe |
| Quem recebe alerta | Notificacoes | Equipe |
| Por onde falar | Canais | Integracoes quando tecnico |
| Pagamento online | Pagamentos e financeiro | Integracoes/Pagamentos quando tecnico |
| O que aluno compra | Planos e modelos | Pagamentos e financeiro |
| Como agenda abre/fecha | Studio | Agenda para excecoes |
| Feriado ou bloqueio | Agenda | Agenda operacional para revisar aulas |
| Agente executando | Agentes/Fluxos | Uso/Cotas, Auditoria, Operacao |
