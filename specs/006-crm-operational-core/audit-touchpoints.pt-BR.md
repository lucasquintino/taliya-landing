# Pontos de auditoria - PT-BR

> Status: Rodada 0 v0.1. Este documento define o que precisa deixar rastro auditavel.

## Regra central

Toda acao sensivel deve registrar quem fez, quando fez, em qual objeto, o que mudou, por que mudou, qual politica/versao foi usada e qual foi o impacto.

## Eventos obrigatorios

| Categoria | Eventos |
| --- | --- |
| Acesso | login, convite, mudanca de papel, permissao, grant de suporte, revogacao. |
| Aluno/contato | criacao, mescla, arquivamento, reativacao, opt-out, responsavel validado. |
| Historico sensivel | nota, restricao, documento, correcao, compartilhamento, visibilidade. |
| Agenda | mudanca de turma, capacidade, chamada corrigida, aula cancelada, reposicao consumida. |
| Financeiro | pagamento confirmado, desconto, cortesia, acordo, reembolso, disputa, mudanca de plano. |
| Contratos | envio, assinatura, cancelamento, retificacao, download sensivel. |
| Atendimento | handoff humano, automacao pausada, envio externo, falha relevante. |
| Comunicados | publico, template, aprovacao, envio, falhas, custo. |
| Agentes | ativar, pausar, mudar modo, publicar fluxo, executar, bloquear, reprocessar. |
| Politicas | criar versao, simular, aprovar, publicar, reverter. |
| Cotas | limite atingido, downgrade, compra/solicitacao de pacote, bloqueio. |
| Privacidade | LGPD recebida, validacao, exportacao, exclusao, anonimizacao, negacao. |
| Integracoes | conectar, desconectar, credencial atualizada, webhook falhou, reprocessamento. |

## Campos minimos do evento

| Campo | Descricao |
| --- | --- |
| tenantId | Studio afetado. |
| actorType | user, agent, system, integration, support. |
| actorId | Identificador seguro do ator. |
| action | Nome padronizado da acao. |
| objectType/objectId | Objeto afetado. |
| before/after | Mudanca quando aplicavel. |
| reason | Motivo informado ou inferido. |
| policyVersion | Politica usada quando houver regra operacional. |
| riskLevel | baixo, medio, alto, critico. |
| quotaImpact | consumo, bloqueio ou downgrade se houver. |
| safeMetadata | Dados seguros sem segredo/credencial. |
| createdAt | Data/hora. |

## Telas de auditoria

| Superficie | Papel |
| --- | --- |
| `/app/auditoria` | Busca e filtro de eventos. |
| `/app/auditoria/[eventId]` | Detalhe do evento. |
| Painel direito contextual | Ultimos eventos do objeto. |
| Aprovacao | Mostra evento que sera gerado. |
| Execucao de agente | Mostra ferramenta, input/output seguro e cota. |
| Mobile auditoria resumida | Consulta curta de evento sensivel. |

## O que nao auditar como dado bruto

- segredos;
- tokens;
- chaves de provedor;
- transcricoes completas sem necessidade;
- dados de saude em safeMetadata;
- conteudo integral de documentos sensiveis.

## Aceite

Se uma acao muda dinheiro, acesso, historico sensivel, mensagem externa, politica, agente, integracao, privacidade ou suporte, precisa de auditoria.
