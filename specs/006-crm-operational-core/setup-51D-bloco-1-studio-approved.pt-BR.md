# Setup Inicial - 51D Bloco 1 Studio Aprovado

> Status: aprovado v0.1. Imagem de referencia: `51D_round-4.1J_onboarding_bloco-1-studio-aprovado.png`.

## Arquivo

Arquivo canonico:

`D:\Downloads\taliya-crm-chatgpt-images-named-20260511-082508\51D_round-4.1J_onboarding_bloco-1-studio-aprovado.png`

Arquivo local observado:

`D:\Downloads\ChatGPT Image May 15, 2026, 08_15_39 AM.png`

## Objetivo Da Imagem

Validar o primeiro bloco real de configuracao dentro de `/onboarding/setup`: **Studio**.

Esta imagem representa a configuracao inicial da janela de funcionamento do studio. Ela nao representa agenda final, turmas, alunos, planos, unidades, salas, feriados ou configuracao profunda de agentes.

## Decisao Principal

O Bloco 1 define somente a base operacional minima:

- nome do studio;
- dias de funcionamento;
- horario geral de abertura e fechamento;
- pausa do dia, quando existir;
- janela semanal de funcionamento como previa visual;
- acao leve para ajustar horarios por dia.

Sem essa base, os blocos seguintes de turmas e agenda nao conseguem validar horarios com seguranca.

## Estrutura Aprovada

### Shell

A imagem usa corretamente:

- 51A como shell global do onboarding;
- stepper lateral esquerdo com os 8 blocos do setup;
- 51B como chat lateral do Agente de Configuracao;
- rodape global com ambiente, autosave e status do bloco.

### Stepper Lateral

Etapas aprovadas para este fluxo de `/onboarding/setup`:

- `Studio`;
- `Equipe`;
- `Canais`;
- `Planos`;
- `Alunos`;
- `Turmas`;
- `Agenda`;
- `Revisao`.

Regra: este stepper e uma sequencia obrigatoria de setup, nao uma sidebar operacional do CRM.

### Area Central

Conteudos aprovados:

- titulo `Studio`;
- badge `Bloco 1 de 8`;
- subtitulo explicando que a configuracao ajuda a montar a grade inicial com seguranca;
- campo `Nome do studio`;
- bloco `Dias de funcionamento`;
- bloco `Horario geral`;
- controle de pausa;
- janela semanal visual;
- acoes `Salvar rascunho` e `Continuar`.

### Janela Semanal De Funcionamento

A imagem aprovou a previa como grade visual, nao como lista.

Nome recomendado para produto/documentacao:

`Janela semanal de funcionamento`

Texto recomendado:

`Essa janela mostra quando o studio pode receber aulas. As turmas e horarios especificos serao configurados nos proximos blocos.`

Regras:

- mostrar colunas por dia selecionado;
- mostrar faixas abertas;
- mostrar pausa como intervalo bloqueado;
- dias fechados nao precisam ocupar destaque;
- nao mostrar alunos, turmas, aulas ou reservas;
- manter `Ajustar horarios por dia` dentro do card da janela semanal.

### Ajustar Horarios Por Dia

`Ajustar horarios por dia` e uma acao secundaria.

Comportamento recomendado:

- abrir drawer ou modal simples;
- nao expandir tabela grande dentro da tela principal;
- permitir ajustar aberto/fechado, abre, fecha e pausa por dia;
- manter o fluxo principal simples.

## Papel Do Agente Nesta Tela

O agente deve explicar que este bloco define a janela em que o studio pode receber aulas.

Mensagens aprovadas:

- `Este bloco define a janela em que o studio pode ter aulas.`
- `Vamos comecar pela base do studio. Esses horarios ainda nao criam aulas; eles so ajudam o Taliya a montar turmas e agenda com seguranca.`
- `Se alguma turma cair fora desses horarios depois, eu vou te avisar antes de publicar.`

Chips aprovados:

- `O que e obrigatorio?`
- `Posso mudar depois?`
- `Isso ja cria agenda?`

## O Que Foi Rejeitado

Nao usar no Bloco 1:

- agenda final;
- turmas;
- alunos;
- planos;
- importacao;
- multiplas unidades;
- salas;
- feriados;
- permissoes;
- configuracao de agentes;
- modos manual/copiloto/autonomo;
- cotas;
- logs;
- publicacao de fluxos.

## Criterio De Aceite

O Bloco 1 esta correto quando:

- configura apenas a base do studio;
- mostra a janela semanal de funcionamento de forma visual;
- nao parece agenda operacional;
- deixa claro que turmas e horarios especificos vem depois;
- mantem o agente como apoio lateral;
- permite salvar rascunho e continuar;
- segue o design system Taliya e o shell 51A.
