# Taliya CRM - Modelo Corrigido De Rotina, Simulacao, Publicacao E Ajuste

Status: contrato funcional v0.2.
Data: 2026-05-21.

## Correcao Importante

Este documento corrige a leitura anterior.

Simular rotina nao e mostrar apenas resultados agregados. Simular rotina e percorrer o fluxo real, passo a passo, com um cenario escolhido.

Publicar rotina nao e um botao generico. Publicar rotina publica uma versao da rotina com:

- modos de cada fluxo;
- ajustes compartilhados;
- requisitos checados;
- bloqueios explicados;
- cota estimada;
- auditoria prevista.

Ajustar rotina precisa mostrar a parte mais importante:

- modo de cada fluxo dentro da rotina;
- depois, poucos ajustes compartilhados.

## Hierarquia Correta

```text
Agente
  -> Rotina
      -> Fluxos
          -> Modo de cada fluxo
          -> Ajustes minimos
```

Exemplo:

```text
Agente Agenda
  -> Rotina Presenca e faltas
      -> B1 Confirmacao de presenca
      -> B2 Falta com aviso
      -> B3 No-show
      -> B14 Correcao de presenca
```

O dono/admin ve a rotina primeiro. Ele so abre fluxo individual se quiser detalhe avancado.

## Tela Do Agente Agenda

```text
Agente Agenda

Status: Ativo
WhatsApp: conectado
Cota: OK
Responsavel padrao: Recepcao

Rotinas do agente

[Presenca e faltas]
Confirma presenca, trata faltas e sugere acompanhamento de no-show.
4 fluxos por baixo
Status: rascunho / pronto para simular / ativo

[Simular] [Publicar] [Ajustar]

[Reposicoes e vagas]
[Agenda estrutural]
[Experimental com agenda]
```

## Rotina: Presenca E Faltas

Fluxos por baixo:

| Fluxo | Maior modo permitido | Modo no perfil Equilibrado |
|---|---|---|
| B1 Confirmacao de presenca | Autonomo | Autonomo |
| B2 Falta com aviso | Autonomo com excecoes | Autonomo com excecoes |
| B3 No-show | Autonomo com excecoes | Copiloto |
| B14 Correcao de presenca | Autonomo com aprovacao | Autonomo com aprovacao |

## Botao Ajustar

`Ajustar` abre primeiro a configuracao da rotina.

O bloco principal deve ser `Modo de cada fluxo`.

```text
Ajustar rotina: Presenca e faltas

1. Modo de cada fluxo

B1 Confirmacao de presenca
Modo: [Manual] [Copiloto] [Autonomo com aprovacao] [Autonomo com excecoes] [Autonomo]
Atual: Autonomo

B2 Falta com aviso
Modo: [Manual] [Copiloto] [Autonomo com aprovacao] [Autonomo com excecoes]
Atual: Autonomo com excecoes

B3 No-show
Modo: [Manual] [Copiloto] [Autonomo com aprovacao] [Autonomo com excecoes]
Atual: Autonomo com excecoes

B14 Correcao de presenca
Modo: [Manual] [Copiloto] [Autonomo com aprovacao]
Atual: Autonomo com aprovacao
```

Depois aparecem padroes herdados da rotina e ajustes realmente necessarios:

```text
2. Padroes da rotina

Lembrete de presenca
- Horario: 9h
- Template: Confirmacao acolhedora

Quando chamar humano
- resposta fora do padrao
- WhatsApp falhou
- pedido de remarcacao

Destino
- Excecoes vao para: Recepcao
- No-show vira tarefa para: Recepcao

Correcao de presenca
- Exige aprovacao: Sim
- Aprovador: Admin

[Simular alteracoes] [Salvar rascunho]
```

Regra:

- mudar modo muda como aquele fluxo opera;
- mudar ajuste muda apenas parametros importantes da rotina/fluxo;
- ajuste nao muda a logica fixa do produto.

## O Que Muda Quando Muda O Modo

Exemplo B2 Falta com aviso.

| Modo escolhido | O que acontece quando aluno avisa falta |
|---|---|
| Manual | Sistema registra pendencia/tarefa. Humano decide. |
| Copiloto | Agente sugere resposta e proxima acao. Humano aprova ou rejeita. |
| Autonomo com aprovacao | Agente prepara registro/reposicao e pede aprovacao antes de confirmar algo sensivel. |
| Autonomo com excecoes | Agente resolve aviso simples e chama humano se regra, credito ou remarcacao ficar ambigua. |
| Autonomo | Nao disponivel para B2 no MVP. |

## Botao Simular

`Simular` deve simular o fluxo real, nao apenas o resultado agregado.

Primeiro o usuario escolhe um cenario:

```text
Simular Presenca e faltas

Escolha um cenario
( ) Confirmar presenca antes da aula
( ) Aluno avisa falta
( ) Aula termina com no-show
( ) Humano corrige presenca
```

Depois a tela mostra o caminho real.

### Cenario 1: Confirmar Presenca Antes Da Aula

Fluxo usado: B1 Confirmacao de presenca.

```text
Cenario
Aula: Pilates solo, amanha 8h
Aluno: Ana
Canal: WhatsApp conectado
Modo: Autonomo

Caminho simulado
1. Gatilho: 24h antes da aula
2. Checar dados: aula existe, aluno tem WhatsApp, sem opt-out
3. Checar regra: lembrete permitido entre 8h e 20h
4. Checar cota: disponivel
5. Acao: enviar template "Confirmacao acolhedora"
6. Resposta esperada: SIM confirma presenca; NAO cria pendencia de falta
7. Auditoria: registrar envio, resposta e cota

Resultado desta simulacao
Executaria automaticamente.

Se falhar
Cria tarefa para Recepcao.
```

### Cenario 2: Aluno Avisa Falta

Fluxo usado: B2 Falta com aviso.

```text
Cenario
Aluno: Ana
Mensagem: "Nao vou conseguir ir hoje"
Modo: Autonomo com excecoes

Caminho simulado
1. Gatilho: mensagem recebida
2. Identificar aluno e aula provavel
3. Checar regra de falta com aviso
4. Checar credito/reposicao
5. Caso simples: registrar falta e sugerir proximo passo
6. Excecao: se aula nao for clara, credito tiver conflito ou aluno pedir remarcacao complexa, chamar humano
7. Auditoria: registrar decisao e tarefa se houver

Resultado desta simulacao
Resolveria caso simples.

Se sair do padrao
Vai para Recepcao em /app/tarefas.
```

### Cenario 3: Aula Termina Com No-show

Fluxo usado: B3 No-show.

```text
Cenario
Aula encerrada
Aluno nao compareceu
Modo: Autonomo com excecoes
Observacao: este modo aparece quando a rotina esta em Mais autonomo ou quando B3 foi personalizado.

Caminho simulado
1. Gatilho: chamada fechada
2. Detectar ausencia sem aviso
3. Checar historico: primeira vez ou recorrente
4. Caso normal: criar tarefa leve de acompanhamento
5. Excecao: se recorrente, risco alto ou contexto sensivel, chamar humano/retencao
6. Auditoria: registrar no-show e tarefa

Resultado desta simulacao
Criaria tarefa de acompanhamento.

Se risco alto
Vai para Retencao/Operacao.
```

### Cenario 4: Humano Corrige Presenca

Fluxo usado: B14 Correcao de presenca.

```text
Cenario
Recepcao quer mudar "faltou" para "presente"
Modo: Autonomo com aprovacao

Caminho simulado
1. Gatilho: usuario pede correcao
2. Checar permissao
3. Pedir motivo
4. Preparar antes/depois
5. Criar aprovacao para Admin
6. Se aprovado: atualizar chamada
7. Auditoria: registrar motivo, aprovador e antes/depois

Resultado desta simulacao
Nao corrigiria sozinho.
Criaria aprovacao em /app/aprovacoes.
```

## O Que A Simulacao Pode Mostrar Como Resumo

Depois de mostrar o caminho real, pode ter um resumo.

Exemplo:

```text
Resumo da simulacao
- Fluxo: B2 Falta com aviso
- Modo: Autonomo com excecoes
- Acao normal: registrar falta simples
- Para quando: aula incerta, credito conflita, pedido complexo
- Continua em: /app/tarefas
- Cota estimada: 1 mensagem, se houver resposta
- Auditoria: sim
```

Resumo e apoio. Nao e a simulacao inteira.

## Botao Publicar

`Publicar` deve publicar a rotina, explicando exatamente o que passa a valer.

```text
Publicar rotina: Presenca e faltas

Versao que sera publicada

Fluxos e modos
B1 Confirmacao de presenca -> Autonomo
B2 Falta com aviso -> Autonomo com excecoes
B3 No-show -> Copiloto
B14 Correcao de presenca -> Autonomo com aprovacao

Padroes herdados e ajustes publicados
Horario do lembrete: 9h
Template: Confirmacao acolhedora
Excecoes: Recepcao
Aprovador de correcao: Admin

O que comeca a acontecer
- B1 passa a enviar confirmacao sozinho quando os requisitos passarem.
- B2 passa a tratar falta simples e chamar humano em excecoes.
- B3 passa a sugerir acompanhamento de no-show para humano decidir.
- B14 passa a pedir aprovacao antes de corrigir chamada.

O que nao acontece
- Nao altera grade.
- Nao cria reposicao automaticamente se regra estiver ambigua.
- Nao envia mensagem para opt-out.
- Nao corrige presenca sem aprovacao.

Requisitos checados
WhatsApp: OK
Template: OK
Cota: OK
Responsavel: OK
Aprovador: OK

[Confirmar publicacao] [Voltar para ajustar]
```

Se algo falhar:

```text
Nao da para publicar tudo

Pronto para publicar
- B14 Correcao de presenca

Bloqueado
- B1 Confirmacao: WhatsApp nao conectado
- B2 Falta com aviso: template ausente

Opcoes
[Publicar somente o que esta pronto]
[Corrigir bloqueios]
[Cancelar]
```

## Como Fica Depois De Publicada

```text
Rotina: Presenca e faltas
Status: Ativa
Versao publicada: v3

Modos
B1 Autonomo
B2 Autonomo com excecoes
B3 Copiloto
B14 Autonomo com aprovacao

Atividade recente
- 42 confirmacoes executadas
- 6 faltas com aviso tratadas
- 3 sugestoes de no-show revisadas
- 1 correcao aguardando aprovacao

[Ver atividade] [Ajustar] [Simular alteracao] [Pausar]
```

## Botao Ver Atividade

Nao e configuracao. E continuidade operacional.

Mostra:

- execucoes recentes;
- aprovacoes abertas;
- tarefas criadas;
- bloqueios;
- cota consumida;
- incidentes, se houver.

Links:

- `/app/fluxos/execucoes/[runId]`;
- `/app/aprovacoes`;
- `/app/tarefas`;
- `/app/hoje`;
- tela de origem.

## Regra Final

```text
Simular = percorrer o caminho real de um fluxo/cenario.
Ajustar = escolher modos dos fluxos + poucos parametros da rotina.
Publicar = publicar a versao da rotina e explicar o que passa a valer.
```

Se uma tela nao deixa essas tres coisas obvias, ela esta errada.

## Criterios De Aceite

Este modelo esta correto quando:

- simulacao mostra caminho real passo a passo;
- publicacao mostra a versao que sera publicada;
- ajuste mostra modo por fluxo;
- rotina continua escondendo a complexidade dos 96 fluxos;
- usuario entende o que cada botao faz antes de clicar;
- configuracao continua minima, sem builder tecnico.
