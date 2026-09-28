# Contrato - Taliya Interno / Backoffice - PT-BR

> Status: v0.1 com imagens 48, 49 e 50 aprovadas. Este contrato define o backoffice interno da Taliya para controlar leads, clientes/studios, usuarios, suporte, grants, incidentes, billing, entitlements e auditoria sem misturar com o CRM dos studios.

Complemento para a primeira fase de leads, landing, ferramentas externas de analise e melhoria controlada do agente comercial:

- `taliya-internal-leads-analytics-contract.pt-BR.md`.

## Auditoria Do Que Ja Existia

Documentos auditados:

- `taliya-internal-ops.pt-BR.md`;
- `round-7-agents-quotas-governance-spec.pt-BR.md`;
- `round-11-product-closure.pt-BR.md`;
- `routes-and-surfaces.md`;
- `final-screen-contract-matrix.pt-BR.md`;
- `technical-product-contracts.pt-BR.md`;
- `source-of-truth-matrix.pt-BR.md`;
- `permissions-matrix.pt-BR.md`;
- `admin-auditoria-integracoes-billing-contract.pt-BR.md`.

Achados:

1. Ja existe separacao correta entre CRM do studio (`/app/*`) e operacao interna da Taliya (`/internal/*`).
2. O documento antigo ainda tratava admin interno como futuro, mas a Rodada 11 fechou D011/D035: o MVP precisa de console interno minimo.
3. `routes-and-surfaces.md` so mapeava `/internal/sales-inbox`, `/internal/sales-inbox/[leadId]` e `/internal/commercial-metrics`, insuficiente para clientes ativos.
4. `round-7-agents-quotas-governance-spec.pt-BR.md` ja lista rotas internas importantes: tenants, grants, incidentes, billing e agent ops.
5. O produto ja exige grants com escopo, prazo, motivo e auditoria para qualquer acesso interno a tenant.
6. Billing Taliya e fonte da verdade para plano, cota, agentes, add-ons e fatura; CRM do studio apenas reflete.
7. Suporte do studio (`/app/suporte`) agora esta definido como studio -> Taliya, com agente 24/7 e tickets; falta o outro lado: Taliya operando esses tickets internamente.
8. Leads comerciais da Taliya existem, mas nao devem ser confundidos com Vendas/Interessados dos studios.

Conclusao:

Precisamos de um contrato novo para `/internal/*`, porque a operacao interna da Taliya tem modelo mental proprio e nao deve herdar automaticamente o CRM dos studios.

## Decisao Central

Criar a familia **Taliya Interno / Backoffice**.

Esta familia e para funcionarios autorizados da Taliya, nao para studios.

Ela responde:

> Como a Taliya acompanha seus proprios leads, clientes, usuarios, suporte, grants, incidentes, billing e entitlements sem acessar dados dos clientes fora de escopo?

## Fronteiras

### Nao e CRM do studio

`/internal/*` nao opera aulas, alunos, reposicoes, vendas ou financeiro do studio como usuario normal.

Quando a Taliya precisa diagnosticar algo dentro da conta do studio, deve usar grant escopado e auditado.

### Nao e `/app/suporte`

`/app/suporte` e a pagina do studio falando com a Taliya.

`/internal/support` e a fila interna da Taliya atendendo esses tickets.

### Nao e `/app/vendas`

`/app/vendas` controla interessados do studio.

`/internal/leads` controla studios interessados em comprar Taliya.

### Nao e `/app/billing`

`/app/billing` mostra assinatura da Taliya para o studio.

`/internal/billing` opera billing da Taliya para todos os clientes, com permissoes internas.

## Usuarios Internos

| Papel interno | Pode fazer |
| --- | --- |
| Taliya Sales | Operar leads, pipeline comercial, trial e handoff para onboarding. |
| Taliya Customer Success | Acompanhar clientes, saude da conta, onboarding, tickets e riscos de churn. |
| Taliya Support | Atender tickets, diagnosticar incidentes, solicitar grant e responder studios. |
| Taliya Engineering/Ops | Investigar incidentes tecnicos, integracoes, execucoes, logs e reprocessamentos seguros. |
| Taliya Billing/Ops | Ver e operar assinatura, faturas, entitlements, add-ons e bloqueios. |
| Taliya Admin | Gerenciar usuarios internos, permissoes, roles, auditoria e acoes sensiveis. |

## Objetos Internos Canonicos

| Objeto | Uso |
| --- | --- |
| InternalLead | Studio interessado em comprar Taliya. |
| InternalDeal | Oportunidade comercial da Taliya. |
| Tenant | Studio cliente/prospect ativado no sistema. |
| TenantUser | Usuario pertencente a um tenant. |
| InternalUser | Funcionario ou prestador autorizado da Taliya. |
| SupportTicket | Ticket do studio com a Taliya. |
| SupportAccessGrant | Acesso temporario autorizado pelo studio. |
| InternalIncident | Incidente tecnico ou operacional da Taliya. |
| Entitlement | Plano, agentes, cotas e add-ons liberados. |
| TaliyaInvoice | Fatura/assinatura do studio com a Taliya. |
| InternalAuditEvent | Evento de auditoria interno da Taliya. |
| TenantHealthSignal | Sinal de saude/risco do cliente Taliya. |

## Rotas Oficiais Do `/internal`

| Rota | Papel |
| --- | --- |
| `/internal` | Visao operacional interna da Taliya. |
| `/internal/leads` | Pipeline/lista de studios interessados em contratar Taliya. |
| `/internal/leads/[leadId]` | Detalhe de lead/oportunidade comercial da Taliya. |
| `/internal/tenants` | Lista de clientes/studios, trials, bloqueados, ativos e cancelados. |
| `/internal/tenants/[tenantId]` | Visao 360 do studio cliente. |
| `/internal/tenants/[tenantId]/users` | Usuarios do tenant, convites, papeis e status. |
| `/internal/tenants/[tenantId]/entitlements` | Plano, agentes, cotas, add-ons e limites do tenant. |
| `/internal/support` | Fila interna de tickets dos studios com a Taliya. |
| `/internal/support/tickets/[ticketId]` | Detalhe interno de ticket. |
| `/internal/support/grants` | Grants solicitados, ativos, expirados, negados e revogados. |
| `/internal/support/grants/[grantId]` | Detalhe e uso de grant. |
| `/internal/incidents` | Incidentes tecnicos/operacionais da Taliya. |
| `/internal/incidents/[incidentId]` | Detalhe de incidente, impacto, causa e mitigacao. |
| `/internal/billing` | Assinaturas, faturas, falhas de pagamento e pacotes. |
| `/internal/billing/[accountId]` | Detalhe billing de um cliente/studio. |
| `/internal/users` | Usuarios internos da Taliya e permissoes. |
| `/internal/audit` | Auditoria interna e eventos de acesso. |
| `/internal/audit/[eventId]` | Detalhe de evento interno. |

Rotas que ja existiam:

- `/internal/sales-inbox` passa a ser alias ou modo de `/internal/leads`;
- `/internal/commercial-metrics` passa a ser aba/relatorio de `/internal/leads` ou `/internal`.

## Paginas E Proposito

### `/internal`

Mesa de comando interna da Taliya.

Blocos:

- leads novos/quentes;
- tenants com risco;
- tickets pendentes;
- incidentes abertos;
- grants ativos/pendentes;
- billing com falha;
- entitlements/cotas em alerta;
- atividade interna recente.

Acoes:

- abrir lead;
- abrir tenant;
- abrir ticket;
- abrir incidente;
- revisar grant;
- abrir billing;
- filtrar por responsavel/time.

### `/internal/leads`

Controla o funil comercial da propria Taliya.

Entram:

- leads vindos da landing;
- pedidos de demo;
- trials;
- contatos manuais;
- indicacoes;
- inbound de WhatsApp/site quando for compra da Taliya.

Nao entram:

- interessados dos studios;
- alunos;
- oportunidades de venda dos clientes.

Padrao visual:

- pode herdar Vendas/Pipeline e Vendas/Lista;
- nao precisa imagem propria se ficar claro no texto.

### `/internal/leads/[leadId]`

Detalhe de um studio interessado em comprar Taliya.

Campos:

- studio;
- contato principal;
- origem;
- etapa comercial;
- interesse;
- plano sugerido;
- demo/trial;
- proxima acao;
- dono interno;
- historico de contato;
- notas internas;
- handoff para tenant/onboarding quando converter.

Acoes:

- atualizar etapa;
- registrar contato;
- agendar demo;
- iniciar trial;
- converter em tenant;
- marcar perdido;
- abrir auditoria.

### `/internal/tenants`

Lista de studios clientes/prospects.

Campos:

- studio;
- status (`lead`, `trial`, `ativo`, `risco`, `bloqueado`, `cancelado`);
- plano;
- agentes contratados;
- uso/cota;
- usuarios ativos;
- ultimo acesso;
- tickets abertos;
- grants ativos;
- incidentes recentes;
- billing;
- responsavel interno Taliya.

Acoes:

- abrir tenant;
- abrir suporte;
- abrir billing;
- abrir grants;
- sinalizar risco;
- iniciar handoff de onboarding;
- bloquear/desbloquear apenas conforme politica e permissao.

### `/internal/tenants/[tenantId]`

Visao 360 do studio cliente.

Abas/blocos:

- resumo;
- assinatura/entitlements;
- usuarios;
- uso/cotas;
- integracoes/status;
- suporte/tickets;
- grants;
- incidentes;
- auditoria;
- notas internas.

Regra critica:

Esta pagina mostra metadados do tenant por padrao. Dados operacionais detalhados do studio so podem ser abertos com grant ativo e escopo compativel.

### `/internal/tenants/[tenantId]/users`

Controle de usuarios do tenant para suporte e administracao.

Campos:

- nome;
- email/telefone;
- papel;
- status;
- ultimo login;
- convite;
- 2FA/seguranca quando aplicavel;
- tenant;
- permissoes de alto risco.

Acoes:

- reenviar convite;
- orientar redefinicao;
- bloquear/desbloquear acesso conforme politica;
- abrir auditoria;
- nunca assumir conta sem trilha e permissao.

### `/internal/tenants/[tenantId]/entitlements`

Controle interno do que o tenant tem direito a usar.

Campos:

- plano atual;
- status de billing;
- agentes contratados;
- agentes ativos;
- cotas;
- pacotes/add-ons;
- limites por fluxo quando aplicavel;
- bloqueios por plano;
- vigencia;
- origem da alteracao;
- historico de mudancas.

Acoes:

- abrir billing;
- abrir uso/cotas;
- aplicar entitlement vindo do billing;
- corrigir inconsistencia com auditoria;
- bloquear/desbloquear recurso conforme politica;
- nunca liberar plano/cota manualmente sem evento confiavel, motivo e permissao interna alta.

### `/internal/support`

Fila interna dos tickets abertos pelos studios em `/app/suporte`.

Campos:

- ticket;
- studio;
- tipo;
- severidade;
- status;
- responsavel Taliya;
- SLA;
- proxima acao;
- grant necessario;
- incidente vinculado;
- ultima resposta.

Acoes:

- responder;
- atribuir;
- pedir contexto;
- solicitar grant;
- abrir incidente;
- abrir tenant;
- marcar resolvido;
- escalar.

### `/internal/support/tickets/[ticketId]`

Detalhe interno de ticket aberto por um studio.

Campos:

- studio;
- solicitante;
- tipo;
- severidade;
- status;
- responsavel Taliya;
- conversa;
- resumo do agente de suporte 24/7;
- anexos;
- origem relacionada;
- logs relacionados;
- incidente vinculado;
- grant vinculado;
- auditoria.

Acoes:

- responder ao studio;
- pedir contexto;
- anexar arquivo;
- solicitar grant;
- abrir incidente;
- abrir tenant;
- escalar;
- marcar resolvido;
- reabrir.

### `/internal/support/grants`

Fila de acessos temporarios autorizados pelos studios.

Campos:

- studio;
- ticket;
- escopo;
- status;
- solicitante;
- aprovador do studio;
- usuario Taliya autorizado;
- inicio;
- expiracao;
- objetos permitidos;
- acoes permitidas;
- auditoria.

Acoes:

- solicitar grant;
- abrir grant;
- usar grant;
- encerrar uso;
- revogar;
- auditar.

Regra:

Grant nao e "impersonar invisivel". Todo uso deve ser visivel, escopado e auditado.

### `/internal/support/grants/[grantId]`

Detalhe e uso auditado de um grant.

Campos:

- studio;
- ticket relacionado;
- motivo;
- escopo;
- dados permitidos;
- acoes permitidas;
- solicitante Taliya;
- aprovador do studio;
- usuarios Taliya autorizados;
- inicio;
- expiracao;
- status;
- eventos de uso.

Acoes:

- usar grant dentro do escopo;
- encerrar sessao;
- revogar;
- abrir auditoria;
- abrir ticket;
- reportar acesso indevido.

### `/internal/incidents`

Incidentes da plataforma Taliya.

Entram:

- falha de WhatsApp/provedor;
- falha de pagamentos;
- erro de importacao;
- incidente de agente/runtime;
- queda de servico;
- bug que afeta tenants;
- billing/entitlement inconsistente.

Campos:

- severidade S1-S4;
- status;
- tenants afetados;
- superficie afetada;
- causa provavel;
- mitigacao;
- responsavel;
- SLA;
- comunicacao;
- postmortem quando necessario.

### `/internal/incidents/[incidentId]`

Detalhe do incidente interno.

Campos:

- severidade;
- status;
- resumo;
- servico afetado;
- tenants afetados;
- tickets relacionados;
- execucoes/logs relacionados;
- causa provavel;
- mitigacao;
- correcao;
- comunicacao enviada;
- responsavel;
- SLA;
- postmortem quando necessario.

Acoes:

- atualizar status;
- vincular tenant;
- vincular ticket;
- comunicar tenants afetados;
- registrar mitigacao;
- resolver;
- abrir postmortem;
- abrir auditoria.

### `/internal/billing`

Operacao interna de assinatura da Taliya.

Inclui:

- faturas;
- status de pagamento;
- planos;
- add-ons;
- pacotes de cota;
- entitlements;
- bloqueios por inadimplencia;
- historico de alteracoes.

Nao inclui:

- financeiro dos alunos do studio.

### `/internal/billing/[accountId]`

Detalhe de billing de um studio cliente.

Campos:

- tenant;
- plano;
- status da assinatura;
- faturas;
- metodo de pagamento;
- add-ons;
- pacotes de cota;
- agentes liberados;
- entitlements efetivos;
- falhas de pagamento;
- historico de alteracoes.

Acoes:

- abrir fatura;
- abrir portal/provedor quando aplicavel;
- reprocessar webhook seguro;
- sincronizar entitlement;
- registrar ajuste com permissao alta;
- abrir suporte;
- abrir auditoria.

### `/internal/users`

Usuarios internos da Taliya.

Inclui:

- usuarios do time Taliya;
- papeis internos;
- permissoes;
- status;
- ultimo acesso;
- escopo de times;
- desligamento/bloqueio.

### `/internal/audit`

Auditoria interna da Taliya.

Inclui:

- acesso a tenant;
- uso de grant;
- alteracao de entitlement;
- alteracao billing;
- resposta de suporte;
- visualizacao/exportacao sensivel;
- acao em incidente;
- alteracao de usuario interno.

### `/internal/audit/[eventId]`

Detalhe de evento interno.

Campos:

- ator;
- time;
- acao;
- objeto;
- tenant afetado quando houver;
- grant relacionado quando houver;
- antes/depois;
- motivo;
- risco;
- horario;
- IP/dispositivo quando disponivel;
- ticket/incidente/billing relacionado.

Acoes:

- abrir objeto;
- abrir tenant;
- abrir grant;
- exportar se permitido;
- reportar problema de auditoria.

## O Que Fica Fora Do MVP Interno

Nao criar rotas proprias agora para:

- `/internal/onboarding`: onboarding de cliente fica em `/internal/tenants` e `/internal/tenants/[tenantId]` por status/blocos;
- `/internal/agent-ops`: operacao de runtime/agentes fica inicialmente em `/internal/incidents` e no detalhe de tenant; pode virar rota propria depois da familia Agentes/Uso/Cotas;
- `/internal/integrations`: status de integracoes fica em tenant, incidentes e suporte; rota propria so se operacao tecnica cross-tenant virar central;
- `/internal/feature-flags`: feature flags/config interna ficam fora do mapeamento visual do MVP;
- `/internal/data-explorer`: proibido como acesso amplo a dados de tenant; qualquer diagnostico usa grant e origem auditada.

## Ciclos Principais

### Lead Taliya -> Tenant

```text
lead entra
  -> Taliya qualifica
  -> demo/trial
  -> checkout/contrato
  -> tenant criado/ativado
  -> onboarding
  -> cliente ativo
```

### Ticket Do Studio -> Suporte Interno

```text
studio abre ticket em /app/suporte
  -> ticket aparece em /internal/support
  -> agente 24/7 anexa resumo/contexto
  -> suporte Taliya responde ou pede dados
  -> se precisar acessar tenant, solicita grant
  -> acao executada dentro do escopo
  -> ticket resolvido
  -> auditoria fica visivel
```

### Grant De Suporte

```text
Taliya solicita grant
  -> studio aprova escopo/prazo
  -> Taliya usa grant
  -> cada visualizacao/acao audita
  -> grant expira ou e revogado
```

### Incidente Interno

```text
falha detectada
  -> incidente aberto
  -> severidade definida
  -> tenants afetados identificados
  -> mitigacao/comunicacao
  -> correcao
  -> postmortem se necessario
```

## Manual, Copiloto E Autonomo

No backoffice interno, autonomia e mais restrita que no CRM dos studios.

| Modo | Comportamento |
| --- | --- |
| Manual | Time Taliya decide e executa acoes sensiveis. |
| Copiloto interno | Resume tickets, logs, incidentes, billing, risco de tenant e sugere proxima acao. |
| Autonomo interno | Permitido apenas para triagem, classificacao, resumo, deduplicacao e rascunhos. |

Bloqueios:

- agente interno nao concede grant;
- agente interno nao acessa tenant sem grant;
- agente interno nao altera billing/entitlement sozinho;
- agente interno nao bloqueia tenant sozinho;
- agente interno nao exporta dados sensiveis sozinho;
- agente interno nao responde como studio a alunos.

## Dados, Permissao E Auditoria

Regras obrigatorias:

- todo registro interno deve ter ator, time, permissao e trilha;
- todo acesso a tenant deve ter motivo;
- dados operacionais do studio ficam mascarados quando nao houver grant;
- billing/entitlement exige permissao interna alta;
- acoes sensiveis exigem confirmacao e motivo;
- suporte interno nunca tem acesso permanente;
- auditoria interna nao e editavel.

## O Que Nao Deve Aparecer

- `/internal` dentro do app shell do studio como se fosse area do cliente;
- dados de alunos visiveis por padrao;
- botao de "entrar como cliente" sem grant e auditoria;
- suporte Taliya respondendo aluno;
- billing Taliya misturado com financeiro do studio;
- leads Taliya misturados com interessados dos studios;
- grants sem expiracao;
- incidentes sem severidade;
- bloqueio de tenant sem motivo e auditoria.

## Cobertura Visual Recomendada

Esta familia deve ter imagem propria porque muda o modelo mental: Taliya operando o SaaS, nao studio operando Pilates.

Imagens recomendadas:

| Imagem | Nome sugerido | Objetivo |
| --- | --- | --- |
| 48 | `48_round-4.1K_internal_01_visao-operacional.png` | Imagem aprovada: mesa interna da Taliya com leads, tenants, tickets, incidentes, billing e grants. |
| 49 | `49_round-4.1K_internal_02_tenants-lista-detalhe.png` | Imagem aprovada: lista de clientes/studios com detalhe lateral de tenant. |
| 50 | `50_round-4.1K_internal_03_tenant-detalhe-usuarios-grants.png` | Imagem aprovada: detalhe 360 de um tenant com usuarios, plano, uso, suporte, grants e auditoria. |

Imagens que podem ser herdadas:

- `/internal/leads` pode herdar Vendas/Pipeline e Lista;
- `/internal/support` pode herdar Suporte 47 + lista/detalhe;
- `/internal/incidents` pode herdar Operacao/Incidentes;
- `/internal/billing` pode herdar Uso/Cotas/Billing quando essa familia for fechada;
- `/internal/audit` pode herdar Auditoria/log.

## Auditoria Visual Da Imagem 48

Imagem aprovada:

`48_round-4.1K_internal_01_visao-operacional.png`

Decisoes registradas:

- cobre `/internal`;
- comprova o modelo mental de console interno da Taliya, separado do CRM dos studios;
- mostra leads Taliya, clientes/tenants, tickets de suporte, grants de acesso, incidentes, billing/entitlements, atividade interna e copiloto interno;
- `Novo lead` cria lead da Taliya, nao interessado do studio;
- `Abrir ticket interno` cria ticket interno da Taliya ou ticket vinculado ao studio, nao ticket para aluno;
- `Billing e entitlements` representa billing da plataforma Taliya, nao financeiro dos alunos;
- `Abrir tenant` abre metadados e visao permitida do studio, nao acesso operacional completo;
- `Abrir importacao` so pode exibir dados detalhados se o grant cobrir importacao/duplicidades;
- `Usar grant` exige sessao escopada e audita cada visualizacao/acao;
- grants sempre precisam escopo, motivo, permissao e expiracao;
- dados de alunos nao aparecem por padrao;
- copiloto interno apenas resume/prioriza e nao concede grant, nao altera billing, nao bloqueia tenant e nao acessa dados sensiveis sozinho;
- painel direito aberto representa estado selecionado para documentacao visual; a tela pode carregar sem detalhe ou com item recente selecionado.

URL:

- rota canonica: `/internal`;
- a imagem mostra `https://app.taliya.com/internal`, valido como host + rota interna.

## Auditoria Visual Da Imagem 49

Imagem aprovada:

`49_round-4.1K_internal_02_tenants-lista-detalhe.png`

Arquivo salvo em:

`D:\Downloads\taliya-crm-chatgpt-images-named-20260511-082508\49_round-4.1K_internal_02_tenants-lista-detalhe.png`

Decisoes registradas:

- cobre `/internal/tenants`;
- comprova a lista interna de clientes/studios da Taliya;
- mostra filtros rapidos por status operacional interno: ativos, trial, em risco, billing falhou, grant ativo, incidente aberto, cota alta e cancelados;
- tabela central mostra apenas metadados de tenant: status, plano, agentes, cota, tickets, grant, billing, responsavel e ultima atividade;
- painel direito mostra detalhe seguro do tenant selecionado;
- `Abrir tenant` abre metadados e visao permitida, nao dados operacionais completos do studio;
- `Solicitar grant` e o caminho correto para diagnostico que exija dados do studio;
- `Ver suporte`, `Ver grants`, `Ver billing`, `Ver auditoria` e `Adicionar nota interna` sao acoes contextuais internas;
- dados de alunos, conversas e financeiro do studio nao aparecem por padrao;
- o copiloto interno resume/prioriza, mas nao concede grant, nao altera billing e nao bloqueia tenant sozinho;
- regras de seguranca devem ficar visiveis na pagina, reforcando grant, auditoria e separacao entre Taliya e studio.

Correcao de implementacao:

- a imagem gerada exibiu checkboxes por linha, mas checkboxes **nao** fazem parte do padrao aprovado para `/internal/tenants`;
- selecao padrao deve ser por clique em uma linha, com fundo selecionado e painel lateral;
- evitar selecao em massa de tenants por padrao, porque acoes sobre cliente/studio sao sensiveis;
- menus de tres pontos por linha podem existir para acoes contextuais;
- acoes em lote so podem existir quando forem seguras e explicitas, como exportar lista filtrada ou atribuir responsavel, sempre com permissao e confirmacao.

URL:

- rota canonica: `/internal/tenants`;
- a imagem mostra `https://app.taliya.com/internal/tenants`, valido como host + rota interna.

## Auditoria Visual Da Imagem 50

Imagem aprovada:

`50_round-4.1K_internal_03_tenant-detalhe-usuarios-grants.png`

Arquivo salvo em:

`D:\Downloads\taliya-crm-chatgpt-images-named-20260511-082508\50_round-4.1K_internal_03_tenant-detalhe-usuarios-grants.png`

Decisoes registradas:

- cobre `/internal/tenants/[tenantId]`;
- comprova a visao 360 interna e segura de um tenant ativo;
- mostra dados administrativos do studio: status, plano, billing Taliya, uso, cota, usuarios, grants, tickets, incidentes, integracoes e auditoria;
- usuarios listados sao usuarios do tenant, nao alunos;
- `Entitlements e uso` representa plano, agentes, cotas e limites contratados na Taliya, nao financeiro dos alunos;
- `Suporte`, `Grants`, `Incidentes` e `Auditoria` aparecem como blocos de diagnostico e atalhos internos, sem expor operacao completa do studio;
- painel direito `Seguranca do tenant` deixa visivel se existe grant ativo, escopo, expiracao, aprovador, usuario interno e permissao;
- `Usar grant` so pode liberar acoes dentro do escopo aprovado e deve auditar cada visualizacao/acao;
- `Solicitar grant`, `Abrir suporte`, `Ver auditoria` e `Abrir billing` sao acoes internas da Taliya;
- nao deve haver botao generico de "entrar como cliente" ou acesso amplo ao CRM do studio;
- dados de alunos, conversas, cobrancas, aulas, agenda e reposicoes nao aparecem por padrao;
- copiloto interno apenas resume, prioriza e recomenda proximas acoes; nao concede grant, nao altera billing, nao bloqueia tenant e nao acessa dados sensiveis sozinho.

Correcao de implementacao:

- a imagem gerada exibiu numeros antes de alguns blocos/cards; esses numeros sao artefato visual da geracao e nao fazem parte obrigatoria do padrao da UI;
- manter a composicao de cards e painel lateral, mas remover numeracao decorativa se a implementacao real nao precisar dela;
- qualquer bloco que leve a dados sensiveis deve respeitar grant, permissao, trilha de auditoria e escopo temporal.

URL:

- rota canonica: `/internal/tenants/[tenantId]`;
- a imagem mostra `https://app.taliya.com/internal/tenants/tenant_vila_mariana`, valido como exemplo de host + rota interna.

## Decisao Para MVP

Para fechar `/internal` sem inflar:

1. Criar contrato novo desta familia.
2. Atualizar o doc antigo `taliya-internal-ops.pt-BR.md` para apontar para este contrato.
3. Imagem 48 aprovada para a visao operacional interna.
4. Imagem 49 aprovada para tenants lista + detalhe, com correcao de nao usar checkboxes por linha.
5. Imagem 50 aprovada para tenant 360, usuarios, grants, entitlements e auditoria.
6. `/internal/leads`, `/internal/support`, `/internal/support/grants`, `/internal/incidents`, `/internal/billing` e `/internal/audit` herdam padroes ja aprovados no MVP e nao precisam imagem propria agora.

Leads internos nao precisam primeira imagem propria, a menos que a venda da Taliya vire foco visual depois.
