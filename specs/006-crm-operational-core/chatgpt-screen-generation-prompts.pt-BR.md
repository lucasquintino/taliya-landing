# Pacote de prompts para gerar telas no ChatGPT - PT-BR

> Status: pronto para pacote final v0.1. As Rodadas 1-11 definem a base funcional; prompts finais devem usar as decisoes fechadas em `round-11-product-closure.pt-BR.md`.

## Objetivo

Transformar as especificacoes finais do Taliya em prompts prontos para gerar paginas web e telas mobile no ChatGPT.

As referencias visuais aprovadas entram aqui como alvo de composicao visual, nao como fonte de regra de negocio.

Referencias:

- Web: `https://dribbble.com/shots/24659454-Customer-Journey-CRM-Dashboard`
- Mobile: `https://dribbble.com/shots/24537717-Sugar-CRM-Customer-Journey-Dashboard`

## Regra principal

```text
Produto vem dos documentos Taliya.
Visual vem das referencias aprovadas.
O ChatGPT nao pode inventar regra, fluxo, campo, permissao, cota ou acao.
```

## Entrada obrigatoria para cada prompt

Cada prompt de tela deve receber dados vindos de `screen-specs-detailed.pt-BR.md`, `final-screen-contract-matrix.pt-BR.md` e das fichas das Rodadas 1-7:

- nome da tela;
- tipo: web ou mobile;
- objetivo;
- usuario principal;
- rotas relacionadas;
- casos de uso cobertos;
- fluxos de agente relacionados;
- blocos da tela;
- campos exibidos;
- campos editaveis;
- botoes;
- estados;
- permissoes;
- cotas;
- auditoria;
- comportamento manual;
- comportamento copiloto;
- comportamento autonomo;
- fallback;
- equivalente web/mobile.

## Prompt base web

```text
Gere uma pagina web para o CRM Taliya usando a composicao visual da referencia web:
https://dribbble.com/shots/24659454-Customer-Journey-CRM-Dashboard

A pagina deve parecer um CRM premium, operacional, denso e orientado por jornada.

Use apenas as informacoes funcionais abaixo. Nao invente regras de negocio, campos, botoes, permissoes, cotas, status ou fluxos.

[COLAR FICHA DA PAGINA WEB AQUI]

Requisitos visuais:
- sidebar de navegacao clara;
- topo com contexto operacional;
- area principal organizada por jornada, cards, listas, graficos ou tabela conforme a ficha;
- acoes visiveis e posicionadas conforme prioridade;
- estados vazios, erro, carregamento, bloqueio, cota e sem permissao quando definidos;
- indicacao de IA/agente somente quando a ficha definir;
- visual inspirado na referencia, mas com conteudo, marca e dominio Taliya/Pilates.

Resultado esperado:
- descreva a tela completa;
- detalhe layout, componentes e hierarquia;
- gere conteudo realista de exemplo;
- nao altere escopo funcional.
```

## Prompt base mobile

```text
Gere uma tela mobile para o app Taliya usando a composicao visual da referencia mobile:
https://dribbble.com/shots/24537717-Sugar-CRM-Customer-Journey-Dashboard

A tela deve parecer um app de CRM premium, operacional, rapido para uso diario e orientado por jornada.

Use apenas as informacoes funcionais abaixo. Nao invente regras de negocio, campos, botoes, permissoes, cotas, status ou fluxos.

[COLAR FICHA DA TELA MOBILE AQUI]

Requisitos visuais:
- cabecalho compacto com contexto;
- conteudo priorizado para uso em movimento;
- cards, listas, etapas, alertas ou acoes conforme a ficha;
- botoes principais com toque facil;
- estados vazios, erro, carregamento, bloqueio, cota e sem permissao quando definidos;
- indicacao de IA/agente somente quando a ficha definir;
- visual inspirado na referencia, mas com conteudo, marca e dominio Taliya/Pilates.

Resultado esperado:
- descreva a tela completa;
- detalhe layout, componentes e hierarquia;
- gere conteudo realista de exemplo;
- nao altere escopo funcional.
```

## Prompts por tela

Esta secao deve ser preenchida com um prompt final por superficie usando as seguintes fontes funcionais:

- `round-11-product-closure.pt-BR.md`
- `final-navigation-web-app.pt-BR.md`
- `studio-operational-presets.pt-BR.md`
- `final-screen-contract-matrix.pt-BR.md`
- `round-1-activation-setup-spec.pt-BR.md`
- `round-2-daily-command-spec.pt-BR.md`
- `round-3-attendance-students-history-spec.pt-BR.md`
- `round-4-schedule-classes-replacements-spec.pt-BR.md`
- `round-5-sales-trials-enrollment-communications-spec.pt-BR.md`
- `round-6-finance-retention-sensitive-spec.pt-BR.md`
- `round-7-agents-quotas-governance-spec.pt-BR.md`

Formato:

```text
## [Nome da pagina/tela]

Tipo:
Referencia visual:
Ficha fonte:
Prompt:
```

## Checklist de aceite

- Toda pagina web tem prompt.
- Toda tela mobile tem prompt.
- Todo prompt aponta a ficha fonte.
- Nenhum prompt pede para o ChatGPT inventar regra de negocio.
- Nenhum prompt remove cota, auditoria, permissao ou fallback.
- Telas com IA mostram motivo, modo, status e acao esperada.
- Telas do plano 0 agentes continuam funcionais sem agente.
- A referencia visual orienta composicao, nao escopo.

## Prompt de seguranca para qualquer tela v0.1

```text
Use somente a ficha funcional fornecida.
Nao altere as premissas fechadas na Rodada 11.
Se faltar campo, mostre como pendencia ou estado de configuracao, nao invente.
Toda acao sensivel precisa exibir permissao, impacto e auditoria.
Toda acao com IA precisa exibir modo manual/copiloto/autonomo, cota e fallback.
O plano Base com 0 agentes deve continuar usavel.
```
