# Matriz de permissoes - PT-BR

> Status: Rodada 0 v0.1. Este documento define o contrato inicial de papeis, permissoes contextuais e acoes sensiveis.

## Papeis padrao

| Papel | Descricao |
| --- | --- |
| Dono | Responsavel maximo pela conta, billing, permissoes e decisoes sensiveis. |
| Admin | Opera configuracoes, equipe e grande parte do CRM, exceto billing restrito quando removido. |
| Recepcao/operacao | Opera inbox, agenda, tarefas, alunos, interessados e rotina diaria. |
| Financeiro | Opera pagamentos, cobrancas, contratos, documentos financeiros e excecoes permitidas. |
| Professor | Opera aulas, chamada, notas e contexto permitido dos alunos. |
| Suporte Taliya | Acesso temporario e escopado mediante autorizacao. |
| Agente/runtime | Ator de sistema limitado por entitlement, modo, politica, cota e permissao. |

## Matriz resumida

| Area/acao | Dono | Admin | Operacao | Financeiro | Professor | Suporte Taliya | Agente |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Ver Hoje | Sim | Sim | Sim | Sim | Parcial | Com grant | Sim, como origem |
| Configurar studio | Sim | Sim | Nao | Nao | Nao | Com grant | Sugere |
| Convidar equipe | Sim | Sim | Nao | Nao | Nao | Nao | Nao |
| Alterar permissoes | Sim | Sim, se permitido | Nao | Nao | Nao | Nao | Nao |
| Ver inbox | Sim | Sim | Sim | Parcial | Nao por padrao | Com grant | Sim, se fluxo ativo |
| Responder conversa | Sim | Sim | Sim | Parcial | Nao por padrao | Nao | Conforme modo |
| Assumir do agente | Sim | Sim | Sim | Sim, em financeiro | Nao | Nao | Nao |
| Ver aluno | Sim | Sim | Sim | Parcial financeiro | Apenas alunos/aulas permitidos | Com grant | Conforme fluxo |
| Editar aluno | Sim | Sim | Sim limitado | Parcial financeiro | Nao | Nao | Sugere |
| Ver historico sensivel | Sim | Sim se permitido | Nao por padrao | Nao por padrao | Apenas permitido | Com grant explicito | Apenas contexto permitido |
| Registrar nota de professor | Sim | Sim | Sim se permitido | Nao | Sim | Nao | Sugere lembrete |
| Operar agenda | Sim | Sim | Sim | Nao | Parcial | Com grant | Conforme fluxo |
| Fazer chamada | Sim | Sim | Sim | Nao | Sim se autorizado | Nao | Sugere/automatiza se permitido |
| Operar vendas | Sim | Sim | Sim | Nao | Nao | Com grant | Conforme fluxo |
| Ver financeiro completo | Sim | Sim se permitido | Nao por padrao | Sim | Nao | Com grant explicito | Apenas dados necessarios |
| Confirmar pagamento | Sim | Sim se permitido | Nao | Sim | Nao | Nao | Sugere/abre caso |
| Dar desconto/cortesia | Sim | Sim se permitido | Nao | Pode solicitar/aprovar se permitido | Nao | Nao | Nunca autonomo |
| Reembolso/disputa | Sim | Sim se permitido | Nao | Sim com aprovacao | Nao | Nao | Nunca autonomo |
| Aprovar comunicados | Sim | Sim | Parcial se permitido | Nao | Nao | Nao | Prepara |
| Configurar agentes | Sim | Sim | Nao | Nao | Nao | Com grant | Nao |
| Pausar automacao | Sim | Sim | Sim em emergencia/contexto | Sim em financeiro | Nao | Com grant tecnico | Auto-pausa por regra |
| Reprocessar execucao | Sim | Sim | Parcial seguro | Parcial financeiro | Nao | Com grant | Nao sem idempotencia |
| Ver uso/cotas | Sim | Sim | Consulta limitada | Consulta limitada | Nao | Com grant | Registra consumo |
| Comprar pacote/add-on | Sim | Admin se permitido | Nao | Nao por padrao | Nao | Nao | Nao |
| Exportar dados | Sim | Admin se permitido | Nao | Financeiro permitido | Nao | Nao | Nao |
| Solicitacao LGPD | Sim | Sim se permitido | Pode abrir | Nao por padrao | Nao | Com grant | Nunca executa sozinho |
| Aprovar suporte Taliya | Sim | Admin se permitido | Nao | Nao | Nao | Solicita | Nao |

## Permissoes contextuais

| Contexto | Regra |
| --- | --- |
| Professor | So ve alunos, aulas e historico permitido de suas turmas/aulas. |
| Financeiro | Ve dados financeiros, mas nao historico de saude/restricoes sem permissao explicita. |
| Recepcao | Pode operar agenda/inbox, mas nao deve ver detalhes financeiros sensiveis por padrao. |
| Responsavel | Nao e usuario interno; suas permissoes controlam comunicacao e acesso externo futuro. |
| Suporte Taliya | Nunca tem acesso permanente; precisa grant com escopo, prazo e motivo. |
| Agente | Nao "tem permissao propria"; herda limites de fluxo, politica, dados e entitlement. |

## Acoes que exigem aprovacao ou confirmacao forte

| Acao | Exigencia minima |
| --- | --- |
| Envio em massa | Aprovacao humana, publico, template, consentimento, custo e auditoria. |
| Desconto/cortesia | Permissao financeira, motivo, impacto e auditoria. |
| Reembolso/disputa | Permissao alta, evidencias e auditoria. |
| Alteracao de plano do aluno | Simulacao de impacto, vigencia e auditoria. |
| Cancelamento/reativacao | Motivo, impacto, comunicacao e auditoria. |
| Exclusao/anonimizacao LGPD | Validacao de identidade, aprovacao e auditoria. |
| Historico sensivel | Permissao contextual, visibilidade e auditoria. |
| Mudanca de politica | Versao, simulacao, aprovacao e auditoria. |
| Ativar autonomia de fluxo | Entitlement, simulacao, limites, cota e auditoria. |
| Acesso de suporte | Dono/admin autorizado, escopo, prazo e auditoria. |

## Regra para UI

Telas nao devem apenas esconder acoes. Quando uma acao for bloqueada e o usuario poderia pedir ajuda, mostrar:

- motivo do bloqueio;
- permissao necessaria;
- quem pode aprovar;
- botao para pedir revisao quando fizer sentido.
