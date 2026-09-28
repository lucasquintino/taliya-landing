# Taliya CRM Operational Core - Indice PT-BR

> Status: fechamento funcional v0.1. Estes documentos definem o escopo funcional do CRM web, app mobile e agentes integrados para gerar telas e prompts finais.

## Decisao De Produto Fechada V0.1

Taliya fica definido v0.1 como:

```text
CRM operacional para studios de Pilates com agentes de IA integrados ao sistema.
```

Os agentes atuam tanto:

- no WhatsApp;
- dentro do CRM web e do app mobile.

WhatsApp e canal. O CRM e o sistema operacional.

## Fonte Da Verdade

Para gerar telas, prompts ou consolidacao de produto, a ordem de leitura e:

1. `product-final-master-map.pt-BR.md`
2. `product-decisions-working-log.pt-BR.md`
3. `final-navigation-web-app.pt-BR.md`
4. `web-screen-map.pt-BR.md`
5. `final-screen-contract-matrix.pt-BR.md`
6. `final-image-route-status-matrix.pt-BR.md`
7. `use-case-final-product-coverage-map.pt-BR.md`
8. `agents-flows-final-route-remap.pt-BR.md`
9. `round-11-product-closure.pt-BR.md`
10. `studio-operational-presets.pt-BR.md`
11. `agent-plan-entitlements.pt-BR.md`
12. `route-agent-mode-entitlement-matrix.pt-BR.md`
13. `screen-ux-depth-contract.pt-BR.md`
14. `technical-product-contracts.pt-BR.md`
15. `agent-guardrails-evals-contract.pt-BR.md`
16. `final-screen-prompts-catalog.pt-BR.md`
17. `remaining-depth-backlog.pt-BR.md`
18. `page-case-coverage.pt-BR.csv`
19. `setup-final-audit.pt-BR.md`
20. `setup-configuration-plan-100.pt-BR.md`
21. `setup-agent-role.pt-BR.md`
22. `setup-billing-class-consumption-models.pt-BR.md`
23. `setup-acceptance-criteria.pt-BR.md`
24. Rodadas 1-7 para fichas profundas por area

Documentos anteriores continuam como historico de descoberta. Se algum rascunho antigo disser "candidato", "validar", "decisao aberta" ou listar como pagina propria algo que a revisao atual marcou como contextual/pos-MVP, prevalecem `product-final-master-map.pt-BR.md`, `product-decisions-working-log.pt-BR.md`, `final-navigation-web-app.pt-BR.md`, `web-screen-map.pt-BR.md`, `final-screen-contract-matrix.pt-BR.md`, `final-image-route-status-matrix.pt-BR.md`, `use-case-final-product-coverage-map.pt-BR.md` e `agents-flows-final-route-remap.pt-BR.md`.

## Numeros Atuais

| Item | Total | Status |
| --- | ---: | --- |
| Fluxos base de agentes | 96 | cobertos v0.1 |
| Fluxos opcionais reclassificados | 2 | E14 virou subfluxo; G13 virou gate |
| Casos de uso gerenciais catalogados | 132 | cobertos v0.1 |
| Lacunas de auditoria incorporadas | 25 | incorporadas ao mapa |
| Universo atual de casos | 157 | coberto v0.1 |

## Documentos Principais

- [spec.md](./spec.md): especificacao base em ingles.
- [product-master-map-v2.pt-BR.md](./product-master-map-v2.pt-BR.md): mapa mestre em linguagem de negocio, com 157 casos cobertos v0.1.
- [product-master-map-v2.pt-BR.csv](./product-master-map-v2.pt-BR.csv): versao filtravel do mapa em linguagem de negocio, sem codigos internos.
- [multi-view-product-audit.pt-BR.md](./multi-view-product-audit.pt-BR.md): auditoria consolidada por diferentes visoes.
- [screen-inventory-tree.pt-BR.md](./screen-inventory-tree.pt-BR.md): arvore exploratoria de telas web e mobile.
- [coverage-heatmap.pt-BR.md](./coverage-heatmap.pt-BR.md): mapa de cobertura, riscos e lacunas.
- [decision-kanban.pt-BR.md](./decision-kanban.pt-BR.md): quadro de decisoes, duvidas, itens que talvez devam ser juntados e fora de escopo.
- [glossario-produto.pt-BR.md](./glossario-produto.pt-BR.md): traducao de termos tecnicos para linguagem de negocio.
- [rodada-1-auditoria-completa.pt-BR.md](./rodada-1-auditoria-completa.pt-BR.md): primeira rodada de revisao completa dos documentos, fluxos, casos, telas, dados, cotas e app mobile.
- [rodada-2-classificacao-157.pt-BR.md](./rodada-2-classificacao-157.pt-BR.md): classificacao sugerida dos 157 casos por profundidade e decisao.
- [rodada-2-classificacao-157.pt-BR.csv](./rodada-2-classificacao-157.pt-BR.csv): versao filtravel da classificacao dos 157 casos.
- [rodada-3-fechamento-consistencia.pt-BR.md](./rodada-3-fechamento-consistencia.pt-BR.md): fechamento de consistencia depois dos checks de rotas, objetos, contagens, autonomia e linguagem PT-BR.
- [product-depth-audit.pt-BR.md](./product-depth-audit.pt-BR.md): auditoria de profundidade por navegacao, telas, dados, automacao, mobile e MVP.
- [product-depth-matrix.pt-BR.md](./product-depth-matrix.pt-BR.md): matriz de profundidade dos 157 casos.
- [product-depth-matrix.pt-BR.csv](./product-depth-matrix.pt-BR.csv): versao filtravel da matriz de profundidade.
- [page-requirements.pt-BR.md](./page-requirements.pt-BR.md): lista concreta de paginas e o que cada pagina precisa ter.
- [page-requirements.pt-BR.csv](./page-requirements.pt-BR.csv): versao filtravel das paginas e requisitos.
- [page-case-coverage.pt-BR.csv](./page-case-coverage.pt-BR.csv): mapa filtravel dos 157 casos para suas paginas donas.
- [reference-aligned-ui-audit.pt-BR.md](./reference-aligned-ui-audit.pt-BR.md): auditoria contra as referencias visuais de CRM por jornada.
- [page-layout-zones.pt-BR.md](./page-layout-zones.pt-BR.md): mapa exato do que fica em cada zona de cada pagina.
- [page-layout-zones.pt-BR.csv](./page-layout-zones.pt-BR.csv): versao filtravel do mapa de zonas por pagina.
- [end-to-end-product-audit.pt-BR.md](./end-to-end-product-audit.pt-BR.md): auditoria ponta a ponta desde os fluxos iniciais ate produto, paginas, cotas e mobile.
- [web-screen-map.pt-BR.md](./web-screen-map.pt-BR.md): mapa consolidado do CRM web com menus, telas e grupos de rotas.
- [mobile-screen-map.pt-BR.md](./mobile-screen-map.pt-BR.md): mapa consolidado do app mobile com telas, profundidade e decisoes de mobile.
- [mobile-coverage-audit.pt-BR.md](./mobile-coverage-audit.pt-BR.md): auditoria de cobertura mobile percorrendo todas as 38 superficies do CRM.
- [screen-depth-readiness-audit.pt-BR.md](./screen-depth-readiness-audit.pt-BR.md): auditoria sobre se cada tela web/mobile ja tem profundidade suficiente para design e implementacao.
- [web-mobile-review-simulation.pt-BR.md](./web-mobile-review-simulation.pt-BR.md): lista consolidada web/mobile com simulacao de uso ponta a ponta.
- [complete-specification-plan.pt-BR.md](./complete-specification-plan.pt-BR.md): plano concreto por rodadas para fechar arquitetura funcional e especificacao profunda de paginas, telas, rotas, casos e fluxos.
- [chatgpt-screen-generation-prompts.pt-BR.md](./chatgpt-screen-generation-prompts.pt-BR.md): esqueleto do pacote final de prompts para gerar paginas web e telas mobile no ChatGPT depois do produto 100% fechado.
- [round-10-technical-user-audit.pt-BR.md](./round-10-technical-user-audit.pt-BR.md): revisao cruzada de todas as rodadas com visao tecnica e visao de gestor de studio.
- [round-11-product-closure.pt-BR.md](./round-11-product-closure.pt-BR.md): fechamento das decisoes D001-D037 como premissas v0.1.
- [studio-operational-presets.pt-BR.md](./studio-operational-presets.pt-BR.md): presets iniciais Conservador, Equilibrado e Crescimento.
- [final-navigation-web-app.pt-BR.md](./final-navigation-web-app.pt-BR.md): navegacao final web/app.
- [final-screen-contract-matrix.pt-BR.md](./final-screen-contract-matrix.pt-BR.md): matriz final de superficies, rotas, blocos, acoes, estados, permissoes, cotas e auditoria.
- [product-decisions-working-log.pt-BR.md](./product-decisions-working-log.pt-BR.md): decisoes tomadas na revisao atual de produto, incluindo cortes de paginas proprias, suporte, checkout, conta/assinatura e itens contextuais.
- [product-final-master-map.pt-BR.md](./product-final-master-map.pt-BR.md): resumo mestre final de produto, navegacao, paginas, contextuais, pos-MVP, cobertura e faltas antes da implementacao.
- [final-image-route-status-matrix.pt-BR.md](./final-image-route-status-matrix.pt-BR.md): matriz visual canonica de imagens, rotas, familias e status.
- [access-subscription-shell-approved.pt-BR.md](./access-subscription-shell-approved.pt-BR.md): contrato visual aprovado da imagem 71, shell base pre-CRM de Acesso e Assinatura.
- [access-subscription-auth-screens-review.pt-BR.md](./access-subscription-auth-screens-review.pt-BR.md): registro das imagens 72/73 de signup/signin, decisao de fluxo Google/Microsoft/e-mail e ajustes finos pendentes.
- [access-subscription-review-checkout-approved.pt-BR.md](./access-subscription-review-checkout-approved.pt-BR.md): contrato aprovado da imagem 74, revisao de assinatura antes do checkout externo.
- [access-subscription-pending-confirmation-approved.pt-BR.md](./access-subscription-pending-confirmation-approved.pt-BR.md): contrato aprovado da imagem 75, aguardando confirmacao automatica da assinatura antes de liberar onboarding.
- [access-subscription-resolution-approved.pt-BR.md](./access-subscription-resolution-approved.pt-BR.md): contrato aprovado da imagem 76, recuperacao de assinatura nao confirmada antes de liberar CRM/onboarding.
- [access-subscription-confirmed-setup-approved.pt-BR.md](./access-subscription-confirmed-setup-approved.pt-BR.md): contrato aprovado da imagem 77, assinatura confirmada e entrada no setup guiado pela Taliya.
- [subscription-to-onboarding-handoff-audit.pt-BR.md](./subscription-to-onboarding-handoff-audit.pt-BR.md): auditoria e contrato do handoff da imagem 77 para `/onboarding` e Setup Inicial 51A-51L.
- [onboarding-welcome-78-approved.pt-BR.md](./onboarding-welcome-78-approved.pt-BR.md): contrato aprovado da imagem 78, boas-vindas a Taliya e nome do studio antes dos blocos do setup.
- [onboarding-studio-block-v2-approved.pt-BR.md](./onboarding-studio-block-v2-approved.pt-BR.md): contrato aprovado da 51D v2, bloco Studio sem repetir nome do studio.
- [use-case-final-product-coverage-map.pt-BR.md](./use-case-final-product-coverage-map.pt-BR.md): remapeamento final dos 157 casos para paginas proprias, contextuais, topbar global e pos-MVP.
- [agents-flows-final-route-remap.pt-BR.md](./agents-flows-final-route-remap.pt-BR.md): remapeamento final das rotas citadas pelos 96 fluxos para a navegacao canonica atual.
- [agent-plan-entitlements.pt-BR.md](./agent-plan-entitlements.pt-BR.md): comportamento detalhado dos planos 0, 1, 3 e 7 agentes.
- [route-agent-mode-entitlement-matrix.pt-BR.md](./route-agent-mode-entitlement-matrix.pt-BR.md): matriz por superficie/rota, plano, agente e modo manual/copiloto/autonomo.
- [screen-ux-depth-contract.pt-BR.md](./screen-ux-depth-contract.pt-BR.md): estados, acoes, hierarquia visual e regras de UX por familia de tela.
- [technical-product-contracts.pt-BR.md](./technical-product-contracts.pt-BR.md): contratos de view model, acao, RBAC, billing, uso/cota e auditoria.
- [agent-guardrails-evals-contract.pt-BR.md](./agent-guardrails-evals-contract.pt-BR.md): guardrails, thresholds, preflight, ferramentas permitidas e evals.
- [final-screen-prompts-catalog.pt-BR.md](./final-screen-prompts-catalog.pt-BR.md): catalogo de prompts finais por superficie.
- [remaining-depth-backlog.pt-BR.md](./remaining-depth-backlog.pt-BR.md): registro do que foi fechado na profundidade e do que resta externo.
- [round-12-final-review.pt-BR.md](./round-12-final-review.pt-BR.md): revisao final de consistencia tecnica e de usuario apos o fechamento v0.1.
- [round-13-depth-closure.pt-BR.md](./round-13-depth-closure.pt-BR.md): fechamento da profundidade de planos, modos, UX, contratos, guardrails e prompts.
- [design-system-round-1-web-visual-dna-tokens.pt-BR.md](./design-system-round-1-web-visual-dna-tokens.pt-BR.md): documentacao da primeira prancha visual de design system web.
- [design-system-round-1-1-web-token-spec.pt-BR.md](./design-system-round-1-1-web-token-spec.pt-BR.md): especificacao precisa dos tokens da Rodada 1.
- [design-system-round-2b-web-app-shell.pt-BR.md](./design-system-round-2b-web-app-shell.pt-BR.md): contrato visual do App Shell Web aprovado a partir da Rodada 2A.2.
- [design-system-round-3a-web-reference-components.pt-BR.md](./design-system-round-3a-web-reference-components.pt-BR.md): biblioteca dos componentes web presentes na referencia e na tela Taliya 2A.2.
- [design-system-round-3b1-web-inputs-forms-filters.pt-BR.md](./design-system-round-3b1-web-inputs-forms-filters.pt-BR.md): biblioteca de inputs, formularios e filtros web aprovada na Rodada 3B.1.
- [design-system-round-3b-remaining-prompts.pt-BR.md](./design-system-round-3b-remaining-prompts.pt-BR.md): prompts e anexos das Rodadas 3B.2 a 3B.5.
- [design-system-round-3b2-web-overlays-feedback.pt-BR.md](./design-system-round-3b2-web-overlays-feedback.pt-BR.md): biblioteca de overlays, feedback e estados de sistema.
- [design-system-round-3b3-web-operational-views.pt-BR.md](./design-system-round-3b3-web-operational-views.pt-BR.md): biblioteca de visualizacoes operacionais web.
- [design-system-round-3b4-web-communication-agents.pt-BR.md](./design-system-round-3b4-web-communication-agents.pt-BR.md): biblioteca de comunicacao, WhatsApp, copiloto e agentes.
- [design-system-round-3b5-web-system-plan-governance.pt-BR.md](./design-system-round-3b5-web-system-plan-governance.pt-BR.md): biblioteca de sistema, plano, cotas e governanca.
- [design-system-component-coverage-audit.pt-BR.md](./design-system-component-coverage-audit.pt-BR.md): auditoria de cobertura dos componentes contra paginas, telas, fluxos e casos de uso.
- [design-system-round-3c1-web-objects-setup-data.pt-BR.md](./design-system-round-3c1-web-objects-setup-data.pt-BR.md): componentes compostos de objetos, setup, importacao, dados e perfis.
- [design-system-round-3c2-web-schedule-finance-documents.pt-BR.md](./design-system-round-3c2-web-schedule-finance-documents.pt-BR.md): componentes compostos de agenda, turmas, chamada, reposicoes, documentos e financeiro.
- [design-system-round-3c3-web-advanced-agents-audit-reports.pt-BR.md](./design-system-round-3c3-web-advanced-agents-audit-reports.pt-BR.md): componentes compostos de agentes avancados, auditoria, privacidade, relatorios e exportacoes.
- [design-system-route-functionality-coverage-post-3c.pt-BR.md](./design-system-route-functionality-coverage-post-3c.pt-BR.md): auditoria pos-3C de cobertura das rotas e funcionalidades web.
- [design-system-round-4-0-web-page-blueprints.pt-BR.md](./design-system-round-4-0-web-page-blueprints.pt-BR.md): blueprint de layout, zonas e componentes para todas as paginas web.
- [hoje-actionable-item-taxonomy.pt-BR.md](./hoje-actionable-item-taxonomy.pt-BR.md): taxonomia dos itens acionaveis da pagina Hoje, definindo o que e tarefa, aprovacao, bloqueio, fila humana, financeiro, origem canonica e quando cada item vira tarefa/caso/aprovacao.
- [drawer-lifecycle-contracts.pt-BR.md](./drawer-lifecycle-contracts.pt-BR.md): ciclos dos drawers acionaveis, com criacao, entrada no Hoje, resolucao, 0/1/3/7 agentes, manual, programatico, copiloto, autonomo e expansao futura para outras familias.
- [onboarding-setup-modes.pt-BR.md](./onboarding-setup-modes.pt-BR.md): decisao de setup unico guiado por agente, com chamada humana Taliya opcional sem mudar o fluxo.
- [setup-configuration-plan-100.pt-BR.md](./setup-configuration-plan-100.pt-BR.md): plano completo para fechar setup, configuracoes, agentes, cotas, publicacao e reconfiguracao.
- [setup-configuration-integrity-contract.pt-BR.md](./setup-configuration-integrity-contract.pt-BR.md): contrato de integridade para evitar duplicidade e conflito de regras.
- [setup-configuration-inventory.pt-BR.md](./setup-configuration-inventory.pt-BR.md): inventario das configuracoes do MVP por dominio e corte de complexidade.
- [setup-initial-configuration-scope.pt-BR.md](./setup-initial-configuration-scope.pt-BR.md): contrato de escopo do Setup Inicial, separando o minimo que o cliente configura antes do go-live do que vira default, pendencia ou configuracao pos-go-live.
- [setup-technical-configuration-contract.pt-BR.md](./setup-technical-configuration-contract.pt-BR.md): contrato tecnico/conceitual das regras de configuracao.
- [setup-source-of-truth-precedence.pt-BR.md](./setup-source-of-truth-precedence.pt-BR.md): ordem de precedencia para resolver conflitos entre regras.
- [setup-consumption-contract-crm-agents.pt-BR.md](./setup-consumption-contract-crm-agents.pt-BR.md): como CRM e agentes consomem configuracoes publicadas.
- [setup-agent-role.pt-BR.md](./setup-agent-role.pt-BR.md): papel exato do agente de setup, seus limites, relacao com humano Taliya e comportamento por plano.
- [setup-onboarding-question-map.pt-BR.md](./setup-onboarding-question-map.pt-BR.md): perguntas simples do setup e configuracoes geradas.
- [setup-diagnostico-page-contract.pt-BR.md](./setup-diagnostico-page-contract.pt-BR.md): contrato aprovado da pagina `/onboarding/diagnostico`, com uma pergunta por vez, 5 perguntas finais, opcoes exatas, resumo e papel do agente.
- [setup-adaptive-decision-tree.pt-BR.md](./setup-adaptive-decision-tree.pt-BR.md): arvore adaptativa do setup para 0/1/3/7 agentes, canais, financeiro e politicas.
- [setup-impact-matrix.pt-BR.md](./setup-impact-matrix.pt-BR.md): impacto das configuracoes em paginas, fluxos, agentes, cotas e auditoria.
- [setup-billing-class-consumption-models.pt-BR.md](./setup-billing-class-consumption-models.pt-BR.md): modelo de cobranca, consumo de aulas, reposicoes e quebra-galhos manuais/copiloto/agentes.
- [setup-partial-publishing-rules.pt-BR.md](./setup-partial-publishing-rules.pt-BR.md): regras para publicar CRM/areas/agentes parcialmente com seguranca.
- [setup-reconfiguration-rules.pt-BR.md](./setup-reconfiguration-rules.pt-BR.md): regras de mudanca pos-go-live com diff, simulacao, snapshot e rollback.
- [setup-conflict-tests.pt-BR.md](./setup-conflict-tests.pt-BR.md): suite funcional de conflitos esperados e resultado correto.
- [setup-scenario-tests.pt-BR.md](./setup-scenario-tests.pt-BR.md): cenarios reais de studios para validar setup e configuracoes.
- [setup-acceptance-criteria.pt-BR.md](./setup-acceptance-criteria.pt-BR.md): criterios de aceite para considerar a arquitetura pronta.
- [setup-screens-blueprint.pt-BR.md](./setup-screens-blueprint.pt-BR.md): blueprint das telas de onboarding/configuracoes e control planes.
- [setup-reusable-visual-assets-map.pt-BR.md](./setup-reusable-visual-assets-map.pt-BR.md): mapa dos assets visuais reutilizaveis do onboarding antes de gerar as paginas finais.
- [setup-reusable-visual-assets-prompts.pt-BR.md](./setup-reusable-visual-assets-prompts.pt-BR.md): prompts completos e mapa de anexos para gerar os assets reutilizaveis no ChatGPT/Gemini.
- [setup-51A-shell-base-approved.pt-BR.md](./setup-51A-shell-base-approved.pt-BR.md): decisao aprovada do 51A como shell global do onboarding, com centro neutro, stepper, chat lateral e rodape.
- [setup-51B-agent-chat-approved.pt-BR.md](./setup-51B-agent-chat-approved.pt-BR.md): decisao aprovada do 51B como chat lateral contextual do agente de configuracao no setup inicial.
- [setup-51C-configuration-workspace-approved.pt-BR.md](./setup-51C-configuration-workspace-approved.pt-BR.md): decisao aprovada do 51C como area central de configuracao guiada, usando Consumo de aulas como exemplo visual.
- [setup-51C-configuration-workspace-standalone-prompt.pt-BR.md](./setup-51C-configuration-workspace-standalone-prompt.pt-BR.md): prompt standalone do 51C, area central de configuracao guiada dentro do shell.
- [setup-image-plan.pt-BR.md](./setup-image-plan.pt-BR.md): plano das imagens 4.1J necessarias e rotas que herdam padroes.
- [setup-and-post-go-live-pages-images-review.pt-BR.md](./setup-and-post-go-live-pages-images-review.pt-BR.md): revisao consolidada das paginas e imagens do setup inicial, configuracoes pos-go-live, agentes/fluxos e control planes.
- [setup-final-audit.pt-BR.md](./setup-final-audit.pt-BR.md): auditoria final v0.1 da arquitetura de setup/configuracoes.

## Design System Web

- [design-system-round-1-web-visual-dna-tokens.pt-BR.md](./design-system-round-1-web-visual-dna-tokens.pt-BR.md): Rodada 1, DNA visual e tokens base.
- [design-system-round-1-1-web-token-spec.pt-BR.md](./design-system-round-1-1-web-token-spec.pt-BR.md): Rodada 1.1, tokens refinados para guiar as proximas imagens.
- [design-system-round-2b-web-app-shell.pt-BR.md](./design-system-round-2b-web-app-shell.pt-BR.md): Rodada 2B, App Shell Web, estrutura visual base para as proximas telas.
- [design-system-round-3a-web-reference-components.pt-BR.md](./design-system-round-3a-web-reference-components.pt-BR.md): Rodada 3A, componentes web ja presentes na referencia.
- [design-system-round-3b1-web-inputs-forms-filters.pt-BR.md](./design-system-round-3b1-web-inputs-forms-filters.pt-BR.md): Rodada 3B.1, inputs, formularios e filtros.
- [design-system-round-3b-remaining-prompts.pt-BR.md](./design-system-round-3b-remaining-prompts.pt-BR.md): prompts para gerar as Rodadas 3B restantes.
- [design-system-round-3b2-web-overlays-feedback.pt-BR.md](./design-system-round-3b2-web-overlays-feedback.pt-BR.md): Rodada 3B.2, overlays e feedback.
- [design-system-round-3b3-web-operational-views.pt-BR.md](./design-system-round-3b3-web-operational-views.pt-BR.md): Rodada 3B.3, visualizacoes operacionais.
- [design-system-round-3b4-web-communication-agents.pt-BR.md](./design-system-round-3b4-web-communication-agents.pt-BR.md): Rodada 3B.4, comunicacao e agentes.
- [design-system-round-3b5-web-system-plan-governance.pt-BR.md](./design-system-round-3b5-web-system-plan-governance.pt-BR.md): Rodada 3B.5, sistema, plano e governanca.
- [design-system-component-coverage-audit.pt-BR.md](./design-system-component-coverage-audit.pt-BR.md): auditoria cruzada de cobertura dos componentes.
- [design-system-round-3c1-web-objects-setup-data.pt-BR.md](./design-system-round-3c1-web-objects-setup-data.pt-BR.md): Rodada 3C.1, objetos, setup e dados.
- [design-system-round-3c2-web-schedule-finance-documents.pt-BR.md](./design-system-round-3c2-web-schedule-finance-documents.pt-BR.md): Rodada 3C.2, agenda, financeiro e documentos.
- [design-system-round-3c3-web-advanced-agents-audit-reports.pt-BR.md](./design-system-round-3c3-web-advanced-agents-audit-reports.pt-BR.md): Rodada 3C.3, agentes avancados, auditoria e relatorios.
- [design-system-route-functionality-coverage-post-3c.pt-BR.md](./design-system-route-functionality-coverage-post-3c.pt-BR.md): auditoria final de cobertura web para seguir a paginas por familia.
- [design-system-round-4-0-web-page-blueprints.pt-BR.md](./design-system-round-4-0-web-page-blueprints.pt-BR.md): Rodada 4.0, blueprint de todas as paginas web.
- [design-system-round-4-0-blueprint-audit.pt-BR.md](./design-system-round-4-0-blueprint-audit.pt-BR.md): auditoria tecnica e de usuario da Rodada 4.0.
- [design-system-round-4-image-coverage-strategy.pt-BR.md](./design-system-round-4-image-coverage-strategy.pt-BR.md): estrategia para decidir quais rotas precisam imagem propria e quais herdam padroes aprovados.
- [design-system-round-4-1S-web-app-shell-approved.pt-BR.md](./design-system-round-4-1S-web-app-shell-approved.pt-BR.md): Rodada 4.1S, App Shell web aprovado e regras de navegacao.
- [design-system-round-4-1A-hoje-image-plan.pt-BR.md](./design-system-round-4-1A-hoje-image-plan.pt-BR.md): Rodada 4.1A, plano de imagens e fronteiras da pagina Hoje.
- [design-system-round-4-1A-hoje-02-drawer-tarefa-approved.pt-BR.md](./design-system-round-4-1A-hoje-02-drawer-tarefa-approved.pt-BR.md): Rodada 4.1A, imagem 02 aprovada da pagina Hoje com drawer de tarefa.
- [design-system-round-4-1A-hoje-03-estado-critico-approved.pt-BR.md](./design-system-round-4-1A-hoje-03-estado-critico-approved.pt-BR.md): Rodada 4.1A, imagem 03 aprovada da pagina Hoje em estado critico.
- [design-system-round-4-1A-hoje-04-historico-approved.pt-BR.md](./design-system-round-4-1A-hoje-04-historico-approved.pt-BR.md): Rodada 4.1A, imagem 04 aprovada da pagina Hoje com historico abaixo da dobra.
- [design-system-round-4-1A-hoje-final-audit.pt-BR.md](./design-system-round-4-1A-hoje-final-audit.pt-BR.md): auditoria final v0.1 da familia Hoje web.
- [design-system-round-4-1B-operacao-jornadas-image-plan.pt-BR.md](./design-system-round-4-1B-operacao-jornadas-image-plan.pt-BR.md): Rodada 4.1B, plano de imagens e contrato visual-funcional da familia Operacao/Jornadas.
- [design-system-round-4-1B-operacao-final-audit.pt-BR.md](./design-system-round-4-1B-operacao-final-audit.pt-BR.md): auditoria final da pagina Operacao web apos imagens 21 e 22 aprovadas.
- [design-system-round-4-1C-tarefas-image-plan.pt-BR.md](./design-system-round-4-1C-tarefas-image-plan.pt-BR.md): Rodada 4.1C, pagina Tarefas aprovada com lista densa e drawer compartilhado de Tarefa.
- [design-system-round-4-1C-checklists-approved.pt-BR.md](./design-system-round-4-1C-checklists-approved.pt-BR.md): Rodada 4.1C, pagina Checklists aprovada com execucoes de rotinas e detalhe lateral.
- [design-system-round-4-1C-aprovacoes-approved.pt-BR.md](./design-system-round-4-1C-aprovacoes-approved.pt-BR.md): Rodada 4.1C, pagina Aprovacoes aprovada com lista de decisoes e detalhe lateral auditavel.
- [design-system-round-4-1C-tarefas-checklists-aprovacoes-final-audit.pt-BR.md](./design-system-round-4-1C-tarefas-checklists-aprovacoes-final-audit.pt-BR.md): auditoria final da familia Tarefas, Checklists e Aprovacoes.
- [design-system-round-4-1D-inbox-image-plan.pt-BR.md](./design-system-round-4-1D-inbox-image-plan.pt-BR.md): Rodada 4.1D, pagina Inbox aprovada com conversa aberta, lista de atendimento, contexto lateral e variacoes por autonomia.
- [design-system-round-4-1D-atendimento-inbox-final-audit.pt-BR.md](./design-system-round-4-1D-atendimento-inbox-final-audit.pt-BR.md): auditoria final da parte Atendimento/InBox, incluindo rotas herdadas, envios e simplificacao de contatos.
- [alunos-scope-decision.pt-BR.md](./alunos-scope-decision.pt-BR.md): decisao de escopo removendo responsaveis/familia e consentimentos como modulos proprios da familia Alunos.
- [design-system-round-4-1E-alunos-lista-approved.pt-BR.md](./design-system-round-4-1E-alunos-lista-approved.pt-BR.md): Rodada 4.1E, pagina Alunos aprovada com lista operacional e resumo lateral acionavel.
- [design-system-round-4-1E-aluno-perfil-approved.pt-BR.md](./design-system-round-4-1E-aluno-perfil-approved.pt-BR.md): Rodada 4.1E, perfil completo do aluno aprovado com aba Resumo operacional.
- [design-system-round-4-1E-alunos-final-audit.pt-BR.md](./design-system-round-4-1E-alunos-final-audit.pt-BR.md): auditoria final da familia Alunos web.
- [hoje-actionable-item-taxonomy.pt-BR.md](./hoje-actionable-item-taxonomy.pt-BR.md): regra funcional da pagina Hoje: origens canonicas, diferenca entre tarefa/aprovacao/bloqueio/fila humana/financeiro e comportamento do drawer.
- [drawer-lifecycle-contracts.pt-BR.md](./drawer-lifecycle-contracts.pt-BR.md): contrato extensivel de ciclos dos drawers, incluindo planos 0/1/3/7 agentes e modos manual/programatico/copiloto/autonomo.

## Rodada 0 - Contratos Globais

- [round-0-foundation-audit.pt-BR.md](./round-0-foundation-audit.pt-BR.md): mini-auditoria da Rodada 0 e criterios para seguir.
- [functional-architecture.pt-BR.md](./functional-architecture.pt-BR.md): esqueleto canonico de arquitetura funcional por area.
- [screen-specs-detailed.pt-BR.md](./screen-specs-detailed.pt-BR.md): esqueleto canonico de especificacao profunda tela por tela.
- [open-product-decisions.pt-BR.md](./open-product-decisions.pt-BR.md): decisoes D001-D037, impacto e status fechado v0.1.
- [canonical-data-model.pt-BR.md](./canonical-data-model.pt-BR.md): objetos canonicos do CRM.
- [object-lifecycle-map.pt-BR.md](./object-lifecycle-map.pt-BR.md): ciclos de vida dos objetos criticos.
- [source-of-truth-matrix.pt-BR.md](./source-of-truth-matrix.pt-BR.md): fonte da verdade e regras de conflito de dados.
- [technical-integrations-master-map.pt-BR.md](./technical-integrations-master-map.pt-BR.md): mapa geral das integracoes tecnicas do CRM, separando WhatsApp, pagamentos, Google Agenda, e-mail e importacoes das configuracoes comuns.
- [technical-integrations-detailed-contract.pt-BR.md](./technical-integrations-detailed-contract.pt-BR.md): contrato detalhado de funcionamento das integracoes tecnicas do MVP e pos-go-live.
- [billing-taliya-master-map.pt-BR.md](./billing-taliya-master-map.pt-BR.md): mapa mestre de Billing Taliya, separando assinatura do studio com a Taliya do financeiro dos alunos e de Pagamentos Taliya.
- [control-planes-master-map.pt-BR.md](./control-planes-master-map.pt-BR.md): mapa mestre dos Control Planes, separando execucoes, incidentes, uso/cotas, auditoria e logs de integracao das configuracoes e dos builders de agente.
- [permissions-matrix.pt-BR.md](./permissions-matrix.pt-BR.md): papeis, permissoes contextuais e acoes sensiveis.
- [action-button-taxonomy.pt-BR.md](./action-button-taxonomy.pt-BR.md): padrao de botoes, verbos e confirmacoes.
- [ui-state-taxonomy.pt-BR.md](./ui-state-taxonomy.pt-BR.md): estados globais, bloqueios e estados por objeto.
- [quota-touchpoints.pt-BR.md](./quota-touchpoints.pt-BR.md): pontos de cota, limites, economia e fallback manual.
- [audit-touchpoints.pt-BR.md](./audit-touchpoints.pt-BR.md): eventos obrigatorios de auditoria.
- [operational-policy-versioning.pt-BR.md](./operational-policy-versioning.pt-BR.md): politicas operacionais versionadas.
- [integration-failure-contracts.pt-BR.md](./integration-failure-contracts.pt-BR.md): contratos de falha de integracoes.
- [zero-agent-operating-model.pt-BR.md](./zero-agent-operating-model.pt-BR.md): operacao completa no plano Base com 0 agentes.
- [agent-quality-evaluation.pt-BR.md](./agent-quality-evaluation.pt-BR.md): qualidade, erro, correcao e confianca dos agentes.
- [migration-import-plan.pt-BR.md](./migration-import-plan.pt-BR.md): migracao e importacao inicial de studios reais.
- [taliya-internal-ops.pt-BR.md](./taliya-internal-ops.pt-BR.md): registro historico da separacao entre CRM dos studios e operacao interna da Taliya.
- [taliya-internal-backoffice-contract.pt-BR.md](./taliya-internal-backoffice-contract.pt-BR.md): contrato completo do backoffice interno `/internal/*`, com leads da Taliya, tenants, usuarios, suporte, grants, incidentes, billing, entitlements, auditoria e imagens 48/49/50 aprovadas.
- [product-success-metrics.pt-BR.md](./product-success-metrics.pt-BR.md): metricas de valor para gestor e para Taliya.
- [notification-template-governance.pt-BR.md](./notification-template-governance.pt-BR.md): mensagens, templates, consentimento e notificacoes.

## Rodada 1 - Ativacao, Setup E Configuracao Essencial

- [round-1-activation-setup-spec.pt-BR.md](./round-1-activation-setup-spec.pt-BR.md): arquitetura funcional e especificacao v0.1 de onboarding, configuracoes essenciais, agentes iniciais, cotas iniciais e qualidade de dados.

## Rodada 2 - Operacao Diaria E Mesa De Comando

- [round-2-daily-command-spec.pt-BR.md](./round-2-daily-command-spec.pt-BR.md): arquitetura funcional e especificacao v0.1 de Hoje, Jornadas/Operacao, Tarefas, Aprovacoes, Notificacoes, Checklist, Caso operacional e Jornadas prioritarias.

## Rodada 3 - Atendimento, Alunos, Historico E Professor

- [round-3-attendance-students-history-spec.pt-BR.md](./round-3-attendance-students-history-spec.pt-BR.md): arquitetura funcional e especificacao v0.2 de Inbox, Conversas, Contatos, Alunos, Historico permitido, Professor e Falhas de envio, sem modulo proprio de responsaveis/familia no MVP.

## Rodada 4 - Agenda, Turmas, Aulas E Reposicoes

- [round-4-schedule-classes-replacements-spec.pt-BR.md](./round-4-schedule-classes-replacements-spec.pt-BR.md): arquitetura funcional e especificacao v0.1 de Agenda, Turmas, Aula, Chamada, Reposicoes, Lista de espera, Eventos/workshops e Recursos/disponibilidade.
- [design-system-round-4-1F-agenda-image-plan.pt-BR.md](./design-system-round-4-1F-agenda-image-plan.pt-BR.md): Rodada 4.1F, paginas Agenda, Turmas, Grade, Aula e Reposicoes aprovadas com calendario operacional, estrutura recorrente, detalhe de aula, drawer de chamada e fluxo de encaixe.
- [design-system-round-4-1F-agenda-final-audit.pt-BR.md](./design-system-round-4-1F-agenda-final-audit.pt-BR.md): auditoria final da familia Agenda/Turmas/Grade/Aula/Reposicoes, com cobertura de rotas, herancas, bloqueios situacionais e mobile futuro.

## Rodada 5 - Vendas, Experimental E Matricula

- [round-5-sales-trials-enrollment-communications-spec.pt-BR.md](./round-5-sales-trials-enrollment-communications-spec.pt-BR.md): arquitetura funcional e especificacao v0.1 de Interessados, Vendas, Aulas experimentais e Matriculas. Comunicados ficam para agente/superficie separada pos-MVP.
- [design-system-round-4-1G-vendas-image-plan.pt-BR.md](./design-system-round-4-1G-vendas-image-plan.pt-BR.md): Rodada 4.1G, plano visual de Vendas/Interessados com Pipeline, Lista, Experimental e Matriculas.
- [design-system-round-4-1I-relatorios-gestao-image-plan.pt-BR.md](./design-system-round-4-1I-relatorios-gestao-image-plan.pt-BR.md): Rodada 4.1I, plano visual de Relatorios/Gestao sem criar rota `/app/gestao`, com foco em decisoes acionaveis.
- [relatorios-gestao-data-contract.pt-BR.md](./relatorios-gestao-data-contract.pt-BR.md): contrato de dados para gerar conteudo de Relatorios/Gestao no MVP, com fonte, regra, acao, destino e itens pos-MVP.
- [admin-auditoria-integracoes-billing-contract.pt-BR.md](./admin-auditoria-integracoes-billing-contract.pt-BR.md): contrato simples para Admin, Auditoria, Integracoes, Suporte completo com imagem 47 aprovada, Privacidade e Billing sem criar familia visual grande no MVP.

## Rodada 6 - Financeiro, Contratos, Retencao E Casos Sensiveis

- [round-6-finance-retention-sensitive-spec.pt-BR.md](./round-6-finance-retention-sensitive-spec.pt-BR.md): arquitetura funcional e especificacao v0.2 de Financeiro, Kanban, Movimentacoes, excecoes financeiras sem pagina propria no MVP, Contratos, Retencao, Cancelamentos, Reclamacoes e Privacidade.
- [design-system-round-4-1F-financeiro-image-plan.pt-BR.md](./design-system-round-4-1F-financeiro-image-plan.pt-BR.md): Rodada 4.1F, Financeiro web com Visao geral, Kanban, Movimentacoes e Documentos herdado.
- [design-system-round-4-1F-financeiro-final-audit.pt-BR.md](./design-system-round-4-1F-financeiro-final-audit.pt-BR.md): auditoria final da familia Financeiro web, incluindo topbar final e decisao de nao criar Casos financeiros no MVP.
- [design-system-round-4-1H-retencao-image-plan.pt-BR.md](./design-system-round-4-1H-retencao-image-plan.pt-BR.md): Rodada 4.1H, imagens aprovadas de Retencao/Riscos, Cancelamentos, Reativacoes e Reclamacoes.
- [design-system-round-4-1H-retencao-final-audit.pt-BR.md](./design-system-round-4-1H-retencao-final-audit.pt-BR.md): auditoria final da familia Retencao/Cancelamentos/Reativacoes/Reclamacoes, com rotas finais, decisoes de MVP e regras para manual/copiloto/autonomo.

## Rodada 7 - Agentes, Cotas, Relatorios E Governanca

- [round-7-agents-quotas-governance-spec.pt-BR.md](./round-7-agents-quotas-governance-spec.pt-BR.md): arquitetura funcional e especificacao v0.1 de Agentes, Fluxos, Execucoes, Incidentes, Cotas, Relatorios, Politicas, Integracoes, Auditoria, Billing e Suporte interno Taliya.

## Rodada 8 - Cobertura Cruzada

- [round-8-cross-coverage-audit.pt-BR.md](./round-8-cross-coverage-audit.pt-BR.md): auditoria v0.1 cruzando Rodadas 1-7 com rotas, casos, fluxos, cotas, auditoria, permissoes e operacao sem agentes.
- [route-screen-coverage.pt-BR.csv](./route-screen-coverage.pt-BR.csv): cobertura resumida de rotas/telas por area.
- [use-case-to-screen-coverage.pt-BR.csv](./use-case-to-screen-coverage.pt-BR.csv): ponte entre casos de uso e fontes de cobertura.
- [agent-flow-screen-coverage.pt-BR.csv](./agent-flow-screen-coverage.pt-BR.csv): cobertura dos fluxos de agentes por familia e fonte.

## Rodada 9 - Simulacoes E Fechamento

- [round-9-user-simulations.pt-BR.md](./round-9-user-simulations.pt-BR.md): simulacoes obrigatorias do produto em manual, copiloto, autonomo e 0 agentes.
- [final-consistency-audit.pt-BR.md](./final-consistency-audit.pt-BR.md): auditoria final v0.1 de consistencia e pendencias conscientes.
- [final-product-decisions.pt-BR.md](./final-product-decisions.pt-BR.md): decisoes assumidas e fechamento funcional v0.1.

## Rodada 10 - Revisao Tecnica E Usuario

- [round-10-technical-user-audit.pt-BR.md](./round-10-technical-user-audit.pt-BR.md): auditoria das Rodadas 0-9 por contrato tecnico e por simulacao de gestor usando o sistema.

## Rodada 11 - Fechamento Funcional

- [round-11-product-closure.pt-BR.md](./round-11-product-closure.pt-BR.md): decisoes D001-D037 fechadas v0.1.
- [studio-operational-presets.pt-BR.md](./studio-operational-presets.pt-BR.md): presets de setup para reduzir friccao do gestor.
- [final-navigation-web-app.pt-BR.md](./final-navigation-web-app.pt-BR.md): menu web, abas app, busca global e regra do Mais.
- [final-screen-contract-matrix.pt-BR.md](./final-screen-contract-matrix.pt-BR.md): contrato final para gerar telas sem inventar produto.
- [agent-plan-entitlements.pt-BR.md](./agent-plan-entitlements.pt-BR.md): entitlements por plano e comportamento com 0/1/3/7 agentes.
- [route-agent-mode-entitlement-matrix.pt-BR.md](./route-agent-mode-entitlement-matrix.pt-BR.md): comportamento por superficie em 0/1/3/7 agentes e modos.
- [screen-ux-depth-contract.pt-BR.md](./screen-ux-depth-contract.pt-BR.md): contrato final de estados, acoes e UX.
- [technical-product-contracts.pt-BR.md](./technical-product-contracts.pt-BR.md): contratos tecnicos de implementacao.
- [agent-guardrails-evals-contract.pt-BR.md](./agent-guardrails-evals-contract.pt-BR.md): seguranca e qualidade de agentes.
- [final-screen-prompts-catalog.pt-BR.md](./final-screen-prompts-catalog.pt-BR.md): prompts finais por superficie.
- [remaining-depth-backlog.pt-BR.md](./remaining-depth-backlog.pt-BR.md): registro do que foi fechado e do que resta externo.

## Rodada 12 - Revisao Final

- [round-12-final-review.pt-BR.md](./round-12-final-review.pt-BR.md): auditoria final de links, contagens, matriz, decisoes, visao tecnica e visao de gestor.

## Rodada 13 - Fechamento De Profundidade

- [round-13-depth-closure.pt-BR.md](./round-13-depth-closure.pt-BR.md): consolidacao final dos contratos de profundidade.

## Documentos De Apoio

- [visual-mapping-toolkit.md](./visual-mapping-toolkit.md): toolkit com 40 formas de visualizar o produto.
- [journey-metro-map.md](./journey-metro-map.md): mapa metro das jornadas.
- [object-action-map.md](./object-action-map.md): objetos do CRM e acoes/botoes.
- [execution-swimlanes.md](./execution-swimlanes.md): raias de execucao humano/sistema/IA/WhatsApp/auditoria.
- [use-case-execution-matrix.md](./use-case-execution-matrix.md): matriz compacta de execucao para os 157 casos.

## Regra De Uso

O conjunto esta fechado como premissa funcional v0.1 para gerar telas e prompts. Se uma premissa se provar errada, abrir nova decisao e revisar o impacto.

Use a tabela mestre v2 para decidir:

- prioridade;
- decisao;
- tipo de rota;
- risco;
- profundidade mobile;
- se vira tela, botao, painel lateral, automacao ou configuracao.
