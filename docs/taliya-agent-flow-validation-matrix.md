# Taliya Agent Flow Validation Matrix

## Objetivo

Validar o mapa final de fluxos antes de criar as configuracoes individuais por studio.

Este documento funciona como uma ferramenta de auditoria. Ele existe para detectar erros como:

- fluxo sem canal claro;
- fluxo sem estado final;
- fluxo que depende de dado nao configurado;
- fluxo sensivel sem handoff;
- fluxo que aponta para outro fluxo inexistente;
- fluxo que deveria nascer no sistema, mas foi tratado como WhatsApp;
- fluxo que deveria economizar creditos, mas nao tem criterio de limite.

## Superficies Do Produto

Taliya opera em duas superficies de produto:

- `whatsapp`: conversa externa com aluno, interessado, ex-aluno ou responsavel.
- `sistema`: Taliya acessada pela web ou pelo app. A plataforma muda, mas a superficie operacional e a mesma.

Para a auditoria, web e app nao sao canais diferentes. Ambos entram como `sistema`:

- configuracao, gestao, financeiro, filas, relatorios, setup e auditoria;
- chamada, observacoes de aula, contexto do aluno, tarefas rapidas e notificacoes.

## Estados Padrao Aceitos

Todo fluxo deve terminar em um ou mais destes estados:

- `resolvido`
- `aguardando_contato`
- `aguardando_equipe`
- `acao_registrada`
- `tarefa_criada`
- `handoff_humano`
- `proximo_fluxo`
- `sem_acao`
- `pausado`

## Checklist Global

Antes de um fluxo virar configuracao, ele precisa responder:

| Check | Pergunta |
| --- | --- |
| Canal | Onde o fluxo nasce, roda, registra e e acompanhado? |
| Estado | Quais estados finais sao possiveis? |
| Dados | Quais dados minimos precisa para rodar? |
| Falta de dado | O que acontece se o dado minimo nao existe? |
| Risco | Existe risco financeiro, saude, LGPD, reputacao ou agenda? |
| Handoff | Quando precisa de humano? |
| Economia | Quando reduzir, agrupar, pausar ou evitar WhatsApp pago? |
| Custo por fluxo | De onde vem o custo deste fluxo em cada modo: IA, WhatsApp, lote, midia ou historico? |
| Alcance autonomo | Se estiver autonomo, ate onde vai e o que acontece depois? |
| Transicao | Para qual fluxo real ele pode ir depois? |
| Auditoria | O que precisa ficar registrado? |

## Matriz 1: Canais Por Fluxo

Legenda:

- `N`: onde o fluxo nasce.
- `R`: onde o fluxo roda.
- `A`: onde a equipe acompanha/aprova.
- `L`: onde registra log/resultado.

| Fluxo | WhatsApp | Sistema | Observacao |
| --- | --- | --- | --- |
| A1 Nova Conversa | N/R | A/L | Entrada externa, registro interno. |
| A2 Duvidas Permitidas | N/R | L | Resposta externa com base configurada. |
| A3 Aluno Existente | N/R | A/L | Classifica e encaminha. |
| A4 Fora Do Escopo | N/R | A/L | Pode pausar ou criar tarefa. |
| A5 Handoff Humano | N | R/A/L | Humano decide no sistema. |
| A6 Consentimento/Opt-Out | N/R | A/L | Preferencias ficam no sistema. |
| A7 Identidade/Midias | N/R | A/L | Midias podem exigir revisao. |
| A8 Privacidade/Dados | N | R/A/L | Nunca responder dado sensivel sem validacao. |
| A9 Grupos/Familiares | N/R | A/L | Evita expor dados em grupo. |
| A10 Ciclo De Vida/SLA | N/R | R/A/L | Controla conversa aberta e atrasos. |
| B1 Confirmacao Presenca | N/R | A/L | Sistema pode mostrar chamada. |
| B2 Falta Com Aviso | N/R | A/L | Pode liberar vaga. |
| B3 No-Show | - | N/R/A/L | Nasce em chamada/aula. |
| B4 Recuperar Vaga | R | R/A/L | Pode convidar via WhatsApp. |
| B5 Reposicao/Remarcacao | N/R | A/L | Reserva e registra. |
| B6 Lista De Espera | R | N/R/A/L | Nasce por pedido ou sistema. |
| B7 Disponibilidade Experimental | R | R/A/L | Normalmente acionado por Vendas. |
| B8 Mudanca Horario Fixo | N/R | R/A/L | Pode afetar plano. |
| B9 Cancelamento Pelo Studio | R | N/R/A/L | Comunicacao em lote exige aprovacao. |
| B10 Conflito Capacidade | - | N/R/A/L | Nao deve enviar mensagem externa automaticamente. |
| B11 Ajuste De Grade | - | N/R/A/L | Impacta varios fluxos. |
| B12 Experimental No-Show | N/R | A/L | Volta para Vendas. |
| B13 Creditos Reposicao | R | N/R/A/L | Controla validade e uso. |
| B14 Correcao Presenca | - | N/R/A/L | Auditoria importante. |
| B15 Primeira Aula | R | N/R/A/L | Sistema/professor tem papel forte. |
| B16 Aula Especial/Workshop | R | N/R/A/L | Pode conectar Vendas/Financeiro. |
| C1 Valores/Planos | N/R | A/L | Politica comercial configurada. |
| C2 Aula Experimental | N/R | A/L | Usa Agenda para disponibilidade. |
| C3 Lembrete Experimental | N/R | L | WhatsApp externo. |
| C4 Pos-Aula Experimental | N/R | A/L | Pode usar nota do professor. |
| C5 Follow-Up Comercial | N/R | A/L | Cadencia limitada. |
| C6 Pre-Matricula | N/R | R/A/L | Normalmente copiloto. |
| C7 Objecoes | N/R | A/L | Desconto vai para humano. |
| C8 Origem/Qualificacao | N/R | R/L | Atualiza CRM. |
| C9 Perda Comercial | N/R | R/L | Registra motivo. |
| C10 Indicacao | N/R | A/L | Beneficio exige Financeiro/humano. |
| C11 Checkout/Abandono | R | N/R/A/L | Depende de link/status. |
| C12 Demanda Sem Vaga | N/R | A/L | Pode gerar lista comercial. |
| C13 Interessado Para Aluno | R | N/R/A/L | Conecta Agenda/Financeiro/Historico. |
| C14 Upsell/Upgrade | N/R | R/A/L | Sensivel, nao empurrar automaticamente. |
| D1 Lembrete Vencimento | N/R | A/L | Customizado por regra. |
| D2 Pagamento Atrasado | N/R | A/L | Limite por faixa de atraso. |
| D3 Pix/Link | N/R | A/L | Nunca coletar dados sensiveis. |
| D4 Confirmacao Pagamento | R | N/R/A/L | Webhook/equipe/comprovante. |
| D5 Renovacao Plano | R | N/R/A/L | Copiloto por padrao. |
| D6 Excecoes Financeiras | N | R/A/L | Humano obrigatorio. |
| D7 Falha Pagamento | R | N/R/A/L | Pode avisar aluno. |
| D8 Recibo/Nota | N/R | R/A/L | Pode exigir documento. |
| D9 Pausa/Trancamento | N | R/A/L | Humano. |
| D10 Conciliacao | - | N/R/A/L | Interno. |
| D11 Contrato/Termos | R | N/R/A/L | Legal exige cuidado. |
| D12 Bloqueio/Liberacao | R | N/R/A/L | Humano. |
| D13 Creditos/Cortesias | - | N/R/A/L | Humano. |
| D14 Fechamento Mensal | - | N/R/L | Vai para Gestao. |
| E1 Queda Frequencia | - | N/R/A/L | Pode virar WhatsApp. |
| E2 Aluno Inativo | N/R | A/L | Economia forte. |
| E3 Retorno | N/R | A/L | Agenda assume horario. |
| E4 Risco Cancelamento | N | R/A/L | Humano. |
| E5 Reativacao Ex-Aluno | N/R | A/L | Copiloto/lote aprovado. |
| E6 Satisfacao | N/R | A/L | Negativo vira humano. |
| E7 Retorno Apos Pausa | N/R | A/L | Conecta Financeiro/Agenda. |
| E8 Risco Por Perfil | - | N/R/A/L | Interno. |
| E9 Pos-Cancelamento | R | R/A/L | Pode pausar contato. |
| E10 Marco Engajamento | R | A/L | Baixa prioridade. |
| E11 Saude/Evento Pessoal | N | R/A/L | Humano e Historico. |
| E12 Segmentacao Risco | - | N/R/A/L | Campanha exige aprovacao. |
| F1 Prioridades Dia | - | N/R/A/L | Gestao. |
| F2 Dinheiro Na Mesa | - | N/R/L | Gestao. |
| F3 Fila Humana | - | N/R/A/L | Aprovar/editar/rejeitar. |
| F4 Gargalos | - | N/R/A/L | Copiloto. |
| F5 Resumo Semanal | R | N/R/A/L | Notificacao interna opcional. |
| F6 Qualidade Dados | - | N/R/A/L | Bloqueia fluxos. |
| F7 Creditos/Limites | - | N/R/A/L | Ativa economia. |
| F8 Performance | - | N/R/L | Gestao. |
| F9 Permissoes/Auditoria | - | N/R/A/L | Interno. |
| F10 Capacidade/Crescimento | - | N/R/A/L | Copiloto. |
| F11 Falhas/Webhooks | - | N/R/A/L | Operacional. |
| F12 Importacao/Migracao | - | N/R/A/L | Setup. |
| F13 Teste De Fluxo | - | N/R/A/L | Antes de ativar. |
| G1 Contexto Antes Aula | - | N/R/A/L | Professor no sistema. |
| G2 Observacao Pos-Aula | - | N/R/L | Professor no sistema. |
| G3 Restricao/Cuidado | - | N/R/A/L | Sensivel. |
| G4 Objetivo/Evolucao | - | N/R/L | Interno. |
| G5 Contexto Para Agente | - | N/R/L | Interno/hibrido. |
| G6 Documentos/Anamnese | R | N/R/A/L | Sensivel. |
| G7 Correcao Historico | - | N/R/A/L | Auditoria. |
| G8 Handoff Professores | - | N/R/A/L | Interno. |
| G9 Lembrete Professor | - | N/R/A/L | Sistema. |
| G10 Compartilhar Contexto | N/R | R/A/L | Copiloto. |
| G11 Permissao Historico | - | N/R/A/L | RBAC. |
| G12 Linha Do Tempo | - | N/R/L | Fonte de contexto. |

## Matriz 2: Dados Obrigatorios Por Familia De Fluxo

| Familia | Dados obrigatorios | Se faltar |
| --- | --- | --- |
| Atendimento externo | contato, canal, mensagem, status de consentimento | criar contato leve ou pausar campanha |
| Atendimento aluno | contato vinculado a aluno, status do aluno, conversa recente | pedir identificador minimo ou tarefa |
| Agenda aula | grade, turma, professor, capacidade, aluno, regra de presenca | bloquear autonomia e criar setup/tarefa |
| Reposicao | aula origem, elegibilidade, credito, validade, disponibilidade | pedir dado, tarefa ou handoff |
| Experimental | interessado, origem, turno, disponibilidade, regra experimental | pedir dado ou tarefa |
| Vendas plano | planos, politica de preco, disponibilidade, etapa CRM | handoff ou tarefa de setup |
| Pre-matricula | interessado, plano, horario, contato, responsavel | perguntar minimo ou tarefa |
| Financeiro | plano, vencimento, status pagamento, link/instrucao, politica | bloquear mensagem automatica se falta dado critico |
| Excecao financeira | aluno, plano, motivo, politica, responsavel | humano obrigatorio |
| Retencao | frequencia, ultimo comparecimento, plano/status, historico recente | monitorar ou tarefa |
| Historico | aluno, nota/contexto, permissao, papel do usuario | bloquear ou pedir anotacao |
| Gestao | eventos dos agentes, pendencias, responsaveis, configuracoes | checklist/setup |

## Matriz 3: Risco E Handoff Obrigatorio

| Tipo de risco | Exemplos | Regra |
| --- | --- | --- |
| Saude/clinico | dor, lesao, gravidez, cirurgia, orientacao de exercicio | humano + Historico; nunca orientar automaticamente |
| Financeiro | desconto, reembolso, contestacao, bloqueio, cortesia | humano ou copiloto com aprovacao |
| LGPD/privacidade | dados pessoais, historico, grupo, responsavel nao validado | validar permissao ou bloquear |
| Reputacao | aluno irritado, reclamacao, cancelamento, conflito | humano ou tarefa prioritaria |
| Agenda critica | overbooking, professor ausente, cancelamento em lote | copiloto/humano antes de mensagem |
| Custo alto | campanha, lote, WhatsApp pago, reativacao em massa | configuracao por fluxo + origem do custo + aprovacao + limite |
| Dado conflitante | pagamento divergente, chamada errada, duplicidade | bloquear autonomia e criar tarefa |
| Baixa confianca | intencao ambigua, pessoa nao identificada | perguntar uma vez ou handoff |

## Matriz 4: Economia De Creditos Por Familia

| Familia | Economia padrao |
| --- | --- |
| Duvidas simples | responder por template/regra, sem IA cara |
| Classificacao | usar modelo barato e contexto resumido |
| Agenda | calcular por regra antes de IA |
| Recuperar vaga | limitar candidatos e evitar conversa paga de baixa prioridade |
| Vendas | cadencia curta, sem follow-up infinito |
| Financeiro | agrupar lembretes e evitar mensagens redundantes |
| Retencao | priorizar alto risco, listas em copiloto antes de lote |
| Gestao | gerar resumo agregado, nao varias mensagens soltas |
| Historico | resumir incrementalmente, nao reenviar historico completo |
| Falhas/retries | idempotencia antes de retry para evitar duplicidade |

## Matriz 5: Testes De Consistencia Do Mapa

Use esta lista ao revisar cada fluxo:

| ID | Teste | Passa quando |
| --- | --- | --- |
| T01 | Fluxo tem dono unico | Um agente e responsavel pela decisao principal. |
| T02 | Fluxo tem canal de nascimento | Esta claro se nasce no WhatsApp ou no sistema. |
| T03 | Fluxo tem local de registro | Resultado fica salvo no sistema. |
| T04 | Fluxo tem estado final | Usa estado padrao aceito. |
| T05 | Fluxo tem dado minimo | Dados obrigatorios estao claros. |
| T06 | Falta de dado tem caminho | Nao fica travado sem tarefa/handoff/setup. |
| T07 | Risco tem handoff | Saude, financeiro, LGPD e conflito param automacao. |
| T08 | Transicao aponta para fluxo real | Proximo fluxo existe no mapa. |
| T09 | Custo tem limite | Lotes, campanhas e mensagens pagas tem controle. |
| T10 | WhatsApp e sistema estao separados | Experiencia externa e interna nao se confundem. |
| T11 | Auditoria existe em acao critica | Alteracao sensivel deixa log. |
| T12 | Fluxo pode ser configurado | Tem variaveis configuraveis claras. |
| T13 | Custo e explicado por fluxo | Cada fluxo mostra se o custo vem de IA, WhatsApp service, utility, marketing, lote, midia ou historico. |
| T14 | Autonomo tem alcance | Cada fluxo autonomo define ate onde vai e o que acontece depois. |
| T15 | Campanha/reativacao e por fluxo | Cada fluxo de campanha, lote ou reativacao tem segmento, opt-out, limite e aprovador. |

## Resultado Da Auditoria Atual

Status: pronto para seguir para configuracao por fluxo.

Riscos residuais aceitos:

- Casos especificos de cada studio podem virar configuracao dentro de fluxo existente.
- Operacoes fora dos 7 agentes entram como agente sob medida.
- Regras legais/contratuais e clinicas sempre exigem humano.
- Automacoes em lote devem nascer em copiloto, mesmo quando tecnicamente poderiam ser automaticas.
