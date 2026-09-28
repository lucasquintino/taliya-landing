<!-- BEGIN:nextjs-agent-rules -->
# This is NOT the Next.js you know

This version has breaking changes - APIs, conventions, and file structure may all differ from your training data. Read the relevant guide in `node_modules/next/dist/docs/` before writing any code. Heed deprecation notices.
<!-- END:nextjs-agent-rules -->

<!-- SPECKIT START -->
Current feature plan for this independent copy: `specs/taliya-migration/001-fundacao-migracao/plan.md`. Migration scope and preservation rules: `docs/landing-migration/plan.md` and `.specify/memory/constitution.md`. The existing commercial-agent specs and implementation remain source-project material, not authority to expand this landing migration.
Before implementation, also read `specs/002-floating-ai-sales-agent/spec.md`, `specs/002-floating-ai-sales-agent/tasks.md`, `specs/001-niche-landing-system/spec.md`, and the source handoff docs under `docs/landing-agentes-pilates/source/`.

Taliya/Copiloto landing migration rules for this copy:
- Work only in this independent copy. Do not publish, push, deploy, alter DNS, or edit the original project.
- The current request authorizes text-content changes, SEO/ChatGPT discovery, one Mural section using existing visual primitives, final integration, and a post-integration architecture/reuse review. Follow the active migration spec for each step.
- Preserve the existing `/pilates` route and its approved visual direction. The new Copiloto landing belongs at `/`; do not change `/pilates` or `/pilates/planos` while the legacy-route decision is open.
- For S01–S14, do not change JSX structure, component tree/order, CSS, spacing, tokens, controls, handlers, state, destinations, forms, or existing interaction behavior. S06 Mural is the only authorized new section. SEO-only technical changes and S018 post-integration refactoring have their own explicit specs.
- Do not add the S02 trust strip, replace the existing calculator with new flows, add new subtab/form behavior, or implement the Copiloto application. If canonical copy does not fit an existing text slot, document the conflict and stop only that dependent change.
- The canonical landing JSON governs copy; SEO addendum v1.1 governs public discovery. Do not invent product capabilities, pricing, integrations, social proof, or indexing results.

LLM-first commercial agent rule:
- Before changing, optimizing, reviewing, debugging, or testing the Taliya commercial agent, use the local skill `taliya-llm-first-agent`.
- The agent must remain LLM-first: the LLM conducts commercial understanding and returns structured JSON; templates, validators, tools, and deterministic code are guardrails/rendering/operations.
- Do not move price, demo, plan-fit, pain-first, diagnostic, waitlist, social/source openings, or mixed-intent messages back into regex/state-machine/template-first shortcuts.
- Deterministic shortcuts are allowed only for operational/safety boundaries such as idempotency, human handoff pause/resume, prompt injection, sensitive data, unsupported media, widget empty opening, and pure cold greeting.

Protected `/pilates` layout rule:
- The current `/pilates` visual/layout direction is approved and must be preserved.
- Before implementing changes that can affect landing behavior, capture or confirm a current desktop and mobile visual baseline for `/pilates`.
- Do not redesign, reorder, restyle or replace `/pilates` sections, spacing, hierarchy, colors, cards, mockups, animations or composition unless the user explicitly asks for visual redesign.
- Future `/pilates` changes are allowed only for CTA wiring, entry metadata, tracking/schema/config alignment, route gates, accessibility fixes, responsive bug fixes or other explicit integration fixes.
- If an implementation task appears to require visual changes on `/pilates`, pause and ask before editing.
<!-- SPECKIT END -->
