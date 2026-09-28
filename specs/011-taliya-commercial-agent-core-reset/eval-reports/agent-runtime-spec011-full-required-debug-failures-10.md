# agent-runtime-spec011-full-required-debug-failures-10

Started at: 2026-05-31T23:01:34Z
Finished at: 2026-05-31T23:01:59Z
Provider: openai
Model: gpt-5.4-mini
Release gate: fail
Passed: 3/4
Estimated cost: US$0.056767

## PASS final-reliable-name

Title: Reliable profile name can be used naturally
Channel: whatsapp

Lead 1: oi
Taliya 1.1: Oi, Mariana, tudo bem?
Taliya 1.2: Em que posso ajudar?
Runtime: http=200 status=succeeded agent=taliya_commercial_spec011_entry_agent trace=trace_turn_whatsapp_e667fa5e23786ab1_03c5548f5830fd32
Decision: {"previous_state": "none", "current_state": "greeting_only", "next_state": "greeting_only", "route": "entry", "opening_type": "cold_greeting_only", "detected_intents": ["greeting"], "direct_question_present": false, "direct_question_answered_first": true, "diagnostic_action": "none", "diagnostic_allowed_now": false, "waitlist_allowed_now": false, "demo_status": "not_offered", "demo_next_step": "none", "profile_name_usage": "used_reliable_name", "facts_used": [], "facts_missing": [], "template_ids": ["opening.cold_greeting_named"], "template_variables": {"opening.cold_greeting_named": {"first_name": {"kind": "short_text", "value": "Mariana", "source": "channel_metadata", "evidence": ["sender.name"], "max_length": 40}}}, "render_plan": [{"template_id": "opening.cold_greeting_named", "channel": "whatsapp", "variables": {"first_name": {"kind": "short_text", "value": "Mariana", "source": "channel_metadata", "evidence": ["sender.name"], "max_length": 40}}}], "diagnostic_ledger_status": "not_started", "next_question_kind": "none", "policy_checks": {"direct_question_answered_first": true, "diagnostic_timing_ok": true, "waitlist_timing_ok": true, "official_facts_only": true, "no_early_contact_capture": true, "no_whatsapp_phone_request": true, "no_fake_certainty": true, "no_human_overlap": true, "channel_brevity_ok": true}}
Waitlist: {"status": "none", "reason": null, "missing_fields": []}
Handoff: {"status": "none", "reason": null}
Sources: [{"type": "product_knowledge", "version": "taliya-commercial-2026-05-22", "keys": ["plans", "prices", "plan_comparison", "links", "demo_status", "waitlist_status", "checkout_status", "availability", "cancellation_or_guarantee_policy", "privacy_or_data_notes", "how_it_works", "routine_areas", "whatsapp_scope", "integration_scope", "comparison_spreadsheet", "comparison_management_system", "security_and_data", "availability_and_onboarding", "out_of_profile", "unsupported_claims"]}]
Usage: {"model": "gpt-5.4-mini", "input_tokens": 15875, "output_tokens": 420, "cost_usd": 0.013796}

## PASS final-unreliable-name

Title: Business profile name is not saved as person name
Channel: whatsapp

Lead 1: oi
Taliya 1.1: Oi, tudo bem?
Taliya 1.2: Em que posso ajudar?
Runtime: http=200 status=succeeded agent=taliya_commercial_spec011_entry_agent trace=trace_turn_whatsapp_b86cd964d7ee8a60_e8b3bae997506f4e
Decision: {"previous_state": "none", "current_state": "greeting_only", "next_state": "greeting_only", "route": "entry", "opening_type": "cold_greeting_only", "detected_intents": ["greeting"], "direct_question_present": false, "direct_question_answered_first": true, "diagnostic_action": "none", "diagnostic_allowed_now": false, "waitlist_allowed_now": false, "demo_status": "not_offered", "demo_next_step": "none", "profile_name_usage": "ignored_unreliable_name", "facts_used": [], "facts_missing": [], "template_ids": ["opening.cold_greeting"], "template_variables": {"opening.cold_greeting": {}}, "render_plan": [{"template_id": "opening.cold_greeting", "channel": "whatsapp", "variables": {}}], "diagnostic_ledger_status": "not_started", "next_question_kind": "none", "policy_checks": {"direct_question_answered_first": true, "diagnostic_timing_ok": true, "waitlist_timing_ok": true, "official_facts_only": true, "no_early_contact_capture": true, "no_whatsapp_phone_request": true, "no_fake_certainty": true, "no_human_overlap": true, "channel_brevity_ok": true}}
Waitlist: {"status": "none", "reason": null, "missing_fields": []}
Handoff: {"status": "none", "reason": null}
Sources: [{"type": "product_knowledge", "version": "taliya-commercial-2026-05-22", "keys": ["plans", "prices", "plan_comparison", "links", "demo_status", "waitlist_status", "checkout_status", "availability", "cancellation_or_guarantee_policy", "privacy_or_data_notes", "how_it_works", "routine_areas", "whatsapp_scope", "integration_scope", "comparison_spreadsheet", "comparison_management_system", "security_and_data", "availability_and_onboarding", "out_of_profile", "unsupported_claims"]}]
Usage: {"model": "gpt-5.4-mini", "input_tokens": 15882, "output_tokens": 378, "cost_usd": 0.013612}

## PASS final-thin-diagnostic-blocks-completion

Title: Thin diagnostic cannot complete
Channel: widget

Lead 1: pode fazer meu diagnostico?
Taliya 1.1: Claro, faco sim.
Taliya 1.2: Pra te devolver algo util, vou entender rapidinho como esta a rotina do studio hoje.
Taliya 1.3: Claro, faco sim. Pra te devolver algo util, vou entender rapidinho como esta a rotina do studio hoje.
Taliya 1.4: Hoje seu studio tem mais ou menos quantos alunos ativos?
Runtime: http=200 status=succeeded agent=taliya_commercial_spec011_diagnostic_agent trace=trace_turn_widget_a0da654fbed9a535_6dcbc5648f4bd99c
Diagnostic: {"status": "in_progress", "ledger": [{"question_key": "active_students_or_size", "status": "missing", "answer_value": null, "evidence": ["pode fazer meu diagnostico?"], "confidence": "high", "may_ask_again": true}, {"question_key": "main_pain", "status": "missing", "answer_value": null, "evidence": ["pode fazer meu diagnostico?"], "confidence": "high", "may_ask_again": true}, {"question_key": "pain_detail", "status": "missing", "answer_value": null, "evidence": ["pode fazer meu diagnostico?"], "confidence": "low", "may_ask_again": true}, {"question_key": "current_process", "status": "missing", "answer_value": null, "evidence": ["pode fazer meu diagnostico?"], "confidence": "high", "may_ask_again": true}, {"question_key": "priority", "status": "missing", "answer_value": null, "evidence": ["pode fazer meu diagnostico?"], "confidence": "high", "may_ask_again": true}, {"question_key": "urgency", "status": "missing", "answer_value": null, "evidence": ["pode fazer meu diagnostico?"], "confidence": "high", "may_ask_again": true}], "facts_used": ["conversation.source", "conversation.entry_intent", "metadata.page_path"], "main_bottleneck": null, "pain_context_human": null, "likely_cause": null, "crm_base_recommendation": null, "first_recommended_step": null, "indicated_routines_or_agents": [], "indicated_agents": [], "plan_or_range_to_compare": null, "final_plan_line": null, "demo_status_at_delivery": "not_offered", "final_demo_line": null, "evidence": ["conversation.source", "conversation.entry_intent", "metadata.page_path"], "unknowns": [], "confidence": "high", "next_question": "active_students_or_size", "validation_question": null, "final_demo_next_step_question": null}
Decision: {"previous_state": "entry.diagnostic_cta", "current_state": "diagnostic_opening", "next_state": "diagnostic_in_progress", "route": "diagnostic", "opening_type": "diagnostic_cta_opening", "detected_intents": ["request_diagnostic", "diagnostic_cta"], "direct_question_present": true, "direct_question_answered_first": true, "diagnostic_action": "start", "diagnostic_allowed_now": true, "waitlist_allowed_now": false, "demo_status": "not_offered", "demo_next_step": "none", "profile_name_usage": "not_available", "facts_used": ["conversation.source", "conversation.entry_intent", "metadata.page_path"], "facts_missing": [], "template_ids": ["opening.diagnostic_cta", "diagnostic.start", "diagnostic.ask_active_students"], "template_variables": {"opening.diagnostic_cta": {}, "diagnostic.start": {}, "diagnostic.ask_active_students": {}}, "render_plan": [{"template_id": "opening.diagnostic_cta", "channel": "widget", "variables": {}}, {"template_id": "diagnostic.start", "channel": "widget", "variables": {}}, {"template_id": "diagnostic.ask_active_students", "channel": "widget", "variables": {}}], "diagnostic_ledger_status": "in_progress", "next_question_kind": "plan_fit", "policy_checks": {"direct_question_answered_first": true, "diagnostic_timing_ok": true, "waitlist_timing_ok": true, "official_facts_only": true, "no_early_contact_capture": true, "no_whatsapp_phone_request": true, "no_fake_certainty": true, "no_human_overlap": true, "channel_brevity_ok": true}}
Waitlist: {"status": "none", "reason": null, "missing_fields": []}
Handoff: {"status": "none", "reason": null}
Sources: [{"type": "product_knowledge", "version": "taliya-commercial-2026-05-22", "keys": ["plans", "prices", "plan_comparison", "links", "demo_status", "waitlist_status", "checkout_status", "availability", "cancellation_or_guarantee_policy", "privacy_or_data_notes", "how_it_works", "routine_areas", "whatsapp_scope", "integration_scope", "comparison_spreadsheet", "comparison_management_system", "security_and_data", "availability_and_onboarding", "out_of_profile", "unsupported_claims"]}]
Usage: {"model": "gpt-5.4-mini", "input_tokens": 15854, "output_tokens": 703, "cost_usd": 0.015054}

## FAIL final-waitlist-pending-details

Title: Waitlist acceptance without details asks missing actionable fields
Channel: whatsapp
Failures:
- runtime returned non-200 status: [200, 500]

Lead 1: quero contratar, como faco para entrar?
Taliya 1.1: Para deixar registrado, qual e o nome do studio?
Runtime: http=200 status=succeeded agent=taliya_commercial_spec011_waitlist_agent trace=trace_turn_whatsapp_49b6fbb8b22ed184_a398ac0d5b517c43
Decision: {"previous_state": "waitlist_pending_details", "current_state": "waitlist_pending_details", "next_state": "waitlist_pending_details", "route": "waitlist", "opening_type": "none", "detected_intents": ["buy_intent", "contract_intent"], "direct_question_present": false, "direct_question_answered_first": false, "diagnostic_action": "none", "diagnostic_allowed_now": false, "waitlist_allowed_now": true, "demo_status": "not_offered", "demo_next_step": "none", "profile_name_usage": "not_available", "facts_used": ["conversation.channel_conversation_id", "metadata.page_path", "sender.whatsapp_phone"], "facts_missing": [], "template_ids": ["waitlist.ask_missing_studio"], "template_variables": {"waitlist.ask_missing_studio": {"missing_detail_label": {"kind": "enum", "value": "studio", "source": "runtime_state", "evidence": ["checkout unavailable and contract intent present", "waitlist pending details state"], "max_length": 0}}}, "render_plan": [{"template_id": "waitlist.ask_missing_studio", "channel": "whatsapp", "variables": {"missing_detail_label": {"kind": "enum", "value": "studio", "source": "runtime_state", "evidence": ["checkout unavailable and contract intent present", "waitlist pending details state"], "max_length": 0}}}], "diagnostic_ledger_status": "not_started", "next_question_kind": "none", "policy_checks": {"direct_question_answered_first": true, "diagnostic_timing_ok": true, "waitlist_timing_ok": true, "official_facts_only": true, "no_early_contact_capture": true, "no_whatsapp_phone_request": true, "no_fake_certainty": true, "no_human_overlap": true, "channel_brevity_ok": true}}
Waitlist: {"status": "pending_details", "reason": null, "missing_fields": ["studio"]}
Handoff: {"status": "none", "reason": null}
Sources: [{"type": "product_knowledge", "version": "taliya-commercial-2026-05-22", "keys": ["plans", "prices", "plan_comparison", "links", "demo_status", "waitlist_status", "checkout_status", "availability", "cancellation_or_guarantee_policy", "privacy_or_data_notes", "how_it_works", "routine_areas", "whatsapp_scope", "integration_scope", "comparison_spreadsheet", "comparison_management_system", "security_and_data", "availability_and_onboarding", "out_of_profile", "unsupported_claims"]}]
Usage: {"model": "gpt-5.4-mini", "input_tokens": 15851, "output_tokens": 537, "cost_usd": 0.014305}

Lead 2: sim
Taliya: [sem resposta automatica]
Runtime: http=500 status=None agent=None trace=None
