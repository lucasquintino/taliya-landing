# Taliya CRM - Agente Gestao/Governanca: Paginas, Conteudo E Dinamicas

Status: contrato funcional v0.1.
Data: 2026-05-21.

## Objetivo

Mapear as paginas, rotinas, fluxos, perfis, ajustes visiveis e dinamicas do Agente Gestao/Governanca.

Segue:

- `agents-flows-routines-pages-final-contract.pt-BR.md`
- `agents-flows-routine-profile-map.pt-BR.md`

## Regra Central

```text
Gestao/Governanca ajuda a priorizar, monitorar e explicar.
Nao substitui Control Plane.
Nao edita billing, permissao real, integracao tecnica ou auditoria imutavel.
```

Responsaveis, aprovadores e filas humanas sao herdados da rotina.
O fluxo so mostra esses campos quando precisa trocar o padrao ou quando a aprovacao/excecao exige alguem especifico.

## Rotinas

| Rotina | Fluxos |
|---|---|
| Comando operacional | F1 Prioridades dia; F2 Dinheiro na mesa; F3 Fila humana; F4 Gargalos; F5 Resumo semanal; F6 Qualidade dados; F10 Capacidade/crescimento |
| Governanca de agentes | F7 Creditos/limites; F8 Performance; F9 Permissoes/auditoria; F13 Teste de fluxo; F14 Incidente de automacao e correcao operacional; F15 Mudanca de politica ou regra operacional |
| Integracoes e importacao | F11 Falhas/webhooks; F12 Importacao/migracao |

Total: 3 rotinas, 15 fluxos.

## Paginas Do Agente

### Visao Geral

Rota:

```text
/app/agentes/gestao-governanca
```

Mostra:

- status do agente;
- rotinas;
- prioridades do dia;
- gargalos;
- cotas/limites;
- incidentes;
- falhas de integracao;
- aprovacoes de politica/permissao;
- execucoes recentes.

Dinamicas:

- incidente alto: destaca pausa/operacao;
- cota em 70/90/100: alerta e caminho para Uso/Cotas;
- falha tecnica: link para integracao/logs;
- mudanca de politica: exige aprovacao e simulacao;
- investigacao profunda vai para Control Plane.

### Pagina Da Rotina

Rota:

```text
/app/agentes/gestao-governanca/rotinas/[routineId]
```

Mostra:

- perfil;
- impacto;
- fluxos e modos;
- alertas/relatorios/tarefas;
- aprovacoes;
- incidentes;
- bloqueios;
- acoes: Ajustar, Simular, Publicar, Ver execucoes, Pausar, Voltar versao.

Dinamicas:

- trocar perfil exige simulacao;
- fluxos de permissao/politica continuam com aprovacao;
- falhas e incidentes podem abrir tarefa/incidente, mas nao configuram integracao;
- personalizacao marca perfil personalizado.

### Ajustar Rotina E Fluxos

Rota:

```text
/app/agentes/gestao-governanca/rotinas/[routineId]/ajustar
```

Mostra:

- perfil;
- modos dos fluxos;
- comportamento por modo;
- ajustes visiveis;
- dependencias fixas;
- fallback;
- simulacao rapida.

Nao mostra:

- logs tecnicos brutos;
- payload de webhook;
- regra de billing;
- permissao real editavel;
- auditoria editavel;
- configuracao livre de control plane.

### Simular Rotina

Rota:

```text
/app/agentes/gestao-governanca/rotinas/[routineId]/simular
```

Cenarios de Comando operacional:

- inicio do dia;
- dinheiro parado;
- fila humana cheia;
- gargalo recorrente;
- resumo semanal;
- dado ruim;
- capacidade perto do limite.

Cenarios de Governanca de agentes:

- cota em 70/90/100;
- performance ruim;
- evento de permissao;
- teste de fluxo;
- incidente de automacao;
- mudanca de politica.

Cenarios de Integracoes e importacao:

- webhook falha;
- retry seguro;
- retry bloqueado;
- importacao com amostra ok;
- importacao com conflito.

Mostra:

- painel operacional;
- tarefa/incidente/aprovacao;
- linha de execucao;
- links para uso, auditoria, integracoes ou operacao.

### Publicar Versao

Rota:

```text
/app/agentes/gestao-governanca/rotinas/[routineId]/publicar
```

Mostra:

- perfil;
- fluxos personalizados;
- o que roda sozinho;
- o que vira alerta/tarefa;
- o que pede aprovacao;
- o que abre incidente;
- preflight.

Bloqueia se faltar:

- simulacao;
- responsavel;
- aprovador para politica/permissao/importacao;
- fallback;
- permissao;
- integracao quando o fluxo depende de logs/status;
- auditoria.

### Execucoes E Detalhe

Rotas:

```text
/app/agentes/gestao-governanca/rotinas/[routineId]/execucoes
/app/fluxos/execucoes/[runId]
```

Mostram:

- rotina;
- perfil;
- fluxo;
- alerta/tarefa/incidente;
- modo;
- cota;
- humano chamado;
- auditoria;
- link para Control Plane quando houver investigacao.

## Perfis Por Rotina

### Comando Operacional

| Fluxo | Mais manual | Equilibrado | Mais autonomo |
|---|---|---|---|
| F1 Prioridades dia | Copiloto | Direto | Direto |
| F2 Dinheiro na mesa | Copiloto | Copiloto | Excecoes |
| F3 Fila humana | Copiloto | Direto | Direto |
| F4 Gargalos | Copiloto | Copiloto | Excecoes |
| F5 Resumo semanal | Copiloto | Direto | Direto |
| F6 Qualidade dados | Copiloto | Copiloto | Excecoes |
| F10 Capacidade/crescimento | Copiloto | Copiloto | Excecoes |

Explicacao:

- Mais manual: agente organiza prioridades e relatorios.
- Equilibrado: resumos e filas rodam; gargalos, dinheiro, qualidade e capacidade viram sugestoes/tarefas revisaveis.
- Mais autonomo: agente monitora e abre tarefas, mas nao muda regra, grade, financeiro ou capacidade sozinho.

### Governanca De Agentes

| Fluxo | Mais manual | Equilibrado | Mais autonomo |
|---|---|---|---|
| F7 Creditos/limites | Copiloto | Direto | Direto |
| F8 Performance | Copiloto | Copiloto | Excecoes |
| F9 Permissoes/auditoria | Manual | Aprovacao | Aprovacao |
| F13 Teste de fluxo | Copiloto | Direto | Direto |
| F14 Incidente de automacao e correcao operacional | Copiloto | Excecoes | Excecoes |
| F15 Mudanca de politica ou regra operacional | Manual | Aprovacao | Aprovacao |

Explicacao:

- Mais manual: agente explica uso, performance e incidentes.
- Equilibrado: cotas e testes rodam; performance vira sugestao; incidentes chamam humano; permissao/politica pedem aprovacao.
- Mais autonomo: agente monitora, testa e pausa quando permitido, mas politica/permissao continua com aprovacao.

### Integracoes E Importacao

| Fluxo | Mais manual | Equilibrado | Mais autonomo |
|---|---|---|---|
| F11 Falhas/webhooks | Copiloto | Copiloto | Excecoes |
| F12 Importacao/migracao | Manual | Aprovacao | Aprovacao |

Explicacao:

- Mais manual: agente explica falhas e prepara revisao.
- Equilibrado: falhas viram explicacao/sugestao; importacao/migracao pede aprovacao.
- Mais autonomo: agente pode auto-pausar/abrir incidente quando permitido, mas importacao e merge continuam com aprovacao.

## Ajustes Visiveis Por Fluxo

| Fluxo | Ajustes visiveis quando necessario | Fixo/dependencia |
|---|---|---|
| F1 Prioridades dia | horario do resumo; responsavel | secoes/fontes vem do produto/CRM |
| F2 Dinheiro na mesa | frequencia; responsavel; quando abrir tarefa | metricas do produto; dados financeiros do CRM |
| F3 Fila humana | prioridade; responsaveis se diferente; tempo de destaque | filas reais; permissao |
| F4 Gargalos | frequencia; responsavel; tipo de alerta; limite de tarefa | metricas do CRM; nao muda operacao sozinho |
| F5 Resumo semanal | dia/hora; destinatarios internos | secoes do produto; dados do periodo |
| F6 Qualidade dados | responsavel; prioridade; quando criar tarefa | tipos de dado do produto; merge/exclusao exige aprovacao |
| F10 Capacidade/crescimento | frequencia; responsavel; limite de alerta | metricas do produto; agenda/capacidade reais |
| F7 Creditos/limites | alertas 70/90/100; responsavel; politica de economia visivel | Billing/Uso sao fonte primaria |
| F8 Performance | frequencia; responsavel; quando abrir tarefa | metricas do produto; execucoes/auditoria |
| F9 Permissoes/auditoria | aprovador; responsavel; prazo | permissao real em Configuracoes; auditoria imutavel |
| F13 Teste de fluxo | cenarios de simulacao; responsavel por revisao | teste nao publica sozinho |
| F14 Incidente automacao | severidade; responsavel; auto-pausa; criterio de reabertura | incidente fica em Operacao |
| F15 Mudanca politica/regra | aprovador; data de vigencia; simulacao; comunicacao interna | politica versionada; auditoria |
| F11 Falhas/webhooks | responsavel; severidade; auto-pausa | logs ficam na integracao; retry seguro do produto |
| F12 Importacao/migracao | aprovador; lote; responsavel; amostra de revisao | job auditavel; merge em lote aprovado |

## Modais E Drawers

- Pausar rotina;
- Pausar fluxo;
- Voltar versao;
- Resolver excecao;
- Revisar aprovacao;
- Abrir incidente;
- Ir para logs/integracao;
- Ir para Uso/Cotas.

## Resumo De UX

```text
1. Usuario escolhe perfil da rotina.
2. Entende o que monitora, alerta, aprova ou vira incidente.
3. Personaliza fluxo so se precisar.
4. Simula painel/tarefa/incidente.
5. Publica versao.
6. Acompanha uso, incidentes, aprovacoes e execucoes.
```
