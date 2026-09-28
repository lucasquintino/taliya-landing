# Onboarding - Bem-vindo A Taliya Aprovado - PT-BR

> Status: imagem 78 aprovada. Este documento registra a primeira tela do Setup Inicial apos a assinatura confirmada.

## Imagem Aprovada

Arquivo:

`78_round-4.1Q_onboarding_bem-vindo-taliya-setup-guiado-aprovado.png`

Local:

`D:\Downloads\taliya-crm-chatgpt-images-named-20260511-082508\78_round-4.1Q_onboarding_bem-vindo-taliya-setup-guiado-aprovado.png`

## Papel Da Tela

A imagem 78 e a recepcao do setup guiado.

Ela aparece depois da 77, quando o usuario clicou em `Comecar setup guiado`. Ela nao e o bloco `Studio` e nao deve mostrar stepper, checklist ou configuracoes operacionais ainda.

Fluxo aprovado:

```text
77 Assinatura confirmada
-> 78 Bem-vindo a Taliya
-> 51D Studio / horarios gerais
-> demais blocos do Setup Inicial
```

## Objetivo

Receber o usuario com uma experiencia premium, confirmar o nome do studio e iniciar o setup guiado.

Em linguagem interna, essa etapa cria/identifica o espaco do studio. Na interface, nao usar termos tecnicos como workspace, tenant, provisionar ou ambiente.

## Conteudo Aprovado

| Elemento | Conteudo |
| --- | --- |
| Header | Logo Taliya, badge `Setup inicial`, Ajuda e conta. |
| Titulo | `Bem-vindo a Taliya` |
| Subtitulo | `Vamos preparar seu studio passo a passo, com ajuda do agente de configuracao.` |
| Orientacao | `Para comecar, informe o nome do seu studio.` |
| Input | Placeholder `Ex.: Studio Leticia`; sem label visivel acima. |
| CTA principal | `Comecar setup guiado` |
| Painel lateral | `Agente de configuracao`, status `Guiando setup`. |
| Mensagem do agente | Explica que primeiro vai identificar o studio e depois seguir por dados principais, equipe, canais, planos, alunos, turmas e agenda. |
| Perguntas rapidas | `O que vou configurar?`, `Posso pedir ajuda humana?`, `Quando o CRM sera liberado?` |
| Link lateral | `Agendar ajuda` |

## Regras Visuais

- Nao usar stepper nesta tela.
- Nao usar card dentro de card.
- Nao usar footer/barra inferior de setup.
- Nao usar chip de `Primeira entrada no setup`.
- Nao usar label `Nome do studio` acima do input.
- Nao usar microcopy `Nada sera publicado...` nesta tela.
- Manter area central ampla, limpa e premium.
- O input e o CTA devem ter largura alinhada.
- O agente lateral deve orientar sem parecer suporte generico.

## O Que Nao Entra Na 78

- dias de funcionamento;
- horario geral;
- WhatsApp;
- unidade;
- endereco;
- equipe;
- canais;
- planos;
- alunos;
- turmas;
- agenda;
- revisao;
- checklist do setup;
- status de pendencias.

## Impacto Na 51D

Como a 78 passa a coletar o nome do studio, a 51D nao deve repetir o campo principal de nome do studio.

A 51D comeca o bloco `Studio` ja com o nome no header/topo e deve focar em dados operacionais do studio, principalmente funcionamento e horarios gerais.

## Criterio De Aceite

A tela esta correta quando o usuario entende:

- que entrou na Taliya depois da assinatura confirmada;
- que o setup sera guiado;
- que precisa apenas informar o nome do studio para comecar;
- que o proximo passo e configurar o studio com ajuda do agente.
