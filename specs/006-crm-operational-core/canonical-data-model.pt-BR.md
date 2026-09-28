# Modelo de dados canonico - PT-BR

> Status: Rodada 0 v0.1. Este documento define os objetos de negocio que as telas, fluxos, permissoes, cotas e auditoria devem usar como linguagem comum.

## Regra central

Todo registro operacional pertence a um studio/tenant. Nenhuma tela, agente, relatorio, integracao ou suporte interno pode operar dado sem escopo de tenant, permissao e auditoria quando aplicavel.

## Objetos de conta e acesso

| Objeto | Papel no produto | Dono do dado | Sensibilidade |
| --- | --- | --- | --- |
| Studio/Tenant | Conta do studio cliente. | Dono/admin do studio; billing Taliya para status de assinatura. | Alta quando envolve plano, status e acesso. |
| Unidade | Unidade fisica do studio, quando existir. | Dono/admin. | Media. |
| Usuario | Pessoa com acesso ao CRM/app. | Dono/admin. | Media. |
| Membro da equipe | Relacao usuario-studio com papel e permissoes. | Dono/admin. | Alta. |
| Papel/permissao | O que cada usuario pode ver e fazer. | Dono/admin; suporte Taliya apenas com autorizacao. | Alta. |
| Convite | Convite pendente para equipe. | Dono/admin. | Media. |
| Acesso de suporte | Acesso temporario autorizado para time Taliya. | Dono/admin concede; Taliya usa. | Muito alta. |

## Objetos CRM

| Objeto | Papel no produto | Dono do dado | Sensibilidade |
| --- | --- | --- | --- |
| Contato | Registro base de pessoa ou telefone. | Studio. | Media. |
| Responsavel | Responsavel por aluno, financeiro, agenda ou emergencia. | Studio. | Alta se envolve menor, emergencia ou financeiro. |
| Aluno | Pessoa matriculada, ativa, pausada, cancelada ou inativa. | Studio. | Alta. |
| Interessado | Pessoa em processo comercial antes da matricula. | Studio. | Media. |
| Ex-aluno | Aluno encerrado com historico e elegibilidade de reativacao. | Studio. | Alta. |
| Grupo/telefone compartilhado | Contexto de familia, responsavel, telefone comum ou grupo. | Studio. | Media. |
| Preferencia de contato | Consentimento, canal preferido e opt-out. | Studio com decisao do contato. | Alta. |

## Objetos de agenda e aula

| Objeto | Papel no produto | Dono do dado | Sensibilidade |
| --- | --- | --- | --- |
| Grade semanal | Estrutura recorrente de horarios. | Studio. | Media. |
| Turma | Grupo com horario, professor, capacidade e alunos. | Studio. | Media. |
| Aula | Ocorrencia de turma/evento em data e horario. | Studio. | Media. |
| Chamada/presenca | Presenca, falta, no-show e correcao. | Studio. | Alta quando usada para cobranca, reposicao ou historico. |
| Direito de aula | Direito operacional gerado por plano, pacote, contrato, aula avulsa ou cortesia. | Studio. | Alta quando afeta cobranca, reposicao ou acesso. |
| Evento de consumo de aula | Reserva, presenca, no-show, uso, devolucao ou ajuste de direito/credito. | Studio. | Alta. |
| Credito de reposicao | Direito de reposicao com origem, validade e status. | Studio. | Media. |
| Pedido de reposicao | Solicitacao, candidatos, encaixe e resposta. | Studio. | Media. |
| Lista de espera | Pessoas aguardando vaga ou horario. | Studio. | Media. |
| Evento/workshop | Aula especial, capacidade, inscricoes e comunicacao. | Studio. | Media. |
| Recurso | Sala, equipamento ou recurso operacional. | Studio. | Baixa/media. |
| Indisponibilidade | Bloqueio de professor, sala, recurso, feriado ou recesso. | Studio. | Media. |

## Objetos comerciais

| Objeto | Papel no produto | Dono do dado | Sensibilidade |
| --- | --- | --- | --- |
| Origem de venda | Canal, campanha, indicacao ou entrada manual. | Studio. | Baixa/media. |
| Experimental | Aula experimental e seu ciclo comercial. | Studio. | Media. |
| Pre-matricula | Checklist antes de virar aluno. | Studio. | Alta quando envolve contrato/pagamento. |
| Indicacao | Relacao de quem indicou, beneficio e elegibilidade. | Studio. | Media. |
| Segmento | Regra salva de publico para acao, comunicacao ou relatorio. | Studio. | Media/alta. |
| Comunicado | Mensagem em massa ou segmentada com aprovacao e envio. | Studio. | Alta quando envolve WhatsApp e consentimento. |

## Objetos financeiros

| Objeto | Papel no produto | Dono do dado | Sensibilidade |
| --- | --- | --- | --- |
| Plano do studio | Produto/servico que o studio vende ao aluno. | Studio. | Media. |
| Plano do aluno | Plano contratado por um aluno, vigencia e status. | Studio. | Alta. |
| Modelo de cobranca | Configuracao de como mensalidade, pacote, parcela, aula avulsa ou contrato gera cobranca. | Studio. | Alta quando afeta direito de aula. |
| Modelo de consumo de aula | Configuracao de quando aula/credito e consumido, devolvido ou preservado. | Studio. | Alta. |
| Pagamento | Valor, vencimento, status e conciliacao. | Studio. | Alta. |
| Cobranca | Lembrete, link, tentativa e status. | Studio. | Alta. |
| Comprovante | Evidencia enviada pelo aluno/responsavel. | Studio. | Alta. |
| Acordo financeiro | Promessa, parcial, renegociacao ou saldo. | Studio. | Alta. |
| Excecao financeira | Desconto, cortesia, bloqueio, liberacao, pausa ou ajuste. | Studio. | Muito alta. |
| Estorno/disputa | Reembolso, contestacao ou chargeback. | Studio. | Muito alta. |
| Contrato | Termo assinado, enviado, expirado ou cancelado. | Studio. | Alta. |
| Documento financeiro | Recibo, nota, termo ou anexo financeiro. | Studio. | Alta. |

## Objetos de historico, saude operacional e privacidade

| Objeto | Papel no produto | Dono do dado | Sensibilidade |
| --- | --- | --- | --- |
| Evento de historico | Linha do tempo do aluno. | Studio. | Alta/muito alta. |
| Nota de professor | Registro pos-aula ou contexto permitido. | Studio. | Alta. |
| Restricao/cuidado | Informacao sensivel para aula. | Studio. | Muito alta. |
| Documento do aluno | Anamnese, consentimento, atestado, imagem ou audio. | Studio. | Muito alta. |
| Gate de anamnese | Bloqueio/alerta por dado essencial ausente. | Studio. | Muito alta. |
| Solicitacao LGPD | Pedido de acesso, correcao, exportacao, exclusao ou anonimizacao. | Contato/aluno solicita; studio executa. | Muito alta. |

## Objetos de operacao

| Objeto | Papel no produto | Dono do dado | Sensibilidade |
| --- | --- | --- | --- |
| Caso operacional | Container para problema, jornada, incidente ou excecao. | Studio. | Varia pelo objeto ligado. |
| Tarefa | Trabalho humano com dono, prazo e origem. | Studio. | Media. |
| Aprovacao | Decisao humana sobre acao proposta. | Studio. | Alta. |
| Checklist | Abertura, fechamento ou setup. | Studio. | Baixa/media. |
| Notificacao | Alerta roteado por papel e prioridade. | Sistema/studio. | Varia. |
| Problema de dados | Dado ausente, duplicado, conflitante ou inseguro. | Studio. | Media/alta. |

## Objetos de canais e mensagens

| Objeto | Papel no produto | Dono do dado | Sensibilidade |
| --- | --- | --- | --- |
| Conversa | Conversa por WhatsApp ou canal conectado. | Studio. | Alta. |
| Mensagem | Inbound/outbound, conteudo, autor, canal e provedor. | Studio. | Alta. |
| Tentativa de envio | Resultado de envio e idempotencia. | Sistema/studio. | Media/alta. |
| Template/modelo | Mensagem aprovada, categoria, versao e canal. | Studio. | Alta quando automatiza envio. |
| Conexao de canal | WhatsApp, provedor, status e credenciais seguras. | Studio/Taliya. | Muito alta. |

## Objetos de agentes e automacao

| Objeto | Papel no produto | Dono do dado | Sensibilidade |
| --- | --- | --- | --- |
| Agente | Capacidade operacional contratada/configurada. | Taliya define; studio habilita. | Media. |
| Fluxo de agente | Rotina configuravel com gatilho, modo e limites. | Taliya define base; studio configura. | Alta. |
| Configuracao de fluxo | Modo, limites, templates, regras, filas e handoff. | Studio. | Alta. |
| Execucao de fluxo | Run de agente com entrada, saida, status e custo. | Sistema. | Alta. |
| Incidente de automacao | Erro, dano, correcao e prevencao. | Studio/Taliya quando tecnico. | Alta. |
| Politica operacional | Regra versionada usada por humanos e agentes. | Studio. | Alta. |
| Versao de politica | Snapshot com vigencia, autor e rollback. | Studio. | Alta. |

## Objetos de uso, billing e auditoria

| Objeto | Papel no produto | Dono do dado | Sensibilidade |
| --- | --- | --- | --- |
| Lancamento de cota | Consumo por origem, fluxo, agente e caso. | Sistema/Taliya. | Media. |
| Regra de economia | Comportamento por limite e prioridade. | Studio/Taliya por plano. | Media. |
| Plano Taliya | Plano Base, 1, 3 ou 7 agentes e entitlements. | Taliya. | Media. |
| Add-on/pacote | Cota extra ou recurso adicional. | Taliya. | Media. |
| Fatura Taliya | Cobranca da assinatura do studio. | Taliya. | Alta. |
| Evento de auditoria | Quem fez o que, antes/depois, objeto e motivo. | Sistema. | Alta. |
| Log de integracao | Evento tecnico seguro, idempotencia e erro. | Sistema/Taliya. | Media/alta. |
| Job de importacao | Entrada inicial ou incremental de dados. | Studio. | Alta. |
| Job de exportacao | Exportacao, backup ou contabilidade. | Studio. | Alta. |

## Decisoes ainda abertas

| Tema | Decisao pendente |
| --- | --- |
| Multi-unidade | Lancamento atual deve tratar uma unidade por studio; multi-unidade deve ficar preparado mas nao prometido. |
| Dados clinicos | Definir limite entre historico operacional permitido e dado de saude sensivel. |
| Fatura Taliya vs financeiro do aluno | Manter billing Taliya separado do financeiro que o studio cobra dos alunos. |
| Marketing/campanhas | Comunicados e reativacao existem; marketing amplo e agente de marketing seguem como agente sob medida/futuro. |
