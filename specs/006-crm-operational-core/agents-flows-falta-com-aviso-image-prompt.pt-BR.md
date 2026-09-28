# Taliya CRM - Prompt Da Imagem Do Fluxo Falta Com Aviso

Status: imagem aprovada v0.2.
Data: 2026-05-22.

## Tela

Rota:

```text
/app/agentes/agenda/rotinas/presenca-e-faltas/fluxos/falta-com-aviso
```

Objetivo da imagem:

Mostrar a pagina `Ver e ajustar fluxo` para o fluxo `Falta com aviso`, com modo `Autonomo com excecoes` selecionado.

Imagem aprovada:

```text
D:/Downloads/taliya-crm-chatgpt-images-named-20260511-082508/56_round-4.1L_agentes_04_fluxo-falta-com-aviso-v2-aprovado.png
```

Observacao:

- A imagem `55_round-4.1L_agentes_04_fluxo-falta-com-aviso-aprovado.png` fica preservada como historico, mas foi substituida pela v2.
- A v2 e a referencia visual atual para a pagina de fluxo.

## Ajustes Anotados Para Implementacao

A imagem v2 esta aprovada como direcao visual. Na implementacao, aplicar estes pequenos ajustes de texto/estado:

- Trocar `Salvar ajuste` por `Salvar ajustes`.
- Trocar `Mensagem usa template aprovado` por `Mensagem aprovada`.
- Se houver espaco no card bloqueado de `Autonomo`, mostrar chip discreto `Bloqueado` junto do cadeado.
- Manter o preview da mensagem legivel; se necessario, aumentar a altura do bloco de ajustes.

## Anexos Necessarios

Usar somente estes anexos:

1. `D:/Downloads/taliya-crm-chatgpt-images-named-20260511-082508/16_round-4.1S_app-shell_01_base-web.png`
2. `D:/Downloads/taliya-crm-chatgpt-images-named-20260511-082508/51B_round-4.1J_onboarding_agente-configuracao-chat-aprovado.png`
3. `D:/Downloads/taliya-crm-chatgpt-images-named-20260511-082508/54_round-4.1L_agentes_03_rotina-presenca-faltas-aprovado.png`

Nao usar imagens antigas da pagina de fluxo substituida como referencia principal.

## Conteudo Exato Da Tela

### Header

- Breadcrumb: `Agentes / Agenda / Presenca e faltas / Falta com aviso`
- Titulo: `Falta com aviso`
- Subtitulo: `Quando o aluno avisa que nao vai comparecer.`
- Chips ao lado do titulo:
  - `Autonomo com excecoes`
  - `Pronto`
  - `7 requisitos OK`

O chip `7 requisitos OK` e o preflight compacto. Nao criar card grande de requisitos.

### Bloco 1: Como este fluxo deve trabalhar?

Bloco principal no topo do conteudo, antes dos detalhes.

Texto curto:

```text
Este fluxo herdou o perfil Mais autonomo da rotina, mas voce pode mudar so este caso.
```

Seletor com 5 opcoes compactas, sem texto longo dentro dos cards:

- Manual
- Copiloto
- Autonomo com aprovacao
- Autonomo com excecoes selecionado
- Autonomo bloqueado

O modo `Autonomo` deve aparecer desabilitado com cadeado pequeno, porque este fluxo nao conclui end-to-end sem excecao.

### Bloco 2: Como funciona neste modo

Titulo:

```text
Como funciona neste modo
```

Este bloco deve explicar claramente o fluxo em inicio, meio e fim.

Usar tres mini secoes ou uma timeline compacta:

Inicio:

```text
O fluxo comeca quando o aluno avisa que nao vai comparecer.
A Taliya identifica o aluno, encontra a aula provavel e confere se o aviso chegou dentro do prazo.
```

Meio:

```text
A Taliya resolve sozinha quando aluno e aula foram identificados, o aviso chegou ate 2 horas antes da aula, a falta ainda nao existe e a mensagem aprovada pode ser usada.
```

Mostrar como lista curta abaixo:

- aluno foi identificado;
- aula existe na agenda;
- aviso chegou ate 2 horas antes da aula;
- falta ainda nao foi registrada;
- mensagem usa template aprovado.

Ainda no Meio, mostrar:

```text
Ela chama a equipe quando o aviso chega fora do prazo, nao encontra aluno/aula, a falta ja existe, o aluno pede excecao ou WhatsApp, cota ou permissao bloqueiam o envio.
```

- aviso chega fora do prazo;
- nao encontra aluno ou aula;
- falta ja foi registrada;
- aluno pede excecao, credito, cancelamento ou reclama;
- WhatsApp, cota ou permissao bloqueiam o envio.

Fim:

```text
A falta fica registrada na aula e a mensagem permitida e enviada.
Se configurado, abre tarefa de reposicao.
Se prazo, aluno, aula, credito ou envio nao fecharem, a equipe decide.
```

Tag discreta:

```text
Pode abrir tarefa em Reposicoes
```

Nao usar frases vagas como `se estiver dentro da regra`.

### Bloco 3: Ajustes deste fluxo

Este bloco deve ter mais destaque que requisitos.

Ele deve ocupar a faixa horizontal principal inteira, com aparencia de formulario operacional.

Campos:

1. `Prazo para aviso`
   - valor: `Ate 2 horas antes da aula`
   - controle: seletor/dropdown
   - ajuda curta: `Fora desse prazo, chama a equipe.`

2. `Proximo passo apos falta`
   - valor: `Criar tarefa de reposicao`
   - controle: dropdown
   - ajuda curta: `A reposicao segue pelas proprias regras.`

3. `Responsaveis por excecao`
   - valor: chips `Recepcao`, `Coordenadora`, `Dono/admin`
   - controle: multi-select
   - ajuda curta: `Quem recebe o caso quando a Taliya nao pode seguir.`

4. `Tom/template da mensagem`
   - valor: `Acolhedor`
   - controle: seletor
   - mostrar preview curto:

```text
Oi, {{nome}}. Vi aqui que voce nao vai conseguir vir a aula de {{horario}}. Vou registrar sua falta e deixar a reposicao encaminhada para a equipe.
```

### Acoes

Barra inferior do conteudo principal:

- botao primario preto: `Testar este fluxo`
- botao secundario: `Salvar ajustes`
- botao secundario: `Voltar para rotina`

Nao usar `Ativar rotina`.

### Painel Direito

Mostrar o `Agente de Configuracao`, igual ao setup inicial.

Titulo:

```text
Agente de Configuracao
```

Subtitulo:

```text
Ajudando neste fluxo
```

Card explicativo:

```text
Este fluxo esta em Autonomo com excecoes. A Taliya trata a falta avisada quando aluno, aula, prazo e mensagem estao claros. Se algum dado faltar ou o envio falhar, chama a equipe definida.
```

Sugestoes/botoes:

- `O que muda no Copiloto?`
- `Quando a equipe sera chamada?`
- `Por que Autonomo esta bloqueado?`
- `Testar aluno fora do prazo`

Input no rodape:

```text
Pergunte sobre este fluxo...
```

## Prompt Para ChatGPT Imagem

```text
Create a high-fidelity desktop web app mockup for Taliya CRM.

Use the attached shell base as the visual system: light background, white cards, subtle borders, compact operational SaaS density, left vertical icon sidebar, top navigation, black primary buttons, blue selected states, green success chips, orange attention chips, minimal shadows, rounded panels, no marketing hero, no decorative gradients.

Use the attached Agente de Configuracao reference for the right assistant panel.
Use the attached Presenca e faltas routine page as continuity reference for spacing, typography, card style and selected blue border behavior.

Screen URL: https://app.taliya.com/app/agentes/agenda/rotinas/presenca-e-faltas/fluxos/falta-com-aviso

Build the full page for:
Breadcrumb: Agentes / Agenda / Presenca e faltas / Falta com aviso
Title: Falta com aviso
Subtitle: Quando o aluno avisa que nao vai comparecer.
Header chips next to title: Autonomo com excecoes, Pronto, 7 requisitos OK.

Main content, left area:

1. Top block: "Como este fluxo deve trabalhar?"
Helper text: "Este fluxo herdou o perfil Mais autonomo da rotina, mas voce pode mudar so este caso."
Show five compact mode cards with icons and labels only:
Manual, Copiloto, Autonomo com aprovacao, Autonomo com excecoes selected, Autonomo locked.
Do not put explanatory paragraphs inside the mode cards.

2. Dynamic explanation block: "Como funciona neste modo"
Show the flow as a compact start-middle-end narrative, not just technical lists.

Use three sections:

Inicio:
"O fluxo comeca quando o aluno avisa que nao vai comparecer."
"A Taliya identifica o aluno, encontra a aula provavel e confere se o aviso chegou dentro do prazo."

Meio:
"A Taliya resolve sozinha quando aluno e aula foram identificados, o aviso chegou ate 2 horas antes da aula, a falta ainda nao existe e a mensagem aprovada pode ser usada."
Then show a compact list:

- aluno foi identificado
- aula existe na agenda
- aviso chegou ate 2 horas antes da aula
- falta ainda nao foi registrada
- mensagem usa template aprovado

"Ela chama a equipe quando o aviso chega fora do prazo, nao encontra aluno/aula, a falta ja existe, o aluno pede excecao ou WhatsApp, cota ou permissao bloqueiam o envio."
Then show a compact exception list:
- aviso chega fora do prazo
- nao encontra aluno ou aula
- falta ja foi registrada
- aluno pede excecao, credito, cancelamento ou reclama
- WhatsApp, cota ou permissao bloqueiam o envio

Fim:
"A falta fica registrada na aula e a mensagem permitida e enviada."
"Se configurado, abre tarefa de reposicao."
"Se prazo, aluno, aula, credito ou envio nao fecharem, a equipe decide."

Small tag in this block:
"Pode abrir tarefa em Reposicoes"

3. Large full-width settings block: "Ajustes deste fluxo"
Make this block prominent, like an operational form.
Fields:
- Prazo para aviso: Ate 2 horas antes da aula. Help text: Fora desse prazo, chama a equipe.
- Proximo passo apos falta: Criar tarefa de reposicao. Help text: A reposicao segue pelas proprias regras.
- Responsaveis por excecao: chips Recepcao, Coordenadora, Dono/admin. Help text: Quem recebe o caso quando a Taliya nao pode seguir.
- Tom/template da mensagem: Acolhedor. Show a short message preview:
"Oi, {{nome}}. Vi aqui que voce nao vai conseguir vir a aula de {{horario}}. Vou registrar sua falta e deixar a reposicao encaminhada para a equipe."

Bottom action row:
Primary black button: Testar este fluxo
Secondary button: Salvar ajustes
Secondary button: Voltar para rotina

Right side panel:
Agente de Configuracao
Subtitle: Ajudando neste fluxo
Info card:
"Este fluxo esta em Autonomo com excecoes. A Taliya trata a falta avisada quando aluno, aula, prazo e mensagem estao claros. Se algum dado faltar ou o envio falhar, chama a equipe definida."
Suggestion buttons:
O que muda no Copiloto?
Quando a equipe sera chamada?
Por que Autonomo esta bloqueado?
Testar aluno fora do prazo
Input placeholder: Pergunte sobre este fluxo...

Important constraints:
- Do not create a separate large requirements/preflight card.
- Explain the flow with Inicio, Meio and Fim.
- Each part must be detailed enough to explain what starts, what Taliya checks, what Taliya does, when humans enter, and how the flow ends.
- Do not put consequences inside the condition list; consequences belong in Fim.
- The preflight must be only the header chip "7 requisitos OK".
- The settings block must span the full width of the main content area.
- Do not show internal IDs like B1, B2 or P03.
- Do not use the labels Automatico direto, Automatico com excecoes or Automatico com aprovacao.
- Do not use vague copy like "se estiver dentro da regra"; use the exact rules above.
- Keep all text readable and non-overlapping.
```
