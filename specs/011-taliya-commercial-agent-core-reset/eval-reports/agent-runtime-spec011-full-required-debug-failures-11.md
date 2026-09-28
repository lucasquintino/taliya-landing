# agent-runtime-spec011-full-required-debug-failures-11

Started at: 2026-05-31T23:06:18Z
Finished at: 2026-05-31T23:06:40Z
Provider: openai
Model: gpt-5.4-mini
Release gate: fail
Passed: 1/2
Estimated cost: US$0.030355

## FAIL final-thin-diagnostic-blocks-completion

Title: Thin diagnostic cannot complete
Channel: widget
Failures:
- runtime returned non-200 status: [500]

Lead 1: pode fazer meu diagnostico?
Taliya: [sem resposta automatica]
Runtime: http=500 status=None agent=None trace=None

## PASS final-waitlist-pending-details

Title: Waitlist acceptance without details asks missing actionable fields
Channel: whatsapp

Lead 1: quero contratar, como faco para entrar?
Taliya 1.1: Para deixar registrado, qual e o nome do studio?
Taliya 1.2: E de qual cidade e estado e o studio?
Taliya 1.3: Para a equipe continuar com seguranca, prefere seguir por esta conversa ou por e-mail?
Runtime: http=200 status=succeeded agent=taliya_commercial_spec011_waitlist_agent trace=trace_turn_whatsapp_49b6fbb8b22ed184_334a99202181908e
Decision: {"previous_state": "unknown", "current_state": "waitlist_pending_details", "next_state": "waitlist_pending_details", "route": "waitlist", "opening_type": "none", "detected_intents": ["buy_intent", "contract_intent", "waitlist_eligible"], "direct_question_present": false, "direct_question_answered_first": true, "diagnostic_action": "none", "diagnostic_allowed_now": false, "waitlist_allowed_now": true, "demo_status": "not_offered", "demo_next_step": "none", "profile_name_usage": "not_available", "facts_used": ["conversation.source", "conversation.channel_conversation_id", "metadata.page_path", "sender.whatsapp_phone", "product_knowledge.waitlist_status", "product_knowledge.checkout_status"], "facts_missing": ["Keep waitlist flow active because checkout is unavailable and the lead has explicit contract intent.", "Do not start diagnostic in this turn; collect only the missing waitlist details.", "Avoid CRM terminology unless the lead asks for it directly."], "template_ids": ["waitlist.ask_missing_studio", "waitlist.ask_missing_city", "waitlist.ask_missing_contact_path"], "template_variables": {"waitlist.ask_missing_studio": {"missing_detail_label": {"kind": "enum", "value": "studio_name", "source": "runtime_state", "evidence": ["quero contratar, como faco para entrar?"], "max_length": 0}}, "waitlist.ask_missing_city": {"missing_detail_label": {"kind": "enum", "value": "city_state", "source": "runtime_state", "evidence": ["quero contratar, como faco para entrar?"], "max_length": 0}}, "waitlist.ask_missing_contact_path": {"missing_detail_label": {"kind": "enum", "value": "contact_path", "source": "runtime_state", "evidence": ["quero contratar, como faco para entrar?"], "max_length": 0}}}, "render_plan": [{"template_id": "waitlist.ask_missing_studio", "channel": "whatsapp", "variables": {"missing_detail_label": {"kind": "enum", "value": "studio_name", "source": "runtime_state", "evidence": ["quero contratar, como faco para entrar?"], "max_length": 0}}}, {"template_id": "waitlist.ask_missing_city", "channel": "whatsapp", "variables": {"missing_detail_label": {"kind": "enum", "value": "city_state", "source": "runtime_state", "evidence": ["quero contratar, como faco para entrar?"], "max_length": 0}}}, {"template_id": "waitlist.ask_missing_contact_path", "channel": "whatsapp", "variables": {"missing_detail_label": {"kind": "enum", "value": "contact_path", "source": "runtime_state", "evidence": ["quero contratar, como faco para entrar?"], "max_length": 0}}}], "diagnostic_ledger_status": "not_started", "next_question_kind": "none", "policy_checks": {"direct_question_answered_first": true, "diagnostic_timing_ok": true, "waitlist_timing_ok": true, "official_facts_only": true, "no_early_contact_capture": true, "no_whatsapp_phone_request": true, "no_fake_certainty": true, "no_human_overlap": true, "channel_brevity_ok": true}}
Waitlist: {"status": "offered", "reason": null, "missing_fields": ["studio_name", "city_state", "contact_path"]}
Handoff: {"status": "none", "reason": null}
Sources: [{"type": "product_knowledge", "version": "taliya-commercial-2026-05-22", "keys": ["plans", "prices", "plan_comparison", "links", "demo_status", "waitlist_status", "checkout_status", "availability", "cancellation_or_guarantee_policy", "privacy_or_data_notes", "how_it_works", "routine_areas", "whatsapp_scope", "integration_scope", "comparison_spreadsheet", "comparison_management_system", "security_and_data", "availability_and_onboarding", "out_of_profile", "unsupported_claims"]}]
Usage: {"model": "gpt-5.4-mini", "input_tokens": 15851, "output_tokens": 830, "cost_usd": 0.015623}

Lead 2: sim
Taliya 2.1: Para deixar registrado, qual e o nome do studio?
Runtime: http=200 status=succeeded agent=taliya_commercial_spec011_waitlist_agent trace=trace_turn_whatsapp_ef8d88b71c319ab8_761d1084aec794a5
Decision: {"previous_state": "waitlist.offered", "current_state": "waitlist_pending_details", "next_state": "waitlist_pending_details", "route": "waitlist", "opening_type": "none", "detected_intents": ["affirmation", "waitlist_progress"], "direct_question_present": false, "direct_question_answered_first": true, "diagnostic_action": "none", "diagnostic_allowed_now": false, "waitlist_allowed_now": true, "demo_status": "not_offered", "demo_next_step": "none", "profile_name_usage": "not_available", "facts_used": [], "facts_missing": ["Keep waitlist pending details until studio name, city/state, and contact path are confirmed.", "Do not start diagnostic or discuss checkout while waitlist details are incomplete."], "template_ids": ["waitlist.ask_missing_studio"], "template_variables": {"waitlist.ask_missing_studio": {}}, "render_plan": [{"template_id": "waitlist.ask_missing_studio", "channel": "whatsapp", "variables": {}}], "diagnostic_ledger_status": "not_started", "next_question_kind": "none", "policy_checks": {"direct_question_answered_first": true, "diagnostic_timing_ok": true, "waitlist_timing_ok": true, "official_facts_only": true, "no_early_contact_capture": true, "no_whatsapp_phone_request": true, "no_fake_certainty": true, "no_human_overlap": true, "channel_brevity_ok": true}}
Waitlist: {"status": "pending_details", "reason": null, "missing_fields": ["studio_name", "city_state"]}
Handoff: {"status": "none", "reason": null}
Sources: [{"type": "product_knowledge", "version": "taliya-commercial-2026-05-22", "keys": ["plans", "prices", "plan_comparison", "links", "demo_status", "waitlist_status", "checkout_status", "availability", "cancellation_or_guarantee_policy", "privacy_or_data_notes", "how_it_works", "routine_areas", "whatsapp_scope", "integration_scope", "comparison_spreadsheet", "comparison_management_system", "security_and_data", "availability_and_onboarding", "out_of_profile", "unsupported_claims"]}]
Usage: {"model": "gpt-5.4-mini", "input_tokens": 16433, "output_tokens": 535, "cost_usd": 0.014732}
