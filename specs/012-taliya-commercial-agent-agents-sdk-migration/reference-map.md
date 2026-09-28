# Reference Map - OpenAI Agents SDK To Taliya

Purpose: map the actual SDK/reference concepts to the Taliya commercial agent so Spec 012 does not treat the SDK as vague inspiration.

## Local And Official References

- OpenAI Agents SDK guide: https://developers.openai.com/api/docs/guides/agents
- OpenAI Agents Python SDK: https://github.com/openai/openai-agents-python
- Agent evals guide: https://developers.openai.com/api/docs/guides/agent-evals
- Local demo: `C:\Users\lucas\AppData\Local\Temp\openai-cs-agents-demo`
- Installed local package: `agents` version `0.17.3`

## SDK Concept Mapping

| Agents SDK concept | Taliya adaptation |
| --- | --- |
| `Agent` | Taliya triage, entry, product, diagnostic, waitlist, handoff, safety agents |
| `instructions` | Behavior-contract and role-specific policy, without hardcoded product facts |
| `handoff` | Specialist transfer and trace-visible responsibility change |
| `function_tool` | Product knowledge reads, state reads, and proposal-only updates |
| Input guardrails | Prompt injection, sensitive data, unsupported media, out-of-scope abuse |
| Runner | SDK execution engine replacing custom action conductor/repair orchestration |
| Run items | Trace source for messages, handoffs, tool calls, tool outputs, guardrails |
| Final output | Structured `TaliyaTurnProposal`, not direct delivery text |
| Context | Typed Taliya context from persisted state, product knowledge, and recent transcript |
| Agent evals | Real-model SDK spike and release gates using Spec 011 fixtures |

## OpenAI CS Demo Mapping

| Demo element | Pattern to keep | Taliya difference |
| --- | --- | --- |
| Airline triage agent | LLM routes to explicit specialist agents | Taliya may start from persisted specialist state to reduce cost |
| Airline specialist agents | Agent-specific instructions/tools | Taliya specialists must respect approved voice, product truth, and diagnostics |
| Airline tools | Tool calls are visible and typed | Taliya normal-turn tools should be read-only/proposal-only before validation |
| Airline context | Typed context attached to run | Taliya context must separate reliable, inferred, internal, and renderable facts |
| Airline guardrails | Guardrails are separate from main prompt | Taliya keeps SDK guardrails plus post-SDK contract validators |
| Airline server event recording | Runner output is inspectable | Taliya trace must also include renderer, projection, delivery, and cost |

## What Not To Copy Literally

- Do not let tools freely mutate production state during model reasoning.
- Do not use mock/demo data as product truth.
- Do not let SDK final text bypass approved templates.
- Do not use multiple handoffs per ordinary short lead message unless correctness requires it and cost is logged.
- Do not assume the demo's UI/ChatKit streaming model applies to Taliya's widget/WhatsApp delivery.

## What Must Be More Strict Than The Demo

Taliya must add:

- official product fact validators;
- diagnostic completeness validators;
- Sales Inbox consistency;
- WhatsApp chunk/deferred-inbound handling;
- no client/studio WhatsApp capture;
- no checkout/discount/date/VIP invention;
- manual product-owner transcript approval;
- production rollback proof.
