# Taliya CRM - Pacotes E Mini Cards De Agentes/Fluxos

Status: contrato funcional v0.2.
Data: 2026-05-21.

## Nota De Atualizacao

Este documento registra a matriz original de pacotes e mini cards.

Na UI final, o termo user-facing e "rotina", nao "pacote". A definicao final de paginas, rotinas, fluxos e ajustes permitidos esta em:

- `agents-flows-routines-pages-final-contract.pt-BR.md`

Onde houver conflito, vale a decisao mais recente:

- agente nao configura;
- rotina organiza;
- fluxo configura;
- canal, integracao, permissao, dado e cota sao dependencias fixas;
- tom de voz e template ficam no fluxo.

## Objetivo

Complementar `agents-flows-functional-architecture.pt-BR.md` com:

- pacotes recomendados por agente;
- modo default por pacote;
- modo default dos 96 fluxos fortes;
- quais fluxos podem ser autonomos no MVP;
- fallback default;
- prioridade de economia;
- preflight minimo por tipo de fluxo.

Este documento ainda nao e implementacao tecnica. Ele e uma decisao de produto para evitar que o dono/admin precise configurar dezenas de fluxos manualmente.

## Regras De Leitura

Modos:

- `M`: Manual.
- `C`: Copiloto.
- `A`: Autonomo.

Autonomia MVP:

- `sim`: pode ser autonomo no MVP se passar preflight.
- `condicional`: pode ser autonomo apenas em casos estreitos, baixo risco e com limites fortes.
- `nao`: nao deve ser autonomo no MVP.

Economia:

- `essencial`: tenta preservar ate 100%, se plano/cota/canal permitir.
- `media`: em 90% pode virar aprovacao ou tarefa.
- `baixa`: em 90% vira tarefa/aprovacao; em 100% para.

Todo fluxo, mesmo quando default e `A`, precisa poder degradar para `C` ou `M` quando plano, cota, canal, dado, risco ou integracao bloquear.

## Pacotes Recomendados

### Atendimento

| Pacote | Fluxos | Modo default | Quando usar |
|---|---|---|---|
| Atendimento essencial | A1, A2, A3, A4, A5, A10 | C com autonomia estreita | Para organizar inbox, respostas permitidas e chamada humana. |
| Identidade e permissao de contato | A6, A7, A8, A9 | C/M | Para proteger opt-out, privacidade, midias e telefone compartilhado. |

### Agenda

| Pacote | Fluxos | Modo default | Quando usar |
|---|---|---|---|
| Presenca e faltas | B1, B2, B3, B14 | A/C | Para confirmar presenca, tratar falta e proteger correcao humana. |
| Reposicoes e vagas | B4, B5, B6, B13 | A/C | Para organizar reposicoes, lista de espera e creditos. |
| Agenda estrutural | B8, B9, B10, B11, B16 | C/M | Para mudancas de grade, turma, conflito e evento. |
| Experimental com agenda | B7, B12, B15 | A/C | Para apoiar aula experimental e primeira aula sem automatizar conversao sensivel. |

### Vendas

| Pacote | Fluxos | Modo default | Quando usar |
|---|---|---|---|
| Captura e qualificacao | C15, C8, C9, C10 | C | Para entrada multicanal, origem, indicacao e perda comercial. |
| Experimental e acompanhamento | C2, C3, C4, C5, C12 | A/C | Para lembretes e follow-up comercial seguro. |
| Conversao e matricula | C1, C6, C7, C11, C13, C14 | C/M | Para preco, objecoes, pre-matricula, checkout e upgrade com humano no controle. |

### Financeiro

| Pacote | Fluxos | Modo default | Quando usar |
|---|---|---|---|
| Lembretes financeiros seguros | D1, D2, D3, D7, D8, D10 | A/C | Para cobrancas simples, link, falha e conciliacao com revisao quando necessario. |
| Ciclo de plano do aluno | D5, D9, D15 | C/M | Para renovacao, pausa, trancamento e encerramento/alteracao efetiva. |
| Excecoes financeiras sensiveis | D4, D6, D11, D12, D13, D14 | C/M | Para confirmacao, contrato, bloqueio, cortesia, fechamento e auditoria. |

### Retencao

| Pacote | Fluxos | Modo default | Quando usar |
|---|---|---|---|
| Retencao preventiva | E1, E2, E3, E6, E7, E8, E10, E12 | A/C | Para sinais de risco, satisfacao preventiva, retorno e segmentacao. |
| Casos sensiveis | E4, E5, E9, E11, E13 | C/M | Para cancelamento, reclamacao, saude/evento pessoal e recuperacao de confianca. |

### Gestao/Governanca

| Pacote | Fluxos | Modo default | Quando usar |
|---|---|---|---|
| Comando operacional | F1, F2, F3, F4, F5, F6, F10 | C | Para prioridade, dinheiro, filas, gargalos, resumo e qualidade de dados. |
| Governanca de agentes | F7, F8, F9, F13, F14, F15 | C/M | Para cota, performance, auditoria, teste, incidente e mudanca de politica. |
| Integracoes e importacao | F11, F12 | C/M | Para explicar falhas, logs, importacao e migracao sem virar painel tecnico. |

### Historico/Professor

| Pacote | Fluxos | Modo default | Quando usar |
|---|---|---|---|
| Aula com contexto | G1, G2, G4, G8, G9, G12 | C com lembretes autonomos | Para professor, nota, evolucao, repasse entre professores e linha do tempo permitida. |
| Historico protegido | G3, G5, G6, G7, G10, G11 | C/M | Para restricao, documentos, permissao, correcao e compartilhamento seguro. |

## Preflight Por Tipo De Fluxo

| Tipo | Preflight minimo |
|---|---|
| Mensagem externa individual | plano, agente, modo, canal, template/janela, consentimento, opt-out, cota, risco, fallback e auditoria. |
| Mensagem externa em lote | tudo de mensagem individual + publico valido, limite de tentativas, aprovacao e estimativa total de custo. |
| Tarefa/caso interno | permissao, dono/fila, objeto origem, prazo, risco e auditoria quando sensivel. |
| Mudanca de agenda | permissao, capacidade, conflito, politica vigente, alunos afetados, comunicacao e auditoria. |
| Mudanca financeira | permissao financeira, evidencia, impacto, aprovacao, politica vigente e auditoria. |
| Historico sensivel | permissao contextual, dado minimo, visibilidade, resumo seguro e auditoria. |
| Integracao/reprocessamento | status do provedor, idempotencia, impacto conhecido, retry seguro e log. |
| Cota/economia | entitlement, saldo, prioridade do fluxo, limite por tentativa, limite mensal e fallback. |

## Mini Cards Dos 96 Fluxos

### Atendimento - 10

| ID | Fluxo | Pacote | Modo | Auto MVP | Gatilho | Dados/canal | Fallback | Economia |
|---|---|---|---|---|---|---|---|---|
| A1 | Nova Conversa | Atendimento essencial | C | condicional | mensagem recebida | contato, conversa, WhatsApp | tarefa/chamada humana | essencial |
| A2 | Duvidas Permitidas | Atendimento essencial | A | sim | pergunta com resposta aprovada | base permitida, canal valido | tarefa de resposta | media |
| A3 | Aluno Existente | Atendimento essencial | C | condicional | pedido de aluno identificado | aluno, conversa, permissao | chamada humana | essencial |
| A4 | Fora Do Escopo | Atendimento essencial | A | condicional | intencao nao atendida | conversa, politica de escopo | tarefa/caso | media |
| A5 | Chamada Humana | Atendimento essencial | A | sim | risco, baixa confianca ou pedido humano | fila, responsavel, resumo | caso operacional | essencial |
| A6 | Consentimento/Opt-Out | Identidade e permissao de contato | A | sim | frase de opt-out/preferencia | contato, canal | bloquear envio e auditar | essencial |
| A7 | Identidade/Midias | Identidade e permissao de contato | C | nao | midia, audio, documento ou identidade incerta | contato, midia, permissao | tarefa de revisao | media |
| A8 | Privacidade/Dados | Identidade e permissao de contato | M | nao | pedido de dados/LGPD | contato, caso, permissao | caso sensivel | essencial |
| A9 | Telefone Compartilhado E Identidade | Identidade e permissao de contato | C | nao | telefone/grupo ambiguo | contato, aluno, conversa | validar identidade | essencial |
| A10 | Ciclo De Vida/SLA | Atendimento essencial | A | condicional | conversa parada ou SLA | conversa, responsavel | tarefa/chamada humana | media |

### Agenda - 16

| ID | Fluxo | Pacote | Modo | Auto MVP | Gatilho | Dados/canal | Fallback | Economia |
|---|---|---|---|---|---|---|---|---|
| B1 | Confirmacao De Presenca | Presenca e faltas | A | sim | janela antes da aula | aula, aluno, WhatsApp | tarefa de confirmacao | essencial |
| B2 | Falta Com Aviso | Presenca e faltas | C | condicional | aviso de falta | aula, credito, politica | tarefa/reposicao manual | essencial |
| B3 | No-Show | Presenca e faltas | C | condicional | falta registrada | chamada, aluno, risco | tarefa de retencao | media |
| B4 | Recuperar Vaga Aberta | Reposicoes e vagas | A | condicional | vaga aberta | aula, lista, consentimento | aprovacao/tarefa | media |
| B5 | Reposicao/Remarcacao | Reposicoes e vagas | C | condicional | pedido de reposicao | credito, agenda, regra | tarefa manual | essencial |
| B6 | Lista De Espera | Reposicoes e vagas | A | condicional | vaga compativel | waitlist, aula, canal | tarefa/aprovacao | media |
| B7 | Disponibilidade Experimental | Experimental com agenda | C | condicional | pedido de experimental | interessado, agenda | tarefa de agendar | media |
| B8 | Mudanca Horario Fixo | Agenda estrutural | C | nao | solicitacao de troca | aluno, turma, impacto | aprovacao | essencial |
| B9 | Cancelamento Pelo Studio | Agenda estrutural | C | nao | aula cancelada pelo studio | aula, alunos, canal | aprovacao/comunicado | essencial |
| B10 | Conflito Capacidade | Agenda estrutural | C | nao | conflito detectado | turma, capacidade | caso operacional | essencial |
| B11 | Ajuste De Grade | Agenda estrutural | C | nao | mudanca de grade | grade, turmas, impacto | simulacao/aprovacao | essencial |
| B12 | Experimental No-Show | Experimental com agenda | A | condicional | no-show experimental | interessado, aula | tarefa comercial | media |
| B13 | Creditos Reposicao | Reposicoes e vagas | C | condicional | credito criado/usado/vencendo | credito, aluno | tarefa/manual | essencial |
| B14 | Correcao Presenca | Presenca e faltas | M | nao | correcao humana | chamada, auditoria | aprovacao | essencial |
| B15 | Primeira Aula | Experimental com agenda | C | condicional | aluno novo com primeira aula | aluno, aula, plano | checklist/tarefa | media |
| B16 | Aula Especial/Workshop | Agenda estrutural | C | nao | evento/workshop | evento, capacidade, pagamento | aprovacao/tarefa | baixa |

### Vendas - 15

| ID | Fluxo | Pacote | Modo | Auto MVP | Gatilho | Dados/canal | Fallback | Economia |
|---|---|---|---|---|---|---|---|---|
| C1 | Valores E Planos | Conversao e matricula | C | condicional | pergunta sobre preco/plano | plano, interessado, conversa | rascunho humano | media |
| C2 | Aula Experimental | Experimental e acompanhamento | C | condicional | interesse em experimental | interessado, agenda | tarefa de agendamento | media |
| C3 | Lembrete Experimental | Experimental e acompanhamento | A | sim | janela antes da experimental | aula, interessado, WhatsApp | tarefa manual | media |
| C4 | Pos-Aula Experimental | Experimental e acompanhamento | A | condicional | aula experimental concluida | interessado, aula, professor | tarefa comercial | media |
| C5 | Follow-Up Comercial | Experimental e acompanhamento | A | condicional | oportunidade parada | interessado, consentimento | tarefa/aprovacao | baixa |
| C6 | Pre-Matricula | Conversao e matricula | C | nao | interessado pronto para matricula | interessado, checklist | aprovacao/tarefa | essencial |
| C7 | Objecoes | Conversao e matricula | C | nao | objecao comercial | conversa, template | aprovacao | media |
| C8 | Origem/Qualificacao | Captura e qualificacao | C | condicional | lead novo/atualizado | interessado, origem | tarefa de qualificar | media |
| C9 | Perda Comercial | Captura e qualificacao | C | nao | oportunidade perdida | motivo, interessado | registro manual | baixa |
| C10 | Indicacao | Captura e qualificacao | C | nao | indicacao recebida | aluno, interessado | tarefa de revisao | baixa |
| C11 | Checkout/Abandono | Conversao e matricula | C | condicional | checkout abandonado | interessado, pagamento | tarefa/aprovacao | baixa |
| C12 | Demanda Sem Vaga | Experimental e acompanhamento | C | condicional | horario desejado indisponivel | interessado, waitlist | tarefa/lista espera | media |
| C13 | Interessado Para Aluno | Conversao e matricula | C | nao | decisao de matricula | interessado, plano, agenda | pre-matricula manual | essencial |
| C14 | Upsell/Upgrade | Conversao e matricula | C | nao | oportunidade de upgrade | aluno, plano, financeiro | aprovacao | baixa |
| C15 | Entrada Multicanal De Lead | Captura e qualificacao | C | condicional | lead de site/social/manual/importacao | interessado, contato, origem | tarefa de triagem | media |

### Financeiro - 15

| ID | Fluxo | Pacote | Modo | Auto MVP | Gatilho | Dados/canal | Fallback | Economia |
|---|---|---|---|---|---|---|---|---|
| D1 | Lembrete Vencimento | Lembretes financeiros seguros | A | sim | vencimento proximo | pagamento, aluno, canal | tarefa cobranca | essencial |
| D2 | Pagamento Atrasado | Lembretes financeiros seguros | C | condicional | atraso detectado | pagamento, historico | aprovacao/tarefa | essencial |
| D3 | Pix/Link | Lembretes financeiros seguros | C | condicional | pedido/envio de link | pagamento, provedor/canal | tarefa manual | essencial |
| D4 | Confirmacao Pagamento | Excecoes financeiras sensiveis | C | condicional | webhook ou comprovante | pagamento, evidencia | analise/aprovacao | essencial |
| D5 | Renovacao Plano | Ciclo de plano do aluno | C | nao | plano perto do fim | plano aluno, financeiro | aprovacao/tarefa | media |
| D6 | Excecoes Financeiras | Excecoes financeiras sensiveis | M | nao | desconto/acordo/cortesia | excecao, permissao | caso/aprovacao | essencial |
| D7 | Falha Pagamento | Lembretes financeiros seguros | C | condicional | falha do pagamento | pagamento, provedor | tarefa/caso | essencial |
| D8 | Recibo/Nota | Lembretes financeiros seguros | C | condicional | pedido de documento | documento, pagamento | tarefa manual | media |
| D9 | Pausa/Trancamento | Ciclo de plano do aluno | C | nao | pedido de pausa | aluno, plano, agenda | caso/aprovacao | essencial |
| D10 | Conciliacao Interna | Lembretes financeiros seguros | C | nao | pagamento sem match | pagamento, candidatos | tarefa financeira | essencial |
| D11 | Contrato/Termos | Excecoes financeiras sensiveis | C | nao | contrato pendente | contrato, aluno | tarefa/aprovacao | media |
| D12 | Bloqueio/Liberacao | Excecoes financeiras sensiveis | M | nao | criterio financeiro | aluno, financeiro | aprovacao | essencial |
| D13 | Creditos/Cortesias | Excecoes financeiras sensiveis | M | nao | credito/cortesia | credito, motivo | aprovacao | essencial |
| D14 | Fechamento Mensal | Excecoes financeiras sensiveis | C | nao | fim de periodo | pagamentos, relatorio | relatorio/manual | media |
| D15 | Encerramento Ou Alteracao Efetiva De Plano | Ciclo de plano do aluno | C | nao | mudanca/encerramento | plano aluno, cobranca, agenda | caso/aprovacao | essencial |

### Retencao - 13

| ID | Fluxo | Pacote | Modo | Auto MVP | Gatilho | Dados/canal | Fallback | Economia |
|---|---|---|---|---|---|---|---|---|
| E1 | Queda Frequencia | Retencao preventiva | C | condicional | queda detectada | presenca, aluno | tarefa contato | media |
| E2 | Aluno Inativo | Retencao preventiva | A | condicional | inatividade | aluno, consentimento | tarefa/aprovacao | baixa |
| E3 | Retorno | Retencao preventiva | C | condicional | aluno quer voltar | aluno, agenda | tarefa/agendamento | media |
| E4 | Risco Cancelamento | Casos sensiveis | C | nao | sinal de cancelamento | aluno, caso | caso humano | essencial |
| E5 | Reativacao Ex-Aluno | Casos sensiveis | C | nao | segmento elegivel | ex-aluno, consentimento | aprovacao | baixa |
| E6 | Satisfacao | Retencao preventiva | A | condicional | janela de satisfacao | aluno, canal | tarefa | baixa |
| E7 | Retorno Apos Pausa | Retencao preventiva | C | condicional | pausa perto do fim | aluno, agenda, financeiro | tarefa | media |
| E8 | Risco Por Perfil | Retencao preventiva | C | nao | score/regra | sinais, aluno | tarefa | media |
| E9 | Pos-Cancelamento | Casos sensiveis | C | nao | cancelamento concluido | aluno, financeiro | caso/tarefa | media |
| E10 | Marco Engajamento | Retencao preventiva | A | condicional | marco detectado | historico, aluno | tarefa | baixa |
| E11 | Saude/Evento Pessoal | Casos sensiveis | M | nao | evento sensivel | historico, aluno | caso humano | essencial |
| E12 | Segmentacao Risco | Retencao preventiva | C | nao | segmentacao | risco, relatorio | aprovacao | media |
| E13 | Reclamacao E Recuperacao De Confianca | Casos sensiveis | C | nao | reclamacao | caso, conversa, severidade | pausar automacao/caso | essencial |

### Gestao/Governanca - 15

| ID | Fluxo | Pacote | Modo | Auto MVP | Gatilho | Dados/canal | Fallback | Economia |
|---|---|---|---|---|---|---|---|---|
| F1 | Prioridades Dia | Comando operacional | C | condicional | inicio do dia | tarefas, agenda, financeiro | lista manual | essencial |
| F2 | Dinheiro Na Mesa | Comando operacional | C | nao | abertura de relatorio | metricas CRM | relatorio manual | media |
| F3 | Fila Humana | Comando operacional | C | condicional | aprovacoes/chamadas humanas | tarefas, aprovacao | fila manual | essencial |
| F4 | Gargalos | Comando operacional | C | nao | padrao recorrente | relatorios, casos | tarefa analise | media |
| F5 | Resumo Semanal | Comando operacional | C | condicional | fim de semana | dados do periodo | relatorio manual | baixa |
| F6 | Qualidade Dados | Comando operacional | C | condicional | dado faltante/conflito | problemas de dados | tarefa correcao | essencial |
| F7 | Creditos/Limites | Governanca de agentes | A | condicional | cota 70/90/100 | uso, cota, plano | economia/manual | essencial |
| F8 | Performance | Governanca de agentes | C | nao | revisao de agentes | execucoes, qualidade | relatorio manual | media |
| F9 | Permissoes/Auditoria | Governanca de agentes | M | nao | evento sensivel | auditoria, permissao | revisao humana | essencial |
| F10 | Capacidade/Crescimento | Comando operacional | C | nao | analise de ocupacao | agenda, turmas | relatorio/tarefa | media |
| F11 | Falhas/Webhooks | Integracoes e importacao | C | condicional | log/falha | integracao, log | incidente/tarefa | essencial |
| F12 | Importacao/Migracao | Integracoes e importacao | C | nao | importacao/job | job, dados | revisao manual | media |
| F13 | Teste De Fluxo | Governanca de agentes | C | nao | usuario simula | config, exemplos | bloquear publicacao | essencial |
| F14 | Incidente De Automacao E Correcao Operacional | Governanca de agentes | C | nao | falha/resultado errado | run, objetos afetados | incidente/pausa | essencial |
| F15 | Mudanca De Politica Ou Regra Operacional | Governanca de agentes | C | nao | alteracao de regra | politica, impacto | simulacao/aprovacao | essencial |

### Historico/Evolucao - 12

| ID | Fluxo | Pacote | Modo | Auto MVP | Gatilho | Dados/canal | Fallback | Economia |
|---|---|---|---|---|---|---|---|---|
| G1 | Contexto Antes Aula | Aula com contexto | C | condicional | aula proxima | aula, aluno, permissao | resumo manual | media |
| G2 | Observacao Pos-Aula | Aula com contexto | C | condicional | aula finalizada | professor, aluno | tarefa nota | media |
| G3 | Restricao/Cuidado | Historico protegido | M | nao | restricao/evento sensivel | historico, permissao | caso humano | essencial |
| G4 | Objetivo/Evolucao | Aula com contexto | C | nao | revisao de aluno | historico, objetivo | tarefa revisao | baixa |
| G5 | Contexto Para Agente | Historico protegido | C | nao | agente precisa contexto | resumo permitido | bloquear contexto | essencial |
| G6 | Documentos/Anamnese | Historico protegido | C | nao | documento enviado/faltante | documento, permissao | aprovacao/tarefa | essencial |
| G7 | Correcao Historico | Historico protegido | M | nao | correcao solicitada | evento, auditoria | caso/aprovacao | essencial |
| G8 | Repasse Entre Professores | Aula com contexto | C | condicional | troca de professor/turma | professor, aluno | tarefa manual | media |
| G9 | Lembrete Professor | Aula com contexto | A | condicional | nota pendente | professor, aula | tarefa interna | baixa |
| G10 | Compartilhar Contexto | Historico protegido | C | nao | pedido de compartilhar | historico, aprovacao | bloquear/aprovacao | essencial |
| G11 | Permissao Historico | Historico protegido | M | nao | ajuste de visibilidade | permissao, papel | aprovacao | essencial |
| G12 | Linha Do Tempo | Aula com contexto | C | nao | consulta de perfil | eventos historico | visualizacao manual | media |

## Fluxos Nao Standalone No MVP

| ID | Decisao |
|---|---|
| E14 Primeira Semana Do Novo Aluno | Fica como checklist/subfluxo de B15, E6, E10 e tarefas de retencao ate provar configuracao independente. |
| G13 Gate De Anamnese, Consentimento E Contato De Emergencia | Fica como gate de G6, G3, B15 e qualidade de dados ate provar configuracao independente. |

## Autonomia Permitida No MVP

Autonomia deve comecar apenas por familias de baixo risco:

- resposta de FAQ permitida;
- opt-out/preferencia detectavel;
- chamada humana automatica por risco/baixa confianca;
- confirmacao de presenca;
- lembrete de aula experimental;
- lembrete de vencimento simples;
- lembrete interno para professor;
- alertas de cota/economia;
- criacao de tarefa por SLA, dado faltante ou fila.

Autonomia condicional deve sempre ter limites:

- maximo de tentativas por contato;
- janela de envio;
- template aprovado quando exigido;
- sem dado sensivel bruto;
- sem alteracao financeira sensivel;
- sem decisao de cancelamento;
- sem envio para opt-out;
- cota disponivel;
- fallback manual.

## Default De Limites Por Pacote

| Pacote | Limite default |
|---|---|
| Atendimento essencial | ate 2 respostas automaticas seguras por conversa antes de chamar humano; chamada humana imediata em risco. |
| Identidade e permissao de contato | nenhuma mescla autonoma; opt-out autonomo permitido. |
| Presenca e faltas | 1 lembrete por aula/aluno; sem insistencia. |
| Reposicoes e vagas | ate 1 convite por vaga para lista priorizada; ampliar exige aprovacao. |
| Agenda estrutural | sem autonomia para mudanca ampla; sempre simular impacto. |
| Experimental e acompanhamento | ate 2 toques por interessado no ciclo da experimental. |
| Captura e qualificacao | pode criar lead/pendencia; baixa confianca vira revisao. |
| Conversao e matricula | sem conversao autonoma; humano confirma matricula. |
| Lembretes financeiros seguros | ate 2 lembretes por cobranca antes de tarefa/aprovacao. |
| Ciclo de plano do aluno | sem autonomia para encerramento, pausa ou mudanca efetiva. |
| Excecoes financeiras sensiveis | sempre humano. |
| Retencao preventiva | ate 1 check-in automatico baixo risco; campanha/lote exige aprovacao. |
| Casos sensiveis | sempre copiloto/manual. |
| Comando operacional | pode priorizar e criar tarefa; nao decide acao sensivel. |
| Governanca de agentes | pode alertar/pausar por regra critica; mudanca permanente exige humano. |
| Integracoes e importacao | pode explicar e criar tarefa/incidente; nao reconecta nem reprocessa sensivel sozinho. |
| Aula com contexto | pode lembrar professor; resumo sensivel respeita permissao. |
| Historico protegido | sem autonomia para criar/compartilhar dado sensivel. |

## Criterios De Publicacao Por Pacote

Um pacote pode ser publicado quando:

- todos os fluxos do pacote estao classificados como `publicavel`, `publicavel_com_aviso` ou `pendente_nao_bloqueante`;
- fluxos bloqueados ficam fora da publicacao e viram pendencia;
- o usuario ve o que fica manual, copiloto e autonomo;
- cota estimada mensal do pacote aparece antes da confirmacao;
- integracoes exigidas estao ok ou os fluxos dependentes ficam pausados;
- fallback esta definido em todos os fluxos;
- auditoria registra pacote, fluxos, versao, aprovador e simulacao.

## Criterios De Aceite

Este documento esta correto quando:

- lista os 96 fluxos fortes;
- nao promove E14/G13 a standalone no MVP;
- define pacotes por agente;
- define modo default e autonomia MVP por fluxo;
- preserva caminho manual em todos os casos;
- deixa acoes sensiveis em copiloto/manual;
- mantem Billing, Integracoes, Uso/Cotas e Control Planes fora do builder;
- reduz complexidade para o dono/admin sem esconder risco, cota, fallback ou auditoria.
