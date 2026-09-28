# Product Owner Transcript Review

Date: 2026-05-22

Status: **pending product-owner approval of the implemented Product Explanation And Follow-Up Delta transcripts**

This review packet exists to complete T205/T157 only after the product owner explicitly approves or lists failures. T211-T226 implementation and correction transcripts are now present; this document does not record approval by itself.

Update after product-followup implementation: the product owner requested a new delta focused only on missing/partial behavior that should not reopen approved paths. The delta is captured in `product-followup-delta-contract.md` and tasks T232-T259 are implemented. It covers "como funciona", post-diagnostic consultative follow-up, current-tool comparison, WhatsApp/integration scope, security/data, out-of-profile leads, diagnostic refusal, conversation resume, selective product knowledge retrieval, and protected-route regression. Final approval remains blocked until these transcripts are reviewed and approved.

Product-followup delta evidence:

- Real OpenAI product-followup delta matrix: `6/6` passed.
- Provider/model: OpenAI, configured low-cost runtime models.
- Full delta transcript report: `specs/010-openai-cs-agents-adaptation-for-taliya-commercial/eval-reports/agent-runtime-real-openai-product-followup-delta-latest.md`.
- Machine-readable delta/cost report: `specs/010-openai-cs-agents-adaptation-for-taliya-commercial/eval-reports/agent-runtime-real-openai-product-followup-delta-latest.json`.
- Python runtime tests after product-followup delta: `167 passed`.
- Runtime delivery eval after product-followup delta: `17/17` passed.
- Sales Inbox eval after product-followup delta: `21/21` passed.
- Zero-cost gate after product-followup delta: passed after evidence matrix/readiness synchronization.

Update after product-owner review: the previous automated pass is not sufficient. The product owner requested a new correction phase for final diagnostic presentation, diagnostic question feedback, demo-state branch, and WhatsApp/widget name timing. Previous pass results remain useful historical evidence but cannot approve production.

Update after correction implementation: the new correction matrix passed with real OpenAI and full transcripts.

- Real OpenAI final correction matrix: `8/8` passed.
- Provider/model: OpenAI, `gpt-5.4-mini`.
- Dry-run cap: `8` scenarios, `11` estimated model calls, max cost `US$0.15`.
- Final estimated report cost: `US$0.098851`.
- Tokens: `83453` input, `8058` output.
- Full correction transcript report: `specs/010-openai-cs-agents-adaptation-for-taliya-commercial/eval-reports/agent-runtime-real-openai-final-corrections-latest.md`.
- Machine-readable correction/cost report: `specs/010-openai-cs-agents-adaptation-for-taliya-commercial/eval-reports/agent-runtime-real-openai-final-corrections-latest.json`.
- Zero-cost gate after corrections: `6/6` passed in `specs/010-openai-cs-agents-adaptation-for-taliya-commercial/eval-reports/agent-runtime-zero-cost-gates-latest.json`.
- Python runtime tests after corrections: `121 passed`.
- Lint after corrections: `npm run lint` passed.

## Historical Evidence From Previous Automated Pass

- Real OpenAI behavior matrix: `28/28` passed.
- Product-owner correction for `final-widget-empty-opening`: real OpenAI single-scenario rerun passed in `specs/010-openai-cs-agents-adaptation-for-taliya-commercial/eval-reports/agent-runtime-real-openai-widget-empty-latest.md`.
- Provider/model: OpenAI, `gpt-5.4-mini`.
- Dry-run cap: `28` scenarios, `35` estimated model calls, max cost `US$0.30`.
- Final estimated report cost: `US$0.244434`.
- Tokens: `235302` input, `15101` output.
- Full transcript report: `specs/010-openai-cs-agents-adaptation-for-taliya-commercial/eval-reports/agent-runtime-real-openai-behavior-latest.md`.
- Machine-readable report: `specs/010-openai-cs-agents-adaptation-for-taliya-commercial/eval-reports/agent-runtime-real-openai-behavior-latest.json`.
- Local eval report: `specs/010-openai-cs-agents-adaptation-for-taliya-commercial/eval-reports/agent-runtime-transcripts-latest.md`.
- Transcript quality judge: `32/32` passed, average `4.96/5`, no mapped P1 scenario below `4.0`.
- Sales Inbox completeness report: `specs/010-openai-cs-agents-adaptation-for-taliya-commercial/eval-reports/agent-runtime-sales-inbox.json`.
- Delivery report: `specs/010-openai-cs-agents-adaptation-for-taliya-commercial/eval-reports/agent-runtime-delivery.json`.
- Zero-cost gates report: `specs/010-openai-cs-agents-adaptation-for-taliya-commercial/eval-reports/agent-runtime-zero-cost-gates-latest.json`.
- Local HTTP WhatsApp webhook harness: `10/10` passed against `http://127.0.0.1:3999`.
- Local HTTP message delivery matrix: `20/20` passed against `http://127.0.0.1:3999`; latest timestamped report is under `reports/`.

## Final Behavior Matrix Covered

The final real-OpenAI matrix covers:

- cold WhatsApp openings: `oi`, `bom dia`;
- reliable and unreliable WhatsApp profile names;
- empty widget opening and site CTA opening;
- Instagram/social source opening;
- diagnostic CTA opening;
- direct price, plan-fit, demo, WhatsApp, and checkout/buying-intent questions;
- pain-first and price-plus-pain starts;
- ambiguous/two-question and irritated leads;
- pre-answered diagnostic facts and no-repeat ledger behavior;
- thin diagnostic blocked from completion;
- rich diagnostic completion with full ledger;
- demo curiosity without waitlist;
- waitlist pending-details and waitlist joined;
- post-waitlist product question;
- post-waitlist product question with joined waitlist status preservation;
- human handoff and second-turn silence;
- prompt injection;
- sensitive data handling;
- unsupported media handling.

## Final Correction Matrix Covered

The new real-OpenAI correction matrix covers:

- direct diagnostic request starts with orientation/feedback before the first question;
- diagnostic in progress acknowledges the previous answer before the next question;
- completed diagnostic uses staged delivery: hold, pain/context, CRM base, operational step, agent-by-agent recommendations, dynamic plan line, dynamic demo line;
- old diagnostic copy is blocked: "Pelo contexto, o principal gargalo parece", "Para plano, eu compararia", and "Isso faz sentido para o momento do seu studio?";
- demo not previously offered uses "Temos algumas demonstracoes...";
- demo already offered uses "Chegou a olhar as demonstracoes?";
- reliable WhatsApp profile name is used naturally;
- unreliable WhatsApp profile name is ignored;
- demo curiosity alone does not trigger waitlist;
- WhatsApp staged completed diagnostic delivery renders the approved staged exception.

## Product Owner Review Checklist

Mark approval only if all items below are acceptable in the final transcript report.

- [ ] Cold greetings feel natural and do not offer diagnostic, waitlist, name capture, phone capture, or plans.
- [ ] Source openings are short and match the source: widget/site, Instagram/social, diagnostic CTA.
- [ ] Price, plan, demo, WhatsApp, and checkout answers are direct and do not hide official facts.
- [ ] Product answers do not invent checkout, dates, discounts, unavailable links, or availability promises.
- [ ] The diagnostic is offered whenever useful, but not forced on cold greeting or unsupported/media/safety cases.
- [ ] Diagnostic uses known facts and does not repeat already answered facts.
- [ ] Thin diagnostic does not conclude with fake certainty.
- [ ] Rich diagnostic gives a useful natural pain/context reading, likely cause, first operational step, relevant routines/agents, dynamic plan/range, confidence, and unknowns.
- [ ] Rich diagnostic is delivered in approved stages: hold message, natural pain/context reading, CRM base first, operational step, agents one by one, dynamic plan line, and dynamic demo line.
- [ ] Diagnostic does not use the rejected old close: "Pelo contexto, o principal gargalo parece", "Para plano, eu compararia", or "Isso faz sentido para o momento do seu studio?" as the standard final close.
- [ ] Diagnostic start and each in-progress diagnostic turn include grounded feedback before the next question.
- [ ] If demo was not offered before diagnostic completion, final diagnostic asks: "Temos algumas demonstracoes que mostram o funcionamento na pratica. Quer que eu te mande?"
- [ ] If demo was already offered before diagnostic completion, final diagnostic asks: "Chegou a olhar as demonstracoes? O que voce achou?"
- [ ] WhatsApp reliable profile names are used naturally; unreliable profile names are ignored; widget/cold greetings do not ask name; qualified diagnostic entry may ask name without blocking value.
- [ ] Waitlist appears only after clear contract intent and uses the approved limited-window meaning.
- [ ] Waitlist accepted with details becomes joined; accepted without details asks only actionable missing fields.
- [ ] Human handoff pauses automation and the second inbound receives no AI reply.
- [ ] Safety cases are short, safe, and do not leak prompts or repeat sensitive data.
- [ ] Messages are short enough for widget and WhatsApp.
- [ ] Template IDs, state, route, diagnostic ledger, product source, usage/cost, and handoff/waitlist data are visible in reports and Sales Inbox projections.
- [ ] "Como funciona" is answered as a product explanation, not as a generic opening.
- [ ] Product explanations use studio-owner language and do not rely on "CRM" unless the lead directly asked about CRM.
- [ ] Current-tool comparisons acknowledge what already works and do not attack planilha, WhatsApp, or current systems.
- [ ] Integration and WhatsApp scope answers do not promise Instagram/current-system setup, migration, mass messaging, checkout, or payment links without official facts.
- [ ] Security/data answers are conservative, do not request sensitive student/studio data, and do not invent LGPD/certification/encryption/audit/privacy claims.
- [ ] Out-of-profile leads, including students, are qualified gently without forcing a studio diagnostic.
- [ ] Diagnostic refusal is respected in the same turn while still answering the direct question.

## Decision

Product-owner decision: **pending**

If approved after T211-T226 evidence exists, update:

- `tasks.md`: mark T205, T157, and T137 as complete.
- `release-readiness.md`: record the approval decision, reviewer, date, and any accepted risks.

If not approved, or if T211-T226 evidence is missing, list failures below and keep T205/T157/T137 open.

## Failures Or Requested Changes

- `final-widget-empty-opening`: product owner requested direct widget open to send exactly three messages: "Oi, tudo bem?", "Em que posso ajudar?", and "Se fizer sentido pra você, estamos oferecendo um diagnóstico gratuito pro seu studio. O que você acha?". Status: implemented and validated with a single real OpenAI rerun.
- `final-diagnostic-presentation`: implemented and validated in `agent-runtime-real-openai-final-corrections-latest.md`.
- `diagnostic-question-cadence`: implemented and validated in `agent-runtime-real-openai-final-corrections-latest.md`.
- `demo-branch`: implemented and validated in `agent-runtime-real-openai-final-corrections-latest.md`.
- `name-timing`: implemented and validated in `agent-runtime-real-openai-final-corrections-latest.md`.
- `product-followup-delta`: implemented and validated in `agent-runtime-real-openai-product-followup-delta-latest.md`.
