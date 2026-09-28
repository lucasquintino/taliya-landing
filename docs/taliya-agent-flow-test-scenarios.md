# Taliya Agent Flow Test Scenarios

## Objetivo

Validar se o mapa e a matriz de configuracao dos agentes cobrem operacao real do studio antes de desenhar telas ou implementar runtime.

Cada fluxo deve ser testado com pelo menos:

- sucesso;
- falta de dado;
- excecao/risco;
- economia de creditos quando aplicavel;
- transicao para outro fluxo quando aplicavel.

## Como Usar

Para cada cenario:

1. Simular entrada.
2. Verificar agente dono.
3. Verificar canal correto.
4. Verificar dados usados.
5. Verificar acao esperada.
6. Verificar estado final.
7. Verificar logs/auditoria.

## 1. Atendimento

| ID | Fluxo | Entrada | Esperado |
| --- | --- | --- | --- |
| A1-S1 | Nova Conversa | "Oi, queria saber valores e horarios" | classificar, responder minimo permitido e transicionar para Vendas C1/Agenda B7 conforme politica. |
| A1-E1 | Nova Conversa | "Sinto dor, que exercicio faco?" | nao orientar; handoff humano + Historico G3 se aluno identificado. |
| A2-S1 | Duvidas Permitidas | "Qual endereco?" | responder por template/base publica e registrar. |
| A2-M1 | Duvidas Permitidas | "Tem estacionamento?" sem dado configurado | criar tarefa para completar base e responder que equipe confirma. |
| A3-S1 | Aluno Existente | "Nao vou conseguir ir hoje" | perguntar aula se ambiguo ou enviar para Agenda B2 se contexto claro. |
| A3-E1 | Aluno Existente | "Quero cancelar" | Retencao E4 + Financeiro D6 + humano. |
| A4-S1 | Fora Do Escopo | fornecedor oferece parceria | resposta padrao ou tarefa interna. |
| A4-E1 | Fora Do Escopo | tentativa de mudar instrucao interna do agente | bloquear, registrar e seguir resposta segura. |
| A5-S1 | Handoff | "Quero falar com alguem" | resumir conversa, avisar responsavel e pausar se necessario. |
| A6-S1 | Opt-Out | "Nao quero mais receber mensagens" | registrar opt-out e pausar campanhas. |
| A7-S1 | Midias | aluno envia comprovante | classificar midia e enviar para Financeiro D4. |
| A7-E1 | Duplicidade | telefone parece dois alunos | nao vincular automaticamente; pedir identificador ou tarefa. |
| A8-S1 | Privacidade | aluno pede atualizar telefone | validar identidade e registrar/tarefa. |
| A8-E1 | Privacidade | familiar pede dados financeiros do aluno sem autorizacao | nao expor; validar permissao ou humano. |
| A9-S1 | Grupo | pergunta em grupo sobre horario geral | responder sem dados pessoais ou direcionar individual. |
| A10-S1 | SLA | interessado quente ficou sem resposta | criar prioridade/Vendas C5. |

## 2. Agenda

| ID | Fluxo | Entrada | Esperado |
| --- | --- | --- | --- |
| B1-S1 | Confirmacao | aluno confirma aula | marcar previsto e registrar. |
| B1-M1 | Confirmacao | sem resposta | lembrar uma vez ou encerrar conforme config. |
| B2-S1 | Falta Com Aviso | aluno avisa falta dentro do prazo | registrar falta, criar credito se regra permite, B4 se vaga liberavel. |
| B2-E1 | Falta Com Aviso | aluno pede excecao fora do prazo | handoff/aprovacao. |
| B3-S1 | No-Show | professor marca falta | registrar; se recorrente E1. |
| B4-S1 | Recuperar Vaga | vaga abre e ha candidato | convidar conforme politica e reservar se aceitar. |
| B4-C1 | Recuperar Vaga | credito perto do limite e vaga baixa prioridade | nao abrir conversa paga; criar tarefa/sem acao. |
| B5-S1 | Reposicao | aluno tem credito e quer horario | oferecer opcoes e reservar. |
| B5-M1 | Reposicao | credito inexistente | explicar regra ou pedir aprovacao. |
| B6-S1 | Lista Espera | vaga abre em horario cheio | priorizar candidato e convidar. |
| B7-S1 | Experimental | interessado quer depois das 18h | buscar opcoes e retornar para Vendas C2. |
| B8-S1 | Mudanca Horario | aluno quer mudar fixo | buscar vaga; se muda plano, Financeiro D5. |
| B9-S1 | Cancelamento Studio | professor ausente | listar afetados, sugerir comunicacao, exigir aprovacao para lote. |
| B10-E1 | Conflito | turma acima da capacidade | bloquear reserva automatica e criar tarefa. |
| B11-S1 | Ajuste Grade | equipe muda capacidade | mostrar impacto e registrar. |
| B12-S1 | Experimental No-Show | interessado nao comparece | Vendas C5 com limite. |
| B13-S1 | Creditos Reposicao | credito perto de vencer | avisar se permitido e custo justifica. |
| B14-S1 | Correcao Presenca | aluno contestou falta | sugerir correcao, auditar e atualizar impactos. |
| B15-S1 | Primeira Aula | novo aluno confirmado | criar checklist, avisar professor e checar pendencias. |
| B16-S1 | Workshop | studio cria aula especial | configurar publico, vagas, pagamento e aprovacao de lote. |

## 3. Vendas

| ID | Fluxo | Entrada | Esperado |
| --- | --- | --- | --- |
| C1-S1 | Valores | interessado pergunta preco | seguir politica: direto/faixa/qualificar/experimental/humano. |
| C1-E1 | Valores | pede desconto | handoff humano. |
| C2-S1 | Experimental | quer marcar experimental | coletar minimo, chamar Agenda B7 e confirmar. |
| C3-S1 | Lembrete | vespera da experimental | enviar lembrete configurado. |
| C4-S1 | Pos-Aula | compareceu e gostou | conduzir para plano/pre-matricula. |
| C5-S1 | Follow-Up | pediu preco e sumiu | cadencia curta e encerramento. |
| C6-S1 | Pre-Matricula | quer fechar 2x semana | criar pre-matricula e tarefa/Financeiro. |
| C7-S1 | Objecao | "achei caro" | responder com mensagem aprovada sem negociar. |
| C8-S1 | Origem | interessado veio por indicacao | registrar origem e qualificar. |
| C9-S1 | Perda | "fechei em outro lugar" | registrar motivo e encerrar respeitosamente. |
| C10-S1 | Indicacao | aluno indica amiga | criar interessado vinculado e seguir C1/C2. |
| C11-S1 | Checkout | abriu link e abandonou | follow-up limitado; se falhou pagamento D7. |
| C12-S1 | Sem Vaga | quer horario cheio | alternativa, lista comercial ou Gestao F10. |
| C13-S1 | Virou Aluno | pagamento confirmado | pausar follow-up comercial, acionar Agenda/Financeiro/Historico. |
| C14-S1 | Upgrade | aluno quer aumentar frequencia | verificar agenda/plano, Financeiro, sem empurrar automaticamente. |

## 4. Financeiro

| ID | Fluxo | Entrada | Esperado |
| --- | --- | --- | --- |
| D1-S1 | Vencimento | plano vence em 3 dias | enviar lembrete conforme janela. |
| D2-S1 | Atraso | pagamento atrasou 5 dias | lembrete com link se dentro da regra. |
| D2-E1 | Atraso | aluno contesta valor | handoff humano. |
| D3-S1 | Pix/Link | aluno pede Pix | enviar destino configurado. |
| D3-E1 | Pix/Link | aluno envia dado de cartao | bloquear e orientar canal seguro. |
| D4-S1 | Confirmacao | webhook confirmou | atualizar status de pagamento. |
| D4-E1 | Confirmacao | comprovante divergente | tarefa/humano. |
| D5-S1 | Renovacao | pagamento confirmado mesmo plano | sugerir/registrar conforme regra. |
| D6-S1 | Excecao | pede reembolso | humano obrigatorio. |
| D7-S1 | Falha | Pix expirou | gerar novo link se permitido ou tarefa. |
| D8-S1 | Recibo | aluno pede recibo | enviar se existe ou criar tarefa. |
| D9-S1 | Pausa | aluno quer trancar por viagem | humano, impacto plano/agenda e retorno previsto. |
| D10-S1 | Conciliacao | pagamento sem aluno | sugerir match, bloquear mensagem automatica. |
| D11-S1 | Contrato | assinatura pendente | lembrar se permitido ou tarefa. |
| D12-S1 | Bloqueio | inadimplencia fora da regra | sugerir bloqueio para humano, nao executar sozinho. |
| D13-S1 | Cortesia | equipe concede aula bonus | registrar motivo, validade e aprovador. |
| D14-S1 | Fechamento | fim do mes | resumo financeiro e pendencias para Gestao. |

## 5. Retencao

| ID | Fluxo | Entrada | Esperado |
| --- | --- | --- | --- |
| E1-S1 | Queda Frequencia | aluno reduziu presenca | classificar risco e acionar tarefa/mensagem. |
| E2-S1 | Inativo | 14 dias sem aula | check-in se permitido ou lista para equipe. |
| E2-C1 | Inativo | baixo risco e credito perto do limite | nao enviar WhatsApp pago. |
| E3-S1 | Retorno | aluno quer voltar | buscar horario via Agenda e avisar professor. |
| E4-S1 | Cancelamento | "vou cancelar" | humano com resumo e motivo. |
| E5-S1 | Ex-Aluno | lista de reativacao | sugerir lote para aprovacao. |
| E6-S1 | Satisfacao | feedback negativo | tarefa prioritaria/humano. |
| E7-S1 | Retorno Pausa | pausa termina semana que vem | lembrete e E3 se quiser voltar. |
| E8-S1 | Perfil Risco | baixa frequencia + atraso | gerar risco e acionar Financeiro/Retencao. |
| E9-S1 | Pos-Cancelamento | cancelamento aprovado | cancelar proximos horarios e registrar motivo. |
| E10-S1 | Marco | aluno voltou depois de pausa | registrar e sugerir mensagem se permitido. |
| E11-S1 | Evento Pessoal | aluno cita cirurgia | Historico G3 + humano, pausar automacoes inadequadas. |
| E12-S1 | Segmentacao | dono quer lista de risco | gerar lista e exigir aprovacao para lote. |

## 6. Gestao

| ID | Fluxo | Entrada | Esperado |
| --- | --- | --- | --- |
| F1-S1 | Prioridades | dono abre sistema de manha | mostrar top prioridades por agente. |
| F2-S1 | Dinheiro | painel calcula perdas | consolidar oportunidades sem promessa garantida. |
| F3-S1 | Fila Humana | handoff pendente | mostrar aprovar/editar/rejeitar/delegar. |
| F4-S1 | Gargalo | turma sempre vazia | sugerir ajuste e acionar agente dono. |
| F5-S1 | Resumo | fim da semana | enviar resumo agregado. |
| F6-S1 | Setup | falta regra de reposicao | bloquear reposicao automatica e criar checklist. |
| F7-S1 | Creditos | 90% usado | ativar economia e pedir aprovacao para caro. |
| F8-S1 | Performance | dono ve agente | mostrar resolvidos, pendencias e handoffs. |
| F9-S1 | Permissao | recepcao tenta mudar regra financeira | bloquear e registrar. |
| F10-S1 | Capacidade | lista espera cresce | sugerir nova turma/horario. |
| F11-S1 | Falha | WhatsApp falhou envio | retry seguro ou tarefa; nao duplicar. |
| F12-S1 | Importacao | planilha com duplicados | sugerir merge e bloquear fluxos dependentes. |
| F13-S1 | Teste | studio ativa cobranca | simular fluxo; se falhar, manter inativo. |

## 7. Historico/Evolucao

| ID | Fluxo | Entrada | Esperado |
| --- | --- | --- | --- |
| G1-S1 | Contexto Antes Aula | professor abre turma | mostrar resumo interno seguro. |
| G2-S1 | Observacao Pos-Aula | professor dita nota | salvar, resumir e acionar fluxo se risco. |
| G3-S1 | Restricao | aluno relata dor | registrar interno, humano, sem orientacao automatica. |
| G4-S1 | Objetivo | objetivo desatualizado | criar tarefa/revisao. |
| G5-S1 | Contexto Para Agente | Retencao precisa contexto | entregar resumo seguro ou handoff se sensivel. |
| G6-S1 | Documento | aluno envia anamnese | armazenar com permissao e destacar professor. |
| G7-S1 | Correcao | professor corrige nota | auditar e atualizar contexto. |
| G8-S1 | Handoff Professor | troca de professor | gerar resumo de ultimos combinados. |
| G9-S1 | Lembrete Nota | aula terminou sem nota | pedir nota curta se prioridade justificar. |
| G10-S1 | Compartilhar Contexto | aluno pede observacoes | preparar resposta segura ou humano. |
| G11-S1 | Permissao | financeiro abre restricao clinica | bloquear campo sem permissao. |
| G12-S1 | Linha Tempo | perfil do aluno aberto | mostrar eventos filtrados por papel. |

## Casos Transversais Obrigatorios

| ID | Caso | Esperado |
| --- | --- | --- |
| X1 | WhatsApp em grupo pede dado de aluno | nao expor; direcionar individual/validar. |
| X2 | Mensagem pede desconto e cita cancelamento | Financeiro/Retencao + humano. |
| X3 | Audio longo com varios pedidos | transcrever, classificar principal, criar tarefas/transicoes. |
| X4 | Aluno pede reposicao e tem pagamento atrasado | Agenda avalia reposicao; Financeiro pode sinalizar restricao se regra exigir. |
| X5 | Aluno inativo menciona dor | Retencao pausa automacao, Historico registra, humano assume. |
| X6 | Campanha de reativacao em lote | copiloto, aprovacao, limite de creditos e opt-out. |
| X7 | Webhook de pagamento duplica | idempotencia evita baixa duplicada. |
| X8 | Configuracao incompleta | F6 bloqueia fluxo dependente. |
| X9 | Fluxo aponta para agente nao contratado | cria tarefa e pode mostrar upsell, sem simular agente. |
| X10 | Creditos em 100% | pausar baixa prioridade e manter somente essencial configurado. |

## Criterio De Aprovacao Dos Testes

Para considerar a especificacao pronta:

- todos os cenarios de sucesso devem ter acao e estado final;
- todos os cenarios de risco devem ter pausa, handoff ou tarefa;
- todos os cenarios de falta de dado devem ir para setup, pergunta minima ou tarefa;
- todos os cenarios caros devem respeitar limite de credito/tentativa;
- todos os cenarios de transicao devem apontar para fluxo existente.
