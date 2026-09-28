# Contrato De Consumo Das Configuracoes Pelo CRM E Agentes

Status: rascunho consolidado.
Data: 2026-05-13.

## Objetivo

Definir como o CRM e os agentes usam configuracoes publicadas sem depender de rascunhos, conversa do agente ou regras duplicadas.

## Regra principal

O CRM e os agentes so podem agir com base em configuracao publicada ou default seguro.

Rascunho de setup nao muda comportamento operacional.

## Camadas de leitura

1. `PublishedConfiguration`
   - Estado ativo do studio.
2. `PolicyVersion`
   - Politica versionada aplicavel.
3. `ResolvedRule`
   - Resultado ja resolvido considerando precedencia.
4. `ExecutionSnapshot`
   - Snapshot gravado quando uma execucao/tarefa/aprovacao nasce.
5. `AuditEvent`
   - Registro imutavel do que foi usado e por que.

## Fluxo de leitura

```text
acao solicitada
  -> identificar tenant, usuario, objeto e fluxo
  -> carregar configuracao publicada
  -> resolver permissao/plano/cota/privacidade
  -> resolver politica e regra especifica
  -> retornar decisao permitida/bloqueada/pendente
  -> executar, criar tarefa ou pedir aprovacao
  -> gravar snapshot e auditoria
```

## Decisoes possiveis

| Decisao | Significado | Exemplo |
|---|---|---|
| Permitido manual | Pessoa pode executar. | Editar aluno, criar tarefa. |
| Permitido copiloto | IA pode sugerir/preparar. | Redigir mensagem de reposicao. |
| Permitido autonomo | Agente pode executar sem aprovacao. | Lembrete seguro dentro da politica. |
| Exige aprovacao | Precisa decisor humano. | Desconto, excecao, mensagem sensivel. |
| Bloqueado por plano | Entitlement nao cobre. | Agente Financeiro no plano 3 sem slot. |
| Bloqueado por cota | Uso chegou ao limite. | Envio autonomo pago com cota 100%. |
| Bloqueado por permissao | Usuario nao pode. | Recepcao tentando dar desconto. |
| Bloqueado por privacidade | Consentimento/opt-out impede. | WhatsApp automatico bloqueado. |
| Pendente de dados | Falta dado necessario. | Aluno sem plano associado. |
| Pendente de integracao | Canal/provedor indisponivel. | WhatsApp desconectado. |
| Pendente de politica | Politica sensivel nao publicada. | Autonomia sem guardrail. |

## Snapshot

Toda acao sensivel precisa guardar:

- tenant;
- usuario ou agente;
- objeto afetado;
- regra resolvida;
- versao de politica;
- modo do fluxo;
- permissao usada;
- cota/ledger;
- template/canal;
- antes/depois quando houver;
- motivo;
- idempotency key quando houver ferramenta externa.

## Quando regra muda

Mudanca em regra publicada nao reescreve historico.

| Situacao | Comportamento |
|---|---|
| Tarefa ja criada | Continua com snapshot original, mas mostra aviso se regra mudou. |
| Aprovacao pendente | Deve recalcular impacto antes de aprovar. |
| Execucao em andamento | Usa snapshot do inicio; se risco alto, pausa. |
| Fluxo autonomo ativo | Reexecuta preflight antes de continuar. |
| Cobranca ja gerada | Mantem regra original salvo ajuste auditado. |
| Aula futura | Pode aplicar nova regra se vigencia permitir. |

## Falta de configuracao

Se falta configuracao:

- acao manual segura pode continuar;
- copiloto pode explicar pendencia;
- autonomia deve bloquear;
- sistema cria pendencia de setup quando necessario.

## Regras para 0 agentes

Com 0 agentes:

- CRM le configuracoes normalmente;
- tarefas/checklists/aprovacoes funcionam;
- resolucoes de regra retornam `manual`;
- cotas de agente nao sao consumidas;
- botoes de IA mostram bloqueado por plano ou preparacao futura.

## Regras para 1, 3 e 7 agentes

| Plano | Consumo |
|---|---|
| 1 agente | Resolver regras apenas para o slot ativo. Outros dominios retornam manual/bloqueado por plano. |
| 3 agentes | Resolver regras dos dominios ativos; demais continuam manuais. |
| 7 agentes | Resolver todos os dominios, mas autonomia ainda depende de politica, cota e permissao. |

## Idempotencia e cota

Todo uso de IA/ferramenta externa precisa:

- evento de uso idempotente;
- origem;
- agente/fluxo;
- custo estimado;
- status;
- retry sem dupla cobranca;
- conciliacao posterior com provedor quando houver.

## Aceite

Este contrato esta correto quando:

- CRM e agentes nunca leem rascunho;
- toda execucao sensivel guarda snapshot;
- mudanca de regra nao corrompe historico;
- falta de configuracao bloqueia autonomia, nao o CRM manual;
- 0/1/3/7 agentes tem leitura consistente.
