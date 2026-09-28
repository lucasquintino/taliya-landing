# Rodada 1 - Ativacao, setup e configuracao essencial - PT-BR

> Status: v0.1. Esta rodada define a base funcional e a primeira especificacao profunda das telas de ativacao inicial, importacao, configuracao essencial, agentes iniciais, cotas e qualidade de dados.

## Objetivo operacional

Permitir que um studio saia de conta paga para CRM operavel no web ou app, sem depender de agente ativo e sem liberar automacoes perigosas antes dos dados minimos.

## Limite desta v0.1

Esta versao ja orienta produto, rotas, objetos, estados e acoes principais, mas ainda deve ser revisada antes de virar prompt final de UI ou tarefa de implementacao.

Faltam, em uma proxima passada da propria Rodada 1:

- detalhar campos exatos por bloco;
- definir colunas de listas/tabelas;
- desenhar estados vazios/erro/bloqueio por tela com mais precisao;
- amarrar cada tela aos casos de uso por ID/linha da matriz;
- definir microcopy de confirmacao para acoes sensiveis;
- separar exatamente o que aparece no app por papel.

## Usuarios envolvidos

| Usuario | Papel na rodada |
| --- | --- |
| Dono | Reivindica conta, define studio, plano, equipe, permissoes e configuracoes sensiveis. |
| Admin | Ajuda setup, importacao, canais, agentes e revisao final. |
| Recepcao/operacao | Pode ajudar dados basicos, importacao simples e canal. |
| Financeiro | Pode ajudar planos financeiros e cobrancas se convidado. |
| Suporte Taliya | Ajuda importacao/integracao somente com autorizacao. |
| Agente/runtime | Nao executa automacao ativa antes do preflight. |

## Objetos de negocio

- Studio/Tenant;
- Unidade;
- Usuario;
- Membro da equipe;
- Convite;
- Papel/permissao;
- Contato;
- Aluno;
- Responsavel;
- Interessado;
- Turma;
- Plano do studio;
- Politica operacional;
- Template/modelo;
- Conexao de canal;
- Job de importacao;
- Problema de dados;
- Agente;
- Fluxo de agente;
- Configuracao de fluxo;
- Lancamento/limite de cota;
- Acesso de suporte.

## Entradas e saidas

| Entrada | Saida esperada |
| --- | --- |
| pagamento/assinatura confirmada | workspace reivindicado e tenant ativo. |
| dados manuais minimos | CRM aberto em modo operacional basico. |
| planilha/importacao | registros importados ou fila de revisao. |
| plano com agentes | agentes incluidos prontos para configurar/testar. |
| dados incompletos | tarefas/problemas de dados, nao automacao cega. |

## Regras de negocio

1. Conta so pode ser reivindicada por link/token valido ou fluxo de billing confirmado.
2. CRM pode abrir com setup minimo, mas deve mostrar pendencias.
3. Base/0 agentes nao ativa automacao, mas permite todos os registros e tarefas manuais.
4. Agente incluido no plano pode ser configurado antes de ativar.
5. Fluxo de agente precisa de preflight antes de publicar: dados, canal, template, cota, permissao, politica e fallback.
6. Importacao nunca mescla duplicidade automaticamente em baixa confianca.
7. Dado sensivel importado deve ficar restrito ate classificacao/revisao.
8. Suporte Taliya so entra com grant escopado.
9. Configuracao feita no app deve ser essencial; configuracao profunda e versionamento ficam web-first.

## Politicas usadas

- permissao de equipe;
- privacidade/consentimento;
- agenda/reposicao;
- cobranca/financeiro;
- autonomia de agente;
- mensagens/templates;
- suporte Taliya.

## Operacao sem agentes

No plano Base, a rodada ainda deve permitir:

- criar studio;
- importar/cadastrar alunos;
- configurar equipe;
- criar agenda/turmas basicas;
- responder manualmente;
- criar tarefas/casos;
- usar Hoje, Inbox, Agenda, Alunos e Financeiro manual.

## Telas web desta rodada

1. Onboarding e configuracao inicial.
2. Configuracoes.
3. Agentes e fluxos.
4. Uso, cotas e economia.
5. Qualidade de dados.

## Telas mobile desta rodada

1. Setup inicial.
2. Importacao assistida.
3. Configuracao inicial de agentes.
4. Configuracao rapida de fluxo.
5. Configuracoes essenciais.
6. Agentes e fluxos.
7. Cotas.

## Tela web: Onboarding e configuracao inicial

| Campo | Definicao |
| --- | --- |
| Tipo | Web, com equivalente mobile guiado. |
| Rotas | `/onboarding/claim/[activationId]`, `/onboarding/studio`, `/onboarding/importacao`, `/onboarding/agentes`, `/onboarding/revisao`. |
| Objetivo | Reivindicar workspace, preencher dados minimos, importar, convidar equipe, configurar agentes iniciais e abrir CRM. |
| Usuario principal | Dono/admin. |
| Blocos | progresso do setup, dados do studio, canais, importacao, equipe, agentes do plano, pendencias, revisao final. |
| Campos exibidos | plano Taliya, status da assinatura, nome do studio, cidade/estado, horarios, WhatsApp, alunos importados, turmas importadas, agentes incluidos, pendencias. |
| Campos editaveis | dados do studio, horarios, canal, convites, mapeamento de importacao, modo inicial de agentes. |
| Campos sensiveis | billing/entitlement, WhatsApp/canal, permissoes, dados importados sensiveis. |
| Acoes | reivindicar conta, salvar etapa, importar, resolver duplicidade, convidar equipe, configurar agente, testar exemplo, abrir CRM. |
| Estados | token invalido, setup incompleto, importando, erro de importacao, duplicidade, sem canal, plano Base, pronto para operar. |
| Permissoes | dono/admin; suporte so com grant. |
| IA/agentes | pode explicar/sugerir configuracao; nao executa automacao antes do preflight. |
| Cotas | mostrar plano e cota contratada; Base = 0 automacao ativa. |
| Auditoria | claim, alteracao de dados, convites, importacao, configuracao inicial de agente. |
| Fallback | se importacao falhar, permitir cadastro manual e fila de qualidade de dados. |
| Aceite | usuario chega ao CRM com pendencias claras e sem automacao perigosa ativa. |

## Tela web: Configuracoes

| Campo | Definicao |
| --- | --- |
| Tipo | Web completo; mobile essencial. |
| Rotas | `/app/configuracoes/studio`, `/app/configuracoes/equipe`, `/app/configuracoes/permissoes`, `/app/configuracoes/canais`, `/app/configuracoes/templates`, `/app/configuracoes/base-conhecimento`, `/app/configuracoes/agenda`, `/app/configuracoes/financeiro`, `/app/configuracoes/vendas`, `/app/configuracoes/retencao`, `/app/configuracoes/politicas`, `/app/configuracoes/privacidade`, `/app/configuracoes/recursos`, `/app/configuracoes/campos`, `/app/configuracoes/notificacoes`. |
| Objetivo | Centralizar regras estruturais do studio. |
| Usuario principal | Dono/admin. |
| Blocos | studio, equipe, permissoes, canais, templates, agenda, financeiro, vendas, retencao, privacidade, recursos, campos, notificacoes. |
| Acoes | editar, salvar, testar canal, publicar politica, simular impacto, pedir suporte, auditar. |
| Estados | salvo, rascunho, mudanca sensivel, exige aprovacao, sem permissao, teste de canal falhou. |
| IA/agentes | sugerem configuracao e validam risco; mudanca sensivel nao e autonoma. |
| Cotas | configuracoes de economia e limites por fluxo apontam para Uso/cotas. |
| Auditoria | toda mudanca de permissao, canal, politica, template, privacidade, recurso e campo. |
| Fallback | se configuracao incompleta, criar problema de dados/configuracao e bloquear fluxo afetado. |

## Tela web: Agentes e fluxos

| Campo | Definicao |
| --- | --- |
| Tipo | Web completo; app faz essencial. |
| Rotas | `/app/agentes`, `/app/agentes/[agentId]`, `/app/agentes/[agentId]/fluxos`, `/app/fluxos`, `/app/fluxos/[flowId]`, `/app/fluxos/[flowId]/simular`. |
| Objetivo | Configurar agentes incluidos no plano, modos, fluxos, limites, templates e simulacao. |
| Blocos | agentes do plano, agentes bloqueados, fluxos, modo manual/copiloto/autonomo, requisitos, limites, templates, simulacao, execucoes recentes. |
| Acoes | ativar, pausar, mudar modo, editar limite, simular, publicar, rollback, abrir execucao. |
| Estados | bloqueado por plano, sem dados, sem canal, sem template, cota insuficiente, rascunho, ativo, pausado, falhou. |
| Permissoes | dono/admin; pausar emergencia pode ser contextual. |
| IA/agentes | simulacao e explicacao; execucao real so depois de publicado. |
| Cotas | estimativa por fluxo, limite mensal, origem de consumo, economia. |
| Auditoria | modo, ativacao, pausa, publicacao, rollback, autonomia. |
| Fallback | se autonomia bloqueada, usar copiloto/manual. |

## Tela web: Uso, cotas e economia

| Campo | Definicao |
| --- | --- |
| Tipo | Web completo; mobile consulta/acao simples. |
| Rotas | `/app/uso`, `/app/uso/cotas`, `/app/uso/custos`, `/app/uso/extrato`, `/app/uso/alertas`, `/app/uso/pacotes`, `/app/uso/regras-economia`, `/app/uso/limites-fluxo`, `/app/uso/limites-fluxo/[flowId]`. |
| Objetivo | Mostrar consumo, limites, previsao, downgrade, pacotes e economia. |
| Blocos | resumo, uso por origem, uso por agente, extrato, alertas, pacotes, limites por fluxo. |
| Acoes | ajustar economia, pausar baixa prioridade, comprar/solicitar pacote, abrir fluxo, ver extrato. |
| Estados | normal, 70%, 90%, 100%, pacote ativo, bloqueado por billing, sem permissao. |
| Auditoria | compra pacote, mudanca de economia, limite por fluxo. |
| Fallback | em 100%, criar tarefa manual para fluxo critico. |

## Tela web: Qualidade de dados

| Campo | Definicao |
| --- | --- |
| Tipo | Web principal; mobile aprovacao/consulta. |
| Rotas | `/app/dados/qualidade`, `/app/dados/duplicidades`. |
| Objetivo | Resolver dados que bloqueiam operacao, importacao e agentes. |
| Blocos | duplicidades, ausentes, conflitos, dados sensiveis, bloqueios por fluxo, origem do problema. |
| Acoes | mesclar, manter separado, corrigir, arquivar, reativar, pedir revisao, desbloquear fluxo. |
| Estados | duplicado, incompleto, conflito, bloqueando automacao, aguardando revisao, resolvido. |
| Permissoes | varia por objeto; historico/financeiro exigem papel especifico. |
| IA/agentes | sugerem match/correcao; humano confirma em baixa confianca. |
| Auditoria | mescla, correcao, arquivamento, reativacao. |
| Fallback | se nao resolver agora, criar tarefa e manter fluxo bloqueado. |

## Tela mobile: Setup inicial

| Campo | Definicao |
| --- | --- |
| Tipo | Mobile acao completa guiada. |
| Objetivo | Ativar conta e chegar ao CRM usando passos curtos. |
| Conteudo | progresso, studio, horarios, canal, equipe, checklist, pendencias. |
| Acoes | salvar etapa, pular permitido, convidar equipe, abrir CRM, pedir ajuda. |
| Estados | incompleto, bloqueado por dado, pronto para operar, precisa web para etapa avancada. |

## Tela mobile: Importacao assistida

| Campo | Definicao |
| --- | --- |
| Tipo | Mobile acao parcial. |
| Conteudo | escolher importacao simples, status, erros, duplicidades, progresso. |
| Acoes | iniciar simples, revisar duplicidade segura, continuar depois, pedir suporte. |
| Fora do mobile | importacao grande, mapeamento complexo e exportacao. |

## Tela mobile: Configuracao inicial de agentes

| Campo | Definicao |
| --- | --- |
| Tipo | Mobile acao completa guiada para essencial. |
| Conteudo | agentes do plano, objetivo, modo inicial, canal, limite, tom, janela, bloqueios. |
| Acoes | escolher agente, ativar/pausar, definir modo, testar exemplo, salvar. |
| Estados | bloqueado por plano, sem dados, sem canal, pronto para testar. |

## Tela mobile: Configuracao rapida de fluxo

| Campo | Definicao |
| --- | --- |
| Tipo | Mobile acao controlada. |
| Conteudo | fluxo, modo, limite, aprovacao, template, estimativa de cota. |
| Acoes | editar modo, editar limite simples, testar exemplo, salvar rascunho, publicar simples quando seguro. |
| Fora do mobile | politica complexa, versionamento profundo, rollback e simulacao longa. |

## Tela mobile: Configuracoes essenciais

| Campo | Definicao |
| --- | --- |
| Tipo | Mobile acao parcial. |
| Conteudo | studio, equipe basica, horarios, canal, templates simples, notificacoes, privacidade basica. |
| Acoes | editar essencial, testar canal, salvar, pedir revisao. |
| Estados | salvo, incompleto, sem permissao, exige web. |

## Tela mobile: Agentes e fluxos

| Campo | Definicao |
| --- | --- |
| Tipo | Mobile configuracao essencial + emergencia. |
| Conteudo | agentes ativos, fluxos principais, modo, limites, ultima execucao, alertas. |
| Acoes | ativar/pausar, mudar modo simples, editar limite simples, testar exemplo, abrir web avancado. |
| Estados | ativo, pausado, bloqueado por plano, bloqueado por dado, cota alta. |

## Tela mobile: Cotas

| Campo | Definicao |
| --- | --- |
| Tipo | Mobile consulta + acao simples. |
| Conteudo | consumo, limite, previsao, origem, alertas, pacote, economia. |
| Acoes | ver motivo, solicitar/comprar pacote, pausar baixa prioridade, abrir fluxo afetado. |
| Estados | normal, 70%, 90%, 100%, pacote ativo. |

## Cobertura de contratos da Rodada 0

| Contrato | Aplicacao nesta rodada |
| --- | --- |
| Dados | Usa tenant, usuario, equipe, contato, aluno, importacao, agente, fluxo, cota. |
| Ciclo de vida | Claim, importacao, fluxo rascunho/ativo, problema de dados, grant de suporte. |
| Fonte da verdade | Billing para plano; CRM para dados; importacao como entrada revisavel. |
| Permissoes | Dono/admin dominam; suporte so com grant. |
| Cotas | Plano Base e limites aparecem antes de ativar agentes. |
| Auditoria | Claim, importacao, permissoes, agentes, politicas e suporte. |
| 0 agentes | CRM abre e funciona sem automacao. |

## Decisoes abertas encontradas

| Tema | Encaminhamento |
| --- | --- |
| Multi-unidade | Premissa provisoria: operar uma unidade no MVP e manter objeto preparado; decisao final continua aberta. |
| Importacao grande no app | Web-first; app faz simples/parcial. |
| Configuracao avancada no app | Manter fora; app faz essencial e emergencia. |
| Provedor financeiro | Nao bloquear setup; tratar como configuracao futura/pendente. |

## Criterio de aceite da rodada

Rodada 1 esta pronta para revisao quando:

- setup abre CRM sem agente ativo;
- plano Base nao bloqueia CRM;
- agente so ativa depois de preflight;
- importacao cria qualidade de dados quando insegura;
- app permite setup essencial;
- web concentra configuracao profunda;
- cotas aparecem antes de automacao;
- suporte Taliya so com grant.
