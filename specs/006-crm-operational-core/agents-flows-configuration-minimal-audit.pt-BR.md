# Taliya CRM - Auditoria De Configuracao Minima Dos 96 Fluxos

Status: contrato funcional v0.1.
Data: 2026-05-21.

## Nota De Atualizacao

Este documento continua como auditoria da configuracao minima dos 96 fluxos.

A decisao final de paginas, rotinas e dinamicas de tela esta em:

- `agents-flows-routines-pages-final-contract.pt-BR.md`

Onde houver conflito, vale a decisao mais recente:

- agente nao configura;
- rotina organiza;
- fluxo configura;
- "pacote" vira "rotina" na UI;
- canal e integracao sao dependencias fixas;
- tom de voz e template ficam no fluxo.
- perfis de rotina (`Mais manual`, `Equilibrado`, `Mais autonomo`) seguem `agents-flows-routine-profile-map.pt-BR.md`;
- `default publicado` deste documento nao deve ser lido como obrigacao do perfil Equilibrado.

## Objetivo

Definir o que fica fixo, o que vem como default e o que o studio pode ajustar em cada fluxo de Agentes/Fluxos.

Regra principal:

O dono/admin nao deve configurar 96 fluxos manualmente. Ele escolhe o perfil da rotina. A tela de fluxo so mostra ajustes quando eles realmente melhoram a operacao do studio.

## Principio De Configuracao Minima

Todo fluxo tem tres camadas.

| Camada | Quem decide | O que contem |
|---|---|---|
| Fixo do produto | Taliya | agente dono, area, teto de automacao, dados obrigatorios, auditoria, limites de seguranca e acoes proibidas. |
| Default da rotina | Taliya sugere; studio publica | modo recomendado, responsavel padrao, aprovador padrao, limite padrao, fallback padrao e cota estimada. |
| Ajuste do studio | Dono/admin ajusta quando necessario | responsavel, aprovador, horario, frequencia, fila de excecao, template aprovado e alguns limites simples. |

Nao expor como configuracao comum:

- prompt livre;
- ferramenta interna;
- retry tecnico;
- politica de seguranca;
- regra de billing;
- status bruto de integracao;
- payload de execucao;
- modelo/LLM;
- thresholds tecnicos finos.

## O Que E Fixo Em Todo Fluxo

Todo fluxo ja vem com:

- ID e nome;
- agente dono;
- rotina recomendada;
- area do CRM;
- teto maximo de automacao;
- gatilho base;
- dados obrigatorios;
- canal ou ausencia de canal;
- integracao necessaria, se houver;
- acoes proibidas;
- eventos de auditoria;
- superficie de continuidade;
- fallback minimo;
- medicao de uso/cota quando houver IA;
- simulacao obrigatoria antes de publicar autonomia;
- pausa automatica por cota, opt-out, falha critica, integracao indisponivel ou incidente alto.

## O Que Muda Por Modo

| Modo escolhido | O que e fixo | O que o studio pode ajustar | Default recomendado |
|---|---|---|---|
| Manual | O agente nao conduz e nao sugere automaticamente. | responsavel, prazo, tipo de tarefa/caso, mostrar ou ocultar botao de ajuda. | criar tarefa/checklist na tela de origem; botao de ajuda ligado se agente contratado. |
| Copiloto | Agente sugere, humano decide. Nao executa sozinho. | quem revisa, que tipo de sugestao aparece, se cria rascunho, se pode virar tarefa. | sugestao automatica + acoes: aprovar, editar, rejeitar, criar tarefa. |
| Autonomo com aprovacao | Agente adianta o trabalho, mas para antes de ponto sensivel. | aprovador, prazo de aprovacao, quando pedir aprovacao, fallback se ninguem aprovar. | aprovador da area; 24h para aprovar; vencido vira tarefa. |
| Autonomo com excecoes | Agente executa caso normal e chama humano quando sai do padrao. | fila de excecao, sinais que chamam humano, limite de tentativas e horario. | fila da area; 1-2 tentativas; excecao vira tarefa/caso. |
| Autonomo | Agente resolve o caso comum sozinho dentro de limites. | horario permitido, limite por evento, template/tom quando aplicavel e fallback. | 1 acao por evento; janela comercial; bloquear se dado/canal/cota falhar. |

## Perfis Reutilizaveis De Configuracao

Estes perfis evitam criar 96 formularios diferentes.

| Perfil | Usado por | Fixo | Ajustes visiveis |
|---|---|---|---|
| P01 Conversa segura | A1-A5, A10 | identidade, opt-out, baixa confianca, fila humana, auditoria de conversa. | fila responsavel, limite de respostas, tom/template, quando chamar humano. |
| P02 Identidade e privacidade | A6-A9 | consentimento, LGPD, identidade, midia/documento, bloqueio de dado sensivel. | responsavel de revisao, botao de ajuda, aprovador de privacidade. |
| P03 Presenca e faltas | B1-B3, B14 | aula, aluno, chamada, janela de envio, auditoria de presenca. | horario de lembrete, responsavel, regra de falta, quando criar tarefa. |
| P04 Reposicoes e vagas | B4-B6, B13 | credito, vaga, lista de espera, capacidade e regra de reposicao. | prioridade da lista, aprovador, limite de convites, validade de credito. |
| P05 Agenda estrutural | B8-B11, B16 | impacto em grade/turma/aula, simulacao e comunicacao. | aprovador, prazo, quem recebe tarefa, template de comunicado. |
| P06 Experimental e primeira aula | B7, B12, B15, C2-C5, C11, C12 | interessado, aula experimental, follow-up, consentimento. | cadencia, responsavel comercial, horario, quando chamar humano. |
| P07 Captura e qualificacao | C8-C10, C15 | origem, duplicidade, dono do lead, qualificacao. | responsavel, campos obrigatorios, regra de perda/indicacao. |
| P08 Conversao e matricula | C1, C6, C7, C13, C14 | preco/plano, promessa comercial, matricula, contrato, upgrade. | aprovador, template, limite de proposta, tarefa comercial. |
| P09 Financeiro simples | D1-D3, D7, D8, D10 | cobranca, pagamento, comprovante, canal, idempotencia. | horario, tentativas, aprovador, fila financeira, template. |
| P10 Financeiro sensivel | D4-D6, D9, D11-D15 | desconto, acordo, bloqueio, contrato, plano, encerramento. | aprovador obrigatorio, prazo, responsavel, tarefa/caso. |
| P11 Retencao preventiva | E1-E3, E6, E7, E10 | frequencia, inatividade, retorno, satisfacao, marco. | cadencia de contato, responsavel, quando chamar humano. |
| P12 Retencao sensivel | E4, E5, E8, E9, E11-E13 | cancelamento, reclamacao, saude/evento pessoal, risco, confianca. | aprovador, dono do caso, pausa automatica, tarefa/caso. |
| P13 Comando e governanca | F1-F10 | prioridade, fila, relatorio, qualidade, cota, capacidade. | responsavel, frequencia de resumo, limite de alertas, fila. |
| P14 Integracao, teste e incidente | F11-F15 | logs, importacao, simulacao, incidente, politica. | responsavel tecnico/operacao, aprovador, auto-pausa, retry seguro. |
| P15 Historico e professor | G1-G12 | permissao de historico, professor, documentos, contexto, auditoria. | visibilidade, responsavel, aprovador, lembrete, tarefa. |

## Defaults Por Perfil Da Rotina

| Perfil | Manual | Copiloto | Autonomo com aprovacao | Autonomo com excecoes | Autonomo |
|---|---|---|---|---|---|
| Mais manual | Mais fluxos com tarefa/checklist. | Ligado nos agentes contratados. | Usado para fluxos sensiveis. | Usado em poucos fluxos de baixo risco. | Apenas lembretes e rotinas internas simples. |
| Equilibrado | Fallback padrao. | Ligado em fluxos nao publicados. | Default para nivel 3. | Default para nivel 4. | Default para nivel 5. |
| Mais autonomo | Fallback e pausa. | Usado quando cota/risco bloqueia. | Mantem aprovacao em sensiveis. | Mais fluxos publicados por rotina. | Ligado nos fluxos simples assim que simulados. |

Regra: antes de publicar, tudo fica em rascunho ou copiloto. Depois de simular e publicar rotina, o default publicado segue o perfil escolhido, salvo ajuste individual mais conservador do studio.

## Auditoria Dos 96 Fluxos

Colunas:

- `Teto`: nivel maximo recomendado no MVP.
- `Default publicado`: modo recomendado depois de simulacao/publicacao.
- `Perfil`: formulario reaproveitado.
- `Ajuste minimo`: o que o studio pode ajustar sem virar painel tecnico.

### Atendimento - 10

| ID | Fluxo | Teto | Default publicado | Perfil | Ajuste minimo |
|---|---|---:|---|---|---|
| A1 | Nova Conversa | 4 | Autonomo com excecoes | P01 | fila de atendimento, limite de respostas, quando chamar humano. |
| A2 | Duvidas Permitidas | 5 | Autonomo | P01 | base/template permitido, limite por conversa, fallback. |
| A3 | Aluno Existente | 4 | Autonomo com excecoes | P01 | fila, dados que exigem humano, botao de ajuda. |
| A4 | Fora Do Escopo | 5 | Autonomo | P01 | resposta padrao, destino da tarefa/caso. |
| A5 | Chamada Humana | 5 | Autonomo | P01 | fila destino, prioridade, resumo obrigatorio. |
| A6 | Consentimento/Opt-Out | 5 | Autonomo | P02 | preferencia de canal, responsavel de revisao em caso ambiguo. |
| A7 | Identidade/Midias | 4 | Autonomo com excecoes | P02 | responsavel de revisao, tipos de midia aceitos. |
| A8 | Privacidade/Dados | 3 | Autonomo com aprovacao | P02 | aprovador de privacidade, SLA do caso. |
| A9 | Telefone Compartilhado E Identidade | 3 | Autonomo com aprovacao | P02 | regra de validacao, responsavel de revisao. |
| A10 | Ciclo De Vida/SLA | 5 | Autonomo | P01 | tempo de SLA, fila destino, prioridade. |

### Agenda - 16

| ID | Fluxo | Teto | Default publicado | Perfil | Ajuste minimo |
|---|---|---:|---|---|---|
| B1 | Confirmacao De Presenca | 5 | Autonomo | P03 | horario do lembrete, template/tom, limite por aula. |
| B2 | Falta Com Aviso | 4 | Autonomo com excecoes | P03 | regra de falta, destino da reposicao, responsavel. |
| B3 | No-Show | 4 | Autonomo com excecoes | P03 | quando vira tarefa de retencao, responsavel. |
| B4 | Recuperar Vaga Aberta | 4 | Autonomo com excecoes | P04 | prioridade da lista, limite de convites, aprovador se lote. |
| B5 | Reposicao/Remarcacao | 3 | Autonomo com aprovacao | P04 | aprovador, regras de credito visiveis, responsavel. |
| B6 | Lista De Espera | 4 | Autonomo com excecoes | P04 | prioridade, limite de convites, canal. |
| B7 | Disponibilidade Experimental | 4 | Autonomo com excecoes | P06 | responsavel comercial, horarios oferecidos, quando chamar humano. |
| B8 | Mudanca Horario Fixo | 3 | Autonomo com aprovacao | P05 | aprovador, prazo, mensagem de confirmacao. |
| B9 | Cancelamento Pelo Studio | 3 | Autonomo com aprovacao | P05 | aprovador, template de comunicado, quem trata excecoes. |
| B10 | Conflito Capacidade | 3 | Autonomo com aprovacao | P05 | aprovador, responsavel do caso, prioridade. |
| B11 | Ajuste De Grade | 3 | Autonomo com aprovacao | P05 | aprovador, data de vigencia, simulacao obrigatoria. |
| B12 | Experimental No-Show | 4 | Autonomo com excecoes | P06 | cadencia, responsavel comercial, limite de contato. |
| B13 | Creditos Reposicao | 3 | Autonomo com aprovacao | P04 | aprovador, validade, destino de excecoes. |
| B14 | Correcao Presenca | 3 | Autonomo com aprovacao | P03 | aprovador, motivo obrigatorio, auditoria. |
| B15 | Primeira Aula | 4 | Autonomo com excecoes | P06 | checklist, responsavel, quando chamar humano. |
| B16 | Aula Especial/Workshop | 3 | Autonomo com aprovacao | P05 | aprovador, capacidade, template, prazo. |

### Vendas - 15

| ID | Fluxo | Teto | Default publicado | Perfil | Ajuste minimo |
|---|---|---:|---|---|---|
| C1 | Valores E Planos | 4 | Autonomo com excecoes | P08 | template/base de planos, quando chamar humano. |
| C2 | Aula Experimental | 4 | Autonomo com excecoes | P06 | horarios oferecidos, responsavel, limite de tentativas. |
| C3 | Lembrete Experimental | 5 | Autonomo | P06 | horario do lembrete, template, limite por aula. |
| C4 | Pos-Aula Experimental | 4 | Autonomo com excecoes | P06 | cadencia, responsavel, quando virar tarefa. |
| C5 | Follow-Up Comercial | 4 | Autonomo com excecoes | P06 | cadencia, limite de tentativas, responsavel. |
| C6 | Pre-Matricula | 3 | Autonomo com aprovacao | P08 | aprovador, checklist, responsavel comercial. |
| C7 | Objecoes | 3 | Autonomo com aprovacao | P08 | aprovador, base de respostas, limite de promessa. |
| C8 | Origem/Qualificacao | 4 | Autonomo com excecoes | P07 | campos obrigatorios, responsavel, regra de duplicidade. |
| C9 | Perda Comercial | 3 | Autonomo com aprovacao | P07 | motivo, aprovador se perda sensivel, responsavel. |
| C10 | Indicacao | 3 | Autonomo com aprovacao | P07 | aprovador de beneficio, regra de vinculo. |
| C11 | Checkout/Abandono | 4 | Autonomo com excecoes | P06 | cadencia, responsavel, limite de contato. |
| C12 | Demanda Sem Vaga | 4 | Autonomo com excecoes | P06 | lista de espera, responsavel, regra de promessa. |
| C13 | Interessado Para Aluno | 3 | Autonomo com aprovacao | P08 | aprovador, plano, checklist de matricula. |
| C14 | Upsell/Upgrade | 3 | Autonomo com aprovacao | P08 | aprovador, template de proposta, responsavel. |
| C15 | Entrada Multicanal De Lead | 4 | Autonomo com excecoes | P07 | fontes aceitas, dono do lead, regra de duplicidade. |

### Financeiro - 15

| ID | Fluxo | Teto | Default publicado | Perfil | Ajuste minimo |
|---|---|---:|---|---|---|
| D1 | Lembrete Vencimento | 5 | Autonomo | P09 | horario, template, limite por cobranca. |
| D2 | Pagamento Atrasado | 4 | Autonomo com excecoes | P09 | tentativas, fila financeira, sinais que chamam humano. |
| D3 | Pix/Link | 3 | Autonomo com aprovacao | P09 | aprovador, template, limite de valor. |
| D4 | Confirmacao Pagamento | 3 | Autonomo com aprovacao | P10 | aprovador, evidencia exigida, responsavel. |
| D5 | Renovacao Plano | 3 | Autonomo com aprovacao | P10 | aprovador, antecedencia, template. |
| D6 | Excecoes Financeiras | 3 | Autonomo com aprovacao | P10 | aprovador obrigatorio, tipos de excecao, prazo. |
| D7 | Falha Pagamento | 4 | Autonomo com excecoes | P09 | fila, tentativas, quando abrir caso. |
| D8 | Recibo/Nota | 4 | Autonomo com excecoes | P09 | responsavel, documentos permitidos, fallback. |
| D9 | Pausa/Trancamento | 3 | Autonomo com aprovacao | P10 | aprovador, impacto em agenda/cobranca, prazo. |
| D10 | Conciliacao Interna | 3 | Autonomo com aprovacao | P09 | aprovador, confianca minima, responsavel. |
| D11 | Contrato/Termos | 3 | Autonomo com aprovacao | P10 | aprovador, template, prazo. |
| D12 | Bloqueio/Liberacao | 3 | Autonomo com aprovacao | P10 | aprovador, motivo obrigatorio, auditoria. |
| D13 | Creditos/Cortesias | 3 | Autonomo com aprovacao | P10 | aprovador, limite de valor, motivo. |
| D14 | Fechamento Mensal | 4 | Autonomo com excecoes | P10 | responsavel, frequencia, quando abrir tarefa. |
| D15 | Encerramento Ou Alteracao Efetiva De Plano | 3 | Autonomo com aprovacao | P10 | aprovador, checklist, comunicacao. |

### Retencao - 13

| ID | Fluxo | Teto | Default publicado | Perfil | Ajuste minimo |
|---|---|---:|---|---|---|
| E1 | Queda Frequencia | 4 | Autonomo com excecoes | P11 | regra de queda, responsavel, cadencia. |
| E2 | Aluno Inativo | 4 | Autonomo com excecoes | P11 | dias de inatividade, responsavel, limite de contato. |
| E3 | Retorno | 4 | Autonomo com excecoes | P11 | responsavel, regra de agenda, quando chamar humano. |
| E4 | Risco Cancelamento | 3 | Autonomo com aprovacao | P12 | dono do caso, aprovador, pausa de automacoes. |
| E5 | Reativacao Ex-Aluno | 3 | Autonomo com aprovacao | P12 | aprovador, segmento permitido, cadencia. |
| E6 | Satisfacao | 4 | Autonomo com excecoes | P11 | janela, responsavel, quando abrir reclamacao. |
| E7 | Retorno Apos Pausa | 4 | Autonomo com excecoes | P11 | antecedencia, responsavel, regra de agenda. |
| E8 | Risco Por Perfil | 3 | Autonomo com aprovacao | P12 | aprovador, uso do segmento, responsavel. |
| E9 | Pos-Cancelamento | 3 | Autonomo com aprovacao | P12 | aprovador, quando contatar, responsavel. |
| E10 | Marco Engajamento | 4 | Autonomo com excecoes | P11 | tipo de marco, responsavel, limite de contato. |
| E11 | Saude/Evento Pessoal | 3 | Autonomo com aprovacao | P12 | dono do caso, visibilidade, aprovador. |
| E12 | Segmentacao Risco | 3 | Autonomo com aprovacao | P12 | aprovador, segmento, acao permitida. |
| E13 | Reclamacao E Recuperacao De Confianca | 3 | Autonomo com aprovacao | P12 | dono do caso, aprovador, pausa automatica. |

### Gestao/Governanca - 15

| ID | Fluxo | Teto | Default publicado | Perfil | Ajuste minimo |
|---|---|---:|---|---|---|
| F1 | Prioridades Dia | 5 | Autonomo | P13 | horario do resumo, responsavel, fontes exibidas. |
| F2 | Dinheiro Na Mesa | 4 | Autonomo com excecoes | P13 | frequencia, responsavel, quando abrir tarefa. |
| F3 | Fila Humana | 5 | Autonomo | P13 | filas, prioridade, responsaveis. |
| F4 | Gargalos | 4 | Autonomo com excecoes | P13 | frequencia, responsavel, tipo de alerta. |
| F5 | Resumo Semanal | 5 | Autonomo | P13 | dia/hora, destinatarios internos, secoes. |
| F6 | Qualidade Dados | 4 | Autonomo com excecoes | P13 | responsavel, tipos de dado, prioridade. |
| F7 | Creditos/Limites | 5 | Autonomo | P13 | alertas 70/90/100, responsavel, economia. |
| F8 | Performance | 4 | Autonomo com excecoes | P13 | frequencia, responsavel, metricas exibidas. |
| F9 | Permissoes/Auditoria | 3 | Autonomo com aprovacao | P13 | aprovador, tipos de evento, responsavel. |
| F10 | Capacidade/Crescimento | 4 | Autonomo com excecoes | P13 | frequencia, responsavel, limite de alerta. |
| F11 | Falhas/Webhooks | 4 | Autonomo com excecoes | P14 | responsavel, severidade, retry seguro. |
| F12 | Importacao/Migracao | 3 | Autonomo com aprovacao | P14 | aprovador, lote, responsavel. |
| F13 | Teste De Fluxo | 5 | Autonomo | P14 | exemplos de simulacao, responsavel. |
| F14 | Incidente De Automacao E Correcao Operacional | 4 | Autonomo com excecoes | P14 | severidade, responsavel, auto-pausa. |
| F15 | Mudanca De Politica Ou Regra Operacional | 3 | Autonomo com aprovacao | P14 | aprovador, data de vigencia, simulacao. |

### Historico/Evolucao - 12

| ID | Fluxo | Teto | Default publicado | Perfil | Ajuste minimo |
|---|---|---:|---|---|---|
| G1 | Contexto Antes Aula | 4 | Autonomo com excecoes | P15 | visibilidade, professor, quando chamar humano. |
| G2 | Observacao Pos-Aula | 4 | Autonomo com excecoes | P15 | lembrete, professor, tipos de nota. |
| G3 | Restricao/Cuidado | 3 | Autonomo com aprovacao | P15 | aprovador, visibilidade, dono do caso. |
| G4 | Objetivo/Evolucao | 4 | Autonomo com excecoes | P15 | professor/responsavel, frequencia, tarefa. |
| G5 | Contexto Para Agente | 3 | Autonomo com aprovacao | P15 | aprovador, dados permitidos, escopo. |
| G6 | Documentos/Anamnese | 3 | Autonomo com aprovacao | P15 | aprovador, documentos exigidos, responsavel. |
| G7 | Correcao Historico | 3 | Autonomo com aprovacao | P15 | aprovador, motivo, auditoria. |
| G8 | Repasse Entre Professores | 4 | Autonomo com excecoes | P15 | professor destino, campos do resumo, quando chamar humano. |
| G9 | Lembrete Professor | 5 | Autonomo | P15 | horario, frequencia, destino. |
| G10 | Compartilhar Contexto | 3 | Autonomo com aprovacao | P15 | aprovador, destinatario, dados permitidos. |
| G11 | Permissao Historico | 3 | Autonomo com aprovacao | P15 | aprovador, papel, escopo de visibilidade. |
| G12 | Linha Do Tempo | 4 | Autonomo com excecoes | P15 | tipos de evento, filtro padrao, responsavel. |

## Campos Que A Tela Do Fluxo Deve Mostrar

Campos sempre visiveis:

- modo atual;
- teto permitido;
- rotina;
- agente;
- status;
- porque esta ativo, bloqueado ou pendente;
- onde continua se parar;
- botao de simular;
- botao de publicar/pausar.

Campos visiveis somente quando importam:

- template/tom: apenas quando ha mensagem externa;
- canal aparece como dependencia fixa, nao como ajuste;
- aprovador: apenas em `Autonomo com aprovacao`;
- fila de excecao: apenas em `Autonomo com excecoes`;
- horario/frequencia: apenas quando ha envio, resumo ou lembrete;
- limite de valor: apenas em financeiro;
- visibilidade/permissao: apenas em historico, privacidade e dados;
- data de vigencia: apenas em politica, grade, plano ou regra estrutural.

## Defaults Que Nao Devem Virar Pergunta

O studio nao deve ser perguntado sobre:

- evento de auditoria;
- idempotencia;
- objeto tecnico de execucao;
- payload do provedor;
- limite interno de retry tecnico;
- regra de isolamento de tenant;
- modelo de IA;
- prompt do agente;
- regra de cota 70/90/100;
- auto-pausa por incidente critico;
- bloqueio por opt-out;
- bloqueio por permissao ausente.

Esses itens sao fixos do produto.

## Criterios De Aceite

Esta auditoria esta correta quando:

- cobre os 96 fluxos;
- cada fluxo tem teto, default publicado, perfil e ajuste minimo;
- a maioria dos fluxos reaproveita perfis em vez de formularios proprios;
- o studio ajusta no maximo o necessario para operar melhor;
- modo manual, copiloto e automatico continuam claros;
- autonomo com aprovacao, autonomo com excecoes e autonomo ficam como nomes de UI;
- configuracoes tecnicas ficam fora da experiencia do dono/admin.
