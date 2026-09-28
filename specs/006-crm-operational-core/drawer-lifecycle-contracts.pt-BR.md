# Contratos De Ciclo Dos Drawers - PT-BR

> Status: v0.1 extensivel. Este documento detalha como os drawers acionaveis nascem, entram no Hoje, sao resolvidos e se comportam em manual, programatico, copiloto e autonomo.
>
> Escopo inicial: drawers da pagina Hoje e reutilizacao dos mesmos drawers na pagina Operacao.
>
> Expansao registrada: as familias Tarefas, Checklists, Aprovacoes, Inbox, Alunos, Agenda/Aula, Reposicoes e Financeiro tambem usam paineis/drawers contextuais. Nem todo painel dessas familias compartilha o mesmo tipo de drawer de Hoje/Operacao, mas todos seguem a regra central de estado selecionado, origem canonica, acao segura e variacao por item clicado.
>
> Este contrato nao e definitivo. Ele deve ser expandido quando novas familias de paginas exigirem ciclos proprios, como Agenda, Financeiro, Alunos, Vendas, Retencao, Agentes, Cotas e Configuracoes.

## Regra Central

Um drawer nao e apenas um painel visual. Ele representa um **estado operacional** de um objeto ou demanda.

Por padrao, as paginas carregam com drawer/painel lateral de detalhe **fechado**.

O drawer/painel abre somente quando o usuario seleciona um item, acessa uma URL direta de detalhe ou aciona explicitamente uma acao de detalhe.

Imagens aprovadas com drawer aberto sao imagens explicativas de estado selecionado. Elas nao definem o estado inicial da rota.

Um mesmo painel/drawer pode ter varios modos dentro da rota. A imagem aprovada costuma documentar apenas um modo representativo; os demais modos herdam a estrutura visual se mantiverem a mesma largura, hierarquia, densidade, origem canonica e padrao de acoes.

Drawers sao compartilhados por tipo de item entre Hoje e Operacao:

- se o tipo real e o mesmo, o drawer deve ter a mesma estrutura, os mesmos blocos principais e as mesmas acoes permitidas;
- Hoje muda o motivo de entrada: por que apareceu na mesa de comando do dia;
- Operacao muda o motivo de entrada: em que etapa esta e por que precisa acompanhamento;
- a origem canonica, acoes permitidas, bloqueios, modos de agente e regras de resolucao continuam iguais.

Todo drawer precisa responder:

```text
O que e isto?
De onde veio?
Por que apareceu agora?
Quem e responsavel?
Qual impacto?
Qual e a proxima acao segura?
O que muda em 0, 1, 3 e 7 agentes?
O que pode ser manual, copiloto ou autonomo?
```

## Padrao De Ciclo

Cada drawer deve ser documentado com:

| Campo | Definicao |
| --- | --- |
| Como nasce | Quais origens criam esse item. |
| Como entra no Hoje | Qual criterio faz aparecer na pagina Hoje. |
| Origem canonica | Onde o objeto vive de verdade. |
| Manual | O que o usuario consegue fazer sem IA. |
| Programatico | O que o CRM consegue detectar/criar por regra simples. |
| Copiloto | O que o agente pode sugerir, resumir ou preencher. |
| Autonomo | O que o agente pode executar sem clique humano. |
| Resolucao | Como o item deixa de exigir atencao. |
| Vira tarefa quando | Quando precisa de trabalho humano acompanhado. |
| Vira aprovacao quando | Quando precisa de decisao/autorizacao. |
| Vira caso quando | Quando cruza areas ou tem varias etapas. |
| Bloqueios | Permissao, cota, politica, dado, integracao, risco ou auditoria. |

## Planos E Modos

| Plano | Regra nos ciclos |
| --- | --- |
| 0 agentes | Tudo deve funcionar manualmente ou por regra programatica. Nenhum ciclo pode depender de IA. |
| 1 agente | IA so atua se o agente configurado cobre o dominio do item. |
| 3 agentes | IA atua nos dominios do bundle ativo, normalmente Atendimento, Agenda e Vendas, salvo troca. |
| 7 agentes | Todos os dominios podem ter IA, respeitando permissao, cota, politica, risco e auditoria. |

| Modo | Regra |
| --- | --- |
| Manual | Usuario executa, decide, cria e conclui. Sempre deve existir no caminho critico. |
| Programatico | CRM detecta estado por regra sem IA. Funciona no plano 0 agentes. |
| Copiloto | Agente sugere, explica, resume, preenche ou prepara. Humano confirma. |
| Autonomo | Agente executa apenas acoes seguras, permitidas, auditaveis e com fallback. |

## Ciclo: Prioridade Do Agora

| Campo | Contrato |
| --- | --- |
| Como nasce | Agregacao de tarefa, fila humana, bloqueio, aprovacao, financeiro, aula, incidente, dado ou alerta. |
| Como entra no Hoje | Ranking por impacto, urgencia, SLA, risco, fila, prazo, cota ou bloqueio do dia. |
| Origem canonica | A origem do tipo real: Tarefas, Inbox, Agenda, Financeiro, Aprovacoes, Operacao, Dados, Uso/Cotas ou Agentes. |
| Manual | Usuario abre item, decide acao e vai para origem. |
| Programatico | CRM ranqueia por regra, prazo, impacto e estado. |
| Copiloto | Agente explica por que subiu, resume contexto e sugere proxima acao. |
| Autonomo | Nao executa por ser agregador; executa apenas se o tipo real permitir autonomia. |
| Resolucao | Resolve o tipo real ou remove motivo de prioridade. |
| Vira tarefa quando | A proxima acao humana ainda nao existe como tarefa. |
| Vira aprovacao quando | A proxima acao exige decisao/autorizacao. |
| Vira caso quando | O item cruza areas ou precisa de timeline e multiplas etapas. |
| Bloqueios | Cota, permissao, risco, dado ausente, origem indisponivel ou tipo real sem autonomia. |

## Ciclo: Checklist Do Dia

| Campo | Contrato |
| --- | --- |
| Como nasce | Rotina configurada do studio, template Taliya, checklist recorrente ou item manual. |
| Como entra no Hoje | Item vence hoje, esta atrasado, bloqueia abertura/fechamento ou exige evidencia. |
| Origem canonica | Checklist. |
| Manual | Marcar feito, comentar, delegar, reabrir, pular com justificativa se permitido. |
| Programatico | CRM cria checklist diario e marca atraso por horario. |
| Copiloto | Agente lembra, explica impacto, sugere responsavel ou transforma pendencia em tarefa. |
| Autonomo | Pode lembrar ou criar tarefa segura; nao deve marcar feito sem evidencia/regra objetiva. |
| Resolucao | Item marcado feito, pulado com justificativa, reaberto ou convertido em tarefa. |
| Vira tarefa quando | A rotina nao pode ser concluida no clique e precisa de dono/prazo. |
| Vira aprovacao quando | Pular item critico ou alterar rotina exigir autorizacao. |
| Vira caso quando | Falha de rotina impacta varias areas ou recorrencia operacional. |
| Bloqueios | Evidencia ausente, permissao, item critico, dependencia de origem. |

## Ciclo: Aula De Hoje

| Campo | Contrato |
| --- | --- |
| Como nasce | Grade recorrente, aula avulsa, reposicao reservada, evento ou ajuste manual. |
| Como entra no Hoje | Aula ocorre hoje, tem chamada pendente, ocupacao critica, alerta, reposicao, conflito ou pendencia. |
| Origem canonica | Agenda/Aula. |
| Manual | Abrir aula, fazer chamada, ver alunos, registrar ocorrencia, criar tarefa, abrir turma/agenda. |
| Programatico | CRM detecta lotacao, vaga, chamada pendente, conflito, falta, reposicao ou professor/sala ausente. |
| Copiloto | Agente resume aula, sugere acao, prepara aviso permitido ou explica conflito. |
| Autonomo | Pode enviar lembrete seguro se permitido; nao altera chamada/presenca sensivel sem evidencia. |
| Resolucao | Aula concluida, chamada feita, pendencia resolvida, tarefa/caso criado ou alerta removido. |
| Vira tarefa quando | Alguem precisa acompanhar algo fora da tela da aula. |
| Vira aprovacao quando | Alteracao ou comunicado sensivel exige decisao. |
| Vira caso quando | Aula impacta varias pessoas/areas ou exige varias acoes. |
| Bloqueios | Permissao de professor, dado sensivel, chamada auditada, cota de mensagem, politica de agenda. |

## Ciclo: Tarefa

| Campo | Contrato |
| --- | --- |
| Como nasce | Manual, origem, regra programatica, copiloto confirmado, autonomia segura, fallback, checklist ou caso. |
| Como entra no Hoje | Prazo hoje, atraso, alta prioridade, sem dono, vinculada a item urgente ou criada por fallback. |
| Origem canonica | Tarefas. |
| Manual | Criar, assumir, concluir, comentar, reagendar, delegar, cancelar, abrir origem. |
| Programatico | CRM cria por regra ou fallback sem IA. |
| Copiloto | Agente sugere titulo, prazo, dono, checklist, resumo e conclusao. Humano confirma. |
| Autonomo | Pode criar tarefa segura e concluir apenas com evidencia objetiva e baixo risco. |
| Resolucao | Concluida, reagendada, delegada, cancelada, convertida em caso/aprovacao ou aguardando resposta. |
| Vira tarefa quando | Ja e tarefa. |
| Vira aprovacao quando | Conclusao ou acao exige decisao sensivel. |
| Vira caso quando | A tarefa revelou problema maior que cruza areas. |
| Bloqueios | Falta de dono, permissao, dado ausente, resultado ambiguo, acao sensivel, auditoria. |

## Ciclo: Fila Humana

| Campo | Contrato |
| --- | --- |
| Como nasce | Conversa aguardando humano, handoff de agente, atendimento pausado, origem com espera ou fluxo sem autonomia. |
| Como entra no Hoje | Tempo acima do SLA, alta prioridade, aluno aguardando, impacto no dia ou falta de dono. |
| Origem canonica | Inbox, Conversa, Operacao ou Agente/Execucao. |
| Manual | Assumir, responder, resolver na origem, delegar, criar tarefa se precisar acompanhar. |
| Programatico | CRM mede espera, SLA e fila. |
| Copiloto | Agente resume conversa, sugere resposta, classifica urgencia e prepara proxima acao. |
| Autonomo | So responde se canal, consentimento, politica, risco e agente permitirem. Caso contrario mantem handoff. |
| Resolucao | Pessoa responde/resolva, fila muda de dono, tarefa criada, caso criado ou conversa encerrada. |
| Vira tarefa quando | Precisa retornar depois, acompanhar ou fazer trabalho fora da conversa. |
| Vira aprovacao quando | Resposta/acao sensivel precisa decisao. |
| Vira caso quando | Conversa revela problema operacional maior. |
| Bloqueios | Identidade, opt-out, cota, canal indisponivel, risco, permissao ou baixa confianca. |

## Ciclo: Bloqueio

| Campo | Contrato |
| --- | --- |
| Como nasce | Agenda, recurso, dado, integracao, cota, permissao, politica, professor, sala, pagamento ou agente bloqueia uma acao. |
| Como entra no Hoje | Bloqueia algo previsto para hoje ou impede execucao/autonomia relevante. |
| Origem canonica | Origem do bloqueio: Agenda, Dados, Integracoes, Uso/Cotas, Financeiro, Operacao ou Agentes. |
| Manual | Abrir origem, resolver causa, criar tarefa, criar caso, delegar ou ignorar com justificativa se permitido. |
| Programatico | CRM detecta estado bloqueante por regra. |
| Copiloto | Agente explica causa, impacto, dependencias e sugere menor caminho. |
| Autonomo | Pode resolver apenas bloqueios seguros e reversiveis; normalmente cria fallback manual. |
| Resolucao | Causa removida, origem atualizada, tarefa/caso/aprovacao criada ou bloqueio aceito com justificativa. |
| Vira tarefa quando | Existe uma acao humana clara para remover o bloqueio. |
| Vira aprovacao quando | Remover bloqueio exige decisao sensivel ou excecao. |
| Vira caso quando | Bloqueio cruza areas ou exige varias acoes. |
| Bloqueios | Proprio tipo representa bloqueio; registrar causa, impacto e caminho manual. |

## Ciclo: Aprovacao

| Campo | Contrato |
| --- | --- |
| Como nasce | Agente, sistema ou usuario propoe acao que exige decisao. |
| Como entra no Hoje | Vence hoje, bloqueia fluxo do dia ou tem risco/impacto alto. |
| Origem canonica | Aprovacoes. |
| Manual | Aprovar, editar, rejeitar, pedir dados, abrir origem. |
| Programatico | CRM cria aprovacao por politica, permissao, cota, risco ou acao sensivel. |
| Copiloto | Agente explica proposta, antes/depois, impacto, risco e texto sugerido. |
| Autonomo | Nao aprova sozinho. Pode executar apos aprovacao se permitido. |
| Resolucao | Aprovada, editada/aprovada, rejeitada, expirada, bloqueada ou convertida em tarefa. |
| Vira tarefa quando | Precisa de revisao humana antes da decisao ou execucao posterior. |
| Vira aprovacao quando | Ja e aprovacao. |
| Vira caso quando | Decisao envolve problema operacional maior. |
| Bloqueios | Permissao, cota, politica, dado ausente, risco, expiracao e auditoria obrigatoria. |

## Ciclo: Financeiro

| Campo | Contrato |
| --- | --- |
| Como nasce | Pagamento vencido, comprovante enviado, cobranca falhou, desconto, excecao, contrato ou bloqueio financeiro. |
| Como entra no Hoje | Impacta aula, matricula, continuidade, cobranca do dia ou exige validacao hoje. |
| Origem canonica | Financeiro, Movimentacoes, Cobrancas, Contratos, Aprovacoes, Tarefas, Aluno ou Operacao. |
| Manual | Validar, cobrar, abrir pagamento, criar tarefa/aprovacao, registrar observacao. |
| Programatico | CRM detecta vencimento, falha, status de provedor, comprovante pendente ou regra de bloqueio. |
| Copiloto | Agente resume historico, sugere mensagem, explica impacto e prepara cobranca. |
| Autonomo | Pode enviar lembrete simples permitido; nao confirma pagamento, desconto ou excecao sensivel. |
| Resolucao | Pago, validado, cobrado, reagendado, em disputa, convertido em tarefa/aprovacao/operacao. |
| Vira tarefa quando | Alguem precisa cobrar, validar, ligar ou revisar. |
| Vira aprovacao quando | Desconto, excecao, liberacao ou acordo exige decisao. |
| Vira operacao quando | Disputa, inadimplencia sensivel ou impacto amplo precisa dono, prazo e acompanhamento fora do financeiro. |
| Bloqueios | Permissao financeira, provedor, comprovante ambiguo, cota de mensagem, auditoria. |

## Ciclo: Alerta Ou Cota Contextual

| Campo | Contrato |
| --- | --- |
| Como nasce | Uso/cota, politica, notificacao urgente, limite, economia, downgrade ou bloqueio de automacao. |
| Como entra no Hoje | Impacta acao de hoje, automacao do dia ou caminho manual necessario. |
| Origem canonica | Uso/Cotas, Notificacoes, Politicas ou Agentes. |
| Manual | Abrir origem, ajustar economia, pausar baixa prioridade, criar tarefa, comprar/solicitar pacote se permitido. |
| Programatico | CRM monitora limite e aplica economia. |
| Copiloto | Agente explica impacto e sugere economia/priorizacao. |
| Autonomo | Nao compra pacote nem muda plano; pode aplicar regras de economia ja configuradas. |
| Resolucao | Uso normalizado, pacote aplicado, regra ajustada, automacao pausada, tarefa/caso criado. |
| Vira tarefa quando | Alguem precisa agir manualmente por limite ou bloqueio. |
| Vira aprovacao quando | Ajuste sensivel de politica/plano/custo exige decisao. |
| Vira caso quando | Cota bloqueia varias operacoes ou causa incidente operacional. |
| Bloqueios | Entitlement, cota 100%, billing, permissao, politica e auditoria. |

## Ciclo: Incidente

| Campo | Contrato |
| --- | --- |
| Como nasce | Falha de agente, execucao, integracao, webhook, provedor, reprocessamento ou ferramenta. |
| Como entra no Hoje | Impacta operacao do dia, bloqueia fluxo, cria fila humana ou exige fallback. |
| Origem canonica | Operacao/Incidentes, Agentes/Execucoes ou Integracoes. |
| Manual | Abrir incidente, reprocessar se seguro, criar tarefa, pausar fluxo, escalar suporte. |
| Programatico | CRM detecta falha, timeout, erro de provedor, retry esgotado ou idempotencia. |
| Copiloto | Agente explica falha, impacto, trace resumido e proximo passo seguro. |
| Autonomo | Pode reprocessar apenas se idempotente, seguro e permitido. Caso contrario cria fallback. |
| Resolucao | Reprocessado, mitigado, pausado, escalado, convertido em tarefa/caso ou marcado como conhecido. |
| Vira tarefa quando | Precisa de acao operacional manual. |
| Vira aprovacao quando | Reprocessar ou executar acao sensivel exige decisao. |
| Vira caso quando | Incidente impacta varias areas ou requer timeline operacional. |
| Bloqueios | Idempotencia, seguranca, cota, permissao, integracao fora, suporte/grant e auditoria. |

## Ciclo: Problema De Dados

| Campo | Contrato |
| --- | --- |
| Como nasce | Dado ausente, duplicidade, conflito, baixa confianca, importacao divergente ou identidade ambigua. |
| Como entra no Hoje | Bloqueia acao de hoje, impede agente, trava agenda/financeiro/comunicacao ou exige revisao. |
| Origem canonica | Qualidade de dados, perfil do objeto ou origem importada. |
| Manual | Corrigir dado, confirmar valor, pedir revisao, criar tarefa, abrir perfil, manter separado. |
| Programatico | CRM detecta conflito por regra, valida formato ou identifica duplicidade candidata. |
| Copiloto | Agente sugere merge/correcao e explica confianca. |
| Autonomo | Nao mescla ou altera dado sensivel sozinho; pode normalizar dado simples permitido. |
| Resolucao | Dado corrigido, revisao solicitada, tarefa criada, duplicidade mantida/mesclada com permissao. |
| Vira tarefa quando | Alguem precisa validar ou buscar informacao. |
| Vira aprovacao quando | Merge, alteracao sensivel ou sobrescrita exige decisao. |
| Vira caso quando | Problema de dados afeta varios objetos ou fluxo critico. |
| Bloqueios | Baixa confianca, identidade, dado sensivel, importacao antiga, permissao e auditoria. |

## Ciclos Fora Da Pagina Hoje

Este documento deve ser expandido quando surgirem ciclos que nao pertencem diretamente ao Hoje.

| Familia | Ciclos provaveis |
| --- | --- |
| Operacao/Jornadas | Caso operacional, etapa de jornada, tarefa vinculada, aprovacao vinculada, incidente vinculado, reabertura. |
| Agenda | Turma, aula, reposicao, lista de espera, recurso, conflito, chamada. |
| Financeiro | Pagamento, cobranca, comprovante, excecao, disputa, acordo, contrato financeiro. |
| Inbox/Atendimento | Conversa, handoff, opt-out, contato desconhecido, resposta sugerida. |
| Alunos | Aluno, responsavel, historico, restricao/cuidado, documento, relacionamento familiar. |
| Vendas | Interessado, experimental, follow-up, pre-matricula, matricula. |
| Retencao | Risco, plano de salvamento, cancelamento, reclamacao, reativacao. |
| Agentes | Fluxo, execucao, ferramenta, preflight, eval, incidente, cota por fluxo. |
| Configuracoes | Politica, permissao, integracao, billing, suporte/grant. |

Regra para futuras expansoes:

- nao criar drawer sem ciclo;
- nao criar ciclo sem origem canonica;
- nao permitir autonomia sem politica, permissao, cota, auditoria e fallback;
- manter caminho manual em todos os ciclos criticos.
