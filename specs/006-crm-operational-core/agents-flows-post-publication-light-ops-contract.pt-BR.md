# Taliya CRM - Contrato De Operacao Leve Pos-Publicacao Em Agentes/Fluxos

Status: contrato funcional v1.0.
Data: 2026-05-23.

## Objetivo

Definir como Agentes/Fluxos se comporta depois que uma rotina ou fluxo foi publicado.

Decisao:

```text
Nao criar paginas novas de operacao leve em Agentes/Fluxos.
```

Aproveitar as mesmas paginas:

```text
/app/agentes/[agentId]/rotinas/[routineId]
/app/agentes/[agentId]/rotinas/[routineId]/fluxos/[flowId]
```

Essas paginas passam a ter dois estados:

- antes de publicar: configuracao, simulacao e publicacao;
- depois de publicar: operacao leve, status, pausa, excecao, execucoes e rascunho de nova versao.

## Regra Central

Publicado nao edita direto.

Qualquer mudanca depois da publicacao cria rascunho.

```text
Versao publicada = protegida.
Nova mudanca = rascunho.
Rascunho precisa simular.
Simulacao valida libera nova publicacao.
Nova publicacao cria nova versao.
```

## O Que E Operacao Leve

Operacao leve e o suficiente para o usuario entender e agir sem virar Control Plane tecnico.

Inclui:

- ver status da rotina;
- ver status dos fluxos;
- ver excecoes abertas;
- pausar/retomar rotina;
- pausar/retomar fluxo;
- abrir execucoes;
- abrir aprovacao/tarefa/incidente relacionada;
- ajustar rascunho;
- simular nova versao;
- publicar nova versao.

Nao inclui:

- logs tecnicos;
- payloads;
- retries detalhados;
- stack trace;
- custo linha a linha;
- investigacao completa de incidente;
- auditoria completa em linha do tempo tecnica.

Essas coisas ficam em:

```text
/app/fluxos/execucoes/[runId]
/app/operacao/incidentes
/app/operacao/incidentes/[incidentId]
/app/uso
/app/auditoria
```

## Pagina Da Rotina Publicada

Rota:

```text
/app/agentes/[agentId]/rotinas/[routineId]
```

Estado canonico:

```text
routine_published_light_ops
```

### Header

Deve mostrar:

- breadcrumb;
- titulo da rotina;
- subtitulo;
- chip `Publicada`;
- chip da versao;
- chip do perfil publicado;
- chip de status operacional.

Exemplos:

```text
[Publicada] [v3] [Mais autonomo] [Operando]
```

```text
[Publicada] [v3] [Mais autonomo] [1 excecao aberta]
```

```text
[Publicada] [v3] [Mais autonomo] [Pausada]
```

```text
[Publicada] [v3] [Rascunho com alteracoes]
```

### Bloco Principal

Antes de publicar, a pagina mostra `Como essa rotina deve trabalhar?`.

Depois de publicar, a pagina deve priorizar:

```text
Como esta rotina esta operando agora?
```

Conteudo:

- versao publicada;
- data de publicacao;
- usuario que publicou;
- perfil publicado;
- ultima simulacao valida;
- status geral;
- fluxos operando;
- fluxos manuais planejados;
- fluxos com aprovacao ao executar;
- excecoes abertas;
- pausas ativas;
- rascunho aberto, se houver.

### Cards Dos Fluxos

Cada card de fluxo continua existindo.

Depois de publicado, cada card mostra:

- nome do fluxo;
- modo publicado;
- status atual;
- resumo do comportamento;
- se houve execucao recente;
- se ha excecao aberta;
- se esta pausado;
- se tem rascunho diferente;
- CTA principal contextual.

Estados de card:

| Estado | Chip | CTA principal |
|---|---|---|
| operando | `Operando` | `Ver fluxo` |
| manual planejado | `Manual planejado` | `Ver caminho manual` |
| aprovacao ao executar | `Aprovacao ao executar` | `Ver aprovadores` |
| excecao aberta | `Excecao aberta` | `Resolver excecao` |
| pausado | `Pausado` | `Retomar fluxo` ou `Ver pausa` |
| rascunho alterado | `Rascunho alterado` | `Revisar rascunho` |
| bloqueado apos publicar | `Bloqueado` | `Ver bloqueio` |

### Acoes Da Rotina Publicada

CTA principal normal:

```text
Ver execucoes
```

CTAs secundarios:

- `Pausar rotina`;
- `Simular novamente`;
- `Ajustar rascunho`;
- `Ver auditoria`;
- `Ver publicacao`;

Se ha rascunho:

- `Continuar rascunho`;
- `Descartar rascunho`;
- `Simular nova versao`;

Se ha excecao:

- `Resolver excecao`;
- `Ver execucao`;

Se pausada:

- `Retomar rotina`;
- `Ver motivo da pausa`;

## Pagina Do Fluxo Publicado

Rota:

```text
/app/agentes/[agentId]/rotinas/[routineId]/fluxos/[flowId]
```

Estado canonico:

```text
flow_published_light_ops
```

### Header

Deve mostrar:

- nome do fluxo;
- modo publicado;
- status atual;
- versao da rotina;
- preflight compacto atual.

Exemplos:

```text
[Autonomo com excecoes] [Operando] [v3]
```

```text
[Autonomo com aprovacao] [Aprovacao pendente] [v3]
```

```text
[Manual] [Manual planejado] [v3]
```

```text
[Autonomo com excecoes] [Pausado] [v3]
```

### Bloco Principal

Antes de publicar:

```text
Como este fluxo deve trabalhar?
```

Depois de publicar:

```text
Como este fluxo esta operando agora?
```

Mostra:

- modo publicado;
- comportamento publicado em Inicio, Meio e Fim;
- ajustes publicados;
- responsaveis/aprovadores publicados;
- fallback publicado;
- ultima execucao, se houver;
- excecao aberta, se houver;
- pausa, se houver;
- rascunho diferente, se houver.

### Ajustar Fluxo Publicado

O botao nao deve editar direto.

CTA:

```text
Ajustar rascunho
```

Ao clicar:

- cria ou abre rascunho do fluxo;
- marca a rotina como `Rascunho com alteracoes`;
- invalida simulacao anterior para nova versao;
- nao altera a versao publicada ate nova publicacao.

### Acoes Do Fluxo Publicado

CTAs possiveis:

- `Ver execucoes`;
- `Simular fluxo`;
- `Ajustar rascunho`;
- `Pausar fluxo`;
- `Retomar fluxo`;
- `Resolver excecao`;
- `Abrir aprovacao`;
- `Ver auditoria`.

Nao mostrar:

- `Salvar ajuste` diretamente na versao publicada;
- `Publicar fluxo` como CTA principal;
- logs tecnicos.

## Rascunho Sobre Versao Publicada

Quando o usuario altera algo depois da publicacao:

Estado:

```text
published_with_draft
```

Como aparece na rotina:

```text
[Publicada] [v3] [Rascunho com alteracoes]
```

Bloco:

```text
Existe um rascunho com mudancas que ainda nao afetam a rotina publicada.
```

Mostra:

- versao publicada atual;
- o que mudou no rascunho;
- fluxos alterados;
- simulacao do rascunho;
- CTA `Simular nova versao`;
- CTA `Descartar rascunho`;
- CTA `Revisar para publicar`, quando simulacao passar.

Regra:

```text
Rascunho nunca altera execucao atual ate nova publicacao.
```

## Excecao Aberta Em Rotina Publicada

Estado:

```text
published_with_exception
```

Como aparece:

```text
[Publicada] [1 excecao aberta]
```

Na rotina:

- card do fluxo afetado mostra `Excecao aberta`;
- mostra motivo simples;
- mostra quem foi chamado;
- mostra onde continuar.

CTA principal:

```text
Resolver excecao
```

CTAs secundarios:

- `Ver execucao`;
- `Abrir tarefa`;
- `Abrir aprovacao`;
- `Pausar fluxo`;

Regra:

Uma excecao localizada nao quebra a rotina inteira.

Se a excecao comprometer a rotina:

```text
[Publicada] [Excecao critica]
```

e a UI deve oferecer `Pausar rotina` ou `Ver incidente`.

## Pausa E Retomada

### Pausar rotina

Acontece na mesma pagina da rotina.

Modal/drawer deve mostrar:

- motivo obrigatorio;
- quais fluxos param;
- o que continua manual;
- execucoes em andamento;
- mensagens futuras;
- auditoria.

CTA:

```text
Confirmar pausa
```

Depois:

```text
[Publicada] [Pausada]
```

### Retomar rotina

Exige:

- permissao;
- preflight atual OK;
- incidente resolvido, se houver;
- cota suficiente;
- integracoes OK;
- nova simulacao se houve mudanca.

CTA:

```text
Retomar rotina
```

### Pausar fluxo

Acontece na pagina do fluxo ou card da rotina.

Pausa apenas aquele fluxo.

Outros fluxos continuam se independentes.

### Retomar fluxo

Exige:

- preflight do fluxo OK;
- motivo de pausa resolvido;
- permissao;
- simulacao se configuracao mudou.

## Rollback

Rollback fica disponivel como acao de rotina publicada, mas nao vira pagina nova.

CTA:

```text
Restaurar versao anterior
```

Modal/drawer mostra:

- versao atual;
- versao anterior;
- diferencas;
- o que volta;
- o que nao volta;
- impacto em rascunho aberto;
- necessidade de simulacao;
- auditoria.

Rollback nunca desfaz:

- mensagem ja enviada;
- pagamento confirmado;
- dado compartilhado;
- tarefa concluida;
- aprovacao decidida;
- auditoria.

## Agente De Configuracao Na Operacao Leve

Aparece na rotina publicada e no fluxo publicado quando houver:

- rascunho;
- pausa;
- excecao;
- simulacao;
- publicacao;
- duvida de configuracao.

Nao deve virar investigador tecnico.

Mensagem base em rotina publicada:

```text
Esta rotina esta publicada. A versao ativa continua rodando enquanto qualquer ajuste novo fica em rascunho ate ser simulado e publicado.
```

Sugestoes:

- `O que esta ativo agora?`
- `Como ajustar sem afetar a versao publicada?`
- `O que acontece se eu pausar?`
- `Onde vejo as execucoes?`

Mensagem base com excecao:

```text
A rotina continua publicada, mas um fluxo abriu uma excecao. A Taliya parou naquele ponto e chamou a equipe definida.
```

## Auditoria

Registrar:

- publicacao;
- abertura de rascunho;
- alteracao de rascunho;
- simulacao de nova versao;
- nova publicacao;
- pausa;
- retomada;
- rollback;
- excecao;
- abertura de execucao;
- decisao humana quando houver.

## O Que Nao Pode Acontecer

- editar versao publicada diretamente;
- esconder rascunho aberto;
- publicar nova versao sem simulacao valida;
- misturar status de rascunho com status publicado;
- transformar pagina da rotina em log tecnico;
- criar rota nova de operacao leve dentro de Agentes/Fluxos;
- chamar Control Plane de configuracao;
- retomar fluxo pausado por incidente sem resolver incidente.

## Checklist De QA

Operacao leve pos-publicacao esta correta quando:

1. usa a mesma pagina da rotina;
2. usa a mesma pagina do fluxo;
3. versao publicada fica protegida;
4. mudanca cria rascunho;
5. rascunho nao altera execucao atual;
6. nova versao exige simulacao;
7. excecao aberta aparece no card do fluxo;
8. pausa/retomada exigem motivo/preflight/permissao;
9. execucao detalhada abre rota global;
10. incidente abre rota de incidente;
11. auditoria registra a decisao;
12. a pagina nao vira painel tecnico.
