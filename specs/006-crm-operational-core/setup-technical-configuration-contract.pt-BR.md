# Contrato Tecnico Das Configuracoes

Status: rascunho consolidado.
Data: 2026-05-13.

## Objetivo

Definir como uma configuracao deve existir no sistema para evitar regra solta, duplicada ou nao auditavel.

Este contrato nao define banco de dados final. Ele define o formato conceitual que qualquer implementacao precisa respeitar.

## Objeto canonico

Toda configuracao publicada deve ser representada como um objeto estruturado.

```text
ConfigurationRule
  id
  key
  domain
  ownerSurface
  businessName
  plainDescription
  type
  status
  scope
  sourceOfTruth
  defaultValue
  currentValue
  presetSource
  version
  effectiveFrom
  effectiveUntil
  dependencies
  impact
  permissions
  sensitivity
  validation
  publicationLayer
  rollbackPolicy
  auditPolicy
```

## Campos obrigatorios

| Campo | Papel |
|---|---|
| `id` | Identificador interno imutavel. |
| `key` | Chave estavel usada por CRM/agentes. |
| `domain` | Area: studio, agenda, financeiro, agentes, politicas, cotas etc. |
| `ownerSurface` | Tela canonica que edita a regra. |
| `businessName` | Nome legivel para gestor. |
| `plainDescription` | Explicacao simples em PT-BR. |
| `type` | Boolean, enum, number, money, duration, schedule, list, policyRef etc. |
| `status` | Draft, validando, pronto, publicado, bloqueado, pausado, obsoleto. |
| `scope` | Tenant, unidade, turma, plano, aluno, fluxo, canal. |
| `sourceOfTruth` | Quem manda nessa regra. |
| `defaultValue` | Default seguro do sistema. |
| `currentValue` | Valor atual em rascunho ou publicado. |
| `version` | Versao publicada. |
| `dependencies` | Regras/dados exigidos antes de publicar. |
| `impact` | Telas, fluxos, agentes e casos afetados. |
| `permissions` | Quem pode editar/publicar. |
| `sensitivity` | Baixa, media, alta, critica. |
| `validation` | Validacoes exigidas. |
| `publicationLayer` | CRM, Agenda, Financeiro, Canais, Politicas, Agentes. |
| `rollbackPolicy` | Como reverter. |
| `auditPolicy` | O que registrar. |

## Estados

| Estado | Significado |
|---|---|
| Draft | Rascunho gerado pelo sistema a partir do setup. |
| Incompleto | Falta dado obrigatorio. |
| Em validacao | Sistema esta checando dependencias/conflitos. |
| Pronto para revisar | Pode ser mostrado ao gestor. |
| Aguardando aprovacao | Exige confirmacao do gestor ou papel autorizado. |
| Publicado | Ativo para CRM/agentes. |
| Publicado parcialmente | Camada segura ativa; parte sensivel pendente. |
| Bloqueado | Regra nao pode publicar por plano, permissao, cota, politica ou conflito. |
| Pausado | Regra publicada foi pausada por usuario, incidente ou risco. |
| Obsoleto | Foi substituida por nova versao. |

## Tipos permitidos

| Tipo | Exemplo |
|---|---|
| Boolean | permitir reposicao com atraso: sim/nao |
| Enum | modo do fluxo: manual/copiloto/autonomo |
| Number | limite de tentativas: 3 |
| Money | valor do plano: R$ 420 |
| Duration | tolerancia de inadimplencia: 7 dias |
| Schedule | janela de envio: 08h-20h |
| List | papeis aprovadores |
| PolicyRef | referencia para politica versionada |
| TemplateRef | template aprovado para envio |
| IntegrationRef | canal/provedor conectado |

## Escopos

Ordem de escopo, do mais especifico ao mais amplo:

1. Aluno.
2. Plano do aluno.
3. Turma/aula.
4. Fluxo de agente.
5. Unidade.
6. Studio.
7. Default do sistema.

O sistema deve resolver a regra por escopo e registrar qual escopo venceu.

## Versionamento

Toda regra sensivel publicada precisa de versao.

Regras sensiveis:

- reposicao;
- consumo de aulas;
- cobranca;
- inadimplencia;
- desconto/cortesia/estorno;
- permissao;
- politica operacional;
- modo autonomo;
- templates externos;
- cota/economia;
- privacidade.

Cada execucao de agente, tarefa sensivel, aprovacao ou ajuste financeiro deve guardar snapshot da versao usada.

## Dependencias

Uma regra pode depender de:

- canal conectado;
- template aprovado;
- plano/entitlement;
- permissao do usuario;
- politica publicada;
- cota disponivel;
- fallback humano;
- dados de aluno;
- plano do aluno;
- turma ativa;
- importacao concluida.

Se dependencia falhar, a regra pode:

- bloquear publicacao;
- publicar manual;
- publicar copiloto;
- pedir aprovacao;
- criar pendencia.

## Validacao

Antes de publicar, o sistema valida:

1. valor no tipo correto;
2. campos obrigatorios;
3. escopo valido;
4. permissao do usuario;
5. conflito com regra mais forte;
6. impacto em dados existentes;
7. impacto em fluxos ativos;
8. politica e cota;
9. auditoria;
10. rollback possivel.

## Consumo por CRM e agentes

O CRM e os agentes nao leem rascunhos. Eles leem apenas:

- regra publicada;
- snapshot de regra para uma execucao;
- default seguro quando permitido;
- estado de bloqueio quando nao ha regra valida.

Se nao houver regra publicada para uma acao sensivel, o comportamento seguro e manual/copiloto, nunca autonomo.

## Exemplo

```text
key: agenda.reposicao.exige_credito_disponivel
domain: agenda
ownerSurface: /app/configuracoes/agenda/consumo-aulas
businessName: Aluno precisa ter aula disponivel para repor?
type: boolean
scope: studio
sourceOfTruth: configuracoes_agenda
defaultValue: true
currentValue: true
sensitivity: alta
publicationLayer: Agenda
dependencies:
  - modelos_de_consumo_publicados
impact:
  pages: Hoje, Agenda, Reposicoes, Aluno, Aprovacoes
  agents: Agenda, Atendimento
  useCases: pedido_de_reposicao, encaixe_em_vaga
permissions:
  edit: Dono, Admin
  approve: Dono, Admin
auditPolicy: antes/depois, ator, motivo, versao
```

## Aceite

Este contrato esta pronto quando:

- toda regra do inventario pode ser representada nesse formato;
- regras sensiveis possuem versao e auditoria;
- rascunho e publicacao estao separados;
- agentes so consomem regras publicadas/snapshots;
- faltas de regra resultam em caminho seguro.
