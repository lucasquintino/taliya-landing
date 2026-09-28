# Taliya CRM - Agente Vendas: Paginas, Conteudo E Dinamicas

Status: contrato funcional v0.1.
Data: 2026-05-21.

## Objetivo

Mapear as paginas, rotinas, fluxos, perfis, ajustes visiveis e dinamicas do Agente Vendas.

Segue:

- `agents-flows-routines-pages-final-contract.pt-BR.md`
- `agents-flows-routine-profile-map.pt-BR.md`

## Regra Central

```text
Agente Vendas nao configura sozinho.
Rotina organiza captura, experimental e conversao.
Perfil da rotina aplica modos nos fluxos.
Fluxo so abre para personalizacao quando necessario.
```

Responsaveis, aprovadores e filas humanas sao herdados da rotina.
O fluxo so mostra esses campos quando precisa trocar o padrao ou quando a aprovacao/excecao exige alguem especifico.

## Rotinas

| Rotina | Fluxos |
|---|---|
| Captura e qualificacao | C15 Entrada multicanal de lead; C8 Origem/qualificacao; C9 Perda comercial; C10 Indicacao |
| Experimental e acompanhamento | C2 Aula experimental; C3 Lembrete experimental; C4 Pos-aula experimental; C5 Follow-up comercial; C12 Demanda sem vaga |
| Conversao e matricula | C1 Valores e planos; C6 Pre-matricula; C7 Objecoes; C11 Checkout/abandono; C13 Interessado para aluno; C14 Upsell/upgrade |

Total: 3 rotinas, 15 fluxos.

## Paginas Do Agente

### Visao Geral

Rota:

```text
/app/agentes/vendas
```

Mostra:

- status do agente;
- rotinas;
- leads/interessados recentes;
- experimentais pendentes;
- follow-ups abertos;
- aprovacoes comerciais;
- excecoes;
- bloqueios por plano, cota, permissao ou canal;
- execucoes recentes.

Dinamicas:

- agente nao contratado: preview e upgrade;
- sem agenda conectada/sem horarios: bloqueia agendamento automatico;
- opt-out: bloqueia contato;
- aprovacao pendente: CTA "Revisar aprovacao";
- lead duplicado: mostra excecao de triagem.

### Pagina Da Rotina

Rota:

```text
/app/agentes/vendas/rotinas/[routineId]
```

Mostra:

- perfil da rotina;
- impacto do perfil;
- fluxos e modos aplicados;
- oportunidades/experimentais afetados;
- excecoes e aprovacoes;
- operacao recente;
- acoes: Ajustar, Simular, Publicar, Ver execucoes, Pausar, Voltar versao.

Dinamicas:

- trocar perfil recalcula modos e exige simulacao;
- personalizar fluxo marca rotina como "perfil personalizado";
- bloqueio de agenda/canal/cota rebaixa ou impede automatico;
- beneficios, conversoes e mudancas comerciais mantem aprovacao.

### Ajustar Rotina E Fluxos

Rota:

```text
/app/agentes/vendas/rotinas/[routineId]/ajustar
```

Mostra:

- perfil atual;
- lista de fluxos;
- modo e origem;
- comportamento por modo;
- ajustes visiveis;
- dependencias fixas;
- simulacao rapida.

Nao mostra:

- desconto livre;
- promessa livre;
- canal como escolha solta;
- fonte tecnica de lead;
- regras de billing.

### Simular Rotina

Rota:

```text
/app/agentes/vendas/rotinas/[routineId]/simular
```

Cenarios de Captura e qualificacao:

- lead novo simples;
- lead duplicado;
- origem desconhecida;
- indicacao com beneficio;
- perda comercial sensivel.

Cenarios de Experimental e acompanhamento:

- interessado pede experimental;
- lembrete antes da aula;
- pos-aula com interesse;
- pos-aula com objecao;
- follow-up sem resposta;
- demanda sem vaga.

Cenarios de Conversao e matricula:

- pergunta sobre plano;
- objecao;
- checkout abandonado;
- pre-matricula;
- conversao para aluno;
- upgrade.

Mostra:

- conversa/celular quando houver mensagem;
- estado do lead/oportunidade;
- agenda se houver experimental;
- linha de execucao;
- aprovacao/excecao.

### Publicar Versao

Rota:

```text
/app/agentes/vendas/rotinas/[routineId]/publicar
```

Mostra:

- perfil;
- fluxos personalizados;
- o que roda sozinho;
- o que vira sugestao;
- o que pede aprovacao;
- o que chama humano;
- preflight.

Bloqueia se faltar:

- simulacao;
- template/tom;
- aprovador para beneficio/conversao/upgrade;
- consentimento;
- cota;
- canal/integracao;
- dados obrigatorios.

### Execucoes E Detalhe

Rotas:

```text
/app/agentes/vendas/rotinas/[routineId]/execucoes
/app/fluxos/execucoes/[runId]
```

Mostram:

- lead/interessado/aluno;
- rotina;
- perfil publicado;
- fluxo;
- modo;
- mensagem/acao;
- aprovacao;
- humano chamado;
- cota;
- auditoria.

## Perfis Por Rotina

### Captura E Qualificacao

| Fluxo | Mais manual | Equilibrado | Mais autonomo |
|---|---|---|---|
| C15 Entrada multicanal de lead | Copiloto | Excecoes | Excecoes |
| C8 Origem/qualificacao | Copiloto | Excecoes | Excecoes |
| C9 Perda comercial | Manual | Aprovacao | Aprovacao |
| C10 Indicacao | Manual | Aprovacao | Aprovacao |

Explicacao:

- Mais manual: leads entram para triagem humana com ajuda do agente.
- Equilibrado: captura e qualificacao rodam com excecoes; perda e indicacao pedem aprovacao.
- Mais autonomo: agente classifica casos claros, mas beneficios/perdas continuam com humano.

### Experimental E Acompanhamento

| Fluxo | Mais manual | Equilibrado | Mais autonomo |
|---|---|---|---|
| C2 Aula experimental | Copiloto | Excecoes | Excecoes |
| C3 Lembrete experimental | Copiloto | Direto | Direto |
| C4 Pos-aula experimental | Copiloto | Copiloto | Excecoes |
| C5 Follow-up comercial | Copiloto | Copiloto | Excecoes |
| C12 Demanda sem vaga | Copiloto | Copiloto | Excecoes |

Explicacao:

- Mais manual: agente prepara lembretes e follow-ups; comercial decide.
- Equilibrado: lembrete roda sozinho; pos-aula, follow-up e demanda sem vaga ficam como sugestao.
- Mais autonomo: agente conduz cadencias claras e chama humano para objecoes, desconto, promessa ou vaga sensivel.

### Conversao E Matricula

| Fluxo | Mais manual | Equilibrado | Mais autonomo |
|---|---|---|---|
| C1 Valores e planos | Copiloto | Copiloto | Excecoes |
| C6 Pre-matricula | Manual | Aprovacao | Aprovacao |
| C7 Objecoes | Copiloto | Aprovacao | Aprovacao |
| C11 Checkout/abandono | Copiloto | Copiloto | Excecoes |
| C13 Interessado para aluno | Manual | Aprovacao | Aprovacao |
| C14 Upsell/upgrade | Manual | Aprovacao | Aprovacao |

Explicacao:

- Mais manual: agente prepara respostas e checklist, humano executa.
- Equilibrado: valores e abandono viram sugestao; matricula, objecoes sensiveis e upgrade pedem aprovacao.
- Mais autonomo: agente conduz o maximo permitido, mas conversao e mudanca comercial continuam com aprovacao.

## Ajustes Visiveis Por Fluxo

| Fluxo | Ajustes visiveis quando necessario | Fixo/dependencia |
|---|---|---|
| C15 Entrada multicanal de lead | fila de triagem se diferente do padrao; regra de duplicidade visivel | origem registrada; fontes aceitas pelo CRM; contato minimo; dono natural; auditoria |
| C8 Origem/qualificacao | responsavel se diferente do padrao | campos de qualificacao vem do CRM; origem auditavel; duplicidade; historico |
| C9 Perda comercial | motivo; aprovador se perda sensivel; texto interno | perda definitiva exige registro; responsavel padrao; auditoria |
| C10 Indicacao | aprovador de beneficio; mensagem/tom se houver aviso | beneficio nao livre; regra de vinculo do produto |
| C2 Aula experimental | janela de horarios; responsavel se diferente; limite de tentativas; template/tom | agenda real; consentimento; interessado |
| C3 Lembrete experimental | quando lembrar; template; tom; limite por aula | aula experimental; opt-out; canal fixo |
| C4 Pos-aula experimental | cadencia; quando virar tarefa; template/tom | aula concluida; interessado; responsavel padrao |
| C5 Follow-up comercial | cadencia; limite de tentativas; template/tom | consentimento; responsavel padrao; opt-out |
| C12 Demanda sem vaga | encaminhamento para lista; template/tom; quando chamar humano | capacidade real; regra de promessa do produto |
| C1 Valores e planos | template/tom; quando chamar humano | valores e planos vem do CRM; sem desconto livre |
| C6 Pre-matricula | aprovador; prazo; responsavel se diferente | dados obrigatorios; checklist do produto; plano valido |
| C7 Objecoes | aprovador; limite de promessa; template/tom | base de respostas do produto/CRM; desconto exige aprovacao |
| C11 Checkout/abandono | cadencia; limite de contato; template/tom | checkout de origem; responsavel padrao; opt-out |
| C13 Interessado para aluno | aprovador; responsavel se diferente | plano vem do CRM; checklist; dados obrigatorios |
| C14 Upsell/upgrade | aprovador; template/tom; limite de oferta | plano/preco do CRM; sem alteracao comercial livre |

## Modais E Drawers

- Pausar rotina;
- Pausar fluxo;
- Voltar versao;
- Resolver excecao;
- Revisar aprovacao;
- Ver conversa/oportunidade.

## Resumo De UX

```text
1. Usuario escolhe perfil da rotina.
2. Ve impacto comercial e operacional.
3. Personaliza fluxo so se precisar.
4. Simula conversa, agenda ou oportunidade.
5. Publica versao.
6. Acompanha leads, aprovacoes, excecoes e execucoes.
```
