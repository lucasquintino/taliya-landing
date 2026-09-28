# Taliya CRM - Contrato Do Resultado De Simular Rotina

Status: contrato funcional v1.0.
Data: 2026-05-23.

## Objetivo

Definir exatamente o que acontece quando o usuario clica em `Simular rotina`.

`Simular rotina` nao e uma pagina visual propria neste momento.

Ela e uma acao da pagina da rotina que valida o conjunto dos fluxos e gera um resultado consolidado para:

- atualizar a pagina da rotina;
- liberar ou bloquear `Revisar para publicar`;
- alimentar a pagina `Publicar rotina`;
- explicar quais fluxos ficam prontos, manuais, bloqueados ou pendentes.

## Onde Acontece

Pagina da rotina:

```text
/app/agentes/[agentId]/rotinas/[routineId]
```

Exemplo:

```text
/app/agentes/agenda/rotinas/presenca-e-faltas
```

Nao usar como rota principal:

```text
/app/agentes/[agentId]/rotinas/[routineId]/simular
```

Essa rota pode existir tecnicamente no futuro, mas o produto MVP trata `Simular rotina` como acao dentro da propria rotina.

## Diferenca Entre Simular Rotina E Simular Fluxo

| Acao | Para que serve | Visual |
|---|---|---|
| `Simular fluxo` | Ensaiar um fluxo especifico em um cenario concreto. | Pode usar celular, objeto do CRM e linha de execucao detalhada. |
| `Simular rotina` | Validar o conjunto dos fluxos de uma rotina antes da publicacao. | Resultado consolidado dentro da rotina/publicacao. |

`Simular rotina` nao mostra conversa detalhada de celular para cada fluxo.

Se o usuario quiser entender um caso especifico, abre `Simular fluxo`.

## Quando O Usuario Clica Em Simular Rotina

A Taliya deve validar:

1. plano/entitlement;
2. permissao do usuario;
3. perfil da rotina;
4. modos de cada fluxo;
5. ajustes individuais;
6. teto de cada fluxo;
7. dados obrigatorios;
8. integracoes/canais;
9. templates e tom quando houver mensagem;
10. responsaveis por excecao;
11. aprovadores obrigatorios;
12. cota estimada;
13. auditoria ativa;
14. incidentes ou pausas abertas;
15. encadeamentos entre fluxos.

## Resultado Geral

O resultado consolidado tem quatro estados possiveis.

| Estado | Chip | Significado | CTA principal |
|---|---|---|---|
| passou | `Simulacao concluida` | Todos os fluxos podem seguir como configurados. | `Revisar para publicar` |
| passou com avisos | `Simulacao com avisos` | Rotina pode publicar, mas ha fluxos manuais, aprovacoes ao executar ou alertas de cota/integracao nao bloqueantes. | `Revisar para publicar` |
| bloqueada | `Simulacao bloqueada` | Um ou mais gates impedem publicar a rotina como prometida. | `Corrigir bloqueios` |
| desatualizada | `Simulacao desatualizada` | Havia resultado anterior, mas ajustes mudaram depois. | `Simular novamente` |

Regra:

```text
Sem simulacao valida = nao publica.
Simulacao desatualizada = nao publica.
Simulacao bloqueada = nao publica.
Agentes/Fluxos nao tem publicacao parcial de rotina.
```

## Onde O Resultado Aparece Na Pagina Da Rotina

Depois de simular, a pagina da rotina deve mostrar:

1. chip no header;
2. bloco curto de resultado consolidado;
3. status em cada card de fluxo;
4. CTA principal atualizado;
5. Agente de Configuracao explicando o resultado.

### Header

Exemplos:

```text
[Mais autonomo] [4 fluxos] [Simulacao concluida]
```

```text
[Mais autonomo] [4 fluxos] [Simulacao com avisos]
```

```text
[Mais autonomo] [4 fluxos] [Simulacao bloqueada]
```

```text
[Mais autonomo personalizado] [4 fluxos] [Simulacao desatualizada]
```

### Bloco De Resultado

Titulo quando passou:

```text
Simulacao concluida
```

Texto:

```text
A Taliya validou os fluxos desta rotina. Revise o que sera publicado antes de colocar em operacao.
```

Titulo quando passou com avisos:

```text
Simulacao concluida com avisos
```

Texto:

```text
A rotina pode seguir, mas alguns fluxos exigem aprovacao, ficam manuais ou dependem de atencao.
```

Titulo quando bloqueou:

```text
Simulacao bloqueada
```

Texto:

```text
A rotina ainda nao pode ser publicada como esta. Resolva os bloqueios abaixo ou ajuste os fluxos afetados.
```

## Resultado Por Fluxo

Cada card de fluxo da rotina deve receber um resultado.

| Resultado do fluxo | Chip | Significado | CTA |
|---|---|---|---|
| pronto | `Pronto` | Pode ser publicado no modo selecionado. | `Ver e ajustar` |
| manual | `Manual` | Fica como tarefa/checklist/caso humano. | `Ver caminho manual` |
| copiloto | `Copiloto` | Prepara sugestao, humano decide. | `Ver e ajustar` |
| aprovacao ao executar | `Aprovacao ao executar` | Publica, mas pede aprovacao quando o caso real acontecer. | `Ver aprovadores` |
| aprovacao pendente para publicar | `Aprovacao para publicar` | Precisa aprovacao antes da publicacao. | `Enviar para aprovacao` |
| bloqueado por integracao | `Integracao pendente` | Falta provedor/canal obrigatorio. | `Abrir integracao` |
| bloqueado por cota | `Cota insuficiente` | Nao ha cota para autonomia prevista. | `Ver cotas` |
| bloqueado por permissao | `Sem permissao` | Usuario atual nao pode publicar/alterar. | `Pedir acesso` |
| bloqueado por dado | `Dado pendente` | Falta dado minimo do CRM. | `Corrigir dado` |
| bloqueado por plano | `Nao contratado` | Agente/fluxo nao esta no plano. | `Ver planos` |
| pausado | `Pausado` | Configuracao existe, mas fluxo nao executa. | `Ver pausa` |
| incidente | `Incidente aberto` | Incidente impede execucao/publicacao. | `Ver incidente` |

## Agrupamentos Do Resultado Consolidado

O resultado deve agrupar os fluxos em blocos simples.

### Fluxos prontos

Mostra fluxos que podem ser publicados exatamente como configurados.

Campos:

- nome do fluxo;
- modo;
- resumo do que faz;
- onde continua;
- cota estimada, quando houver;
- CTA `Ver fluxo`.

Exemplo:

```text
Confirmacao de presenca
Autonomo
Vai enviar confirmacao antes da aula e registrar respostas.
Continua em: Aula / Tarefas
```

### Fluxos manuais

Mostra fluxos que continuam humanos.

Campos:

- nome do fluxo;
- motivo de ficar manual;
- tarefa/checklist/caso criado;
- responsavel;
- CTA `Ver caminho manual`.

Exemplo:

```text
Correcao de presenca
Manual
A equipe revisa e registra a correcao. A Taliya organiza a tarefa e o contexto.
Responsaveis: Coordenacao, Dono/admin
```

### Fluxos com aprovacao

Mostra fluxos que podem publicar, mas exigem decisao humana.

Separar dois tipos:

| Tipo | O que significa |
|---|---|
| Aprovacao para publicar | A rotina nao publica antes da aprovacao. |
| Aprovacao ao executar | A rotina publica, mas o caso real para em aprovacao. |

Campos:

- fluxo;
- tipo de aprovacao;
- aprovadores;
- quando pede aprovacao;
- o que nao faz sozinho;
- CTA.

### Fluxos bloqueados

Mostra fluxos que impedem a publicacao da rotina.

Campos:

- fluxo;
- motivo;
- fonte da verdade;
- por que bloqueia a rotina;
- o que continua manual;
- CTA de correcao.

Exemplo:

```text
Falta com aviso
Integracao pendente
Fonte: Integracoes / WhatsApp
Bloqueia envio automatico. Registro manual continua.
CTA: Abrir integracao
```

## Preflight Consolidado

O resultado da simulacao deve gerar um preflight consolidado.

| Item | Estados possiveis | Bloqueia publicacao? |
|---|---|---|
| Plano | OK, nao contratado | sim |
| Permissao | OK, sem permissao | sim |
| Integracoes | OK, pendente, falha | depende do fluxo |
| Cota | disponivel, alerta, insuficiente | insuficiente bloqueia autonomia |
| Templates | aprovados, pendentes | pendente bloqueia envio |
| Responsaveis | definidos, ausentes | ausente bloqueia excecao/aprovacao |
| Dados obrigatorios | OK, pendentes | sim para fluxo afetado |
| Aprovacoes | ao executar, antes de publicar, ausente | depende |
| Auditoria | ativa, indisponivel | sim para autonomo/aprovacao |
| Incidentes | nenhum, aberto | aberto pode bloquear |
| Pausas | nenhuma, fluxo pausado, rotina pausada | pausa bloqueia execucao |

## Cota No Resultado

Cota deve aparecer de forma simples.

Estados:

| Estado | Texto | Efeito |
|---|---|---|
| disponivel | `Cota disponivel para esta rotina.` | nao bloqueia |
| alerta | `Uso alto; rotina pode publicar, mas sera monitorada.` | nao bloqueia |
| economia ativa | `Economia ativa; fluxos de baixa prioridade podem virar tarefa.` | pode rebaixar fluxo |
| insuficiente | `Cota insuficiente para os fluxos autonomos.` | bloqueia autonomia/publicacao conforme caso |

Nao mostrar:

- calculo tecnico de token;
- custo interno;
- grafico complexo.

Mostrar:

- impacto operacional;
- quais fluxos consomem;
- quais ficam manuais;
- CTA `Ver cotas`.

## Integracao No Resultado

Integracao nao e ajuste de rotina.

Estados:

| Estado | Texto | CTA |
|---|---|---|
| OK | `WhatsApp conectado.` | nenhum ou `Ver detalhes tecnicos em Canais` |
| pendente | `WhatsApp precisa ser conectado para enviar mensagens.` | `Abrir integracao` |
| falha | `WhatsApp esta falhando. Envios automaticos ficam bloqueados.` | `Ver logs` |
| limitada | `Integracao conectada, mas sem permissao para esta acao.` | `Revisar permissao` |

O resultado deve apontar para Integracoes, nao abrir configuracao tecnica dentro da rotina.

## Aprovacao No Resultado

Tipos:

### Aprovacao ao executar

Pode publicar a rotina.

Texto:

```text
Este fluxo sera publicado, mas cada caso sensivel vai pedir aprovacao antes de concluir.
```

### Aprovacao para publicar

Nao publica ainda.

Texto:

```text
Esta rotina precisa de aprovacao antes de entrar em operacao.
```

CTA:

```text
Enviar para aprovacao
```

### Aprovador ausente

Bloqueia.

Texto:

```text
Defina quem aprova este fluxo antes de publicar.
```

CTA:

```text
Definir aprovador
```

## Publicacao Depois De Simular

Agentes/Fluxos nao tem publicacao parcial de rotina.

Para publicar, a rotina precisa estar 100% pronta para o estado configurado.

Isso nao significa que todos os fluxos precisam ser autonomos. Significa que cada fluxo precisa estar pronto para o modo escolhido.

Estados prontos:

- fluxo Manual com responsavel, tarefa, checklist ou caminho humano definido;
- fluxo Copiloto com entrega da sugestao definida;
- fluxo Autonomo com aprovacao com aprovador definido;
- fluxo Autonomo com excecoes com fallback e responsaveis definidos;
- fluxo Autonomo com cota, permissao, integracao, dados e auditoria OK.

Estados que bloqueiam:

- fluxo sem integracao exigida pelo modo;
- fluxo sem cota para autonomia configurada;
- fluxo sem aprovador obrigatorio;
- fluxo pausado;
- fluxo fora do plano;
- simulacao desatualizada;
- template/regra obrigatoria pendente;
- dado obrigatorio ausente.

Texto quando bloqueia:

```text
Esta rotina ainda nao esta pronta para publicar. Resolva os bloqueios ou ajuste o modo dos fluxos afetados e simule novamente.
```

CTA:

```text
Corrigir bloqueios
```
## CTA Seguinte

A simulacao define o CTA principal da rotina.

| Resultado | CTA principal | CTAs secundarios |
|---|---|---|
| passou | `Revisar para publicar` | `Simular novamente`, `Ajustar fluxos` |
| passou com avisos | `Revisar para publicar` | `Ver avisos`, `Ajustar fluxos` |
| bloqueada corrigivel | `Corrigir bloqueios` | `Simular novamente`, `Voltar aos fluxos` |
| bloqueada por simulacao desatualizada | `Simular novamente` | `Ver alteracoes`, `Descartar rascunho` |
| precisa aprovacao para publicar | `Enviar para aprovacao` | `Ver aprovadores`, `Ajustar fluxos` |
| plano nao contratado | `Ver planos` | `Continuar manual` |
| sem permissao | `Pedir acesso` | `Voltar para rotina` |

## Agente De Configuracao

Depois de `Simular rotina`, o painel direito deve explicar o resultado consolidado.

### Passou

```text
A simulacao passou. A Taliya validou os fluxos desta rotina e voce ja pode revisar o que sera publicado.
```

Sugestoes:

- `O que vai acontecer sozinho?`
- `Onde a equipe sera chamada?`
- `Quais fluxos pedem aprovacao?`
- `Posso ajustar um fluxo antes de publicar?`

### Passou com avisos

```text
A simulacao passou com avisos. A rotina pode seguir, mas alguns fluxos ficarao manuais, pedirao aprovacao ou dependem de acompanhamento.
```

Sugestoes:

- `Quais avisos importam?`
- `Isso bloqueia publicacao?`
- `O que fica manual?`
- `Posso publicar assim?`

### Bloqueada

```text
A simulacao encontrou bloqueios. A rotina nao deve ser publicada como esta porque alguns fluxos nao conseguiriam operar do jeito prometido.
```

Sugestoes:

- `O que bloqueou?`
- `Qual fluxo devo corrigir primeiro?`
- `O que falta para publicar?`
- `O que continua manual?`

## Auditoria

Registrar cada simulacao de rotina como evento de auditoria.

Campos:

- routineId;
- agentId;
- profile;
- draftVersion;
- simulationId;
- userId;
- timestamp;
- resultado geral;
- fluxos prontos;
- fluxos manuais;
- fluxos com aprovacao;
- fluxos bloqueados;
- preflight consolidado;
- estimativa de cota;
- integracoes avaliadas;
- plano/entitlements avaliados;
- mudancas desde a simulacao anterior;
- CTA principal gerado.

Nao registrar como execucao real de fluxo.

Simulacao nao envia mensagem, nao altera agenda, nao cobra aluno e nao consome acao externa real.

## Invalidacao Da Simulacao

A simulacao fica desatualizada quando muda:

- perfil da rotina;
- modo de qualquer fluxo;
- ajuste importante de fluxo;
- template ou tom de mensagem;
- responsavel por excecao;
- aprovador;
- regra/politica usada;
- integracao volta ou falha;
- plano/entitlement;
- regra de cota/economia;
- pausa/incidente que afeta fluxo;
- composicao fixa da rotina em nova versao do produto.

Ao invalidar:

- chip vira `Simulacao desatualizada`;
- `Revisar para publicar` fica bloqueado;
- CTA principal vira `Simular novamente`;
- cards alterados mostram `Alterado depois da simulacao`.

## Exemplo: Presenca E Faltas

### Resultado Passou

Header:

```text
[Mais autonomo] [4 fluxos] [Simulacao concluida]
```

Bloco:

```text
Simulacao concluida
A Taliya validou os 4 fluxos. Revise a publicacao antes de colocar em operacao.
```

Fluxos:

| Fluxo | Resultado | Resumo |
|---|---|---|
| Confirmacao de presenca | Pronto | Envia confirmacao e registra respostas. |
| Falta com aviso | Pronto | Registra falta avisada e cria tarefa de reposicao. |
| Falta sem aviso | Pronto | Detecta ausencia depois da aula e abre acompanhamento. |
| Correcao de presenca | Aprovacao ao executar | Prepara correcao, mas nao altera historico sem aprovacao. |

CTA:

```text
Revisar para publicar
```

### Resultado Com Bloqueio

Header:

```text
[Mais autonomo] [4 fluxos] [Simulacao bloqueada]
```

Bloco:

```text
Simulacao bloqueada
WhatsApp esta desconectado. Fluxos que enviam mensagem nao podem operar automaticamente.
```

Fluxos:

| Fluxo | Resultado | CTA |
|---|---|---|
| Confirmacao de presenca | Integracao pendente | Abrir integracao |
| Falta com aviso | Integracao pendente | Abrir integracao |
| Falta sem aviso | Pronto sem envio automatico | Ver fluxo |
| Correcao de presenca | Aprovacao ao executar | Ver aprovadores |

CTA:

```text
Abrir integracao
```

CTA secundario:

```text
Manter manual por enquanto
```

## Checklist De QA

`Simular rotina` esta correto quando:

1. nao abre pagina visual nova;
2. nao usa celular/conversa como visual principal;
3. mostra resultado geral;
4. mostra resultado por fluxo;
5. separa prontos, manuais, bloqueados e aprovacao;
6. mostra cota de forma operacional;
7. mostra integracao como dependencia, nao ajuste;
8. define CTA seguinte;
9. bloqueia publicacao sem simulacao valida;
10. invalida resultado quando ajuste muda;
11. registra auditoria;
12. nao executa acao real externa;
13. alimenta `Publicar rotina`;
14. deixa claro o que continua manual.
