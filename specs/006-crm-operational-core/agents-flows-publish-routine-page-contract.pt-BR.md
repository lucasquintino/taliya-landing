# Taliya CRM - Contrato Da Pagina Publicar Rotina

Status: aprovado v0.1.
Data: 2026-05-23.

## Imagem Aprovada

```text
D:/Downloads/taliya-crm-chatgpt-images-named-20260511-082508/59_round-4.1L_agentes_06_publicar-rotina-presenca-faltas-aprovado.png
```

## Rota

```text
/app/agentes/[agentId]/rotinas/[routineId]/publicar
```

Exemplo aprovado:

```text
/app/agentes/agenda/rotinas/presenca-e-faltas/publicar
```

## Papel Da Pagina

`Publicar rotina` e a revisao final antes de colocar uma rotina em operacao.

Ela nao configura fluxo, nao simula e nao mostra execucao real. Ela confirma o que sera publicado, quais limites estao ativos e se existe algum bloqueio.

Publicacao principal e por rotina. Publicacao individual de fluxo existe apenas como excecao quando um fluxo foi ajustado, bloqueado ou precisa ser republicado sozinho.

Variacoes bloqueadas, parciais e por plano nao precisam de novas imagens. O contrato completo dessas variacoes fica em:

```text
agents-flows-operational-variation-contract.pt-BR.md
```

O estado `Simulacao concluida`, `Simulacao com avisos`, `Simulacao bloqueada` ou `Simulacao desatualizada` vem do contrato:

```text
agents-flows-routine-simulation-result-contract.pt-BR.md
```

## Estrutura Aprovada

1. Header com breadcrumb, titulo, subtitulo e chips.
2. Preflight `Pronta para publicar`.
3. Cards explicativos dos fluxos que serao publicados.
4. Bloco `O que sera ativado`.
5. Rodape de acoes.
6. Painel direito com Agente de Configuracao.

## Header

Titulo exemplo:

```text
Publicar Presenca e faltas
```

Subtitulo:

```text
Revise o que vai entrar em operacao antes de ativar esta rotina.
```

Chips:

- `Mais autonomo`
- `4 fluxos`
- `Simulacao concluida`
- `Pronta para publicar`

## Preflight

Titulo:

```text
Pronta para publicar
```

Texto:

```text
Nenhum bloqueio encontrado. A rotina pode entrar em operacao com os limites abaixo.
```

Checklist compacto:

- WhatsApp conectado
- Templates aprovados
- Responsaveis definidos
- Cota disponivel
- Auditoria ativa

Se houver bloqueio, o bloco troca para estado `Bloqueada para publicar` e lista somente os bloqueios reais.

## Cards Dos Fluxos

Os cards devem resumir a configuracao real de cada fluxo, no mesmo espirito da pagina `Ver e ajustar fluxo`, mas sem edicao.

Cada card deve mostrar:

- modo;
- status;
- inicio;
- o que a Taliya faz;
- parada, chamada humana ou aprovacao;
- ajustes principais;
- onde a operacao continua;
- acoes secundarias `Ver fluxo` e `Simular`.

Os cards nao devem virar tabela, relatorio ou dashboard.

## Exemplo Aprovado: Presenca E Faltas

### Confirmacao De Presenca

- Modo: `Autonomo`.
- Status: `Pronto`.
- Inicio: antes da aula, quando chega o horario de confirmar presenca.
- Faz: confere aula, aluno, horario e template; envia confirmacao; registra respostas; deixa pendente quem nao respondeu.
- Para/chama equipe se: aula mudou, aluno nao confere, resposta conflita ou WhatsApp falha.
- Ajustes: template de confirmacao padrao, canal WhatsApp, tom direto.
- Continua em: Aula / Tarefas.

### Falta Com Aviso

- Modo: `Autonomo com excecoes`.
- Status: `Pronto`.
- Inicio: quando o aluno avisa que nao vai comparecer.
- Faz: confere aluno, aula, prazo e falta anterior; registra falta; envia mensagem aprovada; cria tarefa em Reposicoes.
- Chama equipe se: aviso fora do prazo, aluno pede credito/cancelamento, aula nao encontrada ou WhatsApp falha.
- Ajustes: prazo ate 2h antes, responsaveis Recepcao e Coordenacao, tom acolhedor.
- Continua em: Reposicoes / Tarefas.

### Falta Sem Aviso

- Modo: `Autonomo com excecoes`.
- Status: `Pronto`.
- Inicio: depois da aula, quando o aluno previsto nao apareceu nem avisou.
- Faz: confere chamada, janela de tolerancia e historico; marca ausencia; abre acompanhamento.
- Chama equipe se: chamada nao foi fechada, aviso apareceu em outro canal, recorrencia alta ou risco de cancelamento.
- Ajustes: tolerancia apos aula, responsaveis Recepcao e Retencao, tom cuidadoso.
- Continua em: Aula / Retencao / Tarefas.

### Correcao De Presenca

- Modo: `Autonomo com aprovacao`.
- Status: `Aprovacao ao executar`.
- Inicio: quando alguem solicita corrigir presenca depois da aula.
- Faz: confere aula, aluno, motivo e impacto; prepara a alteracao; cria pedido de aprovacao.
- Nao faz sozinha: nao altera historico de presenca antes da aprovacao.
- Ajustes: aprovadores Coordenacao e Dono/admin, motivo obrigatorio, auditoria ativa.
- Continua em: Aprovacoes / Auditoria.

## O Que Sera Ativado

Usar este titulo, nao `Confirmacoes finais`.

Itens aprovados:

- Envio automatico de confirmacoes de presenca.
- Registro automatico de faltas quando as regras fecharem.
- Criacao de tarefas de reposicao e acompanhamento.
- Aprovacao obrigatoria para corrigir presenca.

## Acoes

CTA principal:

```text
Publicar rotina
```

CTAs secundarios:

```text
Simular novamente
Voltar para ajustes
```

Nao usar `Publicar fluxo` como CTA principal nesta pagina.

## Agente De Configuracao

O painel direito explica a publicacao, mas nunca publica sozinho.

Mensagem aprovada:

```text
Esta rotina esta pronta. A Taliya vai operar confirmacoes e faltas comuns sozinha, chamar a equipe nas excecoes e pedir aprovacao antes de corrigir historico de presenca.
```

Sugestoes:

- O que muda ao publicar?
- Quando a equipe sera chamada?
- Por que correcao pede aprovacao?
- Posso publicar so um fluxo?

Campo:

```text
Pergunte sobre esta publicacao...
```

## Ajustes Documentados Sem Nova Imagem

- Em fluxo autonomo, o label pode ser `Para/chama equipe se` quando o fallback puder virar tarefa humana.
- Em fluxo com aprovacao, manter `Nao faz sozinha` quando isso for mais claro que `Chama equipe se`.
- O chip `Aprovacao ao executar` e o padrao para fluxos que nao alteram dados antes da aprovacao.
- O botao `Publicar rotina` pode usar icone de publicacao/check, mas nao icone de play.
