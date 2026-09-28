# Diagnostic Contract: Taliya Commercial Agent

**Status**: Binding for implementation.  
**Purpose**: Make the free diagnostic useful, evidence-based, non-repetitive, and commercially relevant.

## Diagnostic Principle

The diagnostic is the main value bridge. The agent should guide leads toward it whenever useful, but it must not force it on a cold greeting or fake certainty with weak facts.

## Mandatory Diagnostic Ledger

The runtime must maintain one ledger per conversation.

Each ledger item must contain:

- `question_key`;
- official question intent;
- status: `missing`, `answered`, `inferred_from_prior_message`, `unresolved`, or `not_applicable`;
- answer value;
- evidence message ids or current-turn quote summary;
- confidence;
- last asked timestamp;
- whether it may be asked again.

## Required Question Keys

The exact wording may vary, but these question intents must be covered before a completed diagnostic:

1. `active_students_or_size`: approximate studio size through active students.
2. `main_pain`: which areas give the studio more work today.
3. `pain_detail`: whether the studio can easily see what needs to be solved in the day.
4. `current_process`: whether the routine is handled in a system or mostly in WhatsApp, spreadsheet, notebook, memory, or manual process.
5. `priority`: which task/routine the lead most wants to make lighter first.
6. `urgency`: whether the studio wants to solve it now or is only researching.

`plan_fit_context` is optional and may be captured when the lead explicitly asks to compare a plan/routine/agent fit, but it does not block diagnostic completion. The final plan recommendation must be derived from the official product knowledge plus the answered diagnostic facts.

If the old `009` docs define a stricter or more specific question list, implementation must port that exact list and map each question to these canonical keys or add additional keys.

## No-Repeat Rule

If a lead already answered a diagnostic question before accepting diagnostic, the agent must:

- mark the corresponding ledger item as `answered` or `inferred_from_prior_message`;
- not ask that question again;
- use the known fact naturally;
- move to the next missing question.

The agent may ask a confirmation only when the prior answer is ambiguous or contradictory.

## Conversational Cadence

The diagnostic must feel like a short consultative conversation, not a form.

When the lead explicitly asks for the free diagnostic, the agent must not jump straight into the first question. It must first send a short natural orientation, then ask one question.

Approved meaning for diagnostic start:

```text
Claro, faco sim. Pra te devolver algo util, vou entender rapidinho como esta a rotina do studio hoje.

Hoje seu studio tem mais ou menos quantos alunos ativos?
```

Exact wording may vary, but the behavior may not vary:

- acknowledge the request first;
- explain that the diagnostic will use a few quick questions;
- ask only one focused question;
- do not ask contact details before value;
- do not ask the WhatsApp phone number from WhatsApp leads.

After each lead answer during diagnostic, the agent must acknowledge or reflect the answer before asking the next question.

Examples:

```text
Boa, isso ja me da uma nocao do tamanho da operacao.

Qual rotina voce quer melhorar primeiro?
```

```text
Entendi. Quando a agenda fica no caderno ou na memoria da equipe, reposicoes e faltas acabam escapando.

Como voces lidam com essa rotina hoje?
```

This feedback message must be grounded in the lead answer. It cannot be generic filler and cannot repeat the lead's words mechanically.

## Completion Criteria

A diagnostic may be delivered only when:

- all required question keys are `answered`, `inferred_from_prior_message`, or explicitly `not_applicable`;
- no required key is `missing`;
- no required key is `unresolved`;
- recommendation is grounded in evidence;
- product/plan comparison uses official product knowledge.

The official diagnostic question order is:

1. "Hoje seu studio tem mais ou menos quantos alunos ativos?"
2. "Quais partes mais dao trabalho hoje: WhatsApp, agenda/reposicoes, vendas, financeiro ou acompanhamento dos alunos?"
3. "Hoje voce consegue ver facilmente o que precisa ser resolvido no dia?"
4. "Hoje isso fica em algum sistema ou mais em WhatsApp, planilha e caderno?"
5. "Pensando na rotina do studio, qual tarefa voce mais gostaria de deixar mais leve primeiro?"
6. "Voces estao buscando resolver isso agora ou so pesquisando por enquanto?"

If completion criteria are not met, the agent must ask the next best missing or unresolved official question instead of delivering a full diagnostic. If the lead refuses or cannot answer, the agent may provide a clearly partial orientation, but it must not mark the diagnostic as completed.

## Delivery Shape

Completed diagnostic is an approved staged delivery. It is the main value moment of the conversation and is allowed to exceed the normal 1-3 message turn limit when each message is short, separated by typing/delay where the channel supports it, and each message carries one idea.

Before the final diagnostic content, the agent must send a hold message:

```text
Perfeito. Ja da pra te devolver uma leitura pratica. Vou organizar em partes.
```

After the hold message, the channel delivery plan must include a longer delay/typing cadence before the diagnostic content. The final diagnostic must be delivered in this order:

1. Human reading of the main pain/context, not a stiff label.
2. CRM base that Taliya needs to organize first.
3. First operational recommendation.
4. Indicated agents/routines one by one.
5. Dynamic plan recommendation.
6. Dynamic demo next step.

Completed diagnostic must include:

- internal main bottleneck plus a natural customer-facing pain/context reading;
- why that is likely, citing lead facts without sounding forensic;
- first recommended operational step;
- CRM base/routine that must be organized before thinking about agents;
- indicated Taliya routine/agent areas;
- for each indicated agent/routine: pain it resolves, why it was recommended, and how it acts in practice;
- plan or plan range to recommend only if supported by official knowledge and diagnostic facts;
- demo next-step line based on demo history;
- confidence/unknowns;
- persistence-ready evidence.

The first customer-facing line after the hold message must avoid stiff wording such as "gargalo principal" as a fixed phrase. Internally the model/runtime may keep `main_bottleneck`, but the rendered copy must be natural.

Preferred meaning:

```text
Pelo que voce contou, Lucas, o que mais parece estar pesando hoje e manter faltas, reposicoes e agenda organizadas sem depender de caderno, memoria ou conversa solta.
```

The final plan recommendation line must be dynamic and must use this meaning:

```text
Pelo tamanho, momento do studio e todo o contexto acima, eu recomendaria pra voce o plano [plano_ou_faixa].
```

The last diagnostic line must be a dynamic demo bridge:

- if a demo has not yet been offered in the conversation:

```text
Temos algumas demonstracoes que mostram o funcionamento na pratica. Quer que eu te mande?
```

- if a demo has already been offered in the conversation:

```text
Chegou a olhar as demonstracoes? O que voce achou?
```

It must not:

- imply certainty where facts are weak;
- say "pelo que voce contou" when the lead gave thin context;
- ask for contact data before value;
- offer waitlist unless clear contract intent is present.
- use "Pelo contexto, o principal gargalo parece..." as the rendered final diagnostic format;
- use "Para plano, eu compararia..." as the final plan line;
- use "Isso faz sentido para o momento do seu studio?" as the standard final diagnostic close;
- render an internal `validation_question` after the approved dynamic demo bridge as the normal completed-diagnostic ending;
- jump from diagnostic delivery directly to waitlist without a clear post-diagnostic buying/next-step intent.

## Demo Bridge After Diagnostic

Demo is the default bridge after a completed diagnostic and plan recommendation. It is not a checkout replacement and it is not enough by itself to offer waitlist.

The diagnostic renderer must know the conversation demo state:

- `not_offered`: no demo was offered yet;
- `offered`: demo was offered, sent, or displayed;
- `viewed_or_asked`: the lead asked for or appears to have opened/discussed demo;
- `reacted_positive`: the lead reacted positively to demo or asked how to continue.

If demo state is `not_offered`, the final diagnostic must use the "Temos algumas demonstracoes..." line. If demo state is `offered`, `viewed_or_asked`, or `reacted_positive`, it must use the "Chegou a olhar..." line unless the lead already gave a direct positive next-step intent.

Widget may render a validated demo CTA/button when official. WhatsApp must render an official full link instead of a button.

## Diagnostic State Rules

- `diagnostic_requested` starts from already-known facts.
- `diagnostic_in_progress` asks one missing question at a time.
- `diagnostic_ready` is set only after ledger validation.
- `diagnostic_delivered` persists evidence, unknowns, recommendation, final plan line, demo status at delivery, and final demo next-step line.
- Required ledger keys with `unresolved` status block `diagnostic_ready` and `diagnostic_delivered`.
- Product questions during diagnostic must be answered directly, then the agent may return to the diagnostic ledger.
