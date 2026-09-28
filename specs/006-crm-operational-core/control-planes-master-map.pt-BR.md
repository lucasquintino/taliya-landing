# Taliya CRM - Mapa Mestre De Acompanhamento Operacional

Status: mapa mestre v0.2.
Data: 2026-05-25.

## Decisao Principal

Nao criar uma familia nova de produto chamada Control Planes no MVP.

Tambem nao criar, nesta etapa, uma familia propria de incidentes operacionais.

O que antes era chamado de Control Plane fica distribuido nas paginas onde o dono/admin ja esta trabalhando:

- Agentes/Fluxos;
- Execucao de fluxo;
- Uso/Cotas;
- Auditoria;
- Configuracoes especificas quando houver integracao;
- Hoje, quando houver alerta critico.

Essa decisao evita uma area tecnica demais e reduz superficie para o dono do studio aprender.

## O Que Continua Existindo

Mesmo sem uma familia nova, o produto ainda precisa explicar:

- o que rodou;
- o que consumiu cota;
- o que parou;
- o que virou tarefa;
- o que pediu aprovacao;
- o que chamou humano;
- qual objeto foi afetado;
- onde a operacao continua.

Essas respostas aparecem em paginas de apoio e contexto, nao em um painel central tecnico.

## Rotas Do MVP

| Superficie | Rota | Papel |
|---|---|---|
| Execucao de fluxo | `/app/fluxos/execucoes/[runId]` | Recibo operacional simples de uma execucao real. |
| Uso e cotas | `/app/uso` | Visao geral de consumo, limite, alertas e consequencia operacional. |
| Extrato de uso | `/app/uso/extrato` | Ledger de consumo por origem, agente, fluxo e caso. |
| Auditoria | `/app/auditoria` | Consulta sensivel de eventos importantes. |
| Detalhe de auditoria | `/app/auditoria/[eventId]` | Detalhe de uma mudanca ou acao sensivel. |
| Logs compactos de integracao | Dentro da configuracao especifica | Status tecnico contextual, sem hub proprio. |
| Hoje | `/app/hoje` | Alertas criticos e itens que precisam de acao agora. |

## Rotas Fora Do MVP

Nao criar agora:

- `/app/controle/*`;
- `/app/operacao/incidentes`;
- `/app/operacao/incidentes/[incidentId]`;
- hub tecnico de execucoes;
- painel global de falhas;
- tela separada de logs tecnicos.

Se algum documento antigo citar essas rotas, ler como proposta superada ou conceito historico, nao como rota final do MVP.

## Execucao De Fluxo

Fonte canonica:

- `flow-execution-page-contract.pt-BR.md`

Imagem aprovada:

- `70_round-4.1P_execucoes_01_fluxo-falta-com-aviso-aprovado.png`

Serve para responder:

- o que a Taliya fez neste caso?
- por que seguiu, parou, pediu aprovacao ou chamou humano?
- quanto consumiu?
- onde continua?

Nao mostra:

- prompt;
- pensamento interno;
- payload;
- stack trace;
- tokens;
- custo interno;
- log tecnico;
- configuracao de fluxo;
- publicacao;
- simulacao.

## Uso E Cotas

Fonte canonica:

- `usage-quotas-master-map.pt-BR.md`

Imagens aprovadas:

- `68_round-4.1O_uso_01_visao-geral-aprovado.png`;
- `69_round-4.1O_uso_02_extrato-aprovado.png`.

Uso/Cotas mostra:

- cota contratada;
- consumo;
- restante;
- previsao;
- origem do consumo;
- alertas 70/90/100;
- downgrades ou bloqueios por cota;
- caminho para extrato;
- caminho para add-ons em Billing quando fizer sentido.

Uso/Cotas nao compra add-on por conta propria e nao configura fluxo.

## Auditoria

Auditoria continua como area sensivel separada.

Ela mostra:

- quem fez;
- o que mudou;
- quando;
- objeto afetado;
- antes/depois seguro;
- origem;
- motivo, quando houver;
- link para execucao, aprovacao, cobranca, aluno ou configuracao relacionada.

Auditoria nao e lugar de operar o dia a dia. E consulta e evidencia.

## Integracoes Tecnicas

Integracoes tecnicas nao tem hub proprio no MVP.

Elas aparecem dentro da configuracao especifica:

- canais em `/app/configuracoes/canais`;
- Pagamentos Taliya em `/app/configuracoes/financeiro/pagamentos`;
- agenda/calendario/importacao em `/app/configuracoes/agenda`;
- notificacoes em `/app/configuracoes/notificacoes`.

Quando houver falha, a pagina deve mostrar status tecnico compacto e a acao segura: testar, reconectar, reprocessar quando permitido ou abrir suporte.

## Hoje

Hoje recebe apenas alertas que precisam de atencao agora.

Exemplos:

- automacao importante pausada por cota;
- falha de envio que afeta aula de hoje;
- aprovacao urgente;
- tarefa criada por execucao que precisa de continuidade;
- configuracao bloqueando operacao do dia.

Hoje nao vira painel tecnico.

## Regra De Produto

Quando algo precisar de configuracao permanente, mandar para a pagina dona:

| Problema | Onde corrigir |
|---|---|
| Fluxo precisa mudar modo, regra, responsavel ou template | Agentes/Fluxos |
| Cota chegou perto do limite | Uso/Cotas |
| Precisa comprar add-on ou ver plano | Billing Taliya |
| WhatsApp ou e-mail falhou | Configuracoes/Canais |
| Pagamentos Taliya falhou | Configuracoes/Pagamentos e financeiro |
| Permissao bloqueou acao | Configuracoes/Permissoes |
| Evento sensivel precisa evidencia | Auditoria |

## Papel Do Agente De IA

Nas superficies de acompanhamento, o agente atua como explicador.

Ele pode:

- resumir o que aconteceu;
- explicar por que parou ou seguiu;
- apontar onde a operacao continua;
- explicar consumo de cota;
- sugerir qual pagina abrir;
- preparar pedido de ajuda.

Ele nao pode:

- publicar fluxo;
- mudar regra permanente;
- apagar auditoria;
- esconder falha;
- reprocessar acao sensivel sozinho;
- alterar Billing;
- conceder permissao;
- conectar/desconectar integracao sozinho.

## Decisao Final

No MVP, acompanhamento operacional fica leve e distribuido.

A unica nova imagem aprovada nesta rodada e a pagina de execucao de fluxo como recibo operacional simples.
