# Evidências do código original

Fonte L1. Leitura estática de cópia isolada; nenhuma prova de exploração, publicação ou comportamento de produção. Linhas são dos arquivos dentro do ZIP. Credenciais não foram coletadas.

## EV01 — `AGENTS.md:7–17`
```text
7: <!-- SPECKIT START -->
8: Current feature plan for this independent copy: `specs/taliya-migration/001-fundacao-migracao/plan.md`. Migration scope and preservation rules: `docs/landing-migration/plan.md` and `.specify/memory/constitution.md`. The existing commercial-agent specs and implementation remain source-project material, not authority to expand this landing migration.
9: Before implementation, also read `specs/002-floating-ai-sales-agent/spec.md`, `specs/002-floating-ai-sales-agent/tasks.md`, `specs/001-niche-landing-system/spec.md`, and the source handoff docs under `docs/landing-agentes-pilates/source/`.
10:
11: Taliya/Copiloto landing migration rules for this copy:
12: - Work only in this independent copy. Do not publish, push, deploy, alter DNS, or edit the original project.
13: - The current request authorizes text-content changes, SEO/ChatGPT discovery, one Mural section using existing visual primitives, final integration, and a post-integration architecture/reuse review. Follow the active migration spec for each step.
14: - Preserve the existing `/pilates` route and its approved visual direction. The new Copiloto landing belongs at `/`; do not change `/pilates` or `/pilates/planos` while the legacy-route decision is open.
15: - For S01–S14, do not change JSX structure, component tree/order, CSS, spacing, tokens, controls, handlers, state, destinations, forms, or existing interaction behavior. S06 Mural is the only authorized new section. SEO-only technical changes and S018 post-integration refactoring have their own explicit specs.
16: - Do not add the S02 trust strip, replace the existing calculator with new flows, add new subtab/form behavior, or implement the Copiloto application. If canonical copy does not fit an existing text slot, document the conflict and stop only that dependent change.
17: - The canonical landing JSON governs copy; SEO addendum v1.1 governs public discovery. Do not invent product capabilities, pricing, integrations, social proof, or indexing results.
```

## EV02 — `.specify/memory/constitution.md:29–42`
```text
29: ## Restrições
30:
31: - Não modificar `/pilates` ou `/pilates/planos` enquanto o tratamento de legado não for decidido.
32: - Não inserir a faixa S02, não substituir a calculadora por fluxos, não criar formulários ou controles novos fora do Mural autorizado.
33: - Não alterar endpoints/backend nem simular envio bem-sucedido.
34: - Demos e textos ilustrativos não representam o produto real.
35: - Conteúdo de pacotes conflitante com o pedido mais recente é documentado, não implementado silenciosamente.
36:
37: ## Fluxo de trabalho
38:
39: - Manter o estado e os caminhos ativos em `specs/taliya-migration/README.md`.
40: - Checklists avaliam qualidade documental; `verification.md` registra procedimentos de runtime realmente executados.
41: - Baselines visuais precedem alterações de aplicação e devem ser comparados depois.
42: - Se uma copy for impossível sem quebrar um limite, registrar bloqueio pontual e continuar apenas tarefas independentes.
```

## EV03 — `.specify/init-options.json:1–10`
```text
1: {
2:   "ai": "codex",
3:   "ai_skills": true,
4:   "branch_numbering": "sequential",
5:   "context_file": "AGENTS.md",
6:   "here": true,
7:   "integration": "codex",
8:   "script": "ps",
9:   "speckit_version": "0.8.3.dev0"
10: }
```

## EV04 — `next.config.ts:6–24`
```text
6:   async redirects() {
7:     return [
8:       { source: "/pilates", destination: "/", permanent: true },
9:       { source: "/pilates/planos", destination: "/#planos", permanent: true },
10:       { source: "/pilates/planos/:path*", destination: "/#como-funciona", permanent: true },
11:       { source: "/pilates/demonstracao", destination: "/#como-funciona", permanent: true },
12:     ];
13:   },
14:   async rewrites() {
15:     return [
16:       {
17:         source: "/internal",
18:         destination: "https://taliya-internal.vercel.app/internal",
19:       },
20:       {
21:         source: "/internal/:path*",
22:         destination: "https://taliya-internal.vercel.app/internal/:path*",
23:       },
24:     ];
```

## EV05 — `app/api/internal/sales-inbox/auth.ts:1–23`
```text
1: export function requireSalesInboxAuth(request: Request) {
2:   const expectedToken = process.env.INTERNAL_SALES_INBOX_TOKEN;
3:   if (!expectedToken) {
4:     return {
5:       ok: false as const,
6:       response: Response.json({ error: "Sales Inbox token is not configured." }, { status: 503 }),
7:     };
8:   }
9:
10:   const authorization = request.headers.get("authorization");
11:   const bearer = authorization?.startsWith("Bearer ") ? authorization.slice("Bearer ".length).trim() : undefined;
12:   const headerToken = request.headers.get("x-internal-sales-token") ?? undefined;
13:   const token = bearer ?? headerToken;
14:
15:   if (token !== expectedToken) {
16:     return {
17:       ok: false as const,
18:       response: Response.json({ error: "Unauthorized." }, { status: 401 }),
19:     };
20:   }
21:
22:   return { ok: true as const, actorUserId: request.headers.get("x-operator-id") ?? "internal_operator" };
23: }
```

## EV06 — `app/internal/sales-inbox/page.tsx:14–31`
```text
14: export default async function SalesInboxPage({
15:   searchParams,
16: }: {
17:   searchParams: Promise<{ token?: string | string[] }>;
18: }) {
19:   const expectedToken = process.env.INTERNAL_SALES_INBOX_TOKEN;
20:   const params = await searchParams;
21:   const token = Array.isArray(params.token) ? params.token[0] : params.token;
22:
23:   if (!expectedToken) {
24:     return <InternalState title="Sales Inbox nao configurado" description="Defina INTERNAL_SALES_INBOX_TOKEN para habilitar o painel interno." />;
25:   }
26:
27:   if (token !== expectedToken) {
28:     return <InternalState title="Acesso restrito" description="Informe um token interno valido para abrir o Sales Inbox." />;
29:   }
30:
31:   return <SalesInboxClient token={expectedToken} />;
```

## EV07 — `app/api/landing/ai-attendant/route.ts:1–30`
```text
1: import { after } from "next/server";
2: import { runTaliyaCommercialRuntimeTurn as runAiAttendantTurn } from "@/lib/landing/ai-attendant/runtime-client";
3: import { buildAiAttendantContext } from "@/lib/landing/ai-attendant/context";
4: import { createConversionHandoff } from "@/lib/landing/ai-attendant/conversion";
5: import { createLeadRecord } from "@/lib/landing/ai-attendant/leads";
6: import { dispatchN8nEvent } from "@/lib/landing/ai-attendant/n8n";
7: import { parseAiAttendantRequest } from "@/lib/landing/ai-attendant/schema";
8: import { recordFunnelEvent } from "@/lib/landing/ai-attendant/funnel-events";
9: import { appendSalesLeadMessages, findSalesLeadForSession, getSalesLead, updateSalesLeadSyncStatus, upsertSalesLead } from "@/lib/landing/ai-attendant/sales-inbox-store";
10: import { summarizeConversation } from "@/lib/landing/ai-attendant/summarize";
11:
12: export async function POST(request: Request) {
13:   let body: unknown;
14:
15:   try {
16:     body = await request.json();
17:   } catch {
18:     return Response.json({ error: "Invalid JSON body." }, { status: 400 });
19:   }
20:
21:   const parsed = parseAiAttendantRequest(body);
22:   if (!parsed.ok) {
23:     return Response.json({ error: parsed.error }, { status: 400 });
24:   }
25:
26:   const response = await runAiAttendantTurn(parsed.value);
27:   const context = buildAiAttendantContext(parsed.value);
28:   const userMessageCount = parsed.value.session.messages.filter((message) => message.role === "user").length;
29:   if (userMessageCount === 1) {
30:     afterResponse("record_widget_first_message", () => recordFunnelEvent({
```

## EV08 — `app/api/landing/ai-attendant/route.ts:43–90`
```text
43:   if (response.conversionPath) {
44:     const conversionEventName =
45:       response.conversionPath === "human_whatsapp_assist"
46:         ? "floating_agent_human_whatsapp_handoff"
47:         : response.conversionPath === "waitlist_intent"
48:           ? "floating_agent_waitlist_intent"
49:           : response.conversionPath === "analysis_request"
50:             ? "floating_agent_analysis_handoff"
51:             : response.conversionPath === "crm_agent_diagnostic"
52:               ? "floating_agent_crm_diagnostic_completed"
53:             : response.conversionPath === "view_plans"
54:             ? "floating_agent_view_plans_cta"
55:             : response.conversionPath === "guided_demo"
56:               ? "floating_agent_guided_demo_cta"
57:               : response.conversionPath === "plan_recommendation"
58:                 ? "floating_agent_plan_recommendation_cta"
59:                 : "floating_agent_checkout_cta";
60:     const handoff = createConversionHandoff({
61:       config: context.nicheConfig,
62:       conversionPath: response.conversionPath,
63:       request: parsed.value,
64:       selectedPlanId: response.subscription?.planId,
65:       summary: summarizeConversation(parsed.value),
66:     });
67:     handoff.qualification = {
68:       ...handoff.qualification,
69:       ...response.qualificationPatch,
70:     };
71:     handoff.selectedPainIds = Array.from(new Set([...handoff.selectedPainIds, ...response.capturedPainIds]));
72:     handoff.recommendedAgentIds = Array.from(new Set([...handoff.recommendedAgentIds, ...response.recommendedAgentIds]));
73:     response.handoff = handoff;
74:     const lead = createLeadRecord({
75:       config: context.nicheConfig,
76:       eventName: conversionEventName,
77:       handoff,
78:       request: parsed.value,
79:       response,
80:     });
81:     const existingSessionLead = await findSalesLeadForSession(parsed.value.session.sessionId);
82:     const leadToStore = promoteExistingSessionLead(lead, existingSessionLead);
83:     const salesLead = await upsertSalesLead(leadToStore);
84:     afterResponse("record_widget_lead_created", () => recordFunnelEvent({
85:       eventName: "lead_created",
86:       request: parsed.value,
87:       response,
88:       leadId: salesLead.leadId,
89:     }));
90:     afterResponse("record_widget_conversion_event", () => recordFunnelEvent({
```

## EV09 — `lib/landing/ai-attendant/runtime-client.ts:124–166`
```text
124: export async function runTaliyaCommercialRuntimeTurn(request: AiAttendantRequest): Promise<AiAttendantResponse> {
125:   const localRuntime = process.env.NODE_ENV !== "production" ? "http://127.0.0.1:8088" : undefined;
126:   const url = (process.env.TALIYA_AGENT_RUNTIME_URL ?? localRuntime)?.replace(/\/+$/g, "");
127:   const secret = process.env.TALIYA_AGENT_RUNTIME_HMAC_SECRET ?? (process.env.NODE_ENV !== "production" ? "dev-secret" : undefined);
128:   if (!url || !secret) return createOperationalFallbackResponse("runtime_not_configured", request);
129:
130:   const body = JSON.stringify(createSpec011RuntimeRequestBody(request));
131:   const timestamp = new Date().toISOString().replace(/\.\d{3}Z$/, "Z");
132:   const requestId = createRuntimeRequestId(request);
133:   const timeoutMs = Number(process.env.TALIYA_AGENT_RUNTIME_TIMEOUT_MS || 60000);
134:   const controller = new AbortController();
135:   const timeout = setTimeout(() => controller.abort(), Number.isFinite(timeoutMs) ? timeoutMs : 60000);
136:
137:   try {
138:     const response = await fetch(`${url}${resolveTaliyaCommercialRuntimeEndpointPath(request)}`, {
139:       method: "POST",
140:       headers: {
141:         "content-type": "application/json",
142:         "x-taliya-agent-timestamp": timestamp,
143:         "x-taliya-agent-request-id": requestId,
144:         "x-taliya-agent-signature": signRuntimeRequest(secret, timestamp, body),
145:       },
146:       body,
147:       signal: controller.signal,
148:     });
149:     const payload = (await response.json().catch(() => null)) as unknown;
150:     if (!response.ok) {
151:       const errorCode = getRuntimeErrorCode(payload, `http_${response.status}`);
152:       return createOperationalFallbackResponse(errorCode, request);
153:     }
154:     const runtime = parseRuntimeAgentRunResponse(payload);
155:     if (!runtime) return createOperationalFallbackResponse("runtime_invalid_contract", request);
156:     return mapRuntimeResponseToAiAttendantResponse(runtime, request);
157:   } catch (error) {
158:     return createOperationalFallbackResponse(error instanceof Error ? error.name : "runtime_fetch_failed", request);
159:   } finally {
160:     clearTimeout(timeout);
161:   }
162: }
163:
164: export function resolveTaliyaCommercialRuntimeEndpointPath(request: AiAttendantRequest) {
165:   void request;
166:   return "/v1/taliya-commercial/turn";
```

## EV10 — `services/taliya-agent-runtime/app/core/taliya_commercial_sdk/action_agents.py:41–100`
```text
41: ACTION_AGENT_ORDER = [
42:     TRIAGE_AGENT,
43:     ENTRY_AGENT,
44:     PRODUCT_AGENT,
45:     DIAGNOSTIC_AGENT,
46:     WAITLIST_AGENT,
47:     HANDOFF_AGENT,
48: ]
49: ACTION_MODEL_REASONING_EFFORT = "none"
50:
51: # Deterministic mode -> starting agent (state-based operational selection).
52: STARTING_AGENT_BY_MODE: dict[str, str | None] = {
53:     "entry": TRIAGE_AGENT,
54:     "diagnostic": DIAGNOSTIC_AGENT,
55:     "post_diagnostic": PRODUCT_AGENT,
56:     "product": PRODUCT_AGENT,
57:     "price": PRODUCT_AGENT,
58:     "demo": PRODUCT_AGENT,
59:     "waitlist": WAITLIST_AGENT,
60:     "handoff": HANDOFF_AGENT,
61:     # Operational modes never call the LLM.
62:     "safety": None,
63:     "delivery_deferred": None,
64: }
65:
66: _BASE_ACTION_FIRST_INSTRUCTION = """
67: You are part of Taliya's commercial sales agent for Pilates studio leads.
68: You are the commercial understanding brain: interpret the lead's message in
69: the context of the conversation, then decide the turn.
70:
71: The runtime context block "[runtime context] Turn situation" is authoritative
72: and code-derived: it gives you the mode, the pending diagnostic question, the
73: ALLOWED ACTIONS for this turn, constraints, and compact memory. Trust it; do
74: not re-derive state.
75:
76: Output contract (ConductorActionDecision):
77: 1. selected_action: EXACTLY ONE action from the allowed actions list. Which
78:    action fits the lead's message is your semantic decision; the list only
79:    constrains form.
80: 2. direct_question: only a question asked in the CURRENT inbound message.
81:    Questions already answered in earlier turns are never new obligations.
82: 3. captured_slots: facts the lead just gave (e.g. the pending diagnostic
83:    answer), typed by key, with the lead's words as evidence.
84: 4. composition_variables: the human prose pieces assigned to you (e.g.
85:    pain_context_human, handoff_reason,
86:    clarification_question). Compose them in Brazilian Portuguese with correct
87:    accents and punctuation, in plain Pilates-studio-owner language (no SaaS
88:    jargon, no "CRM" unless the lead used it). Ground each in the lead's
89:    concrete words or the ledger - reuse their meaning naturally, never repeat
90:    their sentence literally, never write generic filler. Preserve concrete
91:    channels, processes, or objects that make the context specific, such as
92:    WhatsApp, agenda, reposições, cobranças, or follow-up. For normal diagnostic
93:    answer capture, do not invent answer_feedback: the runtime renders a short
94:    approved acknowledgement for the answered question. Each composition needs
95:    evidence.
96: 5. You never output final customer text, template ids, or state transitions:
97:    the runtime compiles your chosen action into the approved delivery.
98: 6. Never invent prices, links, dates, discounts, VIP access, availability, or
99:    client/studio WhatsApp connection promises - official facts are injected
100:    by the runtime from official sources.
```

## EV11 — `services/taliya-agent-runtime/app/shared/product_knowledge/source.py:19–44`
```text
19: class ProductKnowledgeSource(BaseModel):
20:     source_key: str = "taliya-commercial-product-knowledge"
21:     scope: str = "taliya_commercial"
22:     version: str = "taliya-commercial-2026-05-22"
23:     last_reviewed_at: str = "2026-05-22T00:00:00Z"
24:     plans: list[ProductPlan]
25:     links: dict[str, str]
26:     demo_status: str = "available"
27:     waitlist_status: str = "limited_studios_waitlist"
28:     checkout_status: str = "unavailable"
29:     availability: str = "Limited rollout for a small number of studios."
30:     cancellation_or_guarantee_policy: str = (
31:         "30 days of guarantee on the first subscription. Monthly cancellation "
32:         "without penalty after that period, according to the current policy."
33:     )
34:     privacy_or_data_notes: str = (
35:         "Do not ask for payment data or sensitive student data in chat."
36:     )
37:     how_it_works: str = (
38:         "Taliya helps a Pilates studio organize the daily routine in one "
39:         "place: conversations, students, agenda, reposicoes, cobrancas, "
40:         "interested leads, and follow-ups. The team can see what needs action. "
41:         "When the studio WhatsApp Business is connected and configured, agents "
42:         "can support conversations with students and interested leads while "
43:         "the team follows and takes over when needed."
44:     )
```

## EV12 — `lib/landing/ai-attendant/storage/postgres.ts:6–43`
```text
6: export function hasPostgresStorage() {
7:   return Boolean(process.env.DATABASE_URL);
8: }
9:
10: export async function postgresQuery<T extends QueryResultRow = QueryResultRow>(text: string, values: unknown[] = []) {
11:   const client = getPool();
12:   await ensureAiAttendantSchema();
13:   return client.query<T>(text, values);
14: }
15:
16: export async function ensureAiAttendantSchema() {
17:   if (!hasPostgresStorage()) return;
18:   if (!schemaReady) {
19:     schemaReady = createSchema();
20:   }
21:   return schemaReady;
22: }
23:
24: function getPool() {
25:   if (!process.env.DATABASE_URL) {
26:     throw new Error("DATABASE_URL is not configured.");
27:   }
28:   if (!pool) {
29:     pool = new Pool({
30:       connectionString: process.env.DATABASE_URL,
31:       max: Number(process.env.DATABASE_POOL_MAX ?? 5),
32:       ssl: process.env.DATABASE_SSL === "true" ? { rejectUnauthorized: false } : undefined,
33:     });
34:   }
35:   return pool;
36: }
37:
38: async function createSchema() {
39:   const client = getPool();
40:   await client.query(`
41:     CREATE TABLE IF NOT EXISTS whatsapp_sessions (
42:       channel_session_id text PRIMARY KEY,
43:       provider text NOT NULL,
```

## EV13 — `app/api/internal/sales-inbox/leads/[leadId]/actions/route.ts:34–73`
```text
34:   const { leadId } = await params;
35:
36:   if (body.action === "send_whatsapp_message") {
37:     const lead = await getSalesLead(leadId);
38:     if (!lead) return Response.json({ error: "lead_not_found" }, { status: 404 });
39:
40:     const content = typeof trustedPayload.payload.message === "string" ? trustedPayload.payload.message.trim() : "";
41:     const to = lead.contact.providerContactId ?? lead.contact.normalizedWhatsapp ?? lead.contact.whatsapp;
42:     if (!content) return Response.json({ error: "Mensagem obrigatoria." }, { status: 400 });
43:     if (!to) return Response.json({ error: "Lead sem WhatsApp/provider contact." }, { status: 400 });
44:     if (!isWithinWhatsAppCustomerServiceWindow(lead.updatedAt)) {
45:       return Response.json(
46:         {
47:           error: "outside_customer_service_window_template_required",
48:           reason: "Envio livre pelo WhatsApp exige janela de atendimento de 24h. Templates aprovados ainda nao estao habilitados neste fluxo.",
49:         },
50:         { status: 409 },
51:       );
52:     }
53:
54:     const clientIdempotencyKey = typeof trustedPayload.payload.idempotencyKey === "string" ? trustedPayload.payload.idempotencyKey : undefined;
55:     const sendResult = await sendMetaWhatsAppText({
56:       content,
57:       to,
58:       phoneNumberId: lead.contact.phoneNumberId,
59:       idempotencyKey: clientIdempotencyKey ?? `operator:${leadId}:${hashString(`${auth.actorUserId}:${content}:${lead.updatedAt}`)}`,
60:       leadId,
61:       channelSessionId: lead.channelSessionId,
62:       providerContactId: lead.contact.providerContactId,
63:     });
64:     if (!sendResult.ok) {
65:       return Response.json({ error: sendResult.reason }, { status: 502 });
66:     }
67:
68:     await appendSalesLeadMessage(leadId, {
69:       id: sendResult.providerMessageId ?? `operator_${Date.now()}`,
70:       role: "assistant",
71:       content,
72:     });
73:   }
```

## EV14 — `app/api/landing/ai-attendant/events/route.ts:1–31`
```text
1: import { recordLandingInteractionEvent } from "@/lib/landing/ai-attendant/funnel-events";
2:
3: const allowedEvents = new Set(["widget_opened", "cta_clicked"]);
4:
5: export async function POST(request: Request) {
6:   let body: Record<string, unknown>;
7:   try {
8:     body = await request.json() as Record<string, unknown>;
9:   } catch {
10:     return Response.json({ error: "Invalid JSON body." }, { status: 400 });
11:   }
12:
13:   const eventName = text(body.eventName);
14:   const occurrenceId = text(body.occurrenceId);
15:   const sessionId = text(body.sessionId);
16:   if (!allowedEvents.has(eventName) || !occurrenceId || !sessionId) {
17:     return Response.json({ error: "Invalid landing event." }, { status: 400 });
18:   }
19:
20:   await recordLandingInteractionEvent({
21:     eventName: eventName as "widget_opened" | "cta_clicked",
22:     occurrenceId,
23:     sessionId,
24:     leadId: text(body.leadId) || undefined,
25:     channel: text(body.channel) || "web",
26:     sourcePage: text(body.sourcePage) || undefined,
27:     sourceSection: text(body.sourceSection) || undefined,
28:     metadata: record(body.metadata),
29:   });
30:
31:   return Response.json({ ok: true });
```

## EV15 — `services/taliya-agent-runtime/pyproject.toml:5–18`
```text
5: [project]
6: name = "taliya-agent-runtime"
7: version = "0.1.0"
8: description = "LLM-first agent runtime for Taliya commercial conversations"
9: requires-python = ">=3.12"
10: dependencies = [
11:   "fastapi==0.139.0",
12:   "uvicorn[standard]==0.51.0",
13:   "pydantic==2.13.4",
14:   "pydantic-settings==2.14.2",
15:   "openai==2.44.0",
16:   "openai-agents==0.18.0",
17:   "psycopg[binary,pool]==3.3.4",
18:   "python-dotenv==1.2.2"
```

## EV16 — `docs/landing-migration/decisions.md:3–13`
```text
3: ## Decisões aplicadas nesta retomada
4:
5: | ID | Decisão | Origem |
6: |---|---|---|
7: | D-001 | Reiniciar em clone limpo do commit do GitHub; manter a tentativa anterior em diretório separado sem a usar como base. | Pedido atual e confirmação Git |
8: | D-002 | Preservar a landing antiga em `/pilates`; construir a home Copiloto em `/` conforme etapa SEO, sem redirecionar `/pilates` por suposição. | Preservação do código + política de legado do SEO |
9: | D-003 | Troca de copy não autoriza mudanças de componentes, layout ou interação. | Correção explícita do usuário |
10: | D-004 | SEO, Mural S06, integração final e arquitetura/reuso após integração são exceções autorizadas e delimitadas. | Pedido atual |
11: | D-005 | Não adicionar faixa S02, converter a calculadora S08 em fluxos ou criar controles/subtabs/forms durante as etapas de copy. | Aplicação do limite atual sobre o pacote |
12: | D-006 | Usar o JSON da landing como autoridade de copy e manter o SEO separado como autoridade técnica de descoberta. | Fontes do ZIP |
13: | D-007 | Considerar o app pronto conforme a atualização direta do usuário em 25/09/2026; o estado `prelaunch` dos documentos de 18–19/09 é um registro anterior. Usar a variante de conteúdo compatível com o produto pronto, sem presumir que trial, preço, checkout ou URL de onboarding estejam ativos. | Atualização direta do usuário; gates comerciais remanescentes do pacote |
```

## EV17 — `lib/landing/ai-attendant/funnel-events.ts:113–163`
```text
113:     sourcePage: input.sourcePage,
114:     sourceSection: input.sourceSection,
115:     ...acquisition,
116:   });
117:
118:   if (hasPostgresStorage()) {
119:     await postgresQuery(
120:       `INSERT INTO ai_funnel_events (
121:         event_id, idempotency_key, session_id, lead_id, channel, event_name,
122:         anonymous_session_id, message_id, page_path, source_section, cta_id,
123:         referrer, utm_source, utm_medium, utm_campaign, utm_content, utm_term,
124:         payload, created_at
125:       ) VALUES (
126:         $1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14,
127:         $15, $16, $17, $18::jsonb, now()
128:       ) ON CONFLICT (idempotency_key) DO NOTHING`,
129:       [
130:         eventId,
131:         idempotencyKey,
132:         input.sessionId,
133:         input.leadId,
134:         input.channel ?? "web",
135:         input.eventName,
136:         readMetadataString(input.metadata, "anonymousSessionId") ?? input.sessionId,
137:         input.occurrenceId,
138:         input.sourcePage,
139:         input.sourceSection,
140:         readMetadataString(input.metadata, "ctaId") ?? input.sourceSection,
141:         acquisition.referrer,
142:         acquisition.utmSource,
143:         acquisition.utmMedium,
144:         acquisition.utmCampaign,
145:         acquisition.utmContent,
146:         acquisition.utmTerm,
147:         JSON.stringify(payload),
148:       ],
149:     );
150:   } else if (!memoryEvents.some((event) => event.idempotencyKey === idempotencyKey)) {
151:     memoryEvents.push({
152:       eventId,
153:       idempotencyKey,
154:       sessionId: input.sessionId,
155:       leadId: input.leadId,
156:       channel: input.channel ?? "web",
157:       eventName: input.eventName,
158:       payload,
159:       createdAt: new Date().toISOString(),
160:     });
161:   }
162:
163:   return { eventId, idempotencyKey };
```

## EV18 — `components/landing/NicheLandingPage.tsx:366–407`
```text
366:   }
367:
368:   function openSalesAgent() {
369:     trackLandingEvent(config.tracking, "cta_click", {
370:       label: config.salesCta.primaryCta,
371:       href: "#floating-agent",
372:       sourceSection: "studio_diagnostic",
373:       entryPath: "diagnostic_cta",
374:       selectedPainId: selectedPain.id,
375:       selectedAgentId: selectedAgent.id,
376:     });
377:     window.dispatchEvent(
378:       new CustomEvent("landing:open-sales-agent", {
379:         detail: {
380:           sourceSection: "studio_diagnostic",
381:           message: "Quero começar meu teste grátis de 14 dias.",
382:         },
383:       }),
384:     );
385:   }
386:
387:   function openPlanOfferAgent(billingPeriod: BillingPeriod) {
388:     const billingOption = billingPeriod === "annual" ? config.launchOffer.annual : config.launchOffer.monthly;
389:     trackLandingEvent(config.tracking, "plan_cta_clicked", {
390:       planId: "taliya_single",
391:       planName: config.launchOffer.name,
392:       billingPeriod,
393:       priceBRL: billingOption.priceBRL,
394:       sourceSection: "plan_offer",
395:     });
396:     window.dispatchEvent(
397:       new CustomEvent("landing:open-sales-agent", {
398:         detail: {
399:           sourceSection: "plan_offer",
400:           message: `Quero começar os 14 dias grátis e seguir com o plano ${billingOption.label.toLowerCase()} da Taliya (${billingOption.price} ${billingOption.period}).`,
401:         },
402:       }),
403:     );
404:   }
405:
406:   function trackFaqSupportEmailClick() {
407:     trackLandingEvent(config.tracking, "faq_doubt_cta_clicked", {
```
