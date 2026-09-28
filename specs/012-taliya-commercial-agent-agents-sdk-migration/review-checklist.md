# Review Checklist - Spec 012

Use this checklist before accepting any Spec 012 design or implementation step.

## Architecture

- Does OpenAI Agents SDK own real agent orchestration instead of being wrapped by the old action conductor?
- Are agents, tools, handoffs, and guardrails declared explicitly?
- Is runtime current-agent selection based on persisted state, not raw lead text?
- Is there a clear max-turn/cost policy for handoffs?
- Is there a clear abort path if SDK does not improve behavior?

## LLM-First

- Does every normal commercial turn still call the model?
- Are price, plan, demo, product, diagnostic, waitlist, pain-first, social/source opening, objection, and mixed-intent turns interpreted by SDK agents?
- Are deterministic components limited to operation, retrieval, validation, rendering, persistence, delivery, handoff state, and pure cold-empty boundaries?
- Are tools prevented from becoming hidden deterministic commercial routers?

## Output Safety

- Is SDK output adapted into a strict proposal schema before validation?
- Is free-form SDK text blocked from direct delivery?
- Are customer-facing semantic fragments typed, bounded, registered, and evidence-grounded?
- Does renderer fail instead of inventing generic fallback copy?

## Product Truth

- Do product facts come only from official product knowledge and Spec 006?
- Are prompts/instructions free from hardcoded prices, dates, discounts, checkout claims, integration promises, or availability claims?
- Does product knowledge retrieval inform the SDK agents without forcing route/answer?

## Diagnostic Quality

- Does the Diagnostic Agent know all mandatory keys?
- Does it ask one question at a time?
- Does it accept simple numeric answers?
- Does it avoid repeated questions?
- Does final diagnostic preserve staged order and practical language?
- Does it reuse actual lead context rather than generic pain wording?

## Sales Inbox And Trace

- Does trace include SDK agent path, handoffs, tools, guardrails, final proposal, validators, render, usage, runtime diff, projection, and delivery?
- Is Sales Inbox still projection, not a second conversation brain?
- Are inferred/channel facts prevented from becoming reliable memory?

## Scope

- No `/pilates` visual/layout/copy changes.
- No multi-tenant.
- No client/studio WhatsApp connection.
- No checkout/payment.
- No Sales Inbox UI redesign.
- No operational CRM agents for client studios.

## Release

- Did golden transcripts pass?
- Did do-not-do fixtures pass?
- Did real-model SDK spike pass before implementation?
- Did shadow mode pass before cutover?
- Did rollback proof pass without reactivating old commercial brain?
- Is product-owner approval recorded?
