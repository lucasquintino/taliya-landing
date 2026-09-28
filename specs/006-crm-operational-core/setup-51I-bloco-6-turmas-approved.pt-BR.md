# Setup Inicial - 51I Bloco 6 Turmas Aprovado

Status: aprovado v0.1.
Data: 2026-05-15.

Nota de numeracao: apos a decisao de incluir `Pagamento` depois de `Planos`, esta tela continua aprovada como padrao visual e funcional de `Turmas`, mas passa a representar o Bloco 7 oficial do setup. Ver `setup-stepper-progress-9-blocks.pt-BR.md`.

Imagem aprovada:

`D:\Downloads\taliya-crm-chatgpt-images-named-20260511-082508\51I_round-4.1J_onboarding_bloco-6-turmas-aprovado.png`

## Objetivo

Validar o Bloco 6 do Setup Inicial: `Turmas`.

Este bloco serve para criar ou importar estruturas recorrentes de turma, antes da montagem da agenda final.

## Decisao Principal

Turma nao e agenda final.

Turma e uma estrutura recorrente ou horario fixo recorrente usado para organizar alunos.

Exemplos:

- `Ter/Qui 18h`;
- `Seg/Qua 07h`;
- `Sexta 09h`;
- `Pilates manha - Ana`.

A agenda sera montada no proximo bloco.

## Escopo Do Setup Inicial

O bloco `Turmas` pode configurar:

- dias recorrentes;
- horario de inicio;
- horario de fim;
- capacidade;
- professor opcional;
- alunos vinculados opcionalmente;
- origem do dado;
- pendencias simples.

Nao configurar aqui:

- calendario final;
- aula avulsa;
- reposicao;
- chamada/presenca;
- faltas;
- encaixes;
- lista de espera avancada;
- bloqueios;
- feriados;
- automacoes;
- agentes operando agenda;
- publicacao automatica.

## Estrutura Aprovada Da Tela

A tela usa o shell global aprovado em `51A`, com:

- stepper lateral esquerdo;
- header do onboarding;
- rodape global de rascunho/pendencias;
- painel lateral do Agente de Configuracao no padrao `51B`.

Na area central, a estrutura aprovada e:

1. linha superior com tres cards;
2. linha inferior com tabela de turmas ocupando a largura total;
3. acoes do bloco no rodape da area central.

## Linha Superior

### Card 1 - Adicionar Turmas

Mostra quatro modos de entrada:

- `Importar arquivos`
  - subtexto: `Planilhas ou exportacoes`;
- `Enviar foto/anotacao`
  - subtexto: `Caderno, grade ou print`;
- `Colar lista`
  - subtexto: `Horarios e alunos`;
- `Criar manualmente`
  - subtexto: `Uma turma por vez`.

Tambem mostra uma opcao secundaria:

- `Nao tenho turmas prontas`
  - subtexto esperado para prompts futuros: `Use uma grade, print ou lista aqui para preparar turmas`.

Essa opcao e importante porque alguns studios nao pensam em turmas; eles so possuem agenda, grade ou prints de horarios.

Regra atualizada apos aprovacao do Bloco 7: esses dados devem ser tratados no proprio Bloco 6 como fonte para criar turmas. O Bloco 7 nao importa agenda nem cria turmas novas.

### Card 2 - Fontes Adicionadas

Mostra os lotes ja adicionados.

Exemplos aprovados:

- `grade_turmas.xlsx`
  - `8 turmas encontradas · 2 pendencias`
  - status: `Processado`;
- `foto_grade_horarios.png`
  - `3 turmas encontradas`
  - status: `Revisar`;
- `lista colada`
  - `3 turmas encontradas`
  - status: `Processado`.

Microcopy aprovada:

`Voce pode adicionar mais fontes antes de continuar.`

### Card 3 - Resumo Das Turmas

Mostra:

- `10 turmas preparadas`;
- `8 prontas`;
- `2 precisam revisao`;
- `34 alunos vinculados`.

Microcopy aprovada:

`A agenda sera montada no proximo bloco.`

## Linha Inferior - Turmas Preparadas

A tabela `Turmas preparadas` ocupa a largura total da linha inferior da area central.

Badge aprovado:

`Agenda sera montada depois`

Colunas:

- `Turma`;
- `Dias`;
- `Horario`;
- `Capacidade`;
- `Professor`;
- `Alunos`;
- `Status`;
- `Acoes`.

Exemplos aprovados:

1. `Ter/Qui 18h`
   - dias: `Ter, Qui`;
   - horario: `18:00-19:00`;
   - capacidade: `6 vagas`;
   - professor: `Ana Martins`;
   - alunos: `5 alunos`;
   - status: `Pronto`.
2. `Seg/Qua 07h`
   - dias: `Seg, Qua`;
   - horario: `07:00-08:00`;
   - capacidade: `6 vagas`;
   - professor: `Sem professor`;
   - alunos: `4 alunos`;
   - status: `Pode seguir`.
3. `Sexta 09h`
   - dias: `Sex`;
   - horario sugerido para implementacao: `09:00-10:00`;
   - capacidade: `Falta capacidade`;
   - professor: `Carla Souza`;
   - alunos: `2 alunos`;
   - status: `Revisar`.
4. `Ter/Qui 19h`
   - dias: `Ter, Qui`;
   - horario: `19:00-20:00`;
   - capacidade: `6 vagas`;
   - professor: `Ana Martins`;
   - alunos: `Aluno nao encontrado`;
   - status: `Revisar`.
5. `Sabado 08h`
   - dias: `Sab`;
   - horario: `08:00-09:00`;
   - capacidade: `4 vagas`;
   - professor: `Sem professor`;
   - alunos: `0 alunos`;
   - status: `Pode seguir`.

Microcopy aprovada no rodape da tabela:

`Para publicar uma turma, informe dias, horario e capacidade.`

## Dados Obrigatorios E Opcionais

Obrigatorios para publicar turma:

- dias da semana;
- horario de inicio;
- horario de fim;
- capacidade.

Opcionais:

- nome personalizado;
- professor;
- alunos vinculados;
- observacao curta;
- origem do dado.

O nome da turma pode ser gerado automaticamente pelo sistema, por exemplo `Ter/Qui 18h`.

## Vinculo Com Alunos

O bloco pode vincular alunos ja preparados no Bloco 5.

Se o dado importado citar um aluno que ainda nao existe na base, o sistema marca pendencia.

Exemplo:

`Aluno nao encontrado`

O usuario pode revisar depois, vincular a um aluno existente ou criar rascunho de aluno quando a implementacao permitir.

## Status

Status aprovados:

- `Pronto`: verde;
- `Pode seguir`: azul ou neutro;
- `Revisar`: amarelo/laranja;
- `Processado`: verde.

Evitar vermelho, salvo erro real.

## Acoes Do Bloco

Acoes aprovadas:

- `Salvar rascunho`;
- `Configurar turmas depois`;
- `Continuar`.

O botao `Continuar` deve seguir o padrao de acao principal do setup.

## Painel Do Agente

O painel do agente deve explicar a diferenca entre turma e agenda.

Mensagens aprovadas:

- `Este bloco organiza os horarios fixos recorrentes do studio.`;
- `Turma ainda nao e agenda. A agenda sera montada no proximo bloco.`;
- `Voce pode importar planilhas, fotos da grade, listas coladas ou criar turmas manualmente.`;
- `Se algum aluno nao for encontrado, eu marco como pendencia para voce revisar.`

Chips aprovados:

- `Turma e diferente de agenda?`;
- `Preciso vincular alunos agora?`;
- `E se eu so tiver print da grade?`.

## Ajuste Fino Registrado

Na imagem aprovada, a linha `Sexta 09h` aparece com horario `09:30-10:00`.

Para implementacao e prompts futuros, preferir `09:00-10:00` para manter consistencia entre nome da turma e horario.

## Nao Fazer

Nao mostrar neste bloco:

- agenda final;
- calendario semanal completo;
- calendario mensal completo;
- reposicoes;
- chamada;
- presenca;
- faltas;
- encaixes;
- lista de espera avancada;
- bloqueios;
- feriados;
- automacoes;
- agentes executando agenda;
- publicacao automatica.

## Criterios De Aceite

- O usuario entende que turma e estrutura recorrente.
- O usuario entende que agenda vem no proximo bloco.
- A tela permite misturar varias fontes.
- A tabela mostra dias, horario, capacidade, professor e alunos.
- Pendencias aparecem perto das turmas afetadas.
- A opcao `Nao tenho turmas prontas` existe e nao bloqueia o setup.
- O agente explica sem competir com a area central.
