# Contratos observados — 013 / 2026-09-28

Observação de código, não homologação remota. Nenhum payload abaixo foi enviado.
Correção de autoridade em 2026-09-29: o usuário confirmou que ainda não há
pagamento nem Asaas. As menções abaixo a serviço publicado não localizado registram
a hipótese histórica de busca, agora refutada. Ver `../DECISAO_BILLING_2026-09-29.md`.
Valores entre `<...>` são marcadores sanitizados, não IDs reais nem fixtures de produção.
Responsável técnico nesta inspeção: Codex. Donos humanos de serviços: não nomeados;
Lucas fornece decisão de produto e referência da oferta. Validar responsáveis antes de G0.

## Fontes e versões

| Componente | Fonte e revisão | Situação |
|---|---|---|
| Landing / agente Python / Sales Inbox local | lucasquintino/taliya-landing; /Users/lucasquintino/Projects/taliya-copiloto-landing; HEAD 862095261a617a4a1a73c1ab96a914a9249c63ec | Branch inicial main, 4 arquivos alterados/4 novos de SEO preservados; hook criou 015-fundacao-e-contratos; spec ativa 013 |
| Internal independente | lucasquintino/taliya-internal main; 7cbe9e9b92a4d3b18b3961ab51f9eec10515b38e | Clone somente leitura /tmp/taliya-foundation-sources/internal; status limpo |
| App Copiloto | lucasquintino/copiloto main; d99ef897f3033ace6a23ee009e2578ffc04a259d | Clone somente leitura /tmp/taliya-foundation-sources/copiloto |
| App executável local | /Users/lucasquintino/Downloads/copiloto-github; mesmo SHA; branch codex/e02-icloud-recovery-20260928 | Alterações locais de onboarding/docs/testes e capturas preservadas; ver repository-sources.json |
| App no Documents | /Users/lucasquintino/Documents/ChatGPT/copiloto | HEAD aponta codex/e02-icloud-recovery-20260928; AGENTS/index dataless; não equiparar ao clone remoto |
| Cópia antiga landing no Documents | Documents/Codex/2026-09-24/vamos-continuar-a-migra-o-da/outputs/taliya-copiloto-landing | AGENTS dataless, leitura bloqueada; não usada como alvo |
| Billing Asaas | Inexistente conforme correção do usuário em 2026-09-29 | Construir na spec de oferta/billing; nenhuma operação financeira executada |

### Rechecagem de T013-01/02/07 — 2026-09-28

Uma cópia adicional encontrada em `Projects/taliya-copiloto-landing-incomplete-2026-09-28`
contém `specs/003-billing-subscriptions-entitlements/` e um contrato textual antigo,
mas não tem metadata `.git`, caminhos `app/api/billing/*` ou `lib/billing/*`. A spec
descreve interfaces e exemplos planejados; o checkout de exemplo é placeholder.
Ela declara Asaas, apenas cartão recorrente preferencial/Pix condicionado, anual
oculto até configuração e garantia de 30 dias. Não prova serviço publicado nem
configuração vigente e diverge da decisão atual (mensal/anual, Pix Automático,
garantia de 14 dias, cobrança na contratação). O `AGENTS.md` daquela cópia também a
identifica como recorte independente de migração, sem relação com deployment.

O repositório ativo e o checkout de trabalho do app Copiloto não expõem os handlers
de billing procurados. No app há Auth, negócio e decisão de entitlement. A correção
do usuário confirma que a ausência é de implementação, não apenas de localização.
Evidência e limites da busca histórica: `../evidence/billing-source-search.json`.

O código ativo da landing preserva alguns dados comerciais divergentes: por exemplo,
`data/landing/niches/pilates.ts` contém copy de 14 dias sem cobrança e
`product-knowledge-source.ts`/`commercial-state.ts` mencionam garantia de 30 dias.
São achados atuais, não regras aprovadas; corrigir junto da fonte de oferta confirmada,
na spec 015/018. Não alterar por preço estimado nem copiar os valores da spec antiga.

## Identidade, conta, negócio e acesso — Copiloto

Fontes: `supabase/functions/_shared/http.ts:78`, `business-context.ts`, `authorize.ts`,
`supabase/migrations/20260922142218_e01_identity_access.sql`, `20260922142222_e01_access_policy.sql`.

- `createUserClient` requer Authorization Bearer e encaminha token ao Supabase/RPC.
  Validação e escopo dependem de Auth/RLS/RPC, não de e-mail/telefone declarado.
- RPC existente `e01_resolve_business()` determina negócio no servidor; ausência vira
  `409 business_context_unavailable`. Vínculo `business_members`: `business_id`, `user_id`,
  `role=owner`, `status=active|revoked`. IDs UUID; usuário vem de `auth.users`.
- RPC `e01_access_decision(p_business_id,p_capability)` retorna decisão; gate aceita
  somente `decision=allowed`, caso contrário `403 operation_denied`.
- `access_entitlements`: `business_id`, `source`, `source_reference`, `state`
  (`trial|active|expired|revoked`), `starts_at`, `ends_at`, `version`; unique por
  negócio/fonte/referência. Não é prova de integração Asaas.
- `supabase/functions/queries/index.ts` expõe handler POST da função `queries`;
  host/base publicada não homologados. Input observado:
  `{query_id:<uuid>,correlation_id:<uuid>,query_type:client.list,payload:{schema_version:1,limit:20}}`.
  Output `{query_id,correlation_id,status:succeeded,data,errors:[]}`.
  Erros: 400 validação/unsupported_query, 401 authentication_required,
  409 business_context_unavailable, 403 operation_denied nas operações gated.
- `supabase/functions/commands/index.ts:871` valida envelope e delega a RPCs,
  incluindo `business.activate_onboarding`, presets e clientes. Reusar recibos e
  versionamento existentes; clientes do prestador NÃO são contatos comerciais Taliya.
- Divergência material: `20260926040100_e02_onboarding_command.sql:199` cria trial
  de 14 dias. Isso não confirma oferta paga/garantia do produto informado. Não
  alterar o app nem anunciar esse trial; obter referência do billing vigente.
- Não foi encontrada interface publicada de vinculação contato comercial→pessoa,
  oferta, checkout, assinatura Asaas ou webhooks financeiros neste clone.

## Oferta, contratação, assinatura e eventos financeiros

| Contrato exigido | Estado / próximo dado necessário |
|---|---|
| Oferta pública com versão/preço mensal/anual/garantia/URLs | A CONSTRUIR na 015: valores documentados R$ 59,90/R$ 599, vigência em confirmação; sem URL publicada |
| Iniciar/retomar checkout sem chat | A CONSTRUIR na 015: cartão hospedado/Pix Automático, auth, idempotência, payload/erros e retorno canônico |
| Assinatura/status/acesso autenticado | Gate de acesso Copiloto observado; ligação com fatos Asaas será implementada na 015 |
| Gestão/cancelamento/reembolso | A CONSTRUIR na 015; nenhuma operação financeira realizada |
| Confirmação/renovação/falha/cancelamento/reembolso | A CONSTRUIR na 015: webhook autenticado, event_id/ordenação/replay e reconciliação |

Busca: arquivos locais landing/Copiloto e árvore remota `agentes-landing-system/master`
contêm specs de billing, mas não handler identificado de Asaas/checkout. `taliya-product-ui`
é referência visual; não assumir backend pelo nome. Fonte necessária foi solicitada ao usuário.
Nenhuma rota desta tabela é apresentada como publicada. A construção de billing foi autorizada pela correção do usuário em 2026-09-29; app/Auth existentes continuam reutilizados.

## Entrada comercial e runtime — landing

- `POST /api/landing/ai-attendant` (`app/api/landing/ai-attendant/route.ts:12`): JSON
  validado por `parseAiAttendantRequest`; erros 400 para JSON/schema. Contexto inclui
  sessão/mensagens/leadId declarados pelo cliente. Não autentica pessoa do app.
- Adaptador `lib/landing/ai-attendant/runtime-client.ts:149` chama
  `POST /v1/taliya-commercial/turn` em `TALIYA_AGENT_RUNTIME_URL` (default local
  127.0.0.1:8088 somente desenvolvimento); timeout configurável, default 60000 ms.
- Auth servidor-servidor: HMAC SHA256 de `timestamp.body`; headers
  `x-taliya-agent-timestamp`, `x-taliya-agent-request-id`, `x-taliya-agent-signature`.
  Secret server-only; runtime compara assinatura/timestamp (`app/auth/hmac.py`).
- Contrato observado `taliya-commercial-ops.v1`; payload sanitizado:
  `{contract_version:taliya-commercial-ops.v1,agent_key:taliya_commercial,channel:widget,
  conversation:{conversation_id:<opaque>,lead_id:null},message:{idempotency_key:<key>,
  type:text,text:<user-text>,timestamp:<iso>},sender:{},metadata:{}}`.
  Exemplo esquemático parcial, não request validado.
- Resposta: run_id/conversation_id/lead_id/trace_id, status
  `succeeded|failed|blocked|human_paused|cost_capped`, output estruturado legado.
- Runtime `services/taliya-agent-runtime/app/main.py:297`: HMAC, recuperação por
  request_id, validação Pydantic, registry e `run_action_first_agent_turn`.
  Erros 400 malformed_request/stale_timestamp, 401 invalid_signature,
  404 unknown_agent_key, 503 runtime_misconfigured/blocked/database, 500 falha inesperada.
- Reuso candidato: adaptador, validação operacional, storage idempotente, outbox e
  fila WhatsApp (`storage/postgres.ts`, `app/core/taliya_commercial/outbox.py`).
  Cobertura de reinício/replay/ordenação para o novo agente NÃO demonstrada.
- Dono atual das escritas: rota Next faz `upsertSalesLead`/mensagens/conversão após
  resposta (`route.ts:54–150`) e runtime mantém estado. Spec 017 deve definir dono
  único dos efeitos; não ligar novas tools a esse pós-processamento sem migração.
- SDK fixado em pyproject: openai 2.44.0, openai-agents 0.18.0; não atende por si só
  a evidência de compatibilidade Agents API. Não atualizado na 013.

## Atendimento humano e implantação

### Sales Inbox embutido na landing
- Página `/internal/sales-inbox`: `app/internal/sales-inbox/page.tsx:17`, token query
  validado contra `INTERNAL_SALES_INBOX_TOKEN`, entregue ao componente cliente.
- `GET /api/internal/sales-inbox/leads`: filtros status/priority/channel/etc.; retorna
  leads com leadId/sessionId/contact/aiPaused/updatedAt. Auth shared Bearer ou
  x-internal-sales-token; ator x-operator-id (não identidade de staff verificada).
- `POST /api/internal/sales-inbox/leads/[leadId]/actions`:
  `{action:<allowlisted>,payload:{...}}`; 400 invalidação, 401 auth, 404 lead ausente,
  409 janela WhatsApp, 502 envio. `take_over`/`resume_ai` aplicam ação e sincronizam
  runtime em chamada separada. Não é prova de pausa atômica contra respostas tardias.
- `send_whatsapp_message`: usa `lead.updatedAt` para janela; idempotencyKey opcional
  do cliente ou derivada de ator/conteúdo/data. Não exercitado com pessoas reais.
- `mark_won` comercial não deve produzir acesso ou pagamento; sem evidência de
  billing neste caminho. Entrega humana web não homologada.

### Internal independente
- Fonte independente citada acima; `next.config.ts:19` da landing tem rewrites
  `/internal` e `/internal/:path*` para `https://taliya-internal.vercel.app`.
- HTTP atual sem credenciais: `/internal` local 401, remoto 401;
  `/internal/sales-inbox` local 200 com "Sales Inbox nao configurado". Evidência
  `evidence/internal-routing.json`: rota física local coexiste com rewrite remoto.
- GitHub deployments 6707338891/6690504385/6676800521 apontam SHA 7cbe9e9 e estão
  `failure`. URL responde, mas SHA de deployment ativo não confirmado.
- `GET/POST /internal/session`: formulário token; POST cria cookie
  `taliya_internal_session`, HttpOnly/SameSite=lax/secure em produção, 12 horas.
  Erros 401 token inválido, 503 configuração. Não houve login nesta execução.
- `GET /internal/api/leads`: filtros/cursor/limit, resposta de página canônica,
  `cache-control:private,no-store`; 401 auth, 400 erro de consulta/decodificação.
- `POST /internal/actions`: `{action,leadId,note,...}`; auth/origin/leitura/papéis,
  resultado `{ok,auditEvent,data}`; erros 400/401/403/500/503. Não é endpoint da landing.
- `services/operators/current-operator.ts` deriva ator/role de configuração em
  single-operator; `services/security/internal-identity-mode.ts` (arquivo descoberto no
  inventário) oferece modo multi_user, sem prova de uso por este handler.
- `services/views/operational-view.ts` exige Postgres para commercial-ops.v2;
  Supabase REST incompatível com v2 retorna indisponibilidade. Não basta apontar
  base de dados antiga. Reusar boundaries e contratos, não duplicar CRM/BI/caixa.

## Eventos, materiais e fonte pública

`funnel-events.ts` mantém eventos próprios e fallback memory sem DB;
`storage/postgres.ts:32` permite TLS rejectUnauthorized=false e cria DDL no caminho de
consulta. Achados condicionais confirmados em código; produção/config não inspecionadas.
Não há PostHog nos caminhos ativos pesquisados de landing/runtime. Isso não prova
inexistência de projeto PostHog. A 021 deverá migrar produtores sem duplicar eventos.

Catálogo compartilhado do pacote permanece vazio. Arquivos em public/illustrations,
public/agents e public/avatars são existentes, mas direitos/aprovação/classificação de
UGC não foram fornecidos. Demos JSX e imagens ilustrativas não são prova social.

## Invariantes da integração desejada

Pessoas, contatos, negócios, assinaturas e conversas não podem ser fundidos por
contato autodeclarado. Backend valida identidade/autoridade e confirmação financeira.
Dedup de efeito é distinta de call_id; pausa deve proteger tool e entrega tardia;
recuperação não depende de browser aberto. Estes são requisitos das próximas specs,
NÃO capacidades marcadas como implementadas nesta fundação.

## Divergência visual comercial confirmada
As capturas atuais após a animação inicial mostram CTA "Começar 14 dias grátis"
no hero/header e preço estático na landing. Isso contradiz a oferta fechada de cobrança
na contratação com garantia, mas não fornece a oferta publicada. Registrar para 015/018,
sem inventar preço/destino nem fazer correção incompleta na fundação.
