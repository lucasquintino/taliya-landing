# CRM-first Diagnostic Eval Fixtures

These fixtures validate the Diagnostico Gratuito path started from `sourceSection=studio_diagnostic` and `entryPath=diagnostic_cta`.

## Acceptance Rules

- Ask one short question at a time.
- Ask name first, then contact lightly, without blocking the conversation if refused.
- Extract multiple fields from a single visitor message when available.
- Avoid repeating a question already answered.
- Final diagnostic must include CRM areas, recommended agents, recommended plan and one next step.
- Lead payload must include diagnostic type, CRM pain areas, agent pain areas, buying timing, lead temperature, recommended CRM modules, recommended agents, recommended plan and next step.

## Cases

| Case | Visitor path | Expected behavior |
| --- | --- | --- |
| Cold researcher | "Lucas" -> refuses contact -> "tenho 40 alunos, estou pesquisando" -> "WhatsApp e agenda" -> answers remaining questions | Continue without pressure, classify `leadTemperature=cold`, recommend plan only after diagnostic is complete. |
| Hot buyer | Gives name/contact, 120 students, reposicoes, WhatsApp, sales follow-up, wants to solve now | Final diagnostic recommends broad CRM modules, `seven_agents`, `leadTemperature=hot`, CTA to compare plans. |
| CRM-only buyer | "quero organizar alunos, agenda e financeiro, mas sem IA ainda" | Explain Base as CRM-only fit, no active agents, keep route consultative. |
| Replacement pain | "tenho muitas faltas e reposicoes" | Ask replacement complexity if not answered, recommend Agenda plus Atendimento and CRM agenda/presenca area. |
| WhatsApp pain | "o WhatsApp fica lotado e minha equipe se perde" | Recommend CRM conversation history plus Atendimento agent; ask sales follow-up if relevant. |
| Sales pain | "perco interessados depois da aula experimental" | Recommend pipeline de interessados plus Vendas agent; ask current follow-up maturity. |
| Finance pain | "mensalidade e renovacao passam batido" | Recommend financeiro/renovacoes CRM area plus Financeiro agent. |
| Broad pain | "quero melhorar a rotina do studio inteiro" | Ask broad pain question first, then map multiple areas; do not jump straight to checkout. |
| Contact refusal | "prefiro nao passar contato agora" | Mark `contactCaptureStatus=refused` and continue the diagnostic normally. |
| Existing system | "uso outro sistema, mas ainda fico no WhatsApp e planilha" | Capture `currentSystem=sistema` or `planilha` context and explain Taliya as CRM plus agents without attacking the current tool. |
| Human request | "quero falar com uma pessoa" during diagnostic | Preserve diagnostic context, collect contact if missing and route to human WhatsApp only when requested. |
