# Fonte Da Verdade E Precedencia Do Setup

Status: rascunho consolidado.
Data: 2026-05-13.

## Objetivo

Definir onde cada regra mora, quem vence quando ha conflito e como o sistema evita duplicidade.

## Principio

Uma regra pode aparecer em varias telas, mas so pode ser editada em uma fonte canonica.

## Matriz de fonte da verdade

| Regra/Dado | Fonte canonica | Telas que exibem/usam | Observacao |
|---|---|---|---|
| Plano Taliya e agentes inclusos | Billing/Entitlements | Configuracoes, Agentes, Uso, Billing | CRM apenas reflete. |
| Membros e papeis | Configuracoes/Permissoes | App shell, tarefas, aprovacao | Agente nao tem permissao propria. |
| Horarios e feriados | Configuracoes/Studio/Agenda | Agenda, Hoje, Agentes | Afeta janelas e conflitos. |
| Turmas/aulas | Agenda/Turmas | Alunos, Hoje, Reposicoes | Agenda e fonte operacional. |
| Chamada/presenca | Aula/Chamada | Aluno, financeiro, historico | Correcao humana auditada vence automacao. |
| Modelo de cobranca | Configuracoes/Financeiro/Modelos | Financeiro, Aluno, Agenda | Sensivel e versionado. |
| Direito/consumo de aulas | Configuracoes/Agenda/Consumo | Chamada, Reposicoes, Aluno | Deve ler mesma regra do financeiro. |
| Politica de reposicao | Configuracoes/Agenda + Politicas | Agenda, Hoje, Agente Agenda | Se sensivel, referenciar politica versionada. |
| Inadimplencia/tolerancia | Configuracoes/Financeiro | Agenda, Financeiro, Hoje | Financeiro vence bloqueio operacional. |
| Opt-out/consentimento | Privacidade | Inbox, Comunicados, Agentes | Regra mais restritiva vence. |
| Template externo | Templates/Canais | Inbox, Agentes, Comunicados | Envio externo exige template aprovado. |
| Fluxo de agente | Agentes/Fluxos | Hoje, Operacao, Execucoes | Studio configura dentro do entitlement. |
| Modo do fluxo | Agentes/Fluxos | Aprovacoes, Execucoes | Manual/copiloto/autonomo. |
| Politica operacional | Politicas | Agentes, Aprovacoes, Auditoria | Versionada e simulavel. |
| Cota/uso | Uso/Cotas/Ledger | Hoje, Agentes, Billing | Ledger vence UI. |
| Integracao | Integracoes | Canais, importacao, financeiro | Provedor informa estado tecnico. |
| Auditoria | Auditoria | Todas as areas sensiveis | Imutavel. |

## Precedencia geral

1. Restricao legal/privacidade.
2. Permissao do usuario.
3. Plano/entitlement Taliya.
4. Cota/limite de uso.
5. Politica operacional publicada.
6. Regra especifica do aluno.
7. Regra do plano do aluno.
8. Regra da turma/aula.
9. Regra padrao do studio.
10. Default seguro do sistema.

## Exemplos de conflito

### Reposicao permitida vs aluno inadimplente

- Regra de reposicao permite.
- Regra financeira bloqueia ou exige aprovacao.
- Resultado: se politica financeira for mais restritiva, agenda cria tarefa/aprovacao; nao envia convite autonomo.

### Mensagem automatica vs opt-out

- Fluxo autonomo esta ativo.
- Aluno deu opt-out.
- Resultado: opt-out vence; sistema bloqueia mensagem e registra motivo.

### Agente ativo vs cota 100%

- Fluxo autonomo publicado.
- Cota chegou a 100%.
- Resultado: automacao paga bloqueada; caminho manual/copiloto local quando permitido.

### Usuario sem permissao vs regra aprovada

- Politica permite excecao.
- Usuario nao tem papel permitido.
- Resultado: acao bloqueada; pode solicitar aprovacao.

### Template aprovado vs canal desconectado

- Template existe.
- WhatsApp desconectado.
- Resultado: envio bloqueado; cria pendencia de integracao.

## Resolucao de regra

O sistema deve resolver regra em quatro passos:

1. Buscar restricoes globais: privacidade, permissao, plano, cota.
2. Buscar politica publicada aplicavel.
3. Buscar regra mais especifica no escopo: aluno, plano, turma, unidade, studio.
4. Se nao houver regra, aplicar default seguro ou bloquear acao sensivel.

## Regra para agentes

Agentes nunca escolhem precedencia.

Eles consultam o resultado ja resolvido pelo sistema:

- permitido;
- permitido com aprovacao;
- permitido apenas manual/copiloto;
- bloqueado;
- pendente de dados;
- pendente de politica;
- pendente de cota;
- pendente de canal.

## Aceite

Este documento esta correto quando:

- toda regra sensivel tem fonte canonica;
- conflitos comuns tem resultado esperado;
- agentes consomem decisao resolvida, nao regras soltas;
- billing, permissao, cota e privacidade sempre vencem quando restringem acao.
