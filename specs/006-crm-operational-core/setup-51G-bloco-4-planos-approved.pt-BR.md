# Setup Inicial - 51G Bloco 4 Planos Aprovado

Status: aprovado v0.1.
Data: 2026-05-15.

Imagem aprovada:

`D:\Downloads\taliya-crm-chatgpt-images-named-20260511-082508\51G_round-4.1J_onboarding_bloco-4-planos-aprovado.png`

## Objetivo

Validar o Bloco 4 do Setup Inicial: `Planos`.

Este bloco serve para cadastrar os principais planos que o studio vende aos alunos, somente no nivel necessario para o CRM comecar a operar com seguranca.

Nao e uma configuracao de pagamento.

Atualizacao de escopo em 2026-05-15: pagamento basico entra no Setup Inicial, mas em um bloco separado logo depois de `Planos`. Esta imagem continua aprovada como Bloco 4 `Planos`.

## Decisao Principal

Plano define:

- tipo de plano;
- valor;
- saldo ou frequencia;
- recorrencia;
- validade;
- regra simples de reposicao.

Plano nao define horario fixo.

Plano tambem nao define como o studio recebe. Pagamento vem no bloco seguinte.

Horario fixo sera configurado depois, nos blocos `Turmas` e `Agenda`.

Um pacote de aulas pode ter horario fixo, mas isso nao muda a natureza do pacote. A diferenca principal e que o pacote tem saldo fechado.

## Regra De Consumo De Aula

Nao existe configuracao `quando a aula e consumida` neste bloco.

Regra do produto:

> A aula prevista consome saldo normalmente. Quando a regra permitir, o sistema gera uma reposicao para compensar a falta.

O usuario configura apenas se o plano permite reposicao, prazo para usar a reposicao e aviso minimo.

## Estrutura Aprovada Da Tela

A tela usa o shell global aprovado em `51A`, com:

- stepper lateral esquerdo;
- header do onboarding;
- rodape global de rascunho/pendencias;
- painel lateral do Agente de Configuracao no padrao `51B`.

Na area central, o bloco usa tres colunas:

1. `Planos criados`;
2. `Editar plano selecionado`;
3. `Como o Taliya vai entender este plano`.

## Coluna 1 - Planos Criados

A coluna esquerda deve ser uma lista compacta, sem accordion.

Cada card de plano mostra somente:

- nome do plano;
- tipo do plano;
- valor;
- quantidade ou frequencia;
- status curto de reposicao;
- acoes pequenas: `Editar`, `Duplicar`, `Remover`.

O plano selecionado usa borda azul e fundo levemente destacado.

Deve existir botao pequeno `+ Novo plano` no topo da coluna.

Nao mostrar detalhes completos dentro do card.

Nao repetir a explicacao interpretada nesta coluna.

## Coluna 2 - Editar Plano Selecionado

Titulo aprovado:

`Editar plano selecionado`

Com badge:

`Rascunho`

Microcopy aprovada:

`Voce pode ajustar este plano depois do go-live.`

Campos aprovados:

1. `Nome do plano`;
2. `Tipo do plano`;
3. `Valor`;
4. `Quantidade de aulas`;
5. `Recorrencia`;
6. `Validade`;
7. `Reposicao`.

### Tipos De Plano

Opcoes:

- `Mensalidade por frequencia semanal`;
- `Mensalidade por quantidade mensal`;
- `Pacote de aulas`;
- `Aula avulsa`;
- `Experimental/Avaliacao`;
- `Outro`.

Exemplo aprovado na imagem:

`Pacote de aulas`

### Quantidade De Aulas

Para `Pacote de aulas`, opcoes exibidas:

- `1 aula`;
- `5 aulas`;
- `8 aulas`;
- `10 aulas`;
- `12 aulas`;
- `20 aulas`;
- `Personalizado`.

Exemplo aprovado:

`8 aulas`

### Recorrencia

Para `Pacote de aulas`, opcoes exibidas:

- `Sem recorrencia`;
- `Renova automaticamente`;
- `Decidir depois`.

Exemplo aprovado:

`Sem recorrencia`

Nao usar `recorrencia semanal` ou `recorrencia mensal` como labels principais para pacote de aulas.

### Validade

Opcoes:

- `30 dias`;
- `60 dias`;
- `90 dias`;
- `Sem validade`;
- `Personalizado`;
- `Decidir depois`.

Exemplo aprovado:

`30 dias`

### Reposicao

Pergunta:

`Este plano permite reposicao?`

Opcoes:

- `Sim`;
- `Nao`;
- `Decidir depois`.

Se `Sim`, mostrar:

Prazo para usar reposicao:

- `7 dias`;
- `15 dias`;
- `30 dias`;
- `Ate o fim do ciclo`;
- `Personalizado`.

Aviso minimo para gerar reposicao:

- `Sem aviso minimo`;
- `2h antes`;
- `6h antes`;
- `12h antes`;
- `24h antes`;
- `Personalizado`.

Exemplo aprovado:

- reposicao: `Sim`;
- prazo: `7 dias`;
- aviso minimo: `12h antes`.

## Tooltips

Cada pergunta principal deve ter tooltip discreto:

- tipo do plano;
- quantidade de aulas;
- recorrencia;
- validade;
- reposicao.

A imagem aprovada mostra o tooltip do tipo de plano aberto:

`O tipo define como o aluno compra aulas. O horario fixo sera configurado depois, em Turmas/Agenda.`

Os demais tooltips podem ficar fechados.

## Coluna 3 - Como O Taliya Vai Entender Este Plano

Esta coluna e o unico lugar com a explicacao interpretada completa.

Texto aprovado para o exemplo:

`Este e um pacote de 8 aulas por R$ 420. O aluno tem 8 aulas no total, independentemente do tamanho do mes. Se esse aluno tiver horario fixo depois, cada aula prevista continua consumindo saldo do pacote. Reposicoes podem ser geradas quando o aluno avisa com 12h de antecedencia e ficam validas por 7 dias.`

Resumo aprovado:

- `Saldo: 8 aulas`;
- `Validade: 30 dias`;
- `Reposicao: Sim, com aviso de 12h`;
- `Horario fixo: Definido depois em Turmas/Agenda`.

## Painel Do Agente

O painel do agente deve orientar sem duplicar a configuracao.

Mensagens aprovadas:

- `Este bloco define como o Taliya entende mensalidades, pacotes e aulas dos alunos.`;
- `Plano define saldo, recorrencia, validade e reposicao.`;
- `Horario fixo sera configurado depois, em Turmas e Agenda.`;
- `Pacote de aulas tambem pode ter horario fixo; a diferenca e que o saldo e fechado.`

Chips aprovados:

- `Qual tipo escolher?`;
- `Pacote pode ter horario fixo?`;
- `Como funciona reposicao?`.

## Ajustes Finos Registrados

Antes de usar como prompt final ou implementar:

- trocar `Nao gera reposicao` vermelho por `Sem reposicao` neutro quando nao for erro;
- garantir `Studio Letícia` com acento no exemplo, quando o gerador permitir;
- manter tooltips sem cobrir chips importantes.

## Nao Fazer

Nao adicionar neste bloco:

- accordion detalhado de planos;
- drawer;
- modal;
- cobranca automatica sofisticada;
- inadimplencia;
- contrato;
- desconto;
- cupom;
- comissao;
- nota fiscal;
- conciliacao bancaria;
- gateway financeiro completo;
- configuracoes financeiras avancadas;
- configuracao profunda de agentes;
- cotas;
- logs;
- auditoria;
- control planes.

## Criterios De Aceite

- A lista de planos e escaneavel.
- O usuario consegue criar novo plano.
- O usuario consegue editar o plano selecionado.
- A explicacao interpretada aparece em um unico lugar.
- O bloco diferencia plano de horario fixo.
- A regra de consumo de aula nao vira configuracao.
- A tela continua simples o bastante para Setup Inicial.
