# Taliya CRM - Matriz Dos 5 Niveis De Automacao Dos 96 Fluxos

Status: contrato funcional v0.1.
Data: 2026-05-21.

## Objetivo

Definir, para cada um dos 96 fluxos de Agentes/Fluxos, qual e o nivel maximo recomendado de automacao no MVP e onde a operacao continua quando o agente precisa parar, pedir aprovacao ou chamar humano.

Este documento nao substitui os tres modos base:

- Manual;
- Copiloto;
- Autonomo.

Ele detalha o modo `Autonomo` em tres formatos de operacao com nomes simples para a UI:

- Autonomo com aprovacao;
- Autonomo com excecoes;
- Autonomo.

## Regra Que Evita Confusao

Existem duas coisas diferentes no produto:

| Coisa | O que controla | Exemplo |
|---|---|---|
| Modo do fluxo | O comportamento automatico quando o fluxo dispara. | D2 detecta atraso e gera sugestao, aprovacao ou envio. |
| Botao de copiloto | Ajuda sob demanda dentro da tela. | Usuario clica em "Sugerir mensagem" ou "Explicar pendencia". |

Um fluxo em modo manual pode ter botao de copiloto, mas esse botao so roda se o usuario clicar.

Um fluxo em modo copiloto gera sugestao automaticamente quando dispara, mas o humano decide a acao.

Um fluxo em modo autonomo e conduzido pelo agente, mas tambem pode mostrar botao de copiloto para explicar, revisar, preparar resposta, apoiar aprovacao ou resumir repasse para humano.

Portanto:

```text
Modo do fluxo = quem conduz quando dispara.
Botao de copiloto = ajuda pontual quando o humano pede ou precisa decidir.
```

## Os 5 Niveis

| Nivel | Nome | Quem conduz | Como para | Onde continua |
|---:|---|---|---|---|
| 1 | Manual | Humano | Nao ha agente conduzindo. | Tela de origem, tarefa, checklist ou caso. |
| 2 | Copiloto | Humano com ajuda do agente | Humano decide cada acao relevante. | Tela de origem, aprovacao ou tarefa. |
| 3 | Autonomo com aprovacao | Agente adianta o trabalho, mas pede aprovacao antes de pontos sensiveis. | Aprovacao obrigatoria antes de impacto sensivel. | `/app/aprovacoes`, `/app/hoje`, tela de origem. |
| 4 | Autonomo com excecoes | Agente segue sozinho enquanto o caso esta normal. | Chama humano quando aparece excecao, ambiguidade, risco ou baixa confianca. | `/app/tarefas`, `/app/operacao`, fila da tela de origem. |
| 5 | Autonomo | Agente resolve o caso comum sozinho dentro de limites. | So para por bloqueio, falha rara, cota, opt-out, integracao ou incidente. | Fallback, execucao, auditoria e alerta se necessario. |

Regra de leitura:

- o nivel abaixo e o teto recomendado do fluxo no MVP;
- se o teto e 5, o usuario tambem pode configurar 1, 2, 3 ou 4;
- se o teto e 4, o usuario tambem pode configurar 1, 2 ou 3;
- se o teto e 3, o usuario tambem pode configurar 1 ou 2;
- o plano contratado, cota, permissao, canal, integracao e risco ainda podem rebaixar o fluxo na pratica.

## Diferenca Entre 2, 3, 4 E 5

Copiloto nao conduz o fluxo. Ele ajuda o humano que esta conduzindo.

No nivel 2, o agente pode preparar uma sugestao automaticamente quando o fluxo dispara, mas a acao final so existe se o humano aceitar. Se o humano rejeitar, editar muito ou transformar em tarefa, aquela execucao segue manual.

Autonomo com aprovacao conduz o fluxo, mas para em pontos planejados de decisao humana.

Autonomo com excecoes conduz o fluxo e so chama humano quando o caso foge do padrao.

Autonomo conduz e termina o caso comum sozinho, dentro de limites claros.

Exemplo com o mesmo fluxo D2 Pagamento Atrasado:

| Configuracao | O que acontece |
|---|---|
| Manual | O sistema mostra a cobranca atrasada. O humano decide e faz. Pode pedir ajuda pelo botao de copiloto, se tiver agente. |
| Copiloto | O agente prepara a mensagem e explica o motivo. O humano aprova, edita, rejeita ou transforma em tarefa. |
| Autonomo com aprovacao | O agente prepara tudo e para antes de enviar ou antes de acao sensivel, pedindo aprovacao. |
| Autonomo com excecoes | O agente envia lembrete simples e chama humano se houver contestacao, pedido de acordo, cancelamento ou duvida sensivel. |
| Autonomo | Nao e o teto recomendado para D2 no MVP, porque atraso normalmente pode gerar excecao humana. |

## Matriz Dos 96 Fluxos

### Atendimento - 10

| ID | Fluxo | Teto MVP | Parada principal | Onde continua |
|---|---|---:|---|---|
| A1 | Nova Conversa | 4 | Chama humano se baixa confianca, identidade incerta, risco ou pedido humano. | `/app/inbox`, `/app/tarefas`, `/app/operacao`. |
| A2 | Duvidas Permitidas | 5 | Bloqueia se pergunta fora da base aprovada ou baixa confianca. | `/app/inbox`, tarefa de resposta. |
| A3 | Aluno Existente | 4 | Chama humano se pedido exigir dado sensivel, agenda, financeiro ou decisao humana. | `/app/inbox`, `/app/alunos/[id]`, `/app/tarefas`. |
| A4 | Fora Do Escopo | 5 | Bloqueia ou encaminha quando intencao nao e atendida. | `/app/inbox`, tarefa/caso. |
| A5 | Chamada Humana | 5 | O proprio resultado normal e chamar humano com resumo. | `/app/inbox`, `/app/operacao`, fila humana. |
| A6 | Consentimento/Opt-Out | 5 | Bloqueia envios futuros e audita; ambiguidade vira revisao. | `/app/contatos/[id]`, auditoria, tarefa. |
| A7 | Identidade/Midias | 4 | Chama humano se midia, documento, audio ou identidade nao puder ser classificado com confianca. | `/app/inbox`, `/app/dados/duplicidades`, `/app/historico/documentos`. |
| A8 | Privacidade/Dados | 3 | Checkpoint/aprovacao para qualquer pedido de dados, LGPD ou exclusao. | `/app/operacao`, `/app/auditoria`, aprovacao. |
| A9 | Telefone Compartilhado E Identidade | 3 | Checkpoint antes de vincular contato, expor dado ou agir em nome de aluno. | `/app/contatos`, `/app/alunos/[id]`, `/app/dados/duplicidades`. |
| A10 | Ciclo De Vida/SLA | 5 | Para se conversa exige julgamento humano ou excede limite. | `/app/inbox`, `/app/tarefas`, `/app/hoje`. |

### Agenda - 16

| ID | Fluxo | Teto MVP | Parada principal | Onde continua |
|---|---|---:|---|---|
| B1 | Confirmacao De Presenca | 5 | Bloqueia por opt-out, canal, cota ou conflito raro. | `/app/agenda`, `/app/aulas/[id]`, execucao. |
| B2 | Falta Com Aviso | 4 | Chama humano se afeta credito, reposicao sensivel ou regra nao clara. | `/app/reposicoes`, `/app/aulas/[id]`, tarefa. |
| B3 | No-Show | 4 | Chama humano se aluno tem risco, recorrencia ou contexto sensivel. | `/app/aulas/[id]`, `/app/retencao`, tarefa. |
| B4 | Recuperar Vaga Aberta | 4 | Chama humano se lista, prioridade, horario ou elegibilidade ficar ambigua. | `/app/lista-espera`, `/app/reposicoes`, aprovacao/tarefa. |
| B5 | Reposicao/Remarcacao | 3 | Checkpoint antes de confirmar vaga quando credito/regra impacta agenda. | `/app/reposicoes`, `/app/agenda`, aprovacao. |
| B6 | Lista De Espera | 4 | Chama humano se prioridade ou compatibilidade nao e clara. | `/app/lista-espera`, `/app/tarefas`. |
| B7 | Disponibilidade Experimental | 4 | Chama humano se horario, turma ou responsavel nao esta claro. | `/app/experimental`, `/app/agenda`, tarefa. |
| B8 | Mudanca Horario Fixo | 3 | Checkpoint antes de alterar rotina fixa do aluno. | `/app/alunos/[id]`, `/app/agenda`, aprovacao. |
| B9 | Cancelamento Pelo Studio | 3 | Checkpoint antes de comunicar alunos e aplicar impacto operacional. | `/app/aulas/[id]`, `/app/aprovacoes`, `/app/hoje`. |
| B10 | Conflito Capacidade | 3 | Checkpoint antes de mover aluno, turma ou capacidade. | `/app/turmas/[id]`, `/app/agenda`, caso operacional. |
| B11 | Ajuste De Grade | 3 | Checkpoint com simulacao antes de mudar grade. | `/app/grade`, `/app/aprovacoes`, `/app/operacao`. |
| B12 | Experimental No-Show | 4 | Chama humano se interessado reclama, pede excecao ou vira venda sensivel. | `/app/experimental`, `/app/interessados/[id]`, tarefa comercial. |
| B13 | Creditos Reposicao | 3 | Checkpoint antes de alterar saldo, validade ou excecao de credito. | `/app/creditos-reposicao`, `/app/aprovacoes`. |
| B14 | Correcao Presenca | 3 | Checkpoint antes de corrigir chamada auditavel. | `/app/aulas/[id]/chamada`, `/app/auditoria`, aprovacao. |
| B15 | Primeira Aula | 4 | Chama humano se falta documento, anamnese, contato ou alinhamento com professor. | `/app/aulas/[id]`, `/app/alunos/[id]`, checklist/tarefa. |
| B16 | Aula Especial/Workshop | 3 | Checkpoint antes de publicar evento, cobrar, reservar ou comunicar lote. | `/app/eventos`, `/app/aprovacoes`, tarefa. |

### Vendas - 15

| ID | Fluxo | Teto MVP | Parada principal | Onde continua |
|---|---|---:|---|---|
| C1 | Valores E Planos | 4 | Chama humano se pergunta envolve desconto, excecao, promessa ou comparacao sensivel. | `/app/inbox`, `/app/vendas`, tarefa comercial. |
| C2 | Aula Experimental | 4 | Chama humano se precisa escolher horario fora da regra ou encaixe sensivel. | `/app/experimental`, `/app/agenda`, tarefa. |
| C3 | Lembrete Experimental | 5 | Bloqueia por opt-out, canal, cota ou aula inexistente. | `/app/experimental`, execucao, tarefa manual. |
| C4 | Pos-Aula Experimental | 4 | Chama humano se resposta indica objecao, negociacao ou decisao de matricula. | `/app/interessados/[id]`, `/app/vendas`, tarefa. |
| C5 | Follow-Up Comercial | 4 | Chama humano se interessado pede desconto, reclama, opt-out ou sinaliza cancelamento. | `/app/vendas`, `/app/tarefas`, `/app/inbox`. |
| C6 | Pre-Matricula | 3 | Checkpoint antes de criar matricula, contrato ou plano. | `/app/matriculas`, `/app/aprovacoes`. |
| C7 | Objecoes | 3 | Checkpoint antes de promessa comercial, desconto ou resposta delicada. | `/app/conversas/[id]`, `/app/aprovacoes`. |
| C8 | Origem/Qualificacao | 4 | Chama humano se origem/qualificacao e incerta ou duplicada. | `/app/interessados/[id]`, `/app/vendas/origens`, tarefa. |
| C9 | Perda Comercial | 3 | Checkpoint antes de marcar perda definitiva ou classificar motivo sensivel. | `/app/vendas`, `/app/interessados/[id]`, aprovacao/tarefa. |
| C10 | Indicacao | 3 | Checkpoint antes de conceder beneficio ou vincular indicacao. | `/app/indicacoes`, `/app/aprovacoes`. |
| C11 | Checkout/Abandono | 4 | Chama humano se envolve pagamento, duvida sensivel, desconto ou objecao. | `/app/checkout-alunos`, `/app/vendas`, tarefa. |
| C12 | Demanda Sem Vaga | 4 | Chama humano se precisa promessa de vaga, encaixe ou prioridade fora da regra. | `/app/vendas`, `/app/lista-espera`, tarefa. |
| C13 | Interessado Para Aluno | 3 | Checkpoint antes de converter pessoa, criar aluno e ativar plano. | `/app/matriculas`, `/app/alunos/[id]`, aprovacao. |
| C14 | Upsell/Upgrade | 3 | Checkpoint antes de proposta, alteracao comercial ou novo plano. | `/app/alunos/[id]`, `/app/aprovacoes`, `/app/vendas`. |
| C15 | Entrada Multicanal De Lead | 4 | Chama humano se lead duplicado, origem incerta ou baixa confianca. | `/app/vendas/captura`, `/app/interessados`, tarefa. |

### Financeiro - 15

| ID | Fluxo | Teto MVP | Parada principal | Onde continua |
|---|---|---:|---|---|
| D1 | Lembrete Vencimento | 5 | Bloqueia por opt-out, canal, cota, valor ausente ou template invalido. | `/app/financeiro/movimentacoes`, execucao, tarefa. |
| D2 | Pagamento Atrasado | 4 | Chama humano se aluno contesta, pede acordo, desconto, cancelamento ou excecao. | `/app/financeiro/movimentacoes/[id]`, tarefa financeira. |
| D3 | Pix/Link | 3 | Checkpoint antes de enviar link ou gerar cobranca quando houver risco/valor sensivel. | `/app/financeiro/movimentacoes`, `/app/aprovacoes`. |
| D4 | Confirmacao Pagamento | 3 | Checkpoint antes de confirmar quando evidencia, webhook ou match e incerto. | `/app/financeiro/movimentacoes/[id]`, aprovacao. |
| D5 | Renovacao Plano | 3 | Checkpoint antes de renovar, alterar preco ou comunicar condicao. | `/app/alunos/[id]`, `/app/financeiro`, aprovacao. |
| D6 | Excecoes Financeiras | 3 | Checkpoint obrigatorio para desconto, acordo, cortesia, estorno ou disputa. | `/app/financeiro/movimentacoes`, `/app/aprovacoes`, caso. |
| D7 | Falha Pagamento | 4 | Chama humano se falha vira disputa, cancelamento, excecao ou erro de provedor. | `/app/financeiro/movimentacoes/[id]`, tarefa/caso. |
| D8 | Recibo/Nota | 4 | Chama humano se documento exige revisao fiscal/financeira ou dado faltante. | `/app/financeiro/documentos`, tarefa. |
| D9 | Pausa/Trancamento | 3 | Checkpoint antes de alterar cobranca, agenda, contrato ou status do aluno. | `/app/financeiro`, `/app/alunos/[id]`, aprovacao/caso. |
| D10 | Conciliacao Interna | 3 | Checkpoint antes de casar pagamento incerto com aluno/cobranca. | `/app/financeiro/movimentacoes`, tarefa financeira. |
| D11 | Contrato/Termos | 3 | Checkpoint antes de enviar, alterar ou aceitar termo. | `/app/contratos`, `/app/aprovacoes`. |
| D12 | Bloqueio/Liberacao | 3 | Checkpoint antes de bloquear ou liberar acesso. | `/app/financeiro`, `/app/aprovacoes`, auditoria. |
| D13 | Creditos/Cortesias | 3 | Checkpoint antes de conceder credito, cortesia ou beneficio financeiro. | `/app/financeiro`, `/app/aprovacoes`. |
| D14 | Fechamento Mensal | 4 | Chama humano se encontra anomalia, divergencia ou decisao financeira. | `/app/relatorios/financeiro`, tarefa financeira. |
| D15 | Encerramento Ou Alteracao Efetiva De Plano | 3 | Checkpoint antes de encerrar, alterar, cobrar ou comunicar mudanca efetiva. | `/app/financeiro`, `/app/alunos/[id]`, aprovacao/caso. |

### Retencao - 13

| ID | Fluxo | Teto MVP | Parada principal | Onde continua |
|---|---|---:|---|---|
| E1 | Queda Frequencia | 4 | Chama humano se risco alto, evento pessoal ou historico sensivel aparece. | `/app/retencao/riscos`, `/app/alunos/[id]`, tarefa. |
| E2 | Aluno Inativo | 4 | Chama humano se contato pode ser invasivo, sem consentimento ou com risco comercial. | `/app/retencao/riscos`, tarefa/aprovacao. |
| E3 | Retorno | 4 | Chama humano se retorno exige agenda, financeiro ou regra fora do padrao. | `/app/retencao`, `/app/agenda`, tarefa. |
| E4 | Risco Cancelamento | 3 | Checkpoint antes de contato, proposta, pausa, desconto ou plano de retencao. | `/app/cancelamentos`, `/app/operacao`, aprovacao/caso. |
| E5 | Reativacao Ex-Aluno | 3 | Checkpoint antes de campanha, contato ou oferta para ex-aluno. | `/app/retencao/reativacoes`, `/app/aprovacoes`. |
| E6 | Satisfacao | 4 | Chama humano se feedback vira reclamacao, saude, professor ou risco alto. | `/app/retencao`, `/app/reclamacoes`, tarefa. |
| E7 | Retorno Apos Pausa | 4 | Chama humano se pausa envolve financeiro, saude, agenda ou excecao. | `/app/retencao`, `/app/agenda`, tarefa. |
| E8 | Risco Por Perfil | 3 | Checkpoint antes de aplicar segmento sensivel ou acao de retencao. | `/app/retencao/riscos`, aprovacao/tarefa. |
| E9 | Pos-Cancelamento | 3 | Checkpoint antes de contato, comunicacao ou oferta pos-cancelamento. | `/app/cancelamentos`, `/app/aprovacoes`, tarefa. |
| E10 | Marco Engajamento | 4 | Chama humano se marco exige contato sensivel, premio ou acao comercial. | `/app/retencao`, tarefa. |
| E11 | Saude/Evento Pessoal | 3 | Checkpoint/caso humano antes de qualquer acao sensivel. | `/app/operacao`, `/app/historico`, caso. |
| E12 | Segmentacao Risco | 3 | Checkpoint antes de usar segmento para campanha ou acao operacional. | `/app/retencao/riscos`, `/app/aprovacoes`. |
| E13 | Reclamacao E Recuperacao De Confianca | 3 | Checkpoint antes de resposta, compensacao ou resolucao; automacao pode pausar fluxos e preparar caso. | `/app/reclamacoes`, `/app/operacao`, `/app/aprovacoes`. |

### Gestao/Governanca - 15

| ID | Fluxo | Teto MVP | Parada principal | Onde continua |
|---|---|---:|---|---|
| F1 | Prioridades Dia | 5 | Bloqueia se falta dado critico; caso contrario gera lista/prioridade. | `/app/hoje`, `/app/tarefas`. |
| F2 | Dinheiro Na Mesa | 4 | Chama humano se recomenda acao financeira ou encontra anomalia. | `/app/dinheiro-na-mesa`, `/app/financeiro`, tarefa. |
| F3 | Fila Humana | 5 | Organiza fila e para se permissao/dono falta. | `/app/operacao`, `/app/aprovacoes`, `/app/tarefas`. |
| F4 | Gargalos | 4 | Chama humano se gargalo exige decisao operacional, equipe ou politica. | `/app/relatorios`, `/app/operacao`, tarefa. |
| F5 | Resumo Semanal | 5 | Bloqueia se dado base falta; caso contrario gera resumo. | `/app/relatorios/semana`, `/app/hoje`. |
| F6 | Qualidade Dados | 4 | Chama humano se correcao envolve merge, exclusao, permissao ou dado sensivel. | `/app/dados/qualidade`, `/app/dados/duplicidades`, tarefa. |
| F7 | Creditos/Limites | 5 | Alerta/degrada por cota; para automacao paga em 100%. | `/app/uso`, `/app/uso/cotas`, `/app/hoje`. |
| F8 | Performance | 4 | Chama humano se recomenda mudar configuracao, pausar ou investigar agente. | `/app/relatorios/agentes`, `/app/agentes`, tarefa. |
| F9 | Permissoes/Auditoria | 3 | Checkpoint antes de permissao, revisao sensivel ou acao auditavel. | `/app/auditoria`, `/app/configuracoes/permissoes`, aprovacao. |
| F10 | Capacidade/Crescimento | 4 | Chama humano se sugestao envolve grade, contratacao, turma ou politica. | `/app/relatorios/ocupacao`, `/app/agenda`, tarefa. |
| F11 | Falhas/Webhooks | 4 | Chama humano se reprocessamento nao e idempotente ou provedor exige acao tecnica. | `configuracao especifica da integracao`, `/app/operacao/incidentes`. |
| F12 | Importacao/Migracao | 3 | Checkpoint antes de aplicar importacao, merge ou correcao em lote. | `/app/importacao/[jobId]`, `/app/dados/qualidade`, aprovacao. |
| F13 | Teste De Fluxo | 5 | Roda simulacao e bloqueia publicacao se falha; nao publica sozinho. | `/app/fluxos/[flowId]/simular`, `/app/fluxos/[flowId]`. |
| F14 | Incidente De Automacao E Correcao Operacional | 4 | Chama humano se correcao exige decisao, impacto externo ou rollback. | `/app/operacao/incidentes/[incidentId]`, `/app/fluxos/execucoes/[runId]`. |
| F15 | Mudanca De Politica Ou Regra Operacional | 3 | Checkpoint com simulacao antes de regra entrar em vigor. | `/app/politicas/[policyId]`, `/app/aprovacoes`, auditoria. |

### Historico/Evolucao - 12

| ID | Fluxo | Teto MVP | Parada principal | Onde continua |
|---|---|---:|---|---|
| G1 | Contexto Antes Aula | 4 | Chama humano se contexto tem dado sensivel, restricao ou permissao incompleta. | `/app/professores`, `/app/aulas/[id]`, tarefa. |
| G2 | Observacao Pos-Aula | 4 | Chama humano se nota envolve saude, restricao, conflito ou dado sensivel. | `/app/aulas/[id]`, `/app/historico`, tarefa. |
| G3 | Restricao/Cuidado | 3 | Checkpoint/caso humano antes de registrar ou usar restricao sensivel. | `/app/historico`, `/app/alunos/[id]`, caso/aprovacao. |
| G4 | Objetivo/Evolucao | 4 | Chama humano se evolucao exige avaliacao humana/professor ou decisao sensivel. | `/app/alunos/[id]/linha-do-tempo`, tarefa. |
| G5 | Contexto Para Agente | 3 | Checkpoint antes de liberar contexto sensivel para agente/fluxo. | `/app/historico/permissoes`, `/app/aprovacoes`. |
| G6 | Documentos/Anamnese | 3 | Checkpoint antes de aceitar, compartilhar ou agir sobre documento/anamnese. | `/app/historico/documentos`, `/app/aprovacoes`, tarefa. |
| G7 | Correcao Historico | 3 | Checkpoint antes de corrigir evento historico auditavel. | `/app/historico`, `/app/auditoria`, aprovacao. |
| G8 | Repasse Entre Professores | 4 | Chama humano se troca envolve restricao, conflito, privacidade ou falta de contexto. | `/app/professores`, `/app/tarefas`. |
| G9 | Lembrete Professor | 5 | Lembra nota pendente; bloqueia se permissao/professor/aula falta. | `/app/professores`, `/app/tarefas`. |
| G10 | Compartilhar Contexto | 3 | Checkpoint antes de compartilhar qualquer contexto com aluno, equipe ou agente. | `/app/aprovacoes`, `/app/conversas/[id]`. |
| G11 | Permissao Historico | 3 | Checkpoint antes de mudar visibilidade ou papel de acesso. | `/app/historico/permissoes`, `/app/configuracoes/permissoes`, auditoria. |
| G12 | Linha Do Tempo | 4 | Chama humano se conflito, dado sensivel ou correcao necessaria aparece. | `/app/alunos/[id]/linha-do-tempo`, tarefa. |

## Contagem Por Teto

| Teto MVP | Quantidade | Leitura |
|---:|---:|---|
| 1 | 0 | Nenhum fluxo precisa ficar preso ao manual como teto de produto. |
| 2 | 0 | Nenhum fluxo precisa ficar preso ao copiloto como teto de produto. |
| 3 | 42 | O agente adianta o trabalho, mas para em aprovacoes obrigatorias. |
| 4 | 40 | O agente conduz e chama humano quando aparece excecao. |
| 5 | 14 | O agente resolve o caso comum sozinho dentro de limites. |
| Total | 96 | Todos os fluxos participam da automacao, com tetos diferentes. |

## O Que O Usuario Configura

Para todos os niveis, o usuario pode escolher operar abaixo do teto.

Configuracoes simples:

- preset: conservador, equilibrado ou crescimento;
- pacote;
- modo do fluxo: manual, copiloto ou autonomo;
- nivel autonomo quando aplicavel: autonomo com aprovacao, autonomo com excecoes ou autonomo;
- responsavel humano/fila;
- aprovadores;
- templates permitidos;
- limites de tentativa, horario, frequencia e cota;
- gatilhos para chamar humano;
- aprovacoes obrigatorias;
- fallback;
- pausa automatica;
- simulacao antes de publicar.

O usuario nao configura prompt livre nem regra tecnica interna. Ele configura comportamento operacional.

## Onde A Operacao Continua

| Parada | Superficie principal | Uso |
|---|---|---|
| Checkpoint | `/app/aprovacoes` | Aprovar, editar, rejeitar ou transformar em tarefa. |
| Chamada humana | `/app/tarefas`, `/app/operacao`, fila da tela de origem | Humano assume com resumo e proxima acao. |
| Bloqueio por dado | `/app/dados/qualidade` ou tela de origem | Corrigir dado ou criar tarefa. |
| Bloqueio por integracao | `configuracao especifica da integracao` | Ver provedor, log, erro e fallback manual. |
| Bloqueio por cota | `/app/uso`, `/app/uso/cotas`, `/app/hoje` | Entrar em economia, comprar/solicitar pacote ou operar manual. |
| Incidente | `/app/operacao/incidentes/[incidentId]` | Investigar, pausar, corrigir ou reprocessar se seguro. |
| Execucao | `/app/fluxos/execucoes/[runId]` | Entender o que rodou, custo, erro, resultado e auditoria. |

## Criterios De Aceite

Esta matriz esta correta quando:

- lista os 96 fluxos;
- nenhum fluxo fica limitado a manual/copiloto como teto conceitual;
- todo fluxo tem um teto de automacao;
- todo fluxo tem uma forma clara de parar;
- todo fluxo tem uma superficie de continuidade operacional;
- pontos de aprovacao viram aprovacoes;
- chamadas humanas viram tarefas, casos ou filas;
- bloqueios viram pendencias, alertas, incidentes ou execucoes investigaveis;
- o dono/admin nao precisa configurar 96 fluxos manualmente, porque pacotes e presets continuam sendo a entrada principal.
