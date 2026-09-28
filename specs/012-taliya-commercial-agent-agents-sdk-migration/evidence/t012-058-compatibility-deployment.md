# T012-058 compatibility deployment

- Service: `taliya-agent-runtime`.
- Environment: `production`.
- Previous deployment: `068c48a8-0113-46b4-a819-0b0874cddd9e`.
- Compatibility deployment: `65201fcd-0848-4d66-9208-0f753f00261d`.
- Railway status: `SUCCESS`.
- Health: `ok=true`.
- Configured and reported model: `gpt-5.4-mini`.
- Provider/runtime: `openai` / `production`.
- Reasoning effort: `none`.
- OpenAI SDK: `2.44.0`.
- Agents SDK: `0.18.0`.

The compatibility code was deployed without changing the production model and
without a paid OpenAI call. Existing no-cost widget fallback/adapter tests are
part of the `526 passed` production gate. The next operation is the explicit
T012-059 model-variable switch.

Rollback after the model switch requires both restoring
`TALIYA_AGENT_MODEL=gpt-5.4-mini` and redeploying the compatibility service;
deployment rollback alone does not revert environment variables.
