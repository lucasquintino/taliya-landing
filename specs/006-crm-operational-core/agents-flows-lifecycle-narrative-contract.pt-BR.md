# Taliya CRM - Contrato De Narrativa Inicio Meio Fim Dos Fluxos

Status: contrato funcional v0.1.
Data: 2026-05-22.

## Objetivo

Todo fluxo precisa ser explicado como uma operacao completa, com inicio, meio e fim.

As regras, modos, excecoes e ajustes continuam existindo, mas a UI nao deve parecer uma lista tecnica de condicoes soltas.

O dono do studio precisa entender:

```text
Quando esse fluxo comeca?
O que a Taliya faz durante o fluxo?
Como esse fluxo termina?
```

## Regra Principal

O bloco `Como funciona neste modo` deve ser estruturado em:

1. `Inicio`
2. `Meio`
3. `Fim`

Essa estrutura vale para todos os modos:

- Manual;
- Copiloto;
- Autonomo com aprovacao;
- Autonomo com excecoes;
- Autonomo.

O que muda por modo e o nivel de execucao da Taliya em cada etapa.

## Estrutura Da Explicacao

Cada parte precisa ser explicativa.

Nao basta escrever:

```text
Inicio: identifica aluno.
Meio: registra falta.
Fim: salva auditoria.
```

Cada parte deve dizer:

- o que dispara;
- o que a Taliya le;
- o que a Taliya decide;
- o que o humano faz, quando houver;
- o que acontece se algo falhar;
- o que fica salvo;
- se ha proximo fluxo.

Na tela principal, cada parte deve ter 2 a 4 linhas curtas.

Detalhes maiores podem ir para tooltip, expansao ou Agente de Configuracao.

### Inicio

Explica o gatilho e a entrada do fluxo.

Deve responder:

- o que faz o fluxo comecar;
- quais dados precisam existir;
- qual pessoa, aluno, aula, pagamento, lead ou conversa esta envolvida;
- qual canal ou tela iniciou o caso, quando houver.

Exemplo:

```text
O fluxo comeca quando um aluno avisa que nao vai comparecer a uma aula.
A Taliya identifica o aluno, a aula e o horario do aviso.
```

### Meio

Explica o trabalho do fluxo no modo selecionado.

Deve responder:

- o que a Taliya verifica;
- o que ela faz sozinha;
- quando pede aprovacao;
- quando chama a equipe;
- quais limites usa.

Exemplo:

```text
No modo Autonomo com excecoes, a Taliya registra a falta quando o aviso chegou no prazo, a aula existe, a falta ainda nao foi registrada e a mensagem aprovada pode ser usada.
Ela chama a equipe se o aviso chegar fora do prazo, se nao encontrar aluno/aula, se a falta ja existir ou se o aluno pedir excecao, credito, cancelamento ou reclamar.
```

### Fim

Explica o resultado do fluxo.

Deve responder:

- o que fica registrado;
- se envia mensagem;
- se cria tarefa, aprovacao ou caso;
- se emenda em outro fluxo;
- onde a operacao continua;
- qual auditoria fica salva.

Exemplo:

```text
O fluxo termina com a falta registrada, mensagem enviada quando permitido e auditoria salva.
Depois disso, se houver reposicao, a Taliya cria uma tarefa para a rotina Vagas, reposicoes e lista de espera.
```

## Como Cada Modo Muda A Narrativa

| Modo | Inicio | Meio | Fim |
|---|---|---|---|
| Manual | Taliya identifica o caso e organiza contexto. | Humano decide e executa. | Humano registra o resultado; Taliya guarda auditoria. |
| Copiloto | Taliya identifica o caso e prepara sugestao. | Taliya sugere acao, texto ou decisao. | Humano aceita, edita ou descarta; Taliya registra a decisao. |
| Autonomo com aprovacao | Taliya identifica e prepara a acao. | Taliya valida regras e monta preview. | Para antes de concluir e pede aprovacao. |
| Autonomo com excecoes | Taliya identifica e executa o caso comum. | Segue sozinha quando as regras passam; chama equipe nas excecoes. | Conclui o caso comum ou entrega a excecao para humano/outro fluxo. |
| Autonomo | Taliya identifica, valida e executa. | Conclui sozinha dentro dos limites publicados. | Registra resultado, auditoria e continuidade sem decisao humana, salvo bloqueio. |

## Profundidade Obrigatoria Por Modo

### Manual

Precisa deixar claro que a Taliya nao decide nem executa a acao principal.

Mostrar:

- o que ela organiza;
- qual tarefa/checklist/caso cria;
- quem executa;
- onde o humano registra o resultado.

### Copiloto

Precisa deixar claro que a Taliya sugere, mas o humano decide.

Mostrar:

- qual sugestao/rascunho/resumo ela prepara;
- quais dados usa como base;
- quais botoes ou decisoes o humano tem;
- o que acontece se o humano rejeitar.

### Autonomo Com Aprovacao

Precisa deixar claro que a Taliya prepara tudo, mas para antes da conclusao.

Mostrar:

- o que ela valida;
- qual acao fica pronta;
- quem aprova;
- o que acontece se aprovar, recusar ou vencer.

### Autonomo Com Excecoes

Precisa deixar claro o caso comum e a excecao.

Mostrar:

- quando a Taliya resolve sozinha;
- acao que a Taliya executa sozinha;
- condicoes que chamam equipe;
- para onde a excecao vai;
- como termina o caso comum.

### Autonomo

Precisa deixar claro o limite de autonomia.

Mostrar:

- quais limites publicados permitem concluir;
- o que ela faz sozinha;
- o que faz parar;
- como registra auditoria;
- como continua em outro fluxo, quando houver.

## Relacao Com Encadeamento

Encadeamento pertence ao `Fim`.

Nao deve aparecer como condicao em `Inicio` ou `Meio`.

Exemplo correto:

```text
Fim
Depois da falta registrada, a Taliya cria uma tarefa de reposicao.
A rotina Vagas, reposicoes e lista de espera decide vaga, credito, prioridade e remarcacao.
```

Exemplo ruim:

```text
Segue sozinho quando o proximo passo apos falta esta definido.
```

## Relacao Com Ajustes

Ajustes aparecem depois da narrativa.

Cada ajuste deve deixar claro que parte do fluxo muda:

| Ajuste | Parte afetada |
|---|---|
| Prazo para aviso | Meio |
| Responsaveis por excecao | Meio/Fim |
| Tom/template da mensagem | Fim |
| Proximo passo apos falta | Fim |

## Exemplo: Falta Com Aviso

### Modo Selecionado

```text
Autonomo com excecoes
```

### Inicio

```text
O fluxo comeca quando o aluno avisa que nao vai comparecer.
A Taliya identifica o aluno, encontra a aula provavel e confere se o aviso chegou dentro do prazo.
```

### Meio

```text
A Taliya resolve sozinha quando o aluno foi identificado, a aula existe, o aviso chegou ate 2 horas antes da aula, a falta ainda nao foi registrada e a mensagem aprovada pode ser usada.

Ela chama a equipe quando o aviso chega fora do prazo, nao encontra aluno ou aula, a falta ja foi registrada, o aluno pede excecao/credito/cancelamento/reclama ou WhatsApp, cota ou permissao bloqueiam o envio.
```

### Fim

```text
Se o caso for comum, a falta fica registrada, a mensagem e enviada quando permitido e a auditoria e salva.
Depois disso, a Taliya cria uma tarefa de reposicao. A rotina Vagas, reposicoes e lista de espera decide vaga, credito, prioridade e remarcacao.
```

## Exemplo Por Modo: Falta Com Aviso

### Manual

Inicio:

```text
O fluxo comeca quando o aluno avisa que nao vai comparecer.
A Taliya identifica o aluno e a aula provavel, mas nao registra a falta sozinha.
```

Meio:

```text
A Taliya cria uma tarefa para a equipe conferir aluno, aula, prazo do aviso e contexto da conversa.
A equipe decide se registra a falta, responde o aluno ou trata como excecao.
```

Fim:

```text
O fluxo termina quando a equipe registra o resultado.
A Taliya salva a auditoria e, se houver reposicao, encaminha a tarefa para a rotina de reposicoes.
```

### Copiloto

Inicio:

```text
O fluxo comeca quando o aluno avisa que nao vai comparecer.
A Taliya identifica o aluno, encontra a aula provavel e mostra o prazo do aviso para a equipe.
```

Meio:

```text
A Taliya sugere registrar a falta avisada, prepara a resposta ao aluno e indica o proximo passo.
A equipe pode aceitar, editar ou descartar a sugestao antes de qualquer registro.
```

Fim:

```text
Se a equipe aceitar, a falta e registrada e a mensagem pode ser enviada.
Se editar ou descartar, a Taliya registra a decisao e mantem o caso como tarefa humana.
```

### Autonomo Com Aprovacao

Inicio:

```text
O fluxo comeca quando o aluno avisa que nao vai comparecer.
A Taliya identifica aluno, aula e prazo, e prepara o caso para revisao.
```

Meio:

```text
A Taliya monta o registro da falta, o texto da mensagem e o proximo passo de reposicao.
Antes de concluir, ela mostra o impacto e pede aprovacao para o responsavel definido.
```

Fim:

```text
Se aprovado, a falta e registrada, a mensagem pode ser enviada e a auditoria fica salva.
Se recusado ou vencido, vira tarefa para a equipe resolver manualmente.
```

### Autonomo Com Excecoes

Inicio:

```text
O fluxo comeca quando o aluno avisa que nao vai comparecer.
A Taliya identifica o aluno, encontra a aula provavel e confere se o aviso chegou dentro do prazo.
```

Meio:

```text
A Taliya resolve sozinha quando aluno e aula foram identificados, o aviso chegou ate 2 horas antes da aula, a falta ainda nao existe e a mensagem aprovada pode ser usada.
Ela chama a equipe quando o aviso chega fora do prazo, nao encontra aluno/aula, a falta ja existe, o aluno pede excecao/credito/cancelamento/reclama ou WhatsApp, cota ou permissao bloqueiam o envio.
```

Fim:

```text
No caso comum, a falta fica registrada, a mensagem e enviada quando permitido e a auditoria e salva.
Depois disso, a Taliya cria uma tarefa de reposicao. A rotina Vagas, reposicoes e lista de espera decide vaga, credito, prioridade e remarcacao.
```

### Autonomo

Este modo fica bloqueado para `Falta com aviso`.

Explicacao:

```text
Este fluxo nao conclui end-to-end porque reposicao, credito e excecoes podem depender de regra de outra rotina ou decisao humana.
Use Autonomo com excecoes para tratar o caso comum e chamar a equipe quando sair do trilho.
```

## Regra Visual

A UI pode mostrar Inicio, Meio e Fim como:

- tres mini cards horizontais;
- uma timeline compacta vertical;
- tres secoes curtas dentro do mesmo card.

Nao usar texto longo demais.

Cada parte deve ter no maximo duas frases na tela principal.

Detalhes extras podem ir para tooltip, expansao ou Agente de Configuracao.
