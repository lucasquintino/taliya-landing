# Taliya CRM - Auditoria Do Que Ainda Falta Em Agentes/Fluxos

Status: auditoria v0.1.
Data: 2026-05-23.

## Objetivo

Auditar a familia Agentes/Fluxos depois da definicao das paginas principais e mapear exatamente o que ainda falta definir, documentar, revisar ou gerar como imagem.

Esta auditoria separa:

- o que ja esta fechado;
- o que esta documentado, mas ainda sem imagem;
- o que esta parcialmente documentado;
- o que ainda pode gerar confusao;
- a ordem recomendada para fechar as proximas etapas.

## Fontes Revisadas

Contratos principais:

- `agents-flows-functional-architecture.pt-BR.md`
- `agents-flows-routines-pages-final-contract.pt-BR.md`
- `agents-flows-final-flow-page-contract.pt-BR.md`
- `agents-flows-test-simulation-page-contract.pt-BR.md`
- `agents-flows-publish-routine-page-contract.pt-BR.md`
- `agents-flows-publication-versioning-and-evals.pt-BR.md`
- `agents-flows-state-variant-map.pt-BR.md`

Matrizes dos 96 fluxos:

- `agents-flows-96-complete-detail-matrix.pt-BR.csv`
- `agents-flows-96-complete-detail-review.pt-BR.md`
- `agents-flows-96-test-simulation-matrix.pt-BR.csv`
- `agents-flows-96-test-simulation-review.pt-BR.md`
- `agents-flows-final-flow-contract-matrix.pt-BR.csv`
- `agents-flows-detailed-mode-rules-matrix.pt-BR.csv`
- `agents-flows-lifecycle-mode-matrix.pt-BR.csv`

Contratos de plano/entitlement/guardrails:

- `agent-plan-entitlements.pt-BR.md`
- `agent-guardrails-evals-contract.pt-BR.md`
- `quota-touchpoints.pt-BR.md`
- `control-planes-master-map.pt-BR.md`
- `technical-integrations-master-map.pt-BR.md`
- `billing-taliya-master-map.pt-BR.md`

Mapas visuais:

- `agents-flows-visual-brief-before-image-generation.pt-BR.md`
- `web-screen-map.pt-BR.md`
- `final-screen-contract-matrix.pt-BR.md`
- manifesto de imagens em `D:/Downloads/taliya-crm-chatgpt-images-named-20260511-082508/MANIFESTO.pt-BR.md`

## O Que Esta Fechado

### 1. Arquitetura Funcional

Status: fechado.

Decisoes consolidadas:

- Agentes/Fluxos e familia propria do produto.
- Agente nao tem configuracao propria.
- Rotina agrupa fluxos e e a principal unidade de publicacao.
- Fluxo configura somente o necessario.
- Setup Inicial nao publica autonomia.
- Configuracoes nao viram builder de agente.
- Integracoes, Billing, Uso/Cotas, Auditoria e Control Planes continuam fontes de verdade das suas areas.

### 2. Sete Agentes Canonicos

Status: fechado.

Agentes:

- Atendimento;
- Agenda;
- Vendas;
- Financeiro;
- Retencao;
- Gestao/Governanca;
- Historico/Evolucao.

Imagem aprovada:

```text
52_round-4.1L_agentes_01_catalogo-agentes-aprovado.png
```

### 3. Pagina Do Agente Agenda

Status: fechado para caminho feliz.

Imagem aprovada:

```text
53_round-4.1L_agentes_02_agente-agenda-rotinas-aprovado.png
```

Falta apenas gerar variações visuais se forem necessarias: plano 0, agente nao contratado, agente pausado ou bloqueado.

### 4. Pagina Da Rotina Presenca E Faltas

Status: fechado para caminho feliz.

Imagem aprovada:

```text
54_round-4.1L_agentes_03_rotina-presenca-faltas-aprovado.png
```

Contrato:

- perfil da rotina;
- cards dos fluxos;
- Agente de Configuracao;
- CTAs `Simular rotina`, `Ajustar fluxos`, `Revisar para publicar`.

### 5. Pagina Ver E Ajustar Fluxo

Status: fechado para exemplo `Falta com aviso`.

Imagem aprovada:

```text
56_round-4.1L_agentes_04_fluxo-falta-com-aviso-v2-aprovado.png
```

Matrizes cobrem os 96 fluxos:

- inicio/meio/fim;
- comportamento por modo;
- ajustes minimos;
- limites;
- fallback;
- continuidade.

### 6. Simular Fluxo

Status: fechado como estrutura.

Imagem aprovada:

```text
58_round-4.1L_agentes_05_teste-fluxo-falta-com-aviso-aprovado.png
```

Decisao de produto:

```text
Nome oficial: Simular fluxo.
Nao existe segunda pagina Testar fluxo.
```

A imagem `58` esta aprovada em layout, com ajuste documentado de nomenclatura:

- `/teste` vira `/simular`;
- `Testar` vira `Simular`;
- `Execucao do teste` vira `Execucao da simulacao`;
- `Teste seguro` vira `Simulacao segura`.

### 7. Publicar Rotina

Status: fechado para caminho feliz.

Imagem aprovada:

```text
59_round-4.1L_agentes_06_publicar-rotina-presenca-faltas-aprovado.png
```

Contrato:

- preflight;
- cards resumindo configuracao real dos fluxos;
- bloco `O que sera ativado`;
- CTA `Publicar rotina`;
- Agente de Configuracao sem publicar sozinho.

### 8. Mapeamento Dos 96 Fluxos

Status: fechado.

Cobertura validada:

- 96 fluxos detalhados;
- 96 simulacoes mapeadas;
- 96 limites explicitos;
- 96 acoes unicas;
- 42 fluxos com aprovacao explicita;
- 43 simulacoes com celular/conversa;
- 53 simulacoes com objeto interno do CRM;
- 18 tipos de visual central.

## O Que Ainda Falta Definir Ou Gerar

### P0 - Estados Alternativos Das Telas Ja Aprovadas

Status: parcialmente fechado.

Agora existe contrato em:

```text
agents-flows-state-variant-map.pt-BR.md
```

Ainda falta decidir quais estados viram imagem.

Estados mais importantes:

1. rotina bloqueada para publicar;
2. simulacao desatualizada;
3. cota insuficiente;
4. integracao/canal bloqueado;
5. plano 0 agentes;
6. agente nao contratado;
7. rotina pausada por incidente;
8. rotina publicada.

Recomendacao:

A pagina normal de `Publicar rotina` ja tem imagem propria aprovada:

```text
59_round-4.1L_agentes_06_publicar-rotina-presenca-faltas-aprovado.png
```

Nao gerar imagem nova para variacoes.

O proximo artefato deve ser documental: detalhar a variacao `Publicar rotina bloqueada`, ou seja, a mesma pagina quando preflight, cota, integracao, simulacao ou permissao impedem a publicacao.

### P0 - Rotina Publicada

Status: falta contrato visual e imagem.

Depois de clicar em `Publicar rotina`, o usuario precisa ver a rotina em estado publicado.

Precisa definir:

- como aparece a versao publicada;
- quais fluxos ficaram ativos;
- quais ficaram manuais/bloqueados;
- onde ver execucoes;
- como pausar;
- como simular novamente;
- como editar rascunho sem alterar a versao publicada.

Proposta de rota:

```text
/app/agentes/[agentId]/rotinas/[routineId]
```

Nao precisa ser rota nova. E um estado da pagina da rotina.

### P0 - Pausar, Retomar E Rollback

Status: contrato funcional existe, mas falta contrato de UI.

Docs existentes dizem que pausa/rollback existem, mas ainda falta desenhar a superficie:

- confirmacao de pausa de fluxo;
- confirmacao de pausa de rotina;
- rotina pausada;
- retomar rotina;
- rollback de versao;
- incidente que pausa automaticamente.

O que a UI deve sempre mostrar:

- motivo;
- impacto;
- fluxos afetados;
- o que continua manual;
- o que nao pode ser desfeito;
- evento de auditoria.

### P0 - Detalhe De Execucao

Status: falta imagem e contrato visual especifico.

Rota ja definida:

```text
/app/fluxos/execucoes/[runId]
```

Precisa mostrar:

- fluxo;
- rotina;
- versao publicada;
- modo;
- entrada;
- checagens;
- decisao;
- acao;
- ferramenta/canal;
- cota/custo;
- auditoria;
- fallback;
- erro/incidente se houver.

Control Plane investiga execucao. Nao configura fluxo.

### P1 - Simular Rotina

Status: nao precisa de nova imagem neste momento.

Importante:

A imagem `58_round-4.1L_agentes_05_teste-fluxo-falta-com-aviso-aprovado.png` e uma imagem de `Simular fluxo`, porque esta dentro de:

```text
/app/agentes/agenda/rotinas/presenca-e-faltas/fluxos/falta-com-aviso/simular
```

Ela simula um fluxo especifico, com cenario, celular/conversa e execucao passo a passo.

`Simular rotina` continua sendo uma acao da pagina da rotina:

```text
/app/agentes/[agentId]/rotinas/[routineId]
```

Decisao atual:

- nao gerar uma pagina visual propria para `Simular rotina` agora;
- `Simular rotina` valida o conjunto dos fluxos da rotina;
- o resultado dessa validacao aparece na rotina e alimenta `Publicar rotina`;
- quando o usuario quiser ver um caso em detalhe, abre `Simular fluxo`.

Regra de produto:

- `Simular fluxo`: ensaio detalhado de um comportamento especifico, como a imagem 58;
- `Simular rotina`: checagem do conjunto, preflight e prontidao para publicacao.

Se no futuro a rotina precisar de uma pagina propria, ela deve ser uma tela de preflight consolidado, nao uma copia da tela de celular do fluxo.

### P1 - Publicacao Sempre Completa

Status: decisao fechada.

Agentes/Fluxos nao tem publicacao parcial de rotina.

Decisao:

- a rotina so publica quando todos os fluxos estao prontos para o modo configurado;
- fluxo Manual pode fazer parte da rotina publicada, desde que esteja planejado, simulado e com caminho humano definido;
- fluxo bloqueado por plano, cota, integracao, permissao, dado, template, pausa ou simulacao desatualizada bloqueia a publicacao;
- se o studio quiser publicar, precisa corrigir o bloqueio ou ajustar o modo do fluxo e simular novamente.

Contrato:

```text
agents-flows-routine-simulation-result-contract.pt-BR.md
```

### P1 - Variações 0/1/3/7 Agentes Nas Telas Aprovadas

Status: regra de produto existe; falta contrato visual consolidado por pagina.

Fonte:

- `agent-plan-entitlements.pt-BR.md`;
- `agents-flows-state-variant-map.pt-BR.md`.

Ainda falta gerar ou documentar em prompt:

- `/app/agentes` com 0 agentes;
- `/app/agentes/agenda` com Agenda nao contratada;
- rotina Agenda em plano sem Agenda;
- fluxo bloqueado por plano;
- publicacao bloqueada por plano;
- upgrade sem pressionar o usuario e mantendo caminho manual.

Contrato esperado por plano:

| Plano | O que o usuario ve | O que pode configurar | O que nao pode acontecer |
| --- | --- | --- | --- |
| 0 agentes | CRM manual, cards dos agentes como catalogo/preview e fluxos como sugestao. | Nada autonomo; no maximo preferencia manual, responsavel humano e leitura de como funcionaria. | Publicar rotina automatica, simular como se estivesse contratado ou bloquear o CRM base. |
| 1 agente | Apenas o agente contratado abre completo; os outros aparecem como nao contratados. | Rotinas e fluxos do agente contratado, respeitando cotas e integracoes. | Configurar fluxo de agente fora do plano como se estivesse ativo. |
| 3 agentes | Bundle contratado abre por areas; demais agentes ficam como upgrade/preview. | Rotinas dos 3 agentes contratados, com perfis de rotina para reduzir trabalho manual. | Obrigar configuracao fluxo a fluxo ou misturar fluxos nao contratados na publicacao. |
| 7 agentes | Todos os agentes ativos, com necessidade maior de status, filtros e bloqueios claros. | Todas as rotinas/fluxos contratados, ainda priorizando perfil de rotina e ajuste por excecao. | Virar painel tecnico de control plane dentro de Agentes/Fluxos. |

Decisao de simplicidade:

- plano muda acesso e capacidade, nao muda a logica do CRM base;
- fluxo nao contratado pode ser explicado, mas nao configurado como ativo;
- caminho manual sempre existe quando o agente nao esta disponivel;
- a UI deve separar claramente `nao contratado`, `bloqueado`, `pausado` e `manual`.

### P1 - Aprovacao Gerada Por Fluxo

Status: integrado conceitualmente, mas sem imagem especifica nesta familia.

Fluxos como `Correcao de presenca` criam aprovacao.

Falta mostrar:

- como a pagina de fluxo aponta para a aprovacao;
- como a pagina `Aprovacoes` mostra origem em Agentes/Fluxos;
- como a execucao fica aguardando aprovacao;
- o que muda depois de aprovar/rejeitar/expirar.

Nao precisa ser uma pagina nova de Agentes/Fluxos, mas precisa de contrato de ligacao.

### P1 - Uso/Cotas Na Pratica

Status: fonte de verdade definida; UI de bloqueio ainda precisa exemplos.

Faltam variações:

- cota 70%;
- cota 90%;
- cota 100%;
- economia ativa;
- pacote extra;
- fluxo degradado por cota.

Regra:

Manual continua disponivel.

### P2 - Mobile/App

Status: fora da prioridade visual atual, mas precisa ser mapeado depois.

Mobile deve cobrir:

- alerta critico;
- aprovacao;
- pausa emergencial;
- acompanhar incidente;
- tarefa criada por fallback.

Nao deve virar builder de fluxo no app.

### P2 - Limpeza De Termos Legados

Status: parcialmente feito.

Termos finais:

- `Simular fluxo`, nao `Testar fluxo`;
- `Publicar rotina`, nao `Ativar rotina`;
- `rotina`, nao `pacote`;
- `perfil da rotina`, nao `preset`;
- `Mais autonomo`, `Equilibrado`, `Mais manual`.

Ainda existem nomes de arquivos legados com `teste` porque foram criados antes da decisao. Isso e aceitavel como artefato interno, desde que UI e contratos finais usem `Simular fluxo`.

Se o projeto quiser limpeza total, criar uma rodada separada de renomeacao de arquivos e referencias.

## Riscos De Confusao Ainda Possiveis

### 1. Simular Rotina vs Simular Fluxo

Risco:

O usuario pode nao entender a diferenca.

Decisao recomendada:

- `Simular fluxo`: ensaio detalhado de um comportamento especifico.
- `Simular rotina`: valida o conjunto e gera preflight para publicacao.

### 2. Publicar Rotina vs Publicar Fluxo

Risco:

O usuario pode achar que precisa publicar 96 fluxos.

Decisao ja tomada:

- publicacao principal e por rotina;
- fluxo individual so como excecao.

Precisa reforcar em todos os prompts.

### 3. Copiloto Como Botao vs Modo Do Fluxo

Risco:

O botao de ajuda pode ser confundido com modo copiloto.

Decisao ja tomada:

- modo do fluxo define quem conduz quando dispara;
- copiloto contextual e ajuda sob demanda.

### 4. Bloqueio Por Dependencia vs Ajuste Do Fluxo

Risco:

Canal, cota, integracao e permissao voltarem como campos editaveis do fluxo.

Decisao ja tomada:

- aparecem como dependencias/preflight;
- correcao acontece na fonte certa.

## Rodadas De Revisao Executadas

### Rodada 1 - Inventario

Verificado:

- documentos base de Agentes/Fluxos;
- contratos de paginas ja aprovadas;
- manifesto da pasta de imagens;
- imagens 52, 53, 54, 56, 58 e 59.

Conclusao:

O caminho principal esta documentado: catalogo de agentes, pagina do agente, pagina da rotina, pagina do fluxo, simulacao do fluxo e publicacao da rotina.

### Rodada 2 - Cobertura De Produto

Verificado:

- 96 fluxos;
- rotinas por agente;
- modos manual, copiloto, autonomo com aprovacao, autonomo com excecoes e autonomo;
- configuracao por perfil de rotina e ajuste por fluxo;
- limites de configuracao para evitar liberdade desnecessaria.

Conclusao:

Nao falta definir quais fluxos existem. O que faltava era mapear estados operacionais fora do caminho feliz.

### Rodada 3 - Estados E Bloqueios

Verificado:

- plano 0/1/3/7;
- cota;
- integracao;
- permissao;
- dado ausente;
- simulacao desatualizada;
- pausa por usuario;
- pausa por incidente;
- publicacao sempre completa;
- rollback.

Conclusao:

Esses estados agora tem contrato inicial em `agents-flows-state-variant-map.pt-BR.md`.

### Rodada 4 - Consistencia Visual E De Linguagem

Verificado:

- `Simular fluxo` substitui `Testar fluxo` na UI final;
- `Publicar rotina` substitui `Ativar rotina`;
- `Agente de Configuracao` aparece apenas em paginas de configuracao/simulacao/publicacao;
- `/app/agentes` e `/app/agentes/[agentId]` continuam sem painel direito de configuracao;
- cards de publicacao resumem inicio, faz, para/chama equipe, ajustes e continua em.

Conclusao:

Os prompts e contratos visuais estao alinhados com as decisoes recentes. Arquivos antigos podem manter nome de `teste` como historico, mas UI final deve usar `Simular`.

### Rodada 5 - Validacao Mecanica Das Matrizes

Verificado:

- `agents-flows-96-complete-detail-matrix.pt-BR.csv`: 96 fluxos, com Inicio, Meio, Fim, ajustes, requisitos, encadeamento e simulacao;
- `agents-flows-detailed-mode-rules-matrix.pt-BR.csv`: 96 fluxos, com comportamento por modo;
- `agents-flows-96-test-simulation-matrix.pt-BR.csv`: 96 simulacoes de fluxo;
- `agents-flows-final-flow-contract-matrix.pt-BR.csv`: 96 contratos finais de pagina do fluxo;
- `agents-flows-lifecycle-mode-matrix.pt-BR.csv`: 480 linhas, cobrindo 96 fluxos x 5 modos.

Conclusao:

A cobertura dos 96 fluxos nao depende mais de memoria ou interpretacao. Ela esta materializada em matrizes revisaveis e em documentos de auditoria.

## Ordem Recomendada A Partir De Agora

1. Documentar em detalhe a variacao `Publicar rotina bloqueada`; a pagina base pronta ja e a imagem 59.
2. Documentar `Rotina publicada` e `Rotina publicada com excecao aberta`.
3. Documentar pausa/retomada/rollback.
4. Documentar detalhe de execucao `/app/fluxos/execucoes/[runId]`.
5. Documentar incidente que pausou fluxo/rotina.
6. Documentar variacoes de plano 0/1/3/7 para as telas ja aprovadas.
7. Documentar variacoes do resultado de `Simular rotina` dentro da rotina/publicacao, sem criar nova pagina por enquanto.

## Conclusao

A arquitetura base de Agentes/Fluxos esta fechada para o caminho feliz e para os 96 fluxos.

O que falta nao e mais "quais fluxos existem" nem "como configurar um fluxo".

O que falta agora e fechar as variacoes operacionais:

- bloqueio;
- publicacao sempre completa;
- rotina publicada;
- pausa;
- rollback;
- execucao;
- incidente;
- entitlements 0/1/3/7;
- simulacao de rotina.

Essas lacunas foram mapeadas e agora tem contrato inicial em:

```text
agents-flows-state-variant-map.pt-BR.md
```

O detalhamento operacional completo das variacoes fica em:

```text
agents-flows-operational-variation-contract.pt-BR.md
```

Operacao leve pos-publicacao usa as mesmas paginas de rotina/fluxo e fica definida em:

```text
agents-flows-post-publication-light-ops-contract.pt-BR.md
```
