# Static Anti-Drift Audit - Spec 012

Purpose: define static checks before implementation so the SDK path cannot quietly become another deterministic commercial bot.

## Blocked Patterns

Block public SDK path if static audit detects:

- imports from old commercial `conductor.py` as the normal SDK brain;
- imports from old `decision_compiler.py` in the SDK runner path;
- old TS v2 responder reachable as public commercial fallback;
- `runtime/runner.py` reachable as Taliya public commercial brain;
- a new file combining SDK run, commercial routing, validation, rendering, persistence, and delivery;
- raw lead text regex/token lists deciding price, plan, demo, diagnostic, waitlist, pain-first, source opening, objection, WhatsApp product question, or mixed intent;
- product prices, discounts, checkout URLs, launch dates, or availability hardcoded in prompts/templates/fallbacks;
- RAG/retrieval code that chooses commercial route from raw lead text;
- SDK output delivered directly to widget or WhatsApp;
- SDK tool that commits commercial state during reasoning;
- generic whole-response variables such as `final_text`, `message`, or `assistant_response` used as delivery source;
- renderer defaults that hide missing semantic variables;
- a large repair module that rewrites conversational meaning instead of escalating safely.

## Allowed Deterministic Patterns

Allowed when small, explicit, and tested:

- idempotency;
- HMAC/auth;
- turn lock;
- human handoff pause/resume;
- unsupported media;
- prompt injection/sensitive-data guardrails;
- official product knowledge lookup;
- RAG retrieval for official facts and source refs;
- validators for hard rules;
- approved template rendering after SDK proposal;
- persistence;
- Sales Inbox projection;
- delivery chunks/outbox;
- cost accounting;
- widget empty opening or pure cold greeting with no product/pain/context signal.

## Required Audit Evidence

Every implementation closure must record:

- static audit command or script path;
- blocked-pattern result;
- protected `/pilates` diff result;
- files reviewed manually if static matching is insufficient;
- whether the change preserved LLM-first commercial understanding.

## First Audit Implementation Target

The first implementation task after design lock should create a no-cost static audit that can run before SDK production code grows.
