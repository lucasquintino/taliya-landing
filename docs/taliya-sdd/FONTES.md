# Fontes e autoridade

Consulta em 2026-09-28. Propostas de arquitetura, metas e estimativas são identificadas como propostas; fontes não comprovam implantação.

## L1 — Código original anexado
taliya-landing-main.zip

Inspeção estática de cópia isolada; SHA-256 f37abaa6ebbdd4bf44e277bc09c944e3889490a41233c945c02b6c9069ed9aab.

## L2 — Pacote anterior
Taliya_Agente_Comercial_v2_Luna_Max.zip

27 arquivos; contratos e propostas, não integração executada. SHA-256 9467dbb9b8c9d05a5e6a49b602e60b5b419b72f712d066c0cf0d811b8b7168a2.

## L3 — Decisões diretas da conversa
Conversa atual

App e assinatura prontos; Agents API; Luna max; PostHog + Internal mínimo; SDD/Spec Kit; materiais compartilhados; simplicidade.

## L4 — Plano de assinatura recuperado
Plano_Assinatura_Taliya_Asaas_v2.md

Política: Asaas, mensal/anual, cartão recorrente/Pix Automático, cobrança na contratação e garantia de 14 dias. Documento de plano não comprova produção; a atualização do usuário prevalece para prontidão.

## L5 — Prompt SDD anterior recuperado
PROMPT_Taliya_Copiloto_Landing_SDD_v2.md

Preservação visual; uma spec por seção na migração de conteúdo. O programa atual acrescenta capacidades transversais sem reexecutar 17 seções.

## O1 — Modelo GPT-6 Luna
https://developers.openai.com/api/docs/models/gpt-6-luna

Modelo e esforço max documentados; compatibilidade integral precisa de smoke test na conta.

## O2 — Agents API — arquitetura
https://developers.openai.com/api/docs/guides/agents-api/architecture

Execução gerenciada, ambiente none, ferramentas do backend.

## O3 — Agents API — configuração
https://developers.openai.com/api/docs/guides/agents-api/configuration

Configuração salva é copiada na criação das sessões.

## O4 — Agents API — funções
https://developers.openai.com/api/docs/guides/agents-api/tools/functions

required_actions e devolução de resultados; handler continua na aplicação.

## O5 — Agents API — eventos
https://developers.openai.com/api/docs/guides/agents-api/sessions/events

Streams não reexecutam eventos perdidos; recuperar itens persistidos.

## O6 — Agents API — dados e visão geral
https://developers.openai.com/api/docs/guides/agents-api/overview

Estado retido; residência somente EUA e ausência de ZDR na documentação consultada.

## P1 — PostHog — preços
https://posthog.com/pricing

Franquia analytics 1M/mês, free com 1 projeto, limites por produto e descarte após teto. Sem garantia de custo futuro.

## P2 — PostHog — Next.js
https://posthog.com/docs/libraries/next-js

Identificação estável, eventos cliente/servidor e reset no logout.

## P3 — PostHog — otimização de custos
https://posthog.com/handbook/cs-and-onboarding/cost-optimization

Controlar autocapture, identify/group repetidos e gravações.

## P4 — PostHog — Group Analytics
https://github.com/PostHog/posthog.com/blob/master/contents/docs/product-analytics/group-analytics.mdx

Adicional a avaliar; não condição para a identidade de negócio no backend.

## P5 — PostHog — receita
https://posthog.com/docs/revenue-analytics

Dashboard dedicado removido; configurar insights/SQL/views para o modelo da Taliya.

## P6 — PostHog — Postgres
https://posthog.com/docs/data-warehouse/sources/postgres

Integração seletiva. CDC implica permissões extras; não presumir que basta SELECT.

## P7 — PostHog — Workflows
https://posthog.com/workflows

Fluxos e integrações; nenhuma transferência de autoridade financeira.

## P8 — PostHog — envio
https://posthog.com/docs/workflows/sending-reputation

Limites de envio e reputação. Franquia mensal não garante capacidade imediata de envio.

## K1 — Spec Kit — fluxo de comandos
https://github.github.com/spec-kit/reference/agentic-sdd.html

Specify/clarify/plan/checklist/tasks/analyze/implement/converge; forma da invocação depende da integração.

## K2 — Spec Kit — evolução de projetos
https://github.github.com/spec-kit/guides/evolving-specs.html

Distinguir atualizar ferramenta de evoluir specs; preservar artefatos e customizações.

## K3 — Spec Kit — instalação
https://github.github.com/spec-kit/installation.html

Fixar versão; variantes de scripts; não forçar refresh sobre trabalho local.

## S1 — OWASP — autenticação
https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html

Referência para revisão de identidade e sessões do Internal.

## S2 — W3C — WCAG 2.2
https://www.w3.org/TR/WCAG22/

Referência de acessibilidade; adoção como alvo de QA, não certificação.

## S3 — Web.dev — métricas web
https://web.dev/articles/defining-core-web-vitals-thresholds

Metas de LCP, INP e CLS precisam de medição de campo; laboratório não a substitui.

## S4 — ANPD — guia de cookies
https://www.gov.br/anpd/pt-br/centrais-de-conteudo/materiais-educativos-e-publicacoes/guia-orientativo-cookies-e-protecao-de-dados-pessoais.pdf

Referência oficial para revisão de cookies e privacidade; este pacote não é parecer jurídico.
