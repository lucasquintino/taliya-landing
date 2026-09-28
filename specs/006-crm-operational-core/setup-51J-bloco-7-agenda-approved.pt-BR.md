# Setup Inicial - 51J Bloco 7 Agenda Aprovado

Status: aprovado v0.1.
Data: 2026-05-15.

Nota de numeracao: apos a decisao de incluir `Pagamento` depois de `Planos`, esta tela continua aprovada como padrao visual e funcional de `Agenda`, mas passa a representar o Bloco 8 oficial do setup. Ver `setup-stepper-progress-9-blocks.pt-BR.md`.

Imagem aprovada:

`D:\Downloads\taliya-crm-chatgpt-images-named-20260511-082508\51J_round-4.1J_onboarding_bloco-7-agenda-aprovado.png`

## Objetivo

Validar o Bloco 7 do Setup Inicial: `Agenda`.

Este bloco serve para revisar a semana base gerada dentro do Taliya a partir das turmas preparadas.

A tela responde:

`Essa e a semana base que sera publicada?`

## Decisao Principal

O Bloco 7 `Agenda` nao permite importacao externa.

Nao mostrar neste bloco:

- conectar Google Agenda;
- importar arquivos;
- enviar foto/anotacao;
- colar agenda;
- fontes externas;
- upload;
- planilha;
- print;
- foto;
- fluxo de importacao.

Importacoes que revelam alunos, turmas, horarios ou vinculos devem acontecer antes:

- no Bloco 5 `Alunos`, quando a fonte ajuda a montar alunos ativos;
- no Bloco 6 `Turmas`, quando a fonte ajuda a montar turmas, horarios recorrentes e vinculos.

O Bloco 7 trabalha somente com dados ja preparados dentro do sistema.

## Escopo Do Setup Inicial

O bloco `Agenda` pode:

- mostrar semana base completa;
- mostrar como cada turma virou ocorrencias na agenda;
- destacar pendencias integradas nos itens e na grade;
- permitir voltar para `Turmas` quando a origem estiver errada;
- salvar rascunho;
- continuar para revisao.

Nao configurar aqui:

- reposicoes;
- encaixes;
- chamada/presenca;
- faltas;
- lista de espera;
- bloqueios avancados;
- regras finas de no-show;
- feriados complexos;
- automacoes;
- agentes operando agenda;
- envio automatico de mensagens;
- publicacao automatica.

## Estrutura Aprovada Da Tela

A tela usa o shell global aprovado em `51A`, com:

- stepper lateral esquerdo;
- header do onboarding;
- rodape global de rascunho/pendencias;
- painel lateral do Agente de Configuracao no padrao `51B`.

Na area central, a estrutura aprovada e:

1. cards compactos de resumo no topo;
2. area principal com duas colunas:
   - `Controle da semana`;
   - `Agenda semanal completa`;
3. acoes do bloco no rodape da area central.

## Cards De Resumo

### Card 1 - Agenda Gerada

Mostra:

- `24 aulas semanais`;
- `10 turmas usadas`.

Microcopy:

`Criada a partir das turmas preparadas.`

### Card 2 - Cobertura

Mostra:

- `6 dias com aulas`;
- `4 horarios principais`.

Microcopy:

`Dentro da janela de funcionamento.`

### Card 3 - Revisao

Mostra:

- `7 turmas prontas`;
- `3 precisam atencao`.

Microcopy:

`Pendencias aparecem na semana e no controle.`

## Area Principal - Controle Da Semana

A coluna esquerda nao e uma lista cadastral de turmas.

Ela mostra como cada turma virou ocorrencias na agenda.

Titulo:

`Controle da semana`

Subtexto:

`Veja como cada turma apareceu na agenda.`

Chips aprovados:

- `Todas`;
- `Revisar`;
- `Avisos`.

Itens aprovados:

1. `Ter/Qui 18h`
   - `2 aulas geradas · Ter e Qui`;
   - `5 alunos · Pronto`;
   - item selecionado.
2. `Seg/Qua 07h`
   - `2 aulas geradas · Seg e Qua`;
   - `4 alunos · Pronto`.
3. `Sexta 09h`
   - `1 aula gerada · Sex`;
   - `Falta capacidade · Revisar`.
4. `Sabado 08h`
   - `1 aula gerada · Sab`;
   - `Fora da janela · Aviso`.
5. `Ter/Qui 19h`
   - `2 aulas geradas · Ter e Qui`;
   - `Aluno pendente · Revisar`.

Quando um item estiver selecionado no controle, as ocorrencias correspondentes devem ficar destacadas na agenda semanal.

## Area Principal - Agenda Semanal Completa

A coluna direita e o componente principal da tela.

Titulo:

`Agenda semanal completa`

Badge:

`Previa antes da publicacao`

Grade semanal:

- colunas: `Seg`, `Ter`, `Qua`, `Qui`, `Sex`, `Sab`;
- linhas: `07h`, `08h`, `09h`, `12h`, `18h`, `19h`.

Blocos aprovados:

- `Seg/Qua 07h`
  - `4 alunos`
  - aparece em `Seg 07h` e `Qua 07h`;
- `Ter/Qui 18h`
  - `5 alunos`
  - aparece em `Ter 18h` e `Qui 18h`;
  - destacado por estar selecionado no controle;
- `Sexta 09h`
  - `Revisar capacidade`
  - marcador laranja;
- `Sabado 08h`
  - `Fora da janela`
  - marcador de aviso;
- `Ter/Qui 19h`
  - `Aluno pendente`
  - aparece em `Ter 19h` e `Qui 19h`;
  - marcador laranja.

Legenda aprovada:

- `Pronto`;
- `Selecionado`;
- `Revisar`;
- `Aviso`.

## Pendencias

Nao criar um card grande separado de `Conflitos encontrados`.

Pendencias aparecem integradas:

- no item correspondente do `Controle da semana`;
- no bloco correspondente da `Agenda semanal completa`;
- no rodape global como quantidade de pendencias do setup.

## Acoes Do Bloco

Acoes aprovadas:

- `Salvar rascunho`;
- `Voltar para turmas`;
- `Continuar`.

`Voltar para turmas` existe porque erro de origem deve ser corrigido no bloco anterior.

## Painel Do Agente

O painel do agente deve explicar a relacao entre controle e agenda.

Mensagens aprovadas:

- `Este bloco revisa a agenda inicial gerada pelo Taliya.`;
- `A esquerda esta o controle de como cada turma virou agenda.`;
- `A direita esta a semana completa que sera publicada.`;
- `Se algo estiver errado na origem, volte para Turmas.`;
- `Reposicoes, encaixes e ajustes avancados ficam para depois do go-live.`

Chips aprovados:

- `O que bloqueia publicacao?`;
- `Posso ajustar depois?`;
- `Por que voltar para turmas?`.

## Ajustes Finos Registrados

Na imagem aprovada, o item selecionado `Ter/Qui 18h` usa um icone azul que pode parecer alerta.

Na implementacao, usar icone neutro de selecao ou agenda, nao um simbolo de problema.

Se houver muitos horarios, a grade semanal pode ganhar scroll vertical na implementacao.

## Nao Fazer

Nao mostrar neste bloco:

- importacao;
- fontes externas;
- Google Agenda;
- planilha;
- upload;
- foto/anotacao;
- calendario mensal completo;
- agenda operacional cheia;
- chamada/presenca;
- reposicoes;
- encaixe automatico;
- lista de espera;
- bloqueios avancados;
- regras finas de no-show;
- feriados complexos;
- automacoes;
- agentes operando agenda;
- publicacao automatica;
- envio automatico de mensagens;
- card grande separado de conflitos;
- card grande de ajustes rapidos.

## Criterios De Aceite

- A agenda semanal e o componente visual principal.
- A coluna esquerda nao repete o cadastro de turmas do Bloco 6.
- A coluna esquerda mostra como cada turma virou agenda.
- Pendencias aparecem integradas, nao em um painel separado.
- O usuario entende que importacoes aconteceram antes.
- O usuario entende que erros de origem voltam para `Turmas`.
- O agente explica sem competir com a area central.
