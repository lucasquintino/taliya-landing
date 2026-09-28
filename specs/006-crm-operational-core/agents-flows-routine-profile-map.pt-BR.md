# Taliya CRM - Mapa Exato De Perfis Por Rotina

Status: contrato funcional v0.1.
Data: 2026-05-21.

## Objetivo

Definir exatamente como os perfis de rotina configuram os fluxos de todos os agentes.

Este documento complementa:

- `agents-flows-routines-pages-final-contract.pt-BR.md`

Onde houver conflito com matrizes antigas de `default_publicado`, este mapa vence para a UI.

Leitura:

- `Mais autonomo` e o perfil inicial exibido nas paginas de rotina quando o plano e o preflight permitem;
- `Mais autonomo` representa o maior modo recomendado pelo teto de cada fluxo;
- `Equilibrado` continua disponivel para studios que querem mais revisao humana;
- `default_publicado` de documentos antigos nao deve obrigar o perfil Equilibrado a usar o teto.

Regra principal:

```text
O usuario escolhe o perfil da rotina.
O perfil aplica modos nos fluxos da rotina.
O usuario so entra no fluxo individual quando precisar personalizar.
```

## Legenda

| Nome curto | Nome na UI |
|---|---|
| Manual | Manual |
| Copiloto | Copiloto |
| Aprovacao | Autonomo com aprovacao |
| Excecoes | Autonomo com excecoes |
| Direto | Autonomo |

## Regras Globais

### Mais Manual

Serve para studios que querem humano conduzindo quase tudo.

Padrao:

- fluxos simples ficam em Copiloto;
- fluxos sensiveis ficam em Manual ou Copiloto;
- autonomos so aparecem quando o proprio resultado e organizar, alertar ou chamar humano.

### Equilibrado

Serve como default recomendado para a maioria dos studios.

Padrao:

- casos simples podem rodar autonomos;
- casos com excecao chamam humano;
- fluxos que exigem julgamento comercial, relacionamento, analise ou recorrencia podem ficar em Copiloto;
- casos sensiveis pedem aprovacao;
- o dono entende o que vai acontecer antes de publicar.

### Mais Autonomo

Serve para studios que querem mais operacao conduzida por agentes.

Padrao:

- cada fluxo sobe ate o maior modo permitido pelo seu teto;
- nenhum fluxo ultrapassa o teto;
- aprovacoes, excecoes, cota, permissao e integracao continuam valendo;
- se houver bloqueio, o modo e rebaixado ou a publicacao bloqueia.

Leitura importante:

```text
Equilibrado nao precisa ser igual ao teto do fluxo.
Mais autonomo tende a usar o teto do fluxo.
```

## Atendimento

### Rotina: Conversas E Triagem

Rota:

```text
/app/agentes/atendimento/rotinas/conversas-e-triagem
```

| ID | Fluxo | Mais manual | Equilibrado | Mais autonomo |
|---|---|---|---|---|
| A1 | Nova Conversa | Copiloto | Excecoes | Excecoes |
| A2 | Duvidas Permitidas | Copiloto | Direto | Direto |
| A3 | Aluno Existente | Copiloto | Excecoes | Excecoes |
| A4 | Fora Do Escopo | Copiloto | Direto | Direto |
| A5 | Chamada Humana | Direto | Direto | Direto |
| A10 | Ciclo De Vida/SLA | Copiloto | Direto | Direto |

Explicacao na pagina:

- Mais manual: o agente organiza conversas e sugere respostas, mas a equipe decide.
- Equilibrado: perguntas permitidas e fora de escopo sao tratadas automaticamente; casos ambiguos chamam humano.
- Mais autonomo: o agente conduz tudo que estiver dentro da base aprovada e chama humano quando sair do escopo.

### Rotina: Identidade E Privacidade

Rota:

```text
/app/agentes/atendimento/rotinas/identidade-e-privacidade
```

| ID | Fluxo | Mais manual | Equilibrado | Mais autonomo |
|---|---|---|---|---|
| A6 | Consentimento/Opt-Out | Direto | Direto | Direto |
| A7 | Identidade/Midias | Copiloto | Excecoes | Excecoes |
| A8 | Privacidade/Dados | Manual | Aprovacao | Aprovacao |
| A9 | Telefone Compartilhado E Identidade | Manual | Aprovacao | Aprovacao |

Explicacao na pagina:

- Mais manual: opt-out continua autonomo, mas identidade e privacidade ficam com humano.
- Equilibrado: opt-out roda sozinho; midias incertas chamam humano; privacidade pede aprovacao.
- Mais autonomo: o agente adianta triagens, mas pedidos de dado e identidade ambigua continuam com aprovacao.

## Agenda

### Rotina: Presenca E Faltas

Rota:

```text
/app/agentes/agenda/rotinas/presenca-e-faltas
```

| ID | Fluxo | Mais manual | Equilibrado | Mais autonomo |
|---|---|---|---|---|
| B1 | Confirmacao De Presenca | Copiloto | Direto | Direto |
| B2 | Falta Com Aviso | Manual | Excecoes | Excecoes |
| B3 | No-Show | Manual | Copiloto | Excecoes |
| B14 | Correcao Presenca | Manual | Aprovacao | Aprovacao |

Explicacao na pagina:

- Mais manual: a equipe confirma, registra faltas e trata no-show; o agente ajuda quando solicitado.
- Equilibrado: confirmacoes simples rodam sozinhas; falta avisada roda com excecoes; no-show vira sugestao; correcao pede aprovacao.
- Mais autonomo: confirmacao, falta clara e no-show comum rodam com excecoes; correcao auditavel continua com aprovacao.

### Rotina: Vagas, Reposicoes E Lista De Espera

Rota:

```text
/app/agentes/agenda/rotinas/vagas-reposicoes-lista-espera
```

| ID | Fluxo | Mais manual | Equilibrado | Mais autonomo |
|---|---|---|---|---|
| B4 | Recuperar Vaga Aberta | Copiloto | Copiloto | Excecoes |
| B5 | Reposicao/Remarcacao | Manual | Aprovacao | Aprovacao |
| B6 | Lista De Espera | Copiloto | Excecoes | Excecoes |
| B13 | Creditos Reposicao | Manual | Aprovacao | Aprovacao |

Explicacao na pagina:

- Mais manual: o agente sugere vagas e reposicoes, mas a equipe confirma.
- Equilibrado: lista de espera roda em casos claros; vaga aberta vira sugestao; reposicao e credito pedem aprovacao.
- Mais autonomo: o agente conduz o que estiver dentro da regra e chama humano para excecoes ou impacto em credito.

### Rotina: Grade E Capacidade

Rota:

```text
/app/agentes/agenda/rotinas/grade-e-capacidade
```

| ID | Fluxo | Mais manual | Equilibrado | Mais autonomo |
|---|---|---|---|---|
| B8 | Mudanca Horario Fixo | Manual | Aprovacao | Aprovacao |
| B9 | Cancelamento Pelo Studio | Manual | Aprovacao | Aprovacao |
| B10 | Conflito Capacidade | Copiloto | Aprovacao | Aprovacao |
| B11 | Ajuste De Grade | Manual | Aprovacao | Aprovacao |

Explicacao na pagina:

- Mais manual: a rotina so organiza impacto e tarefas.
- Equilibrado: o agente prepara a mudanca e para em aprovacao antes de afetar agenda ou alunos.
- Mais autonomo: o agente adianta simulacao, comunicacao e preparo, mas toda mudanca estrutural continua exigindo aprovacao.

### Rotina: Primeira Aula E Aulas Especiais

Rota:

```text
/app/agentes/agenda/rotinas/primeira-aula-aulas-especiais
```

| ID | Fluxo | Mais manual | Equilibrado | Mais autonomo |
|---|---|---|---|---|
| B15 | Primeira Aula | Copiloto | Excecoes | Excecoes |
| B16 | Aula Especial/Workshop | Manual | Aprovacao | Aprovacao |

Explicacao na pagina:

- Mais manual: o agente organiza checklist e sugestoes; equipe conduz.
- Equilibrado: primeira aula roda com excecoes; workshop pede aprovacao.
- Mais autonomo: primeira aula conduz casos normais; eventos continuam com aprovacao antes de publicar/comunicar.

### Rotina: Agenda Experimental

Rota:

```text
/app/agentes/agenda/rotinas/agenda-experimental
```

| ID | Fluxo | Mais manual | Equilibrado | Mais autonomo |
|---|---|---|---|---|
| B7 | Disponibilidade Experimental | Copiloto | Copiloto | Excecoes |
| B12 | Experimental No-Show | Copiloto | Excecoes | Excecoes |

Explicacao na pagina:

- Mais manual: o agente sugere horarios e abordagens; equipe envia.
- Equilibrado: o agente sugere disponibilidade e conduz no-show experimental com excecoes.
- Mais autonomo: disponibilidade e no-show experimental rodam com excecoes e limites de contato.

## Vendas

### Rotina: Captura E Qualificacao

Rota:

```text
/app/agentes/vendas/rotinas/captura-e-qualificacao
```

| ID | Fluxo | Mais manual | Equilibrado | Mais autonomo |
|---|---|---|---|---|
| C15 | Entrada Multicanal De Lead | Copiloto | Excecoes | Excecoes |
| C8 | Origem/Qualificacao | Copiloto | Excecoes | Excecoes |
| C9 | Perda Comercial | Manual | Aprovacao | Aprovacao |
| C10 | Indicacao | Manual | Aprovacao | Aprovacao |

Explicacao na pagina:

- Mais manual: leads entram para triagem humana com ajuda do agente.
- Equilibrado: captura e qualificacao rodam com excecoes; perda e indicacao pedem aprovacao.
- Mais autonomo: o agente classifica casos claros, mas beneficios e perdas continuam aprovados por humano.

### Rotina: Experimental E Acompanhamento

Rota:

```text
/app/agentes/vendas/rotinas/experimental-e-acompanhamento
```

| ID | Fluxo | Mais manual | Equilibrado | Mais autonomo |
|---|---|---|---|---|
| C2 | Aula Experimental | Copiloto | Excecoes | Excecoes |
| C3 | Lembrete Experimental | Copiloto | Direto | Direto |
| C4 | Pos-Aula Experimental | Copiloto | Copiloto | Excecoes |
| C5 | Follow-Up Comercial | Copiloto | Copiloto | Excecoes |
| C12 | Demanda Sem Vaga | Copiloto | Copiloto | Excecoes |

Explicacao na pagina:

- Mais manual: o agente prepara lembretes e follow-ups; comercial decide.
- Equilibrado: lembrete simples roda sozinho; follow-up, pos-aula e demanda sem vaga ficam como sugestao para comercial.
- Mais autonomo: o agente conduz cadencias claras e chama humano para objecoes, desconto, promessa ou vaga sensivel.

### Rotina: Conversao E Matricula

Rota:

```text
/app/agentes/vendas/rotinas/conversao-e-matricula
```

| ID | Fluxo | Mais manual | Equilibrado | Mais autonomo |
|---|---|---|---|---|
| C1 | Valores E Planos | Copiloto | Copiloto | Excecoes |
| C6 | Pre-Matricula | Manual | Aprovacao | Aprovacao |
| C7 | Objecoes | Copiloto | Aprovacao | Aprovacao |
| C11 | Checkout/Abandono | Copiloto | Copiloto | Excecoes |
| C13 | Interessado Para Aluno | Manual | Aprovacao | Aprovacao |
| C14 | Upsell/Upgrade | Manual | Aprovacao | Aprovacao |

Explicacao na pagina:

- Mais manual: o agente prepara respostas e checklist, mas comercial/admin executa.
- Equilibrado: valores e abandono viram sugestao; matricula, objecoes sensiveis e upgrade pedem aprovacao.
- Mais autonomo: o agente conduz o maximo permitido, mas conversao, matricula e mudanca comercial continuam com aprovacao.

## Financeiro

### Rotina: Lembretes E Pagamentos

Rota:

```text
/app/agentes/financeiro/rotinas/lembretes-e-pagamentos
```

| ID | Fluxo | Mais manual | Equilibrado | Mais autonomo |
|---|---|---|---|---|
| D1 | Lembrete Vencimento | Copiloto | Direto | Direto |
| D2 | Pagamento Atrasado | Copiloto | Copiloto | Excecoes |
| D3 | Pix/Link | Manual | Aprovacao | Aprovacao |
| D7 | Falha Pagamento | Copiloto | Copiloto | Excecoes |
| D8 | Recibo/Nota | Copiloto | Copiloto | Excecoes |
| D10 | Conciliacao Interna | Manual | Aprovacao | Aprovacao |

Explicacao na pagina:

- Mais manual: financeiro recebe sugestoes, mas envia e confirma manualmente.
- Equilibrado: lembrete simples roda sozinho; atraso, falha e documento ficam como sugestao; link e conciliacao pedem aprovacao.
- Mais autonomo: o agente conduz cobrancas simples e casos claros; qualquer acordo, disputa ou match incerto continua com humano.

### Rotina: Ciclo Do Plano Do Aluno

Rota:

```text
/app/agentes/financeiro/rotinas/ciclo-do-plano-do-aluno
```

| ID | Fluxo | Mais manual | Equilibrado | Mais autonomo |
|---|---|---|---|---|
| D5 | Renovacao Plano | Manual | Aprovacao | Aprovacao |
| D9 | Pausa/Trancamento | Manual | Aprovacao | Aprovacao |
| D15 | Encerramento Ou Alteracao Efetiva De Plano | Manual | Aprovacao | Aprovacao |

Explicacao na pagina:

- Mais manual: o agente organiza casos e impacto; humano decide tudo.
- Equilibrado: o agente prepara renovacao, pausa ou encerramento e para em aprovacao.
- Mais autonomo: o agente adianta comunicacao, checklist e impacto, mas mudanca efetiva de plano nunca passa sem aprovacao.

### Rotina: Excecoes E Documentos Financeiros

Rota:

```text
/app/agentes/financeiro/rotinas/excecoes-documentos-financeiros
```

| ID | Fluxo | Mais manual | Equilibrado | Mais autonomo |
|---|---|---|---|---|
| D4 | Confirmacao Pagamento | Manual | Aprovacao | Aprovacao |
| D6 | Excecoes Financeiras | Manual | Aprovacao | Aprovacao |
| D11 | Contrato/Termos | Manual | Aprovacao | Aprovacao |
| D12 | Bloqueio/Liberacao | Manual | Aprovacao | Aprovacao |
| D13 | Creditos/Cortesias | Manual | Aprovacao | Aprovacao |
| D14 | Fechamento Mensal | Copiloto | Copiloto | Excecoes |

Explicacao na pagina:

- Mais manual: financeiro recebe organizacao e rascunhos, mas decide.
- Equilibrado: fechamento mensal vira resumo sugerido; acoes financeiras sensiveis pedem aprovacao.
- Mais autonomo: o agente antecipa analise e preparo, mas desconto, contrato, bloqueio, credito e confirmacao sensivel continuam com aprovacao.

## Retencao

### Rotina: Retencao Preventiva

Rota:

```text
/app/agentes/retencao/rotinas/retencao-preventiva
```

| ID | Fluxo | Mais manual | Equilibrado | Mais autonomo |
|---|---|---|---|---|
| E1 | Queda Frequencia | Copiloto | Excecoes | Excecoes |
| E2 | Aluno Inativo | Copiloto | Copiloto | Excecoes |
| E3 | Retorno | Copiloto | Copiloto | Excecoes |
| E6 | Satisfacao | Copiloto | Copiloto | Excecoes |
| E7 | Retorno Apos Pausa | Copiloto | Copiloto | Excecoes |
| E10 | Marco Engajamento | Copiloto | Copiloto | Excecoes |

Explicacao na pagina:

- Mais manual: o agente mostra sinais e sugere abordagem; equipe conduz.
- Equilibrado: queda de frequencia roda com excecoes; demais casos preventivos viram sugestao para a equipe.
- Mais autonomo: o agente conduz cadencias preventivas dentro dos limites e chama humano em risco, reclamacao ou contexto sensivel.

### Rotina: Casos Sensiveis

Rota:

```text
/app/agentes/retencao/rotinas/casos-sensiveis
```

| ID | Fluxo | Mais manual | Equilibrado | Mais autonomo |
|---|---|---|---|---|
| E4 | Risco Cancelamento | Manual | Aprovacao | Aprovacao |
| E5 | Reativacao Ex-Aluno | Copiloto | Aprovacao | Aprovacao |
| E8 | Risco Por Perfil | Manual | Aprovacao | Aprovacao |
| E9 | Pos-Cancelamento | Manual | Aprovacao | Aprovacao |
| E11 | Saude/Evento Pessoal | Manual | Aprovacao | Aprovacao |
| E12 | Segmentacao Risco | Manual | Aprovacao | Aprovacao |
| E13 | Reclamacao E Recuperacao De Confianca | Manual | Aprovacao | Aprovacao |

Explicacao na pagina:

- Mais manual: o agente organiza caso e contexto, mas nao conduz contato sensivel.
- Equilibrado: o agente prepara a acao e pede aprovacao antes de contato, oferta, pausa ou recuperacao.
- Mais autonomo: o agente adianta tudo que for seguro, mas casos sensiveis continuam parando em aprovacao.

## Gestao/Governanca

### Rotina: Comando Operacional

Rota:

```text
/app/agentes/gestao-governanca/rotinas/comando-operacional
```

| ID | Fluxo | Mais manual | Equilibrado | Mais autonomo |
|---|---|---|---|---|
| F1 | Prioridades Dia | Copiloto | Direto | Direto |
| F2 | Dinheiro Na Mesa | Copiloto | Copiloto | Excecoes |
| F3 | Fila Humana | Copiloto | Direto | Direto |
| F4 | Gargalos | Copiloto | Copiloto | Excecoes |
| F5 | Resumo Semanal | Copiloto | Direto | Direto |
| F6 | Qualidade Dados | Copiloto | Copiloto | Excecoes |
| F10 | Capacidade/Crescimento | Copiloto | Copiloto | Excecoes |

Explicacao na pagina:

- Mais manual: o agente organiza prioridades e relatorios, mas a equipe age.
- Equilibrado: resumos e filas rodam automaticamente; gargalos, dinheiro, qualidade e capacidade viram sugestoes/tarefas revisaveis.
- Mais autonomo: o agente monitora e abre tarefas, mas nao muda regra, grade, financeiro ou capacidade sozinho.

### Rotina: Governanca De Agentes

Rota:

```text
/app/agentes/gestao-governanca/rotinas/governanca-de-agentes
```

| ID | Fluxo | Mais manual | Equilibrado | Mais autonomo |
|---|---|---|---|---|
| F7 | Creditos/Limites | Copiloto | Direto | Direto |
| F8 | Performance | Copiloto | Copiloto | Excecoes |
| F9 | Permissoes/Auditoria | Manual | Aprovacao | Aprovacao |
| F13 | Teste De Fluxo | Copiloto | Direto | Direto |
| F14 | Incidente De Automacao E Correcao Operacional | Copiloto | Excecoes | Excecoes |
| F15 | Mudanca De Politica Ou Regra Operacional | Manual | Aprovacao | Aprovacao |

Explicacao na pagina:

- Mais manual: o agente explica uso, performance e incidentes; humano decide.
- Equilibrado: cotas e testes rodam automaticamente; performance vira sugestao; incidentes chamam humano; permissao e politica pedem aprovacao.
- Mais autonomo: o agente monitora, testa e pausa quando permitido, mas mudanca de politica/permissao continua com aprovacao.

### Rotina: Integracoes E Importacao

Rota:

```text
/app/agentes/gestao-governanca/rotinas/integracoes-e-importacao
```

| ID | Fluxo | Mais manual | Equilibrado | Mais autonomo |
|---|---|---|---|---|
| F11 | Falhas/Webhooks | Copiloto | Copiloto | Excecoes |
| F12 | Importacao/Migracao | Manual | Aprovacao | Aprovacao |

Explicacao na pagina:

- Mais manual: o agente explica falhas e prepara revisao.
- Equilibrado: falhas viram explicacao/sugestao operacional; importacao/migracao pede aprovacao.
- Mais autonomo: o agente pode auto-pausar e abrir incidente quando permitido, mas importacao e merge continuam com aprovacao.

## Historico/Professor

### Rotina: Aula Com Contexto

Rota:

```text
/app/agentes/historico-professor/rotinas/aula-com-contexto
```

| ID | Fluxo | Mais manual | Equilibrado | Mais autonomo |
|---|---|---|---|---|
| G1 | Contexto Antes Aula | Copiloto | Copiloto | Excecoes |
| G2 | Observacao Pos-Aula | Copiloto | Copiloto | Excecoes |
| G4 | Objetivo/Evolucao | Copiloto | Copiloto | Excecoes |
| G8 | Repasse Entre Professores | Copiloto | Copiloto | Excecoes |
| G9 | Lembrete Professor | Copiloto | Direto | Direto |
| G12 | Linha Do Tempo | Copiloto | Copiloto | Excecoes |

Explicacao na pagina:

- Mais manual: o agente prepara contexto e lembretes para o professor.
- Equilibrado: lembretes rodam; contexto, notas, linha do tempo e repasses ficam como apoio do professor.
- Mais autonomo: o agente conduz resumos e lembretes permitidos, respeitando visibilidade e permissao.

### Rotina: Historico Protegido

Rota:

```text
/app/agentes/historico-professor/rotinas/historico-protegido
```

| ID | Fluxo | Mais manual | Equilibrado | Mais autonomo |
|---|---|---|---|---|
| G3 | Restricao/Cuidado | Manual | Aprovacao | Aprovacao |
| G5 | Contexto Para Agente | Manual | Aprovacao | Aprovacao |
| G6 | Documentos/Anamnese | Manual | Aprovacao | Aprovacao |
| G7 | Correcao Historico | Manual | Aprovacao | Aprovacao |
| G10 | Compartilhar Contexto | Manual | Aprovacao | Aprovacao |
| G11 | Permissao Historico | Manual | Aprovacao | Aprovacao |

Explicacao na pagina:

- Mais manual: historico protegido fica com humano.
- Equilibrado: o agente prepara contexto, documento ou correcao e pede aprovacao.
- Mais autonomo: o agente adianta revisao e bloqueios, mas historico protegido continua exigindo aprovacao.

## Como A UI Deve Usar Este Mapa

Na pagina da rotina:

1. O usuario escolhe o perfil.
2. A tabela de fluxos mostra os modos aplicados.
3. A tela explica o que muda em linguagem simples.
4. Se o usuario personalizar um fluxo, a rotina vira "perfil personalizado".
5. Simulacao e publicacao usam o mapa resultante.

Na simulacao:

- mostrar o perfil escolhido;
- mostrar o fluxo testado;
- mostrar se aquele fluxo segue o perfil ou foi personalizado;
- mostrar o caminho real da execucao.

Na publicacao:

- listar perfil;
- listar fluxos personalizados;
- listar o que roda sozinho;
- listar o que pede aprovacao;
- listar o que chama humano;
- listar o que continua manual.
