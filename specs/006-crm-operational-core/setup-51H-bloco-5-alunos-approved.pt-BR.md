# Setup Inicial - 51H Bloco 5 Alunos Aprovado

Status: aprovado v0.1.
Data: 2026-05-15.

Nota de numeracao: apos a decisao de incluir `Pagamento` depois de `Planos`, esta tela continua aprovada como padrao visual e funcional de `Alunos`, mas passa a representar o Bloco 6 oficial do setup. Ver `setup-stepper-progress-9-blocks.pt-BR.md`.

Imagem aprovada:

`D:\Downloads\taliya-crm-chatgpt-images-named-20260511-082508\51H_round-4.1J_onboarding_bloco-5-alunos-aprovado.png`

## Objetivo

Validar o Bloco 5 do Setup Inicial: `Alunos`.

Este bloco serve para montar a base inicial de alunos ativos do studio a partir de uma ou varias fontes.

Nao e uma tela de CRM completo de alunos.

Nao e uma tela de lead, ex-aluno, inadimplencia, historico de aulas, ficha clinica completa ou anamnese completa.

## Decisao Principal

O bloco `Alunos` trabalha com uma fila de entradas.

O usuario pode misturar:

- planilhas;
- exportacoes;
- fotos de caderno;
- fichas fisicas;
- prints;
- listas coladas;
- cadastros manuais.

Cada fonte vira um lote de rascunho.

O sistema consolida tudo em uma tabela unica de `Alunos preparados`, marca pendencias e duplicidades, e o dono revisa antes de continuar.

## Escopo Do Setup Inicial

Neste bloco, todos os alunos entram como:

`Ativo`

Nao configurar aqui:

- horario fixo;
- turma;
- agenda;
- historico financeiro;
- historico de aulas;
- contrato;
- documentos;
- ficha clinica completa;
- anamnese completa;
- tags avancadas;
- segmentacao;
- funil de vendas.

Horarios e turmas serao vinculados nos proximos blocos.

## Estrutura Aprovada Da Tela

A tela usa o shell global aprovado em `51A`, com:

- stepper lateral esquerdo;
- header do onboarding;
- rodape global de rascunho/pendencias;
- painel lateral do Agente de Configuracao no padrao `51B`.

Na area central, a estrutura aprovada e:

1. linha superior com tres cards;
2. linha inferior com tabela de alunos ocupando a largura total;
3. acoes do bloco no rodape da area central.

## Linha Superior

### Card 1 - Adicionar Alunos

Mostra quatro modos de entrada:

- `Importar arquivos`
  - subtexto: `Planilhas ou exportacoes`;
- `Enviar foto/anotacao`
  - subtexto: `Caderno, ficha ou print`;
- `Colar lista`
  - subtexto: `Nomes e telefones`;
- `Adicionar manualmente`
  - subtexto: `Um aluno por vez`.

Essas opcoes nao sao etapas separadas.

Sao formas diferentes de adicionar dados a mesma fila de rascunho.

### Card 2 - Fontes Adicionadas

Mostra os lotes ja adicionados.

Exemplos aprovados:

- `alunos_maio.xlsx`
  - `42 alunos encontrados · 3 pendencias`
  - status: `Processado`;
- `foto_caderno_01.png`
  - `8 alunos encontrados · aguardando revisao`
  - status: `Revisar`;
- `lista colada`
  - `5 alunos encontrados`
  - status: `Processado`;
- `manual`
  - `2 alunos adicionados`
  - status: `Rascunho`.

Microcopy aprovada:

`Voce pode adicionar mais fontes antes de continuar.`

### Card 3 - Resumo Da Base

Mostra:

- `57 alunos preparados`;
- `49 prontos`;
- `6 precisam revisao`;
- `2 possiveis duplicidades`.

Microcopy aprovada:

`Obrigatorio: nome + WhatsApp/telefone.`

## Linha Inferior - Alunos Preparados

A tabela `Alunos preparados` ocupa a largura total da linha inferior da area central.

Badge aprovado:

`Todos entram como Ativo`

Colunas:

- `Aluno`;
- `WhatsApp`;
- `Plano`;
- `Origem`;
- `Status`;
- `Acoes`.

Exemplos aprovados:

1. `Ana Martins`
   - WhatsApp: `(11) 98888-1111`;
   - plano: `Pacote 8 aulas`;
   - origem: `planilha`;
   - status: `Pronto`.
2. `Carla Souza`
   - WhatsApp: `(11) 97777-2222`;
   - plano: `Pilates 2x por semana`;
   - origem: `manual`;
   - status: `Pronto`.
3. `Roberto Lima`
   - WhatsApp: `Falta telefone`;
   - plano: `Plano nao informado`;
   - origem: `foto`;
   - status: `Revisar`.
4. `Mariana Alves`
   - WhatsApp: `Possivel duplicidade`;
   - plano: `Pacote 8 aulas`;
   - origem: `lista`;
   - status: `Revisar`.
5. `Beatriz Nunes`
   - WhatsApp: `(11) 96666-3333`;
   - plano: `Sem plano ainda`;
   - origem: `planilha`;
   - status: `Pode seguir`.

Microcopy aprovada no rodape da tabela:

`Para publicar, cada aluno precisa ter nome e WhatsApp/telefone.`

## Dados Obrigatorios E Opcionais

Nao mostrar uma lista fixa de dados esperados na tela principal.

Esses dados aparecem quando o usuario abre `Adicionar aluno`, `Editar aluno` ou `Ver detalhes`.

Obrigatorios para publicar aluno:

- nome do aluno;
- WhatsApp ou telefone.

Opcionais reconhecidos:

- e-mail;
- plano;
- data de nascimento;
- observacao curta;
- responsavel, se menor;
- professor preferencial;
- restricoes/atencoes simples;
- origem do dado.

## Status

Status aprovados:

- `Pronto`: verde;
- `Pode seguir`: azul ou neutro;
- `Revisar`: amarelo/laranja;
- `Processado`: verde;
- `Rascunho`: neutro.

Evitar vermelho, salvo erro real.

## Acoes Do Bloco

Acoes aprovadas:

- `Salvar rascunho`;
- `Configurar alunos depois`;
- `Continuar`.

O botao `Continuar` deve seguir o padrao de acao principal do setup.

## Painel Do Agente

O painel do agente deve orientar sem capturar o formulario principal.

Mensagens aprovadas:

- `Este bloco cria a base inicial de alunos ativos.`;
- `Voce pode misturar planilhas, fotos de caderno, listas coladas e cadastros manuais.`;
- `Eu transformo tudo em rascunho e marco o que precisa de revisao antes de publicar.`;
- `Horarios e turmas serao vinculados nos proximos blocos.`

Chips aprovados:

- `O que e obrigatorio?`;
- `Posso importar foto de caderno?`;
- `E se tiver duplicidade?`.

## Nao Fazer

Nao mostrar neste bloco:

- leads;
- ex-alunos;
- inadimplentes;
- cancelados;
- ficha clinica completa;
- anamnese completa;
- historico financeiro;
- historico de aulas;
- contrato;
- documentos;
- tags avancadas;
- horario fixo;
- turma;
- agenda;
- publicacao automatica.

## Criterios De Aceite

- O usuario entende que pode misturar varias fontes.
- A tela mostra que cada fonte vira rascunho.
- A tabela consolidada ocupa o foco principal.
- Pendencias aparecem perto dos alunos afetados.
- Campos obrigatorios/opcionais nao poluem a tela principal.
- O bloco deixa claro que todos entram como alunos ativos.
- O agente explica sem competir com a area central.
