# Taliya Agent Flow Configuration Matrix

## Objetivo

Definir o que cada studio pode configurar em cada fluxo dos 7 agentes da Taliya.

A matriz segue a regra do produto:

- fluxos sao prontos;
- studio configura comportamento;
- guardrails sensiveis nao podem ser removidos;
- economia de creditos fica ativa por padrao.

## Campos Por Fluxo

Todo fluxo pode herdar ou sobrescrever:

- `ativo`: ligado/desligado.
- `modo_operacao`: manual, copiloto ou autonomo.
- `alcance_autonomo`: ate onde o agente vai quando roda sozinho.
- `depois_do_limite`: parar, criar tarefa, pedir aprovacao, chamar responsavel ou mover para outro fluxo.
- `tom`: direto, acolhedor, consultivo, formal, curto.
- `template`: mensagens aprovadas para cada etapa.
- `janela_envio`: dias/horarios permitidos.
- `limite_tentativas`: maximo de tentativas por contato/fluxo.
- `limite_creditos`: teto mensal ou por execucao.
- `custo_estimado`: baixo, medio, alto ou variavel.
- `origem_do_custo`: IA, WhatsApp service, WhatsApp utility, WhatsApp marketing, job em lote, midia ou historico.
- `prioridade_modo_economia`: essencial, media ou baixa.
- `responsavel`: pessoa/fila que recebe handoff.
- `aprovacao`: quando precisa aprovar antes de enviar/agir.
- `pausa`: opt-out, dado ausente, risco, limite ou baixa confianca.
- `transicoes`: proximos fluxos permitidos.
- `logs`: eventos que precisam ficar registrados.

## Limites Globais De Seguranca

Estas configuracoes nao substituem a decisao por fluxo. Elas funcionam como teto e protecao para todos os fluxos:

| Configuracao | Padrao Recomendado | Observacao |
| --- | --- | --- |
| Economia de creditos | ligada | Nao deve ser desligada no MVP. |
| Teto mensal de creditos | definido por plano/studio | Um fluxo nunca pode ultrapassar o teto global. |
| Modo economia | ativar em 70/90/100 | Fluxos de baixa prioridade pausam primeiro. |
| Horario geral de envio | horario comercial | Cada fluxo pode ter janela mais restrita. |
| Handoff de saude | humano | Nunca automatizar orientacao clinica. |
| Handoff financeiro critico | humano | Desconto, reembolso, cortesia, bloqueio e contestacao. |
| Opt-out | sempre respeitar | Bloqueia campanhas e mensagens nao essenciais. |
| Grupos WhatsApp | resposta limitada | Nao expor dados pessoais. |
| Baixa confianca | perguntar uma vez ou humano | Evita fluxo errado. |
| Dados conflitantes | pausar autonomia | Criar tarefa ou handoff. |

## Regras De Custo Por Fluxo

| Tipo de decisao | Regra |
| --- | --- |
| Manual | Menor custo. Taliya organiza, registra e cria tarefa; equipe executa. |
| Copiloto | Custo medio. Taliya usa IA para preparar acao/mensagem, mas espera aprovacao. |
| Autonomo | Custo variavel. Taliya executa sozinha; ao selecionar este modo, o studio define limites e ponto de parada. |
| WhatsApp pago | O custo aparece quando o modo permite iniciar conversa externa fora da janela aberta. |
| Utility | Usado para pendencias operacionais configuradas, como agenda e financeiro. |
| Marketing | Usado quando o fluxo envolve campanha, reativacao, promocao ou comunicacao comercial. |
| Campanha/lote | No MVP deve ficar em copiloto ou manual, com aprovacao antes de enviar. |
| Reativacao de inativos | Configurada nos fluxos de Retencao, com segmento, limite, aprovacao e opt-out. |
| Modo economia | Fluxos essenciais continuam; fluxos comerciais/baixa prioridade viram sugestao ou pausa. |

## Modos Exibidos Para O Studio

| Modo | Como explicar | Custo esperado |
| --- | --- | --- |
| Manual | Taliya mostra o que precisa ser feito e registra a decisao da equipe. | Baixo: sistema, regras e pouco uso de IA. |
| Copiloto | Taliya prepara mensagem, acao ou lista e pede aprovacao antes de executar. | Medio: usa IA e pode gerar custo se aprovado. |
| Autonomo | Taliya trabalha sozinha dentro das regras do fluxo. Ao selecionar, abre a configuracao de limites. | Variavel: depende de tentativas, WhatsApp, IA e etapas executadas. |

## 1. Atendimento

| Codigo | Fluxo | Modo padrao | Configuracoes do studio | Dados obrigatorios | Handoff/Economia |
| --- | --- | --- | --- | --- | --- |
| A1 | Nova Conversa | autonomo | saudacao, pergunta inicial, roteamento permitido, coleta minima | telefone, mensagem, status contato | saude/desconto/tom irritado vai para humano; classificar com IA leve |
| A2 | Duvidas Permitidas | autonomo | FAQs, respostas publicas, estilo curto/consultivo, avancar para venda/agenda | base publica, regras aprovadas | se resposta faltar cria tarefa; usar template antes de IA |
| A3 | Aluno Existente | autonomo | tipos de pedido aceitos, pergunta de desambiguacao, rotas permitidas | aluno identificado, status, mensagem | ambiguo pergunta uma vez; dado sensivel para humano |
| A4 | Fora Do Escopo | autonomo | resposta para fornecedor, parceria, vaga, spam | mensagem, classificacao | spam/prompt injection pausa; tarefa se for parceria |
| A5 | Handoff Humano | manual | responsavel, fila, resumo, SLA, resposta de espera | contato, motivo, historico recente | sempre registra resumo e pausa quando critico |
| A6 | Consentimento/Opt-Out | autonomo | preferencias, opt-out, horario de atendimento, resposta fora de horario | contato, consentimento, janela | respeitar opt-out; evitar campanha sem consentimento |
| A7 | Identidade/Midias | autonomo | transcrever audio, aceitar midias, vincular responsavel, revisao de duplicidade | contato, midia, tipo detectado | merge sempre humano; comprovante vai para financeiro |
| A8 | Privacidade/Dados | copiloto | dados que podem ser corrigidos, validacao de identidade, solicitacoes LGPD | contato, permissao, pedido | nao expor historico sensivel; humano quando dado pessoal critico |
| A9 | Grupos/Familiares | autonomo | resposta em grupo, responsaveis autorizados, limite de informacao | origem, autorizacao, aluno vinculado | nunca expor financeiro/saude sem permissao |
| A10 | Ciclo De Vida/SLA | autonomo | tempo aberto, cadencia, encerramento, SLA por tipo | conversa, estado atual, responsavel | conversa critica vencida vira tarefa prioritaria |

## 2. Agenda

| Codigo | Fluxo | Modo padrao | Configuracoes do studio | Dados obrigatorios | Handoff/Economia |
| --- | --- | --- | --- | --- | --- |
| B1 | Confirmacao De Presenca | autonomo | janela, mensagem, tentativas, turmas incluidas | agenda, aluno, aula, janela | uma tentativa por padrao; sem insistencia cara |
| B2 | Falta Com Aviso | autonomo | prazo, credito, liberar vaga, excecao | aula, aluno, regra reposicao, plano | fora da regra pede aprovacao; liberar vaga se permitido |
| B3 | No-Show | autonomo | quando registrar, mensagem leve, limite recorrencia | chamada, aula, aluno | recorrente vai para Retencao; primeira falta pode ser interna |
| B4 | Recuperar Vaga Aberta | autonomo | criterio candidato, lote/um por vez, limite convite | vaga, turma, candidatos, preferencias | lote exige aprovacao; evitar WhatsApp pago baixa prioridade |
| B5 | Reposicao/Remarcacao | autonomo | elegibilidade, validade, opcoes exibidas, max opcoes | credito, aluno, agenda, capacidade | pedido especial vai para humano |
| B6 | Lista De Espera | autonomo | prioridade, ordem, lote, validade do convite | lista, vaga, candidatos | sem candidato vai para Gestao |
| B7 | Disponibilidade Experimental | autonomo | tipos de turma, horarios permitidos, opcoes ofertadas | interessado, preferencia, grade, regra experimental | restricao/saude vai para humano |
| B8 | Mudanca Horario Fixo | autonomo | permitir sugestao, lista espera, impacto plano | aluno, horario atual, grade, plano | muda plano/frequencia vai para Financeiro |
| B9 | Cancelamento Pelo Studio | copiloto | mensagens em lote, compensacao, reposicao, aprovador | aula, alunos afetados, motivo | lote sempre aprovado; impacto vira tarefa |
| B10 | Conflito Capacidade | copiloto | regras de bloqueio, alerta, responsavel | sala, professor, capacidade, turma | bloquear reserva automatica com conflito |
| B11 | Ajuste De Grade | copiloto | quem pode alterar, impacto, avisos, simulacao | grade, professor, capacidade | mensagens so apos aprovacao |
| B12 | Experimental No-Show | autonomo | follow-up, remarcar, limite tentativas | interessado, aula, status | no-show recorrente encerra ou tarefa |
| B13 | Creditos Reposicao | autonomo | validade, aviso vencimento, acumulado, uso manual | credito, aluno, regra, validade | muitos creditos vai para Retencao/Gestao |
| B14 | Correcao Presenca | copiloto | quem corrige, auditoria, impacto em credito | aula, aluno, presenca, usuario | toda correcao registra auditoria |
| B15 | Primeira Aula | autonomo | boas-vindas, checklist, orientacoes, professor | aluno, horario, plano, status inicio | pendencia contrato/pagamento bloqueia ou tarefa |
| B16 | Aula Especial/Workshop | autonomo | publico, lote, pagamento, lista, limite | evento, vagas, publico, regra | comunicacao em lote exige aprovacao |

## 3. Vendas

| Codigo | Fluxo | Modo padrao | Configuracoes do studio | Dados obrigatorios | Handoff/Economia |
| --- | --- | --- | --- | --- | --- |
| C1 | Valores E Planos | autonomo | informar direto/faixa/qualificar, perguntas, CTA | planos, politica preco, contato | desconto/negociacao humano; usar politica antes de IA |
| C2 | Aula Experimental | autonomo | dados minimos, opcoes, mensagem confirmacao | interessado, disponibilidade, regra | saude/restricao humano |
| C3 | Lembrete Experimental | autonomo | janela, tentativas, mensagem | reserva, contato, horario | lembrete unico por padrao |
| C4 | Pos-Aula Experimental | autonomo | janela, tom, usar nota professor, CTA | comparecimento, interessado, plano | sem resposta vai para C5; excecao humano |
| C5 | Follow-Up Comercial | autonomo | cadencia, limite, motivo, encerramento | etapa CRM, ultima interacao | sem follow-up infinito; opt-out pausa |
| C6 | Pre-Matricula | copiloto | dados minimos, responsavel, checkout/manual | interessado, plano, horario | excecao comercial humano |
| C7 | Objecoes | autonomo | respostas aprovadas, follow-up, limites | objecao, politica, contato | desconto/negociacao humano |
| C8 | Origem/Qualificacao | autonomo | campos de origem, perguntas, score simples | contato, origem ou mensagem | atualizar CRM sem mensagem extra quando possivel |
| C9 | Perda Comercial | autonomo | motivos, encerramento, lembrete futuro | interessado, etapa, motivo | opt-out pausa; registra aprendizado |
| C10 | Indicacao | autonomo | beneficio indicacao, agradecimento, vinculo | indicado, indicador, politica | beneficio financeiro humano/Financeiro |
| C11 | Checkout/Abandono | autonomo | link, follow-up abandono, expiracao | checkout, interessado, plano | limitar cobranca/follow-up |
| C12 | Demanda Sem Vaga | autonomo | alternativas, lista comercial, aviso futuro | interesse, horario desejado, grade | gerar sinal para Gestao |
| C13 | Interessado Para Aluno | copiloto | checklist inicio, mensagem boas-vindas, responsavel | interessado, plano, horario, status | pausar follow-ups comerciais antigos |
| C14 | Upsell/Upgrade | copiloto | gatilhos, ofertas permitidas, responsavel | aluno, plano atual, interesse | nao empurrar sem aprovacao; excecao humano |

## 4. Financeiro

| Codigo | Fluxo | Modo padrao | Configuracoes do studio | Dados obrigatorios | Handoff/Economia |
| --- | --- | --- | --- | --- | --- |
| D1 | Lembrete Vencimento | autonomo | janela, mensagem, tentativas, agrupamento | aluno, plano, vencimento, status | agrupar lembretes; limitar WhatsApp |
| D2 | Pagamento Atrasado | autonomo | faixas atraso, limite, tom, aprovacao | aluno, vencimento, status, historico | acima do limite humano/tarefa |
| D3 | Pix/Link | autonomo | link fixo, gerar link, instrucoes Pix | aluno, plano, destino pagamento | nunca coletar cartao/senha |
| D4 | Confirmacao Pagamento | autonomo | webhook, comprovante, baixa manual, aviso | pagamento, aluno, plano | divergencia humano; idempotencia obrigatoria |
| D5 | Renovacao Plano | copiloto | renovar sozinho quando permitido ou sugerir, manter horario | plano, pagamento, agenda | mudanca de plano/frequencia pede revisao |
| D6 | Excecoes Financeiras | manual | responsavel, politica simples, SLA | aluno, plano, motivo | decisao financeira sempre humano |
| D7 | Falha Pagamento | autonomo | nova tentativa, novo link, aviso, limite | falha, aluno, plano | retry com limite; nao duplicar cobranca |
| D8 | Recibo/Nota | autonomo | documentos disponiveis, envio, responsavel | aluno, pagamento, documento | dado fiscal/sensivel pode exigir humano |
| D9 | Pausa/Trancamento | manual | politica, retorno previsto, impacto agenda | aluno, plano, motivo | sempre humano; conecta Retencao |
| D10 | Conciliacao Interna | copiloto | match sugerido, revisao, bloqueio mensagem | pagamento, aluno, valor | bloquear autonomia ate resolver |
| D11 | Contrato/Termos | copiloto | modelo, assinatura, lembrete, responsavel | contrato, aluno, plano | duvida juridica humano |
| D12 | Bloqueio/Liberacao | manual | criterio, aprovador, mensagem, impacto agenda | aluno, plano, status | nunca bloquear sozinho no MVP |
| D13 | Creditos/Cortesias | manual | tipos, validade, motivo, aprovador | aluno, beneficio, motivo | auditoria obrigatoria |
| D14 | Fechamento Mensal | autonomo | periodo, indicadores, destinatarios | pagamentos, planos, pendencias | resumo agregado, sem mensagem solta |

## 5. Retencao

| Codigo | Fluxo | Modo padrao | Configuracoes do studio | Dados obrigatorios | Handoff/Economia |
| --- | --- | --- | --- | --- | --- |
| E1 | Queda Frequencia | autonomo | limiares, pesos, acao por risco | presencas, plano, historico | alto risco tarefa; baixo risco monitorar |
| E2 | Aluno Inativo | autonomo | janelas, mensagem, aprovacao lote | aluno, ultima aula, status | evitar WhatsApp pago baixo impacto |
| E3 | Retorno | autonomo | horarios preferidos, tom, aviso professor | aluno, disponibilidade, contexto | dor/restricao humano/Historico |
| E4 | Risco Cancelamento | manual | responsavel, SLA, resumo, motivo | aluno, sinais, historico | sempre humano |
| E5 | Reativacao Ex-Aluno | copiloto | segmentos, lote, mensagem, limite | ex-aluno, motivo saida, consentimento | lote aprovado e limitado |
| E6 | Satisfacao | autonomo | pergunta, janela, escala, responsavel | aluno, evento, feedback | negativo vai para humano |
| E7 | Retorno Apos Pausa | autonomo | data retorno, lembrete, horario antigo | aluno, pausa, retorno previsto | se quer cancelar vai para E4 |
| E8 | Risco Por Perfil | autonomo | pesos, sinais, prioridade | frequencia, financeiro, agenda | interno antes de WhatsApp |
| E9 | Pos-Cancelamento | copiloto | mensagem final, feedback, reativacao futura | cancelamento, aluno, motivo | respeitar opt-out |
| E10 | Marco Engajamento | autonomo | marcos, mensagem, aprovacao, prioridade | aluno, marco, contexto | baixa prioridade; pausar perto do limite |
| E11 | Saude/Evento Pessoal | manual | responsavel, pausa automacoes, nota sensivel | aluno, evento, contexto | nunca usar comercialmente sem humano |
| E12 | Segmentacao Risco | copiloto | segmentos, lote, limite, aprovador | base alunos, sinais, consentimento | campanha/lote exige aprovacao |

## 6. Gestao

| Codigo | Fluxo | Modo padrao | Configuracoes do studio | Dados obrigatorios | Handoff/Economia |
| --- | --- | --- | --- | --- | --- |
| F1 | Prioridades Dia | autonomo | ranking, categorias, responsaveis | eventos, tarefas, agentes | resumo agregado |
| F2 | Dinheiro Na Mesa | autonomo | calculos, pesos, exibicao, periodo | agenda, vendas, financeiro, retencao | sem prometer valor garantido |
| F3 | Fila Humana | autonomo | filas, SLA, responsaveis, prioridade | handoffs, aprovacoes, tarefas | vencido vira prioridade |
| F4 | Gargalos | copiloto | thresholds, sugestoes, responsavel | historico, padroes, metricas | recomendacao antes de acao |
| F5 | Resumo Semanal | autonomo | destinatario, dia, canais, secoes | logs, tarefas, metricas | uma notificacao agregada |
| F6 | Qualidade Dados | autonomo | checklist, obrigatorios, bloqueios | setup, dados base | bloqueia fluxo dependente |
| F7 | Creditos/Limites | autonomo | alertas, modo economia, compra extra | uso, plano, limite | ativa economia em 70/90/100 |
| F8 | Performance | autonomo | indicadores, periodo, responsaveis | flow runs, tarefas, handoffs | sem mensagens externas |
| F9 | Permissoes/Auditoria | autonomo | papeis, logs, avisos criticos | usuario, acao, permissao | bloquear sem permissao |
| F10 | Capacidade/Crescimento | copiloto | demanda, lista, ocupacao, sugestoes | grade, ocupacao, vendas | sugestao, nao mudanca automatica |
| F11 | Falhas/Webhooks | autonomo | retry, alerta, pausa, responsavel | eventos integracao, idempotencia | retry seguro; evitar duplicidade |
| F12 | Importacao/Migracao | copiloto | checklist, merges, validacao, bloqueios | dados importados, origem | bloquear autonomia ate dado minimo |
| F13 | Teste De Fluxo | copiloto | simulacoes, gates, aprovador | config fluxo, dados teste | fluxo falho fica inativo |

## 7. Historico/Evolucao

| Codigo | Fluxo | Modo padrao | Configuracoes do studio | Dados obrigatorios | Handoff/Economia |
| --- | --- | --- | --- | --- | --- |
| G1 | Contexto Antes Aula | autonomo | resumo, campos, destaque, visibilidade | aluno, aula, historico | interno; sem WhatsApp externo |
| G2 | Observacao Pos-Aula | autonomo | campos, voz/texto, lembrete, professor | aluno, aula, nota | resumo incremental |
| G3 | Restricao/Cuidado | copiloto | tipos, visibilidade, alerta professor | aluno, restricao, permissao | humano para orientacao clinica |
| G4 | Objetivo/Evolucao | autonomo | periodo revisao, campos, lembrete | aluno, objetivo, notas | interno; baixa prioridade |
| G5 | Contexto Para Agente | autonomo | quais agentes podem consultar, filtros | aluno, solicitante, permissao | sensivel retorna handoff |
| G6 | Documentos/Anamnese | copiloto | tipos, permissao, armazenamento | aluno, documento, tipo | nao usar em mensagem externa automatica |
| G7 | Correcao Historico | copiloto | quem corrige, auditoria, confirmacao | aluno, registro, usuario | auditoria obrigatoria |
| G8 | Handoff Professores | autonomo | formato resumo, leitura obrigatoria | aluno, professor, contexto | tarefa se cuidado importante |
| G9 | Lembrete Professor | autonomo | quando lembrar, campos, prioridade | aula, professor, alunos | pular se baixa prioridade |
| G10 | Compartilhar Contexto | copiloto | dados compartilhaveis, aprovador | aluno, pedido, permissao | clinico/sensivel humano |
| G11 | Permissao Historico | autonomo | papeis, campos, logs, bloqueios | usuario, papel, aluno | bloquear sem permissao |
| G12 | Linha Do Tempo | autonomo | eventos, filtros, resumos, visibilidade | eventos aluno, permissao | detectar conflitos e criar tarefa |

## Padroes De Configuracao Por Plano

| Plano | Configuracao recomendada |
| --- | --- |
| 0 agentes | fluxos ficam inativos; sistema registra dados e tarefas manuais. |
| 1 agente | ativar apenas fluxos do agente contratado e dependencias minimas em copiloto. |
| 3 agentes | ativar rotinas conectadas entre os agentes inclusos; transicoes para agentes bloqueados viram tarefa. |
| 7 agentes | ativar transicoes completas, mantendo financeiro critico, saude e lotes em humano/copiloto. |

## Regras Para Agente Bloqueado Por Plano

Quando um fluxo precisa de um agente nao contratado:

- criar tarefa interna;
- mostrar upsell se fizer sentido;
- nunca simular que o agente bloqueado esta trabalhando;
- manter registro do evento para demonstrar oportunidade.

