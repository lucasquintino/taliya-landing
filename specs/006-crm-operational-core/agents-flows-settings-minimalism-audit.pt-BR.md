# Taliya CRM - Auditoria De Configuracoes Minimas Dos Fluxos

Status: auditoria aplicada v0.1.
Data: 2026-05-22.

## Objetivo

Revisar os 96 fluxos para garantir que `ajustes_do_studio` contenha somente configuracoes realmente importantes para aquele fluxo.

O problema encontrado foi exemplificado por `Falta com aviso`: `destino da reposicao` parecia configurar reposicao dentro de um fluxo que deveria apenas registrar falta avisada e encaminhar o proximo passo.

## Criterio Usado

Um item fica como ajuste do fluxo somente quando o dono/admin pode mudar aquilo e essa mudanca melhora a operacao daquele fluxo.

Nao fica como ajuste do fluxo quando for:

- requisito fixo/preflight: canal conectado, permissao, cota, auditoria, dado obrigatorio;
- dado calculado: impacto, capacidade real, conflito, risco, cota consumida;
- politica global ou configuracao base: planos, billing, integracao tecnica, fonte de dados global;
- responsabilidade principal de outra rotina: reposicao, agenda, lista de espera, historico protegido;
- mecanismo interno: fallback, simulacao obrigatoria, retry tecnico, auditoria.

## Resultado

- Fluxos auditados: 96.
- Fluxos corrigidos: 20.
- Fluxos mantidos sem alteracao: 76.

## Correcoes Aplicadas

| ID | Fluxo | Antes | Depois | Motivo |
|---|---|---|---|---|
| A2 | Duvidas permitidas | base/template permitido; limite por conversa; fallback | tom/template de resposta; limite por conversa; quando chamar humano | `fallback` nao e ajuste do studio; base aprovada e fonte de conteudo, nao liberdade solta dentro do fluxo. |
| A3 | Aluno existente | fila; dados que exigem humano; botao de ajuda | fila de atendimento; dados que chamam humano; botao chamar humano | Renomeado para deixar claro que sao regras de handoff e entrada da conversa. |
| A5 | Chamada humana | fila destino; prioridade; resumo obrigatorio | fila de handoff; prioridade inicial; campos do resumo | `resumo obrigatorio` era requisito de execucao; o ajuste real sao os campos do resumo. |
| B2 | Falta com aviso | prazo para aviso; destino da reposicao; responsaveis por excecao; tom/template da mensagem | prazo para aviso; proximo passo apos falta; responsaveis por excecao; tom/template da mensagem | `destino da reposicao` invadia a rotina de reposicoes; aqui o fluxo so registra a falta e encaminha o proximo passo. |
| B5 | Reposicao/remarcacao | aprovador; regras de credito visiveis; responsavel | aprovador; prazo maximo da reposicao; responsavel por excecao | `regras de credito` sao politica/configuracao; o fluxo ajusta prazo operacional e excecao. |
| B11 | Ajuste de grade | aprovador; data de vigencia; simulacao obrigatoria | aprovador; data de vigencia; escopo da mudanca | Simulacao e requisito de publicacao, nao ajuste. |
| B13 | Creditos reposicao | aprovador; validade; destino de excecoes | aprovador; validade do credito; responsavel por excecao | `destino de excecoes` estava vago; o ajuste real e quem resolve a excecao. |
| C1 | Valores e planos | template/base de planos; quando chamar humano | tom/template de resposta; quando chamar humano | Planos e valores vem da configuracao de Planos; este fluxo so ajusta resposta e handoff. |
| C12 | Demanda sem vaga | lista de espera; responsavel; regra de promessa | proximo passo sem vaga; responsavel; promessa permitida | Lista de espera pertence a Agenda; Vendas define o proximo passo e o que pode prometer. |
| C13 | Interessado para aluno | aprovador; plano; checklist de matricula | aprovador; checklist de matricula; responsavel comercial | Plano escolhido e dado do aluno/proposta; nao configuracao do fluxo. |
| D7 | Falha pagamento | fila; tentativas; quando abrir caso | fila financeira; tentativas; quando abrir caso | Renomeado para evitar fila generica. |
| D8 | Recibo/nota | responsavel; documentos permitidos; fallback | responsavel; tipo de documento; quando abrir tarefa | Fallback e mecanismo fixo; o ajuste e qual documento tratar e quando virar tarefa. |
| D9 | Pausa/trancamento | aprovador; impacto em agenda/cobranca; prazo | aprovador; data de inicio/fim; prazo de aprovacao | Impacto em agenda/cobranca e calculado/read-only, nao campo livre. |
| D15 | Encerramento ou alteracao efetiva de plano | aprovador; checklist; comunicacao | aprovador; checklist; template de comunicacao | Renomeado para mostrar o ajuste real. |
| E3 | Retorno | responsavel; regra de agenda; quando chamar humano | responsavel; tipo de retorno; quando chamar Agenda | Regra de agenda pertence a Agenda; Retencao decide quando envolver Agenda. |
| E7 | Retorno apos pausa | antecedencia; responsavel; regra de agenda | antecedencia; responsavel; quando chamar Agenda | Regra de agenda pertence a Agenda; este fluxo so define quando acionar Agenda. |
| F7 | Creditos/limites | alertas 70/90/100; responsavel; economia | limiares de alerta; responsavel; mensagem interna | Economia/cota vem de Uso/Billing; o fluxo ajusta alertas e mensagem interna. |
| F11 | Falhas/webhooks | responsavel; severidade; retry seguro | responsavel; severidade; quando tentar novamente | Retry tecnico pertence a integracao; o fluxo define quando tentar de novo. |
| F15 | Mudanca de politica ou regra operacional | aprovador; data de vigencia; simulacao | aprovador; data de vigencia; resumo da mudanca | Simulacao e requisito; ajuste real e a descricao/resumo da mudanca. |
| G4 | Objetivo/evolucao | professor/responsavel; frequencia; tarefa | professor/responsavel; frequencia; quando abrir tarefa | `tarefa` sozinho nao explica o comportamento ajustavel. |

## Matriz Final De Ajustes

| ID | Agente | Rotina | Fluxo | Status | Ajustes finais |
|---|---|---|---|---|---|
| A1 | Atendimento | Conversas e triagem | Nova conversa | Mantido | fila de atendimento; limite de respostas; quando chamar humano |
| A2 | Atendimento | Conversas e triagem | Duvidas permitidas | Corrigido | tom/template de resposta; limite por conversa; quando chamar humano |
| A3 | Atendimento | Conversas e triagem | Aluno existente | Corrigido | fila de atendimento; dados que chamam humano; botao chamar humano |
| A4 | Atendimento | Conversas e triagem | Fora do escopo | Mantido | resposta padrao; destino da tarefa/caso |
| A5 | Atendimento | Conversas e triagem | Chamada humana | Corrigido | fila de handoff; prioridade inicial; campos do resumo |
| A6 | Atendimento | Identidade e privacidade | Consentimento/opt-out | Mantido | texto de confirmacao; responsavel de revisao em caso ambiguo |
| A7 | Atendimento | Identidade e privacidade | Identidade/midias | Mantido | responsavel de revisao; tipos de midia aceitos |
| A8 | Atendimento | Identidade e privacidade | Privacidade/dados | Mantido | aprovador de privacidade; SLA do caso |
| A9 | Atendimento | Identidade e privacidade | Telefone compartilhado e identidade | Mantido | regra de validacao; responsavel de revisao |
| A10 | Atendimento | Conversas e triagem | Ciclo de vida/SLA | Mantido | tempo de SLA; fila destino; prioridade |
| B1 | Agenda | Presenca e faltas | Confirmacao de presenca | Mantido | horario do lembrete; tom/template; limite por aula |
| B2 | Agenda | Presenca e faltas | Falta com aviso | Corrigido | prazo para aviso; proximo passo apos falta; responsaveis por excecao; tom/template da mensagem |
| B3 | Agenda | Presenca e faltas | No-show | Mantido | quando vira tarefa de retencao; responsavel |
| B4 | Agenda | Vagas, reposicoes e lista de espera | Recuperar vaga aberta | Mantido | prioridade da lista; limite de convites; aprovador se lote |
| B5 | Agenda | Vagas, reposicoes e lista de espera | Reposicao/remarcacao | Corrigido | aprovador; prazo maximo da reposicao; responsavel por excecao |
| B6 | Agenda | Vagas, reposicoes e lista de espera | Lista de espera | Mantido | prioridade; limite de convites; responsavel por excecao |
| B7 | Agenda | Agenda experimental | Disponibilidade experimental | Mantido | responsavel comercial; horarios oferecidos; quando chamar humano |
| B8 | Agenda | Grade e capacidade | Mudanca horario fixo | Mantido | aprovador; prazo; mensagem de confirmacao |
| B9 | Agenda | Grade e capacidade | Cancelamento pelo studio | Mantido | aprovador; template de comunicado; quem trata excecoes |
| B10 | Agenda | Grade e capacidade | Conflito capacidade | Mantido | aprovador; responsavel do caso; prioridade |
| B11 | Agenda | Grade e capacidade | Ajuste de grade | Corrigido | aprovador; data de vigencia; escopo da mudanca |
| B12 | Agenda | Agenda experimental | Experimental no-show | Mantido | cadencia; responsavel comercial; limite de contato |
| B13 | Agenda | Vagas, reposicoes e lista de espera | Creditos reposicao | Corrigido | aprovador; validade do credito; responsavel por excecao |
| B14 | Agenda | Presenca e faltas | Correcao presenca | Mantido | aprovador; motivo obrigatorio; prazo de aprovacao |
| B15 | Agenda | Primeira aula e aulas especiais | Primeira aula | Mantido | checklist; responsavel; quando chamar humano |
| B16 | Agenda | Primeira aula e aulas especiais | Aula especial/workshop | Mantido | aprovador; capacidade; template; prazo |
| C1 | Vendas | Conversao e matricula | Valores e planos | Corrigido | tom/template de resposta; quando chamar humano |
| C2 | Vendas | Experimental e acompanhamento | Aula experimental | Mantido | horarios oferecidos; responsavel; limite de tentativas |
| C3 | Vendas | Experimental e acompanhamento | Lembrete experimental | Mantido | horario do lembrete; template; limite por aula |
| C4 | Vendas | Experimental e acompanhamento | Pos-aula experimental | Mantido | cadencia; responsavel; quando virar tarefa |
| C5 | Vendas | Experimental e acompanhamento | Follow-up comercial | Mantido | cadencia; limite de tentativas; responsavel |
| C6 | Vendas | Conversao e matricula | Pre-matricula | Mantido | aprovador; checklist; responsavel comercial |
| C7 | Vendas | Conversao e matricula | Objecoes | Mantido | aprovador; base de respostas; limite de promessa |
| C8 | Vendas | Captura e qualificacao | Origem/qualificacao | Mantido | campos obrigatorios; responsavel; regra de duplicidade |
| C9 | Vendas | Captura e qualificacao | Perda comercial | Mantido | motivo; aprovador se perda sensivel; responsavel |
| C10 | Vendas | Captura e qualificacao | Indicacao | Mantido | aprovador de beneficio; regra de vinculo |
| C11 | Vendas | Conversao e matricula | Checkout/abandono | Mantido | cadencia; responsavel; limite de contato |
| C12 | Vendas | Experimental e acompanhamento | Demanda sem vaga | Corrigido | proximo passo sem vaga; responsavel; promessa permitida |
| C13 | Vendas | Conversao e matricula | Interessado para aluno | Corrigido | aprovador; checklist de matricula; responsavel comercial |
| C14 | Vendas | Conversao e matricula | Upsell/upgrade | Mantido | aprovador; template de proposta; responsavel |
| C15 | Vendas | Captura e qualificacao | Entrada multicanal de lead | Mantido | fontes aceitas; dono do lead; regra de duplicidade |
| D1 | Financeiro | Lembretes e pagamentos | Lembrete vencimento | Mantido | horario; template; limite por cobranca |
| D2 | Financeiro | Lembretes e pagamentos | Pagamento atrasado | Mantido | tentativas; fila financeira; sinais que chamam humano |
| D3 | Financeiro | Lembretes e pagamentos | Pix/link | Mantido | aprovador; template; limite de valor |
| D4 | Financeiro | Excecoes e documentos financeiros | Confirmacao pagamento | Mantido | aprovador; evidencia exigida; responsavel |
| D5 | Financeiro | Ciclo do plano do aluno | Renovacao plano | Mantido | aprovador; antecedencia; template |
| D6 | Financeiro | Excecoes e documentos financeiros | Excecoes financeiras | Mantido | aprovador obrigatorio; tipos de excecao; prazo |
| D7 | Financeiro | Lembretes e pagamentos | Falha pagamento | Corrigido | fila financeira; tentativas; quando abrir caso |
| D8 | Financeiro | Lembretes e pagamentos | Recibo/nota | Corrigido | responsavel; tipo de documento; quando abrir tarefa |
| D9 | Financeiro | Ciclo do plano do aluno | Pausa/trancamento | Corrigido | aprovador; data de inicio/fim; prazo de aprovacao |
| D10 | Financeiro | Lembretes e pagamentos | Conciliacao interna | Mantido | aprovador; confianca minima; responsavel |
| D11 | Financeiro | Excecoes e documentos financeiros | Contrato/termos | Mantido | aprovador; template; prazo |
| D12 | Financeiro | Excecoes e documentos financeiros | Bloqueio/liberacao | Mantido | aprovador; motivo obrigatorio; prazo de aprovacao |
| D13 | Financeiro | Excecoes e documentos financeiros | Creditos/cortesias | Mantido | aprovador; limite de valor; motivo |
| D14 | Financeiro | Excecoes e documentos financeiros | Fechamento mensal | Mantido | responsavel; frequencia; quando abrir tarefa |
| D15 | Financeiro | Ciclo do plano do aluno | Encerramento ou alteracao efetiva de plano | Corrigido | aprovador; checklist; template de comunicacao |
| E1 | Retencao | Retencao preventiva | Queda frequencia | Mantido | regra de queda; responsavel; cadencia |
| E2 | Retencao | Retencao preventiva | Aluno inativo | Mantido | dias de inatividade; responsavel; limite de contato |
| E3 | Retencao | Retencao preventiva | Retorno | Corrigido | responsavel; tipo de retorno; quando chamar Agenda |
| E4 | Retencao | Casos sensiveis | Risco cancelamento | Mantido | dono do caso; aprovador; pausa de automacoes |
| E5 | Retencao | Casos sensiveis | Reativacao ex-aluno | Mantido | aprovador; segmento permitido; cadencia |
| E6 | Retencao | Retencao preventiva | Satisfacao | Mantido | janela; responsavel; quando abrir reclamacao |
| E7 | Retencao | Retencao preventiva | Retorno apos pausa | Corrigido | antecedencia; responsavel; quando chamar Agenda |
| E8 | Retencao | Casos sensiveis | Risco por perfil | Mantido | aprovador; uso do segmento; responsavel |
| E9 | Retencao | Casos sensiveis | Pos-cancelamento | Mantido | aprovador; quando contatar; responsavel |
| E10 | Retencao | Retencao preventiva | Marco engajamento | Mantido | tipo de marco; responsavel; limite de contato |
| E11 | Retencao | Casos sensiveis | Saude/evento pessoal | Mantido | dono do caso; visibilidade; aprovador |
| E12 | Retencao | Casos sensiveis | Segmentacao risco | Mantido | aprovador; segmento; acao permitida |
| E13 | Retencao | Casos sensiveis | Reclamacao e recuperacao de confianca | Mantido | dono do caso; aprovador; pausa automatica |
| F1 | Gestao/Governanca | Comando operacional | Prioridades dia | Mantido | horario do resumo; responsavel; fontes exibidas |
| F2 | Gestao/Governanca | Comando operacional | Dinheiro na mesa | Mantido | frequencia; responsavel; quando abrir tarefa |
| F3 | Gestao/Governanca | Comando operacional | Fila humana | Mantido | filas; prioridade; responsaveis |
| F4 | Gestao/Governanca | Comando operacional | Gargalos | Mantido | frequencia; responsavel; tipo de alerta |
| F5 | Gestao/Governanca | Comando operacional | Resumo semanal | Mantido | dia/hora; destinatarios internos; secoes |
| F6 | Gestao/Governanca | Comando operacional | Qualidade dados | Mantido | responsavel; tipos de dado; prioridade |
| F7 | Gestao/Governanca | Governanca de agentes | Creditos/limites | Corrigido | limiares de alerta; responsavel; mensagem interna |
| F8 | Gestao/Governanca | Governanca de agentes | Performance | Mantido | frequencia; responsavel; metricas exibidas |
| F9 | Gestao/Governanca | Governanca de agentes | Permissoes/auditoria | Mantido | aprovador; tipos de evento; responsavel |
| F10 | Gestao/Governanca | Comando operacional | Capacidade/crescimento | Mantido | frequencia; responsavel; limite de alerta |
| F11 | Gestao/Governanca | Integracoes e importacao | Falhas/webhooks | Corrigido | responsavel; severidade; quando tentar novamente |
| F12 | Gestao/Governanca | Integracoes e importacao | Importacao/migracao | Mantido | aprovador; lote; responsavel |
| F13 | Gestao/Governanca | Governanca de agentes | Teste de fluxo | Mantido | exemplos de simulacao; responsavel |
| F14 | Gestao/Governanca | Governanca de agentes | Incidente de automacao e correcao operacional | Mantido | severidade; responsavel; auto-pausa |
| F15 | Gestao/Governanca | Governanca de agentes | Mudanca de politica ou regra operacional | Corrigido | aprovador; data de vigencia; resumo da mudanca |
| G1 | Historico/Evolucao | Aula com contexto | Contexto antes aula | Mantido | visibilidade; professor; quando chamar humano |
| G2 | Historico/Evolucao | Aula com contexto | Observacao pos-aula | Mantido | lembrete; professor; tipos de nota |
| G3 | Historico/Evolucao | Historico protegido | Restricao/cuidado | Mantido | aprovador; visibilidade; dono do caso |
| G4 | Historico/Evolucao | Aula com contexto | Objetivo/evolucao | Corrigido | professor/responsavel; frequencia; quando abrir tarefa |
| G5 | Historico/Evolucao | Historico protegido | Contexto para agente | Mantido | aprovador; dados permitidos; escopo |
| G6 | Historico/Evolucao | Historico protegido | Documentos/anamnese | Mantido | aprovador; documentos exigidos; responsavel |
| G7 | Historico/Evolucao | Historico protegido | Correcao historico | Mantido | aprovador; motivo obrigatorio; prazo de aprovacao |
| G8 | Historico/Evolucao | Aula com contexto | Repasse entre professores | Mantido | professor destino; campos do resumo; quando chamar humano |
| G9 | Historico/Evolucao | Aula com contexto | Lembrete professor | Mantido | horario; frequencia; destino |
| G10 | Historico/Evolucao | Historico protegido | Compartilhar contexto | Mantido | aprovador; destinatario; dados permitidos |
| G11 | Historico/Evolucao | Historico protegido | Permissao historico | Mantido | aprovador; papel; escopo de visibilidade |
| G12 | Historico/Evolucao | Aula com contexto | Linha do tempo | Mantido | tipos de evento; filtro padrao; responsavel |

## Decisao Especifica: Falta Com Aviso

`Falta com aviso` nao configura reposicao profundamente.

Ele configura:

- prazo para aceitar o aviso como falta avisada;
- proximo passo apos a falta;
- responsaveis por excecao;
- tom/template da mensagem.

A rotina `Vagas, reposicoes e lista de espera` continua dona da logica de reposicao, vaga, prioridade e lista.

## Relacao Com Encadeamento

Esta auditoria nao quer dizer que os fluxos sao isolados.

O correto e:

```text
um fluxo pode emendar em outro fluxo;
mas um fluxo nao configura o outro.
```

Por isso `Falta com aviso` pode continuar em `Reposicao/remarcacao`, mas nao deve editar prioridade de vaga, regra de credito ou lista de espera dentro da propria pagina.

Na UI, essa continuidade aparece no `Fim` do bloco `Como funciona neste modo`.

Nao colocar consequencias dentro de `Segue sozinho quando`; esse grupo deve ter apenas condicoes para o fluxo atual executar.

Contrato complementar:

```text
agents-flows-chain-contract.pt-BR.md
```

## Arquivos Atualizados

- `agents-flows-final-flow-contract-matrix.pt-BR.csv`
- `agents-flows-detailed-mode-rules-matrix.pt-BR.csv`
- `agents-flows-detailed-mode-rules-review.pt-BR.md`
- `agents-flows-chain-contract.pt-BR.md`
- `scripts/generate-taliya-detailed-mode-rules.py`
