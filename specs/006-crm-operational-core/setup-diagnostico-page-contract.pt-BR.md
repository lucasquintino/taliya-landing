# Setup Inicial - Contrato Da Pagina Diagnostico

Status: aprovado v0.1.
Data: 2026-05-14.

## Rota

`/onboarding/diagnostico`

## Objetivo

Fazer um diagnostico rapido do studio para preparar bons defaults e reduzir atrito nas proximas etapas do Setup Inicial.

Esta pagina nao configura o CRM profundamente, nao importa dados, nao cria planos e nao publica nada.

## Comportamento Da Pagina

O diagnostico deve aparecer como uma sequencia guiada, com uma pergunta por vez.

Fluxo:

1. mostra a pergunta atual;
2. mostra as opcoes em cards;
3. usuario escolhe uma opcao;
4. botao `Continuar` fica ativo;
5. ao continuar, avanca para a proxima pergunta;
6. ao final, mostra resumo das respostas;
7. usuario clica em `Continuar para o setup`.

## Estrutura Visual

Area central:

- titulo `Diagnostico rapido`;
- texto curto: `Responda 5 perguntas para preparar o setup inicial. Nada sera publicado agora.`;
- progresso `Pergunta X de 5`;
- pergunta em destaque;
- opcoes em cards;
- botao principal `Continuar`;
- botao secundario/discreto `Voltar`.

Painel lateral do agente:

- explica por que a pergunta importa;
- responde duvidas sobre a pergunta atual;
- reforca que nada sera publicado;
- nao faz a pergunta principal dentro do chat;
- nao altera a ordem das perguntas.

## Perguntas E Opcoes

### 1. Quantos alunos ativos o studio tem hoje?

Tipo:

- selecao unica.

Opcoes:

- `Ate 20 alunos`;
- `21 a 50 alunos`;
- `51 a 100 alunos`;
- `101 a 200 alunos`;
- `Mais de 200 alunos`;
- `Nao sei exatamente`.

Uso da resposta:

- ajustar volume esperado de importacao;
- prever revisao de conflitos;
- sugerir ajuda humana Taliya quando o volume for alto;
- preparar densidade de listas/tabelas.

### 2. Onde estao agenda, turmas ou horarios hoje?

Tipo:

- selecao unica.

Opcoes:

- `Google Agenda`;
- `Planilha`;
- `Sistema antigo`;
- `Caderno ou papel`;
- `PDF, print ou foto`;
- `Ainda nao esta organizado`;
- `Outro`.

Se escolher `Outro`, mostrar campo curto:

- `Onde esta hoje?`

Uso da resposta:

- preparar a etapa de importacao de agenda/turmas;
- sugerir fonte padrao quando a tela de importacao aparecer;
- prever se havera leitura de foto/PDF/planilha.

### 3. Onde estao alunos, planos e contatos hoje?

Tipo:

- selecao unica.

Opcoes:

- `Planilha`;
- `Sistema antigo`;
- `Fichas ou caderno`;
- `PDF, print ou foto`;
- `Contatos do celular/WhatsApp`;
- `Ainda nao esta organizado`;
- `Outro`.

Se escolher `Outro`, mostrar campo curto:

- `Onde estao hoje?`

Uso da resposta:

- preparar importacao de alunos, contatos e planos;
- prever duplicidades;
- prever telefone compartilhado/responsavel;
- preparar revisao de dados extraidos.

### 4. Quais tipos de planos o studio oferece pro aluno?

Tipo:

- multipla escolha.

Opcoes:

- `Mensalidade com aulas por semana`;
- `Mensalidade com quantidade de aulas`;
- `Pacote de aulas`;
- `Aula avulsa`;
- `Experimental`;
- `Plano familiar ou compartilhado`;
- `Planos diferentes por aluno`;
- `Ainda nao sei organizar isso`;
- `Outro`.

Se escolher `Outro`, mostrar campo curto:

- `Qual tipo de plano?`

Uso da resposta:

- preparar a pagina de Consumo de aulas;
- sugerir modelos de plano iniciais;
- nao criar planos ainda;
- nao configurar consumo ainda.

### 5. Como o studio lida com reposicoes?

Tipo:

- selecao unica.

Opcoes:

- `Permite reposicao com prazo`;
- `Permite reposicao sem prazo definido`;
- `So permite em alguns planos`;
- `Decide caso a caso`;
- `Nao permite reposicao`;
- `Ainda nao sei definir`.

Uso da resposta:

- preparar defaults de reposicao;
- decidir se reposicao aparece com mais destaque em Consumo de aulas;
- antecipar impacto em agenda, saldo de aulas e planos;
- nao configurar regra final.

## Resumo Final

Depois da quinta pergunta, a pagina mostra um resumo:

- alunos ativos;
- fonte atual de agenda/turmas/horarios;
- fonte atual de alunos/planos/contatos;
- tipos de planos oferecidos;
- forma atual de lidar com reposicoes.

Exemplo:

`Studio com 51 a 100 alunos, agenda em Google Agenda, alunos e planos em planilha, planos por mensalidade e pacote, reposicoes permitidas com prazo.`

CTA principal:

- `Continuar para o setup`.

Acao secundaria:

- `Editar respostas`.

## O Que Nao Entra Nesta Pagina

Nao perguntar:

- se usa WhatsApp;
- se quer importar agora;
- se trabalha com horario fixo;
- se o plano tem agentes;
- quantas pessoas vao usar o Taliya;
- quais areas quer configurar primeiro;
- permissoes;
- templates;
- automacoes;
- criacao de planos;
- upload/importacao.

## Criterio De Aceite

A pagina esta correta quando:

- tem exatamente 5 perguntas;
- mostra uma pergunta por vez;
- `Continuar` so ativa depois da resposta;
- o diagnostico nao configura nada definitivo;
- o agente lateral explica sem duplicar o formulario;
- o resumo final prepara o usuario para o setup sem parecer publicacao.
