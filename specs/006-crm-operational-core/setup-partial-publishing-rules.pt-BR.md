# Regras De Publicacao Parcial Do Setup

Status: rascunho consolidado.
Data: 2026-05-13.

## Objetivo

Permitir que o studio comece a usar o Taliya sem esperar todas as configuracoes ficarem perfeitas, mantendo seguranca para regras sensiveis e agentes.

## Principio

Publicar parcialmente e melhor do que bloquear o CRM.

No setup inicial, autonomia nao e publicada. Quando algum fluxo exigir autonomia, modo, limite, cota por fluxo, aprovacao detalhada, fallback ou simulacao, o resultado correto e criar rascunho/pendencia para Agentes/Fluxos pos-go-live.

## Camadas de publicacao

### 1. CRM manual

Pode publicar quando:

- workspace criado;
- usuario dono/admin existe;
- horario basico configurado;
- pelo menos uma forma de cadastrar/importar alunos existe;
- permissoes basicas existem.

Pode faltar:

- WhatsApp;
- agentes;
- financeiro completo;
- modelos de mensagem;
- regras avancadas.

Resultado:

- Hoje, tarefas, alunos, agenda basica e configuracoes funcionam manualmente.

### 2. Agenda

Pode publicar quando:

- tipos de aula existem;
- turmas/aulas basicas existem;
- professor ou responsavel definido;
- capacidade por turma definida;
- chamada manual definida.

Se reposicao nao estiver fechada:

- reposicoes sensiveis ficam manuais;
- sistema cria pendencias.

### 3. Financeiro

Pode publicar quando:

- modelo de cobranca definido;
- planos principais definidos;
- regra de vencimento definida;
- regra de inadimplencia definida;
- consumo/direito de aula definido quando agenda depende disso.

Se provedor financeiro nao estiver conectado:

- operacao manual/programatica;
- conciliacao/importacao ficam pendentes.

### 4. Canais e modelos de mensagem

Pode publicar quando:

- canal conectado ou marcado como manual;
- janela de envio definida;
- opt-out/consentimento definido;
- modelos essenciais aprovados ou marcados como rascunho manual.

Sem canal externo:

- mensagens automaticas bloqueadas;
- modelos podem ficar prontos para envio manual quando permitido.

Canal conectado ou modelo aprovado nao significa automacao pronta. Automacao externa fica pendente para Agentes/Fluxos pos-go-live.

### 5. Regras de seguranca, aprovacoes e excecoes

Pode publicar quando:

- regra sensivel tem dono;
- aprovador definido;
- impacto revisado;
- versao criada;
- previa de impacto realizada quando necessario.

Sem regra de seguranca publicada:

- automacao sensivel bloqueada;
- caminho manual pode seguir quando permitido.

### 6. Agentes preparados

Pode publicar quando:

- agente incluso no entitlement;
- dominio/slot escolhido quando o plano exigir;
- responsavel humano definido;
- pacotes recomendados escolhidos como rascunho;
- areas sem agente mantem caminho manual.

Resultado:

- agentes ficam preparados conforme plano;
- fluxos recomendados ficam como rascunho/pendencia;
- CRM manual continua operavel mesmo sem ativar fluxo.

### 7. Autonomia de agentes

Nao e publicada no setup inicial.

O setup apenas cria pendencia para Agentes/Fluxos pos-go-live quando o fluxo exigir:

- regra operacional publicada;
- politica publicada;
- canal conectado;
- modelo de mensagem aprovado;
- opt-out respeitado;
- cota disponivel;
- fallback definido;
- simulacao aprovada;
- permissao valida;
- auditoria ativa;
- gestor confirmou.

Resultado:

- o setup mostra que isso ficou para depois quando convem;
- o usuario sabe onde continuar sem sentir que o CRM ficou incompleto;
- Control Planes entram depois para execucoes, falhas, uso, cotas, incidentes, logs e auditoria.

## Estados de publicacao

| Estado | Significado |
|---|---|
| Nao publicado | Nada daquela camada esta ativo. |
| Pronto para publicar | Validacoes passaram. |
| Publicado | Camada ativa. |
| Publicado parcialmente | Parte segura ativa; parte sensivel pendente. |
| Bloqueado | Falha em dependencia obrigatoria. |
| Pausado | Publicado, mas pausado por risco/incidente/cota. |

## Bloqueios comuns

| Bloqueio | Resultado correto |
|---|---|
| Sem permissao | Pedir aprovacao ou bloquear. |
| Sem regra de seguranca | Permitir caminho manual quando seguro; bloquear automacao. |
| Sem cota | Bloquear automacao paga, manter manual. |
| Sem canal | Bloquear envio externo. |
| Sem modelo de mensagem | Bloquear envio externo automatizado; permitir rascunho manual. |
| Dados importados conflitantes | Importar parte segura, publicar CRM e deixar area afetada pendente. |
| Modelo financeiro hibrido incompleto | Publicar CRM/agenda, manter financeiro em revisao. |

## Pendencias rastreaveis

Toda pendencia gerada por publicacao parcial precisa virar objeto rastreavel.

Cada pendencia deve ter:

- area;
- motivo;
- responsavel;
- destino para continuar;
- prioridade;
- se bloqueia publicacao;
- camada afetada;
- status.

Pendencia sem destino claro nao deve ser criada.

## Aceite

Estas regras estao corretas quando:

- o studio sempre consegue avancar com CRM manual;
- cada camada tem criterio minimo;
- toda publicacao parcial mostra o que ficou pendente;
- autonomia nunca e publicada no setup inicial;
- pendencias de Agentes/Fluxos ficam claras quando isso evitar confusao.
