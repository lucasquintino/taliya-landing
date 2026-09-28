# Setup E Configuracoes - Cenarios De Teste

Status: contrato v0.1.
Data: 2026-05-13.

## Objetivo

Simular studios reais para provar que o setup ativa o CRM sem criar complexidade desnecessaria e sem depender de agente contratado.

Cada cenario deve validar:

- setup guiado por agente;
- opcao de chamada com humano Taliya sem mudar o fluxo;
- publicacao parcial;
- CRM com 0 agentes;
- planos 1, 3 e 7 agentes;
- modos manual, copiloto e autonomo;
- cotas;
- permissoes;
- integracoes;
- auditoria.

## Cenarios obrigatorios

### S01 - Studio simples com 0 agentes

Contexto:

- uma unidade;
- mensalidade fixa;
- agenda simples;
- sem WhatsApp conectado no inicio;
- plano Base Taliya com 0 agentes.

Resultado esperado:

- CRM manual publicado;
- agenda, alunos, tarefas, checklists, financeiro e configuracoes basicas funcionando;
- agentes aparecem como opcionais/bloqueados por plano;
- automacoes externas bloqueadas;
- setup nao trava por falta de agente.

### S02 - Studio com 1 agente de Agenda

Contexto:

- studio quer ajuda em reposicoes e encaixes;
- WhatsApp conectado;
- financeiro manual;
- reposicoes dependem de credito disponivel.

Resultado esperado:

- Agenda publica regras de aula, reposicao e encaixe;
- agente de Agenda fica preparado, com pacotes recomendados em rascunho/pendencia para Agentes/Fluxos;
- financeiro continua manual;
- reposicao sensivel cria aprovacao ou tarefa;
- encaixe automatico fica para configuracao pos-go-live e so pode ser avaliado com vaga, consentimento, credito e regra publicada.

### S03 - Studio com 3 agentes

Contexto:

- agentes de Atendimento, Agenda e Vendas;
- financeiro sem agente;
- gestor quer reduzir fila humana.

Resultado esperado:

- Atendimento, Agenda e Vendas preparados com responsaveis humanos e pacotes recomendados;
- Financeiro aparece como CRM manual/programatico;
- cota de mensagens/IA visivel;
- handoff humano definido por area;
- fluxos sensiveis ficam como pendencia para Agentes/Fluxos ate validacao pos-go-live.

### S04 - Studio com 7 agentes e cota em 90%

Contexto:

- operacao madura;
- todos os agentes contratados;
- automacoes ativas;
- cota proxima do limite.

Resultado esperado:

- preflight obrigatorio para autonomia;
- painel de uso/cotas mostra risco;
- sistema prioriza acoes com maior impacto;
- fluxos nao essenciais podem pausar ou migrar para copiloto;
- queda de cota nao quebra CRM manual.

### S05 - Studio por pacote/credito de aulas

Contexto:

- aluno compra pacote;
- credito expira;
- reposicao consome ou nao consome aula conforme regra;
- gestor aceita "quebrar galho" em casos pontuais.

Resultado esperado:

- modelo de consumo publicado separado da cobranca;
- reposicao consulta saldo, validade e excecao;
- excecao exige permissao, motivo, impacto e auditoria;
- agente nao concede credito fora da regra sem aprovacao.

### S06 - Studio hibrido de mensalidade e pacote

Contexto:

- alguns alunos por mensalidade;
- outros por pacote;
- aulas avulsas;
- regras diferentes por plano do aluno.

Resultado esperado:

- setup recomenda revisao humana Taliya, mas permite continuar;
- regras ficam por plano/tipo de produto, nao duplicadas por pagina;
- simulador mostra exemplos antes de publicar;
- publicacao parcial permite ativar CRM antes de automatizar.

### S07 - Importacao com dados ruins

Contexto:

- CSV antigo;
- telefones duplicados;
- alunos sem turma;
- responsaveis inconsistentes.

Resultado esperado:

- CRM publica apenas areas seguras;
- dados conflitantes entram em fila de qualidade;
- agentes externos ficam bloqueados para registros incertos;
- gestor consegue operar manualmente enquanto corrige dados.

### S08 - WhatsApp desconecta depois do go-live

Contexto:

- fluxos estavam publicados;
- integracao cai;
- existem mensagens programadas.

Resultado esperado:

- envios externos pausam;
- tarefas/incidentes sao criados conforme criticidade;
- rascunhos e filas internas continuam;
- auditoria registra falha;
- reconexao retoma somente o que ainda for valido.

### S09 - Mudanca de modelo financeiro pos-go-live

Contexto:

- studio muda de mensalidade fixa para hibrido;
- ha cobranças abertas;
- ha reposicoes pendentes.

Resultado esperado:

- sistema cria diff de impacto;
- regra nova aplica em data definida;
- execucoes antigas preservam snapshot;
- pendencias sensiveis exigem revisao;
- agentes nao usam regra nova ate publicacao.

### S10 - Reclamacao e cancelamento sensivel

Contexto:

- aluno reclama de reposicao;
- automacao de retencao estava ativa;
- existe cobranca pendente.

Resultado esperado:

- automacoes externas pausam;
- caso sensivel concentra contexto;
- copiloto pode sugerir resposta, mas envio exige humano se severidade alta;
- financeiro nao faz cobranca agressiva sem politica;
- historico fica auditavel.

## Criterios de aceite dos cenarios

Cada cenario so esta aprovado quando:

1. o setup consegue chegar a algum estado util;
2. o CRM nunca fica inutil por falta de agente;
3. regras bloqueadas mostram o motivo;
4. publicacao parcial e possivel;
5. cada decisao sensivel tem aprovador;
6. uso/cota e permissao aparecem antes da execucao;
7. agente de setup explica sem virar fonte da verdade;
8. reconfiguracao futura tem caminho claro.
