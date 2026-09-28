# T012-056 Luna Migration Preflight

Date: 2026-08-04

## Result

The no-cost preflight is complete. No OpenAI request was made. The currently
deployed Railway service remains on `gpt-5.4-mini` until T012-057 passes and the
production switch is explicitly executed.

## Runtime Changes

- default target model: `gpt-5.6-luna`;
- action-agent reasoning: `none`;
- public commercial endpoint: Spec 012 action-first only, with no old-engine
  fallback;
- invalid, failed, cost-capped, blocked-empty, and succeeded-empty responses:
  safe operational reply instead of silence;
- usage: model operations, input/cached/output/reasoning tokens, repairs,
  latency, cache-write tokens, and cache-aware cost;
- health: build SHA, model, reasoning effort, OpenAI SDK, and Agents SDK;
- dependencies: exact direct pins plus Linux `requirements.lock`;
- waitlist hesitation: neutral `pause_waitlist_decision`, with no data capture,
  join, decline, or state mutation.

## Evidence

- Spec 012: `283 passed, 717 deselected`;
- active production gate: `514 passed`;
- public widget adapter: `10/10`;
- zero-cost aggregate gate: `6/6`;
- delivery/static audit: `34/34`;
- focused Ruff: passed;
- Docker image: `taliya-agent-runtime:luna-preflight`, build passed;
- container `/healthz`: model `gpt-5.6-luna`, reasoning `none`, OpenAI SDK
  `2.44.0`, Agents SDK `0.18.0`;
- targeted fixture preflight: 3 scenarios loaded, key available, Luna pricing
  recorded, `paid_call_status=not_attempted_preflight_only`;
- approval-block probe: 0 scenarios executed, `$0`,
  `paid_call_status=blocked_before_openai_call`.
- official OpenAI verification on 2026-08-04: model ID `gpt-5.6-luna`,
  structured outputs and function calling supported, `reasoning=none`
  supported, standard pricing `$1.00` input / `$0.10` cached input / `$6.00`
  output per million tokens, with cache writes billed at `$1.25` per million;
- landing TypeScript: `npx tsc --noEmit` passed;
- touched landing files: ESLint passed;
- Next.js production build: passed, including `/api/landing/ai-attendant` and
  `/api/landing/ai-attendant/whatsapp`.

## Cache-write accounting correction

A subsequent official-guidance review found that GPT-5.6 cache writes are
billed at 1.25 times the uncached input rate. The pinned OpenAI and Agents SDK
models preserve `cache_write_tokens` as an extra input-token detail even though
the generated annotation only lists `cached_tokens`. T012-056 now extracts and
propagates that value through the action report, response schema, trace, model
usage persistence, paid harness, and cost cap. Cost calculation separates
ordinary input, cache reads, cache writes, and output rather than treating
cache writes as ordinary input.

Verification after the correction: focused accounting/runner/adapter harness
`71 passed`; full Spec 012 `283 passed / 718 deselected`; active production gate
`515 passed`; focused Ruff and TypeScript passed; rebuilt Linux image health
reported Luna, reasoning none, OpenAI SDK `2.44.0`, and Agents SDK `0.18.0`;
container calculation for 250k cache-read + 500k cache-write + 250k ordinary
input + 1M output returned `$6.90`. Paid-call status remains `$0`.

The first aggregate-gate attempt exposed one stale static assertion that still
expected unsanitized transport metadata. The runtime already strips legacy
commercial hints before forwarding metadata to the LLM runtime. The assertion
was corrected to enforce the current sanitized contract, the focused delivery
audit then passed `34/34`, and the complete zero-cost aggregate rerun passed
`6/6`.

The raw all-history Python suite has 42 failures, all under `test_spec011_*`.
Those tests exercise the legacy engine that AGENTS.md forbids implementing.
The production gate excludes that named historical group transparently; it does
not hide active Spec 012 failures.

## Paid Gate Lock

T012-057 remains blocked. Proposed cumulative hard ceiling: `$0.75` for:

1. one targeted Luna canary;
2. all 3 targeted Luna scenarios;
3. the canonical 9-scenario set on Luna three consecutive times.

Every run must save complete transcripts, actions, templates, traces, token
usage, latency, repairs, and cost. Stop immediately on model-access/runtime
failure, a safety or internal-language leak, a silent successful turn, a failed
scenario, or the budget cap.
