# Rodada 7 - Agentes, execucoes, cotas, relatorios e governanca - PT-BR

> Status: v0.1. Esta rodada define a base funcional e a primeira especificacao profunda das telas de Agentes, Fluxos, Execucoes, Incidentes, Cotas, Relatorios, Politicas, Integracoes, Auditoria, Billing e Suporte interno Taliya.

## Objetivo operacional

Fechar confiabilidade do sistema, governanca dos agentes, cotas, relatorios e operacao interna da Taliya sem fazer os agentes parecerem magicos ou indispensaveis para o CRM funcionar.

## Limite desta v0.1

Esta versao orienta produto, rotas, objetos, estados e acoes principais. Ainda falta, em passada posterior:

- fechar thresholds de qualidade para autonomia;
- definir severidade oficial de incidente;
- fechar relatorios profundos do MVP;
- definir precos/pacotes finais de cota;
- fechar escopo exato do admin interno Taliya;
- definir integracoes reais do MVP;
- transformar esta rodada em prompts finais de UI.

## Usuarios envolvidos

| Usuario | Papel na rodada |
| --- | --- |
| Dono/gestor | Decide planos, agentes, cotas, autonomia, billing, grants e relatorios. |
| Admin | Configura fluxos, politicas, integracoes, limites e operacao. |
| Recepcao/operacao | Ve alertas, aprovacoes, incidentes e fallback manual. |
| Financeiro | Ve cotas/billing permitido e integracoes financeiras quando autorizado. |
| Suporte Taliya | Diagnostica tenants, grants, incidentes e integracoes dentro de escopo autorizado. |
| Agente/runtime | Executa fluxos com modo, politica, cota, permissao, ferramenta, log e auditoria. |

## Objetos de negocio

- Agente;
- Fluxo de agente;
- Configuracao de fluxo;
- Execucao de fluxo;
- Incidente de automacao;
- Politica operacional;
- Versao de politica;
- Lancamento de cota;
- Regra de economia;
- Plano Taliya;
- Add-on/pacote;
- Fatura Taliya;
- Integracao;
- Log de integracao;
- Acesso de suporte;
- Evento de auditoria;
- Relatorio;
- Job de exportacao;
- Job de importacao;
- Caso operacional;
- Tarefa;
- Aprovacao.

## Jornadas cobertas

| Jornada | Resultado esperado |
| --- | --- |
| Configurar agentes incluidos no plano | Gestor ve entitlement, agentes disponiveis, bloqueios, setup e limites. |
| Configurar um agente | Agente tem objetivo, canais, modo, tom, limites, filas, aprovacoes e fallback. |
| Configurar fluxo do agente | Fluxo tem gatilho, regra, politica, template, cota estimada, simulacao e rollback. |
| Simular fluxo antes de ativar | Usuario ve entradas, saidas, custo, risco, bloqueios e evento de auditoria previsto. |
| Ativar/pausar fluxo | Mudanca respeita permissao, plano, cota, preflight e auditoria. |
| Revisar execucao de fluxo | Usuario ve input/output seguro, ferramentas, custo, resultado, erro e proxima acao. |
| Aprovar/rejeitar acao sugerida | Decisor ve antes/depois, risco, custo, politica e origem. |
| Revisar desempenho dos agentes | Gestor ve acerto, erro, economia, handoff, custo, incidentes e comparacao manual. |
| Investigar incidente de automacao | Incidente tem severidade, impacto, causa, correcao, prevencao e comunicacao. |
| Alterar regra operacional | Politica versionada mostra simulacao, vigencia, aprovacao, rollback e impacto. |
| Resolver fluxo bloqueado por dado | Bloqueio aponta dado faltante, dono, objeto, tarefa/caso e retomada segura. |
| Revisar cotas e uso | Usuario ve consumo, origem, previsao, limite, pacote e economia. |
| Configurar economia de uso | Baixa prioridade vira tarefa/aprovacao/manual em 90% e bloqueia em 100%. |
| Comprar/solicitar pacote | Dono/admin ve custo, pacote, retomada e billing. |
| Gerenciar assinatura Taliya | Plano, faturas, add-ons, agentes inclusos e falhas ficam claros. |
| Revisar integracoes/falhas | WhatsApp, pagamentos, importacao e webhooks mostram status, log e recuperacao. |
| Revisar auditoria | Usuario autorizado filtra eventos e abre objeto origem. |
| Abrir relatorios/exportacoes | Gestor ve financeiro, vendas, ocupacao, risco, agentes e exportacoes. |
| Aprovar acesso de suporte | Grant tem escopo, prazo, motivo, dados permitidos e revogacao. |

## Regras de negocio

1. CRM completo precisa funcionar sem agentes ativos.
2. Agente nao tem permissao propria; executa dentro de plano, politica, modo, cota, permissao e dados permitidos.
3. Todo fluxo precisa ter modo: manual, copiloto ou autonomo.
4. Todo fluxo autonomo precisa de preflight: dados, canal, template, consentimento, cota, politica, permissao, fallback e auditoria.
5. Toda execucao registra custo, ferramentas, resultado, erro, politica e output seguro.
6. Reprocessamento so pode ocorrer quando houver idempotencia e impacto conhecido.
7. Incidente de automacao precisa severidade, dono, impacto, correcao e prevencao.
8. Cota 70 alerta; 90 aplica economia; 100 bloqueia automacao paga e preserva caminho manual.
9. Relatorio nao pode virar fonte de verdade; sempre aponta objetos origem.
10. Politica operacional sensivel e versionada, simulada, aprovada e auditada.
11. Integracao falha vira estado, tarefa, caso ou incidente, nao erro silencioso.
12. Suporte Taliya exige grant, escopo, prazo, motivo e auditoria.
13. Billing Taliya controla entitlements; CRM apenas reflete plano/cota/fatura.
14. Qualidade de agente deve comparar automacao com resolucao manual quando possivel.

## Modos de execucao

| Modo | Como funciona nesta rodada |
| --- | --- |
| Manual | Fluxo vira tarefa, aprovacao, caso ou acao humana, sem execucao autonoma. |
| Copiloto | Agente prepara sugestao/rascunho/resumo e usuario decide. |
| Autonomo | Agente executa dentro de limites, com logs, cotas, politica, auditoria, rollback/fallback quando aplicavel. |

## Telas web desta rodada

1. Agentes e fluxos.
2. Execucoes e incidentes de agentes.
3. Uso, cotas e economia.
4. Relatorios e exportacoes.
5. Politicas operacionais.
6. Integracoes.
7. Auditoria.
8. Assinatura e billing.
9. Suporte interno Taliya.

## Telas mobile desta rodada

1. Agentes/alertas.
2. Agentes e fluxos.
3. Execucao de agente.
4. Cotas.
5. Relatorios resumidos.
6. Auditoria resumida.
7. Integracoes/status.
8. Assinatura/billing.
9. Suporte/autorizacao de acesso.

## Tela web: Agentes e fluxos

| Campo | Definicao |
| --- | --- |
| Tipo | Web configuracao completa; mobile configuracao essencial/emergencia. |
| Rotas | `/app/agentes`, `/app/agentes/[agentId]`, `/app/agentes/[agentId]/fluxos`, `/app/fluxos`, `/app/fluxos/[flowId]`, `/app/fluxos/[flowId]/simular`. |
| Objetivo | Configurar agentes e fluxos com modo, limites, regras, templates, simulacao e fallback. |
| Blocos | agentes, fluxos, modo, gatilhos, politicas, templates, limites, filas, simulacao, preflight, execucoes recentes. |
| Acoes | configurar, simular, ativar, pausar, mudar modo, editar limite, publicar, rollback, abrir execucoes. |
| Estados | bloqueado por plano, sem dados, sem canal, rascunho, pronto para teste, ativo, pausado, incidente, cota alta. |
| Permissoes | dono/admin; operacao pode pausar emergencia quando permitido. |
| Cotas | estimativa por fluxo, limite mensal, limite por tentativa e consumo recente. |
| Auditoria | ativacao, pausa, modo, regra, politica, publicacao e rollback. |
| 0 agentes | tela explica agentes disponiveis/upgrade, mas CRM segue manual. |

## Tela web: Execucoes e incidentes de agentes

| Campo | Definicao |
| --- | --- |
| Tipo | Web observabilidade; mobile alerta/acompanhamento. |
| Rotas | `/app/fluxos/execucoes/[runId]`, `/app/operacao/incidentes`, `/app/operacao/incidentes/[incidentId]`. |
| Objetivo | Investigar execucoes, falhas, incidentes, custo, ferramentas e recuperacao. |
| Blocos | execucao, timeline, input seguro, output seguro, ferramentas, custo, politica, erro, incidente, correcao, auditoria. |
| Acoes | explicar falha, abrir incidente, corrigir dado, reprocessar seguro, pausar fluxo, criar tarefa, resolver incidente. |
| Estados | sucesso, aguardando aprovacao, bloqueado, falhou, incidente, reprocessado, resolvido. |
| Permissoes | execucao sensivel respeita objeto afetado; suporte so com grant. |
| Cotas | mostra lancamentos, origem e impacto de reprocessamento. |
| Auditoria | execucao, reprocessamento, pausa, incidente, correcao e resolucao. |
| Fallback | se reprocessar nao for seguro, criar caso/tarefa manual. |

## Tela web: Uso, cotas e economia

| Campo | Definicao |
| --- | --- |
| Tipo | Web governanca de custo; mobile consulta + acao simples. |
| Rotas | `/app/uso`, `/app/uso/cotas`, `/app/uso/custos`, `/app/uso/extrato`, `/app/uso/alertas`, `/app/uso/pacotes`, `/app/uso/regras-economia`, `/app/uso/limites-fluxo`, `/app/uso/limites-fluxo/[flowId]`. |
| Objetivo | Mostrar consumo, previsao, origem, limites, pacote, economia e comportamento por cota. |
| Blocos | consumo, restante, previsao, origem por fluxo, alertas 70/90/100, pacote, regras de economia, limites por fluxo, extrato. |
| Acoes | ver consumo, ajustar economia, pausar baixa prioridade, comprar/solicitar pacote, abrir fluxo afetado. |
| Estados | normal, 70%, 90%, 100%, pacote ativo, automacao convertida em tarefa, bloqueado. |
| Permissoes | dono/admin compram pacote; operacao ve alerta e abre origem. |
| Auditoria | limite atingido, downgrade, pacote, compra/solicitacao, regra de economia. |
| 0 agentes | uso de agentes fica 0; CRM manual segue. |

## Tela web: Relatorios e exportacoes

| Campo | Definicao |
| --- | --- |
| Tipo | Web-first; mobile resumo acionavel. |
| Rotas | `/app/relatorios`, `/app/relatorios/semana`, `/app/relatorios/financeiro`, `/app/relatorios/vendas`, `/app/relatorios/risco`, `/app/relatorios/agentes`, `/app/relatorios/ocupacao`, `/app/dinheiro-na-mesa`, `/app/exportacoes`, `/app/exportacoes/[jobId]`. Gargalos e capacidade ficam como blocos/indicadores que abrem origens filtradas; sem rota dedicada no MVP. |
| Objetivo | Mostrar indicadores e exportacoes com origem rastreavel e acao relacionada. |
| Blocos | financeiro, vendas, ocupacao, capacidade, origens, risco, agentes, gargalos, exportacoes, filtros. |
| Acoes | filtrar, abrir origem, exportar quando permitido, agendar relatorio, criar caso relacionado. |
| Estados | sem dados, atualizado, alerta, exportando, pronto, sem permissao, falhou. |
| Permissoes | dados financeiros/sensiveis respeitam papel; exportacao exige permissao. |
| IA/agentes | resumir tendencia e explicar gargalo; relatorio nao vira fonte da verdade. |
| Auditoria | exportacao, acesso sensivel e compartilhamento. |

## Tela web: Politicas operacionais

| Campo | Definicao |
| --- | --- |
| Tipo | Web configuracao sensivel. |
| Rotas | `/app/politicas`, `/app/politicas/[policyId]`, `/app/politicas/[policyId]/simular`. |
| Objetivo | Versionar regras de agenda, reposicao, cobranca, cancelamento, comunicados, historico e autonomia. |
| Blocos | politicas, versoes, editor em linguagem simples, regra estruturada, simulacao, aprovacao, vigencia, rollback. |
| Acoes | criar versao, simular impacto, aprovar, publicar, reverter, arquivar. |
| Estados | rascunho, simulada, aguardando aprovacao, ativa, substituida, revertida, arquivada. |
| Auditoria | toda mudanca de politica e sensivel. |

## Tela web: Integracoes

| Campo | Definicao |
| --- | --- |
| Tipo | Web administracao tecnica; mobile status/alerta. |
| Rotas | `configuracao especifica da integracao`, `configuracao especifica da integracao`, `/app/importacao`, `/app/importacao/[jobId]`. |
| Objetivo | Conectar, testar e diagnosticar WhatsApp, pagamentos, importacao, webhooks e outros provedores. |
| Blocos | conexoes, status, credenciais seguras, logs, webhooks, importacoes, falhas, reprocessamento, incidentes. |
| Acoes | conectar, desconectar, testar, ver log, reprocessar quando seguro, abrir incidente, corrigir dado. |
| Estados | conectado, desconectado, falhou, provedor indisponivel, aguardando webhook, erro recorrente, reprocessando. |
| Permissoes | admin/dono; suporte com grant tecnico. |
| Auditoria | conectar, desconectar, credencial atualizada, webhook falhou e reprocessamento. |

## Tela web: Auditoria

| Campo | Definicao |
| --- | --- |
| Tipo | Web consulta sensivel; mobile resumo. |
| Rotas | `/app/auditoria`, `/app/auditoria/[eventId]`. |
| Objetivo | Ver quem fez o que, em qual objeto, quando, com antes/depois seguro, motivo e politica. |
| Blocos | busca, filtros, evento, objeto, ator, antes/depois, risco, cota, politica, exportacao permitida. |
| Acoes | filtrar, abrir objeto, abrir execucao, exportar quando permitido, reportar problema. |
| Estados | sem permissao, evento sensivel, alteracao critica, sem resultado. |
| Auditoria | a propria visualizacao/exportacao sensivel pode auditar. |

## Tela web: Assinatura e billing

| Campo | Definicao |
| --- | --- |
| Tipo | Web billing Taliya; mobile consulta + acao simples. |
| Rotas | `/app/billing`, `/app/billing/add-ons`, `/app/billing/invoices`. |
| Objetivo | Mostrar plano Taliya, agentes inclusos, faturas, add-ons, pacote de cota e falhas. |
| Blocos | plano, entitlements, agentes, cotas, faturas, add-ons, portal, falhas, historico. |
| Acoes | ver fatura, abrir portal, comprar/solicitar pacote, atualizar plano, abrir suporte. |
| Estados | ativo, vencido, falha, pacote ativo, upgrade pendente, plano bloqueado. |
| Permissoes | dono/admin; financeiro pode consultar se permitido. |
| Auditoria | upgrade, pacote, falha, alteracao de entitlement. |

## Tela web: Suporte interno Taliya

| Campo | Definicao |
| --- | --- |
| Tipo | Admin interno com acesso escopado. |
| Rotas | `/internal/tenants`, `/internal/tenants/[tenantId]`, `/internal/incidentes`, `/internal/suporte/grants`, `/internal/billing`, `/internal/agent-ops`. |
| Objetivo | Permitir diagnostico e suporte Taliya com autorizacao, escopo, prazo, incidente e auditoria. |
| Blocos | tenants, plano, status, grants, incidentes, integracoes, execucoes, billing, bloqueios, auditoria. |
| Acoes | solicitar grant, usar grant, diagnosticar, abrir incidente, bloquear/desbloquear recurso conforme politica, revogar acesso. |
| Estados | sem grant, grant ativo, expirado, tenant bloqueado, incidente aberto, suporte encerrado. |
| Permissoes | apenas time Taliya autorizado; dados do tenant conforme escopo. |
| Auditoria | toda acao interna auditada. |

## Telas mobile

### Agentes/alertas

| Campo | Definicao |
| --- | --- |
| Profundidade | Consulta + emergencia. |
| Conteudo | fluxos pausados, bloqueados, incidentes, execucoes falhas, custo alto. |
| Acoes | pausar emergencia, abrir incidente, ver explicacao, reprocessar se seguro. |
| Estados | falhou, bloqueado, incidente, cota alta. |

### Agentes e fluxos

| Campo | Definicao |
| --- | --- |
| Profundidade | Configuracao essencial. |
| Conteudo | agentes ativos, fluxos principais, modo, limites basicos, templates, ultima execucao. |
| Acoes | ativar, pausar, mudar modo, editar limite simples, testar exemplo, abrir web avancado. |
| Estados | bloqueado por plano, pausado, ativo, sem dados. |

### Execucao de agente

| Campo | Definicao |
| --- | --- |
| Profundidade | Alerta + acompanhamento. |
| Conteudo | resultado, custo, ferramenta, erro, objeto afetado, proxima acao. |
| Acoes | abrir origem, criar tarefa, pausar fluxo, reprocessar se seguro. |
| Estados | sucesso, falhou, incidente, aguardando aprovacao. |

### Cotas

| Campo | Definicao |
| --- | --- |
| Profundidade | Consulta + acao simples. |
| Conteudo | consumo, limite, previsao, origem, alertas, pacote, modo economia. |
| Acoes | ver motivo, solicitar/comprar pacote, pausar baixa prioridade, abrir fluxo afetado. |
| Estados | 70%, 90%, 100%, pacote ativo. |

### Relatorios resumidos

| Campo | Definicao |
| --- | --- |
| Profundidade | Consulta acionavel. |
| Conteudo | dinheiro, vendas, ocupacao, risco, agentes, gargalos. |
| Acoes | abrir origem, compartilhar resumo se permitido, exportar depois no web. |
| Estados | sem dados, atualizado, alerta. |

### Auditoria resumida

| Campo | Definicao |
| --- | --- |
| Profundidade | Consulta sensivel. |
| Conteudo | evento sensivel, ator, objeto, horario, antes/depois resumido. |
| Acoes | abrir objeto, reportar problema. |
| Estados | sem permissao, evento critico. |

### Integracoes/status

| Campo | Definicao |
| --- | --- |
| Profundidade | Consulta + alerta. |
| Conteudo | WhatsApp, pagamentos, importacao, ultima sincronizacao, falhas. |
| Acoes | abrir incidente, reprocessar quando seguro, avisar responsavel. |
| Estados | conectado, falhou, provedor indisponivel. |

### Assinatura/billing

| Campo | Definicao |
| --- | --- |
| Profundidade | Consulta + acao simples. |
| Conteudo | plano, status, fatura, pacote de cota, falha de pagamento. |
| Acoes | ver fatura, abrir portal, solicitar pacote. |
| Estados | ativo, vencido, falha, pacote ativo. |

### Suporte/autorizacao de acesso

| Campo | Definicao |
| --- | --- |
| Profundidade | Aprovacao sensivel. |
| Conteudo | solicitacao de suporte, escopo, prazo, motivo, dados permitidos. |
| Acoes | aprovar grant, negar, revogar, expirar acesso. |
| Estados | pendente, grant ativo, expirado, negado. |

## Cobertura de contratos da Rodada 0

| Contrato | Aplicacao nesta rodada |
| --- | --- |
| Dados | Usa agente, fluxo, execucao, incidente, politica, cota, integracao, auditoria, billing e suporte. |
| Ciclo de vida | Fluxo, execucao, incidente, politica, integracao, cota, fatura, grant e exportacao. |
| Fonte da verdade | Billing Taliya vence plano/cota; runtime registra execucao; CRM exibe e audita. |
| Permissoes | Dono/admin configuram; suporte so com grant; agente herda limites. |
| Botoes | Configurar, simular, ativar, pausar, aprovar, reprocessar, comprar pacote, exportar, conceder grant. |
| Estados | Ativo, pausado, bloqueado, falhou, incidente, cota 70/90/100, grant ativo, sem permissao. |
| Cotas | Cada acao paga mostra origem, custo, limite, downgrade, bloqueio e fallback manual. |
| Auditoria | Agentes, politicas, cotas, integracoes, billing, exportacao e suporte. |
| 0 agentes | CRM continua operando; agentes ficam como configuracao/upgrade/preview sem automacao ativa. |

## Decisoes abertas encontradas

| Tema | Encaminhamento |
| --- | --- |
| Qualidade minima para autonomia | Definir thresholds de acerto, erro, handoff, reclamacao e custo para liberar modo autonomo. |
| Reprocessamento seguro | Definir idempotencia por tipo de ferramenta e quando reexecutar e proibido. |
| Severidade de incidente | Definir niveis, SLA, comunicacao, bloqueio automatico e pos-mortem. |
| Relatorios do MVP | Escolher quais paineis profundos entram no primeiro design. |
| Suporte interno Taliya | Definir telas internas exatas, papeis e limites de acao. |

## Criterio de aceite da rodada

Rodada 7 esta pronta para revisao quando:

- agentes e fluxos mostram modo, limite, politica, cota, simulacao e fallback;
- execucao mostra resultado, custo, ferramenta, erro, objeto, politica e auditoria;
- incidente tem severidade, dono, impacto, correcao e prevencao;
- cota 70/90/100 tem comportamento visivel e caminho manual;
- relatorios apontam origem e respeitam permissao;
- politicas sao versionadas, simuladas, aprovadas e auditadas;
- integracoes falham de modo recuperavel;
- billing mostra plano, agentes, cotas, faturas e pacotes;
- suporte Taliya usa grant, escopo, prazo e auditoria;
- plano Base continua CRM completo com 0 agentes ativos.
