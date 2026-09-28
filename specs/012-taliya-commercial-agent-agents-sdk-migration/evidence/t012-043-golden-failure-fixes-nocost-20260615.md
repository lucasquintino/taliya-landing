# T012-043 golden failure fixes - no-cost closure before paid rerun

Status: no-cost manual-review fixes completed; paid golden rerun still required.

Corrections implemented after manual review of the 2026-06-15 real-model
golden transcripts:

- `final-price-plus-pain`
  - `answer_price` now uses `diagnostic.price_hook_with_context` when
    `plan_fit_context` is present.
  - The contextual hook now uses the approved natural copy and does not repeat
    the pain literally.
  - Validator still requires contextual hook selection when the LLM declares
    price + pain/context, but no longer requires the final copy to quote the
    lead's exact pain anchor.
- `final-pain-first`
  - `offer_diagnostic_from_pain` no longer starts the diagnostic in the same
    turn.
  - The compiler now renders only `opening.contextual_ack` +
    `diagnostic.offer_soft` for first-contact pain offers.
  - The preserved validator no longer requires `diagnostic.ask_active_students`
    on a pain-first offer.
- `final-instagram-interest`
  - `opening.instagram_source` copy no longer says
    `Legal voce vir por aqui`.
  - The diagnostic CTA now says it will understand the studio routine,
    bottlenecks, and priority instead of the vague
    `entender por onde comecar`.
- `step3g-long-conversation`
  - Diagnostic answer capture now renders only the next diagnostic question.
    The next question template can still include `answer_feedback`, but the
    separate `diagnostic.partial_progress` chunk no longer duplicates it.
  - Waitlist product-question continuation can render `waitlist.answer_question`
    from structured `answer_feedback` when no official product fact key is
    selected, then resumes the persisted missing waitlist detail.
  - Report checks now clear failure detail text on passing checks, avoiding
    inverted PASS rows such as "missing expected rendered text".
- `final-waitlist-joined`
  - `waitlist.offer_after_contract_intent` no longer renders
    `waitlist_context_summary`; the internal summary can exist in the decision
    for trace/state, but not in customer-visible copy.
  - The action validator now blocks checkout/discount/VIP/special-condition
    language directly in the structured waitlist context before render.
- `final-demo-request`
  - `product.demo_direct` no longer ends with
    `faz sentido pensar na parte de agenda...`.
  - It now asks the lead to say whether they want to evaluate agenda,
    atendimento, or vendas after watching.
- WhatsApp scope direct answer
  - `product.whatsapp_direct` now uses the approved fixed copy:
    the student does not download an app or create a password; the student
    talks on WhatsApp; Taliya registers the action, updates the panel, and
    alerts the responsible person.
  - The template no longer renders `product_fact_summary`, preventing internal
    policy/fact-summary leaks.
- Final diagnostic and handoff copy
  - `diagnostic.deliver_agent_recommendation` now uses the approved simpler
    agent recommendation format and avoids broken punctuation.
  - `diagnostic.deliver_demo_not_offered` now offers to send a demo without
    directly sending the link at final diagnostic delivery.
  - `handoff.acknowledge` now says:
    `Vou deixar o contexto da conversa salvo para voce nao precisar repetir tudo.`
- Final customer-visible guardrail
  - Added a post-render validator that blocks internal markers, unresolved
    placeholders, mojibake artifacts, and broken punctuation before delivery.
  - This is a rendering/safety boundary only; it does not route commercial
    intent or replace LLM action selection.
- Encoding item
  - The mojibake observation from the manual review was confirmed as a terminal
    reading artifact; saved transcript evidence is UTF-8 and did not require a
    runtime behavior fix.

No-cost verification:

- `python -m pytest services/taliya-agent-runtime/tests/test_spec012_action_validators.py services/taliya-agent-runtime/tests/test_spec012_decision_compiler.py services/taliya-agent-runtime/tests/test_spec012_renderer_compiler.py -q`
  -> `58 passed`.
- `python -m pytest services/taliya-agent-runtime/tests -k spec012 -q`
  -> `270 passed, 716 deselected`.
- Focused `ruff check` on touched files -> passed.
- No paid OpenAI call was run for this no-cost fix pass.

Completion decision:

T012-043 remains open until the paid real-model golden transcripts are rerun
and pass. Do not advance to T012-044 until that rerun is reviewed.
