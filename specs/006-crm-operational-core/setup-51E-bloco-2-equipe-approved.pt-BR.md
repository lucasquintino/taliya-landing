# Setup Inicial - 51E Bloco 2 Equipe Aprovado

> Status: aprovado v0.1. Imagem de referencia: `51E_round-4.1J_onboarding_bloco-2-equipe-aprovado.png`.

## Arquivo

Arquivo canonico:

`D:\Downloads\taliya-crm-chatgpt-images-named-20260511-082508\51E_round-4.1J_onboarding_bloco-2-equipe-aprovado.png`

Arquivo local observado:

`D:\Downloads\ChatGPT Image May 15, 2026, 09_18_47 AM.png`

## Objetivo Da Imagem

Validar o segundo bloco real de configuracao dentro de `/onboarding/setup`: **Equipe**.

Esta imagem representa a preparacao das pessoas que terao acesso ao Taliya quando o setup inicial for publicado. Ela nao representa configuracao avancada de permissoes, escala, salarios, comissoes, controle de ponto ou envio imediato de convites.

## Decisao Principal

O Bloco 2 prepara equipe em rascunho.

Convites **nao sao enviados neste bloco**. Eles ficam preparados e sao enviados automaticamente somente quando o setup inicial for publicado.

Motivo:

- evita convidar equipe antes do CRM estar pronto;
- evita acesso a workspace incompleto;
- mantem a revisao final como ponto unico de confirmacao;
- reduz complexidade do setup inicial.

## Estrutura Aprovada

### Shell

A imagem usa corretamente:

- 51A como shell global do onboarding;
- stepper lateral esquerdo com `Studio` concluido e `Equipe` em andamento;
- 51B como chat lateral do Agente de Configuracao;
- rodape global com ambiente, autosave e pendencias.

### Area Central

Conteudos aprovados:

- titulo `Equipe`;
- badge `Bloco 2 de 8`;
- subtitulo explicando que convites serao enviados quando o setup for publicado;
- card fixo do dono do studio;
- formulario compacto para adicionar pessoa;
- lista/tabela leve de equipe preparada;
- aviso inline sobre envio futuro dos convites;
- acoes da etapa.

### Dono Do Studio

O dono/admin principal aparece no topo como usuario confirmado.

Campos exibidos:

- avatar;
- nome;
- papel/responsabilidade;
- e-mail;
- WhatsApp;
- status `Confirmado`.

Recomendacao de nomenclatura para produto:

- preferir `Dono` em vez de `Dono/Admin`, quando o objetivo for identificar o responsavel principal do workspace.

### Adicionar Pessoa

Campos aprovados:

- `Nome`;
- `E-mail`;
- `WhatsApp`;
- `Papel`.

Papeis simples para setup:

- `Admin`;
- `Recepcao`;
- `Professor`;
- `Financeiro`.

Regra: se uma pessoa for adicionada, os campos principais devem estar completos para virar convite preparado.

### Equipe Preparada

Tabela/lista aprovada:

- nome;
- papel;
- e-mail;
- WhatsApp;
- status;
- acoes pequenas.

Status aprovados:

- `Convite preparado`;
- `Dados incompletos`.

Nao usar neste bloco:

- `Convite enviado`;
- `Reenviar convite`;
- `Aceito`;
- `Erro no convite`.

Esses estados pertencem ao pos-publicacao ou a Configuracoes > Equipe depois do go-live.

### Acoes Da Etapa

Acoes aprovadas:

- `Salvar rascunho`;
- `Configurar equipe depois`;
- `Continuar`.

`Continuar` e a acao primaria.

`Configurar equipe depois` e permitido porque um studio pequeno pode iniciar apenas com o dono.

## Papel Do Agente Nesta Tela

O agente deve explicar que a equipe esta sendo preparada, nao convidada imediatamente.

Mensagens aprovadas:

- `Este bloco prepara quem tera acesso ao Taliya quando o setup for publicado.`
- `Voce pode comecar so com o dono do studio. Se adicionar equipe agora, eu deixo os convites preparados para o final do setup.`
- `Nenhum convite sera enviado enquanto o setup estiver em rascunho.`

Chips aprovados, com ajuste de nomenclatura:

- `Preciso convidar equipe agora?`
- `Quando o convite e enviado?`
- `Posso mudar os papeis depois?`

Recomendacao: trocar o titulo `Duvidas frequentes` por `Perguntas sugeridas` nas proximas imagens/implementacao.

## Pendencias

Pendencias deste bloco aparecem no rodape global ou inline perto da linha afetada.

Exemplo aprovado:

- `Dados incompletos` em uma pessoa preparada;
- `Pendencias do setup (1)` no rodape global.

## O Que Foi Rejeitado

Nao usar no Bloco 2:

- botao `Enviar convite`;
- botao `Reenviar convite`;
- convite enviado antes da publicacao;
- permissao avancada;
- matriz de acesso;
- escala de professores;
- comissoes;
- salarios;
- controle de ponto;
- substituicoes;
- configuracao profunda de agentes;
- alunos, planos, turmas ou agenda.

## Criterio De Aceite

O Bloco 2 esta correto quando:

- mostra o dono como responsavel confirmado;
- permite preparar equipe em rascunho;
- deixa claro que convites so serao enviados na publicacao;
- permite pular equipe para depois;
- mostra pendencias sem bloquear indevidamente;
- mantem o agente como apoio lateral;
- segue o design system Taliya e o shell 51A.
