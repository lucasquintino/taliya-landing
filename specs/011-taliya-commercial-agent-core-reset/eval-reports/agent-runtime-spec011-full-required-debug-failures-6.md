# agent-runtime-spec011-full-required-debug-failures-6

Started at: 2026-05-31T22:24:31Z
Finished at: 2026-05-31T22:24:58Z
Provider: openai
Model: gpt-5.4-mini
Release gate: fail
Passed: 1/2
Estimated cost: US$0.058745

## PASS final-waitlist-pending-details

Title: Waitlist acceptance without details asks missing actionable fields
Channel: whatsapp

Lead 1: quero contratar, como faco para entrar?
Taliya 1.1: Para deixar registrado, qual e o nome do studio?
Runtime: http=200 status=succeeded agent=taliya_commercial_spec011_waitlist_agent trace=trace_turn_whatsapp_49b6fbb8b22ed184_d0c4b425987550a7
Decision: {"previous_state": "none", "current_state": "waitlist.pending_details", "next_state": "waitlist.pending_details", "route": "waitlist", "opening_type": "none", "detected_intents": ["contract_intent", "waitlist_eligible_intent"], "direct_question_present": true, "direct_question_answered_first": false, "diagnostic_action": "none", "diagnostic_allowed_now": false, "waitlist_allowed_now": true, "demo_status": "not_offered", "demo_next_step": "none", "profile_name_usage": "not_available", "facts_used": ["conversation.channel_conversation_id", "conversation.source", "metadata.page_path", "sender.whatsapp_phone", "quero contratar, como faco para entrar?"], "facts_missing": ["Waitlist is appropriate because the lead expressed clear intent to contract and official context says checkout is unavailable.", "Ask only for the missing studio detail; do not request phone or payment data."], "template_ids": ["waitlist.ask_missing_studio"], "template_variables": {"waitlist.ask_missing_studio": {"missing_detail_label": {"kind": "enum", "value": "studio", "source": "runtime_state", "evidence": ["quero contratar, como faco para entrar?"], "max_length": 0}}}, "render_plan": [{"template_id": "waitlist.ask_missing_studio", "channel": "whatsapp", "variables": {"missing_detail_label": {"kind": "enum", "value": "studio", "source": "runtime_state", "evidence": ["quero contratar, como faco para entrar?"], "max_length": 0}}}], "diagnostic_ledger_status": "not_started", "next_question_kind": "none", "policy_checks": {"direct_question_answered_first": true, "diagnostic_timing_ok": true, "waitlist_timing_ok": true, "official_facts_only": true, "no_early_contact_capture": true, "no_whatsapp_phone_request": true, "no_fake_certainty": true, "no_human_overlap": true, "channel_brevity_ok": true}}
Waitlist: {"status": "pending_details", "reason": null, "missing_fields": ["studio"]}
Handoff: {"status": "none", "reason": null}
Sources: [{"type": "product_knowledge", "version": "taliya-commercial-2026-05-22", "keys": ["plans", "prices", "plan_comparison", "links", "demo_status", "waitlist_status", "checkout_status", "availability", "cancellation_or_guarantee_policy", "privacy_or_data_notes", "how_it_works", "routine_areas", "whatsapp_scope", "integration_scope", "comparison_spreadsheet", "comparison_management_system", "security_and_data", "availability_and_onboarding", "out_of_profile", "unsupported_claims"]}]
Usage: {"model": "gpt-5.4-mini", "input_tokens": 15851, "output_tokens": 653, "cost_usd": 0.014827}

Lead 2: sim
Taliya 2.1: Para deixar registrado, qual e o nome do studio?
Runtime: http=200 status=succeeded agent=taliya_commercial_spec011_waitlist_agent trace=trace_turn_whatsapp_ef8d88b71c319ab8_761d1084aec794a5
Decision: {"previous_state": "waitlist.pending_details", "current_state": "waitlist.pending_details", "next_state": "waitlist.pending_details", "route": "waitlist", "opening_type": "none", "detected_intents": ["waitlist_intent", "confirmation"], "direct_question_present": false, "direct_question_answered_first": true, "diagnostic_action": "none", "diagnostic_allowed_now": false, "waitlist_allowed_now": true, "demo_status": "not_offered", "demo_next_step": "none", "profile_name_usage": "not_available", "facts_used": ["conversation.source", "conversation.channel_conversation_id", "metadata.page_path", "sender.whatsapp_phone", "quero contratar, como faco para entrar?"], "facts_missing": ["Keep waitlist pending_details because only studio is missing.", "Do not start diagnostic or ask for phone on WhatsApp.", "Use a single waitlist prompt for the missing studio detail."], "template_ids": ["waitlist.ask_missing_studio"], "template_variables": {"waitlist.ask_missing_studio": {"missing_detail_label": {"kind": "enum", "value": "studio", "source": "runtime_state", "evidence": ["waitlist_state.missing_details", "sales_inbox_inputs.waitlist_status"], "max_length": 0}}}, "render_plan": [{"template_id": "waitlist.ask_missing_studio", "channel": "whatsapp", "variables": {"missing_detail_label": {"kind": "enum", "value": "studio", "source": "runtime_state", "evidence": ["waitlist_state.missing_details", "sales_inbox_inputs.waitlist_status"], "max_length": 0}}}], "diagnostic_ledger_status": "not_started", "next_question_kind": "none", "policy_checks": {"direct_question_answered_first": true, "diagnostic_timing_ok": true, "waitlist_timing_ok": true, "official_facts_only": true, "no_early_contact_capture": true, "no_whatsapp_phone_request": true, "no_fake_certainty": true, "no_human_overlap": true, "channel_brevity_ok": true}}
Waitlist: {"status": "pending_details", "reason": null, "missing_fields": ["studio"]}
Handoff: {"status": "none", "reason": null}
Sources: [{"type": "product_knowledge", "version": "taliya-commercial-2026-05-22", "keys": ["plans", "prices", "plan_comparison", "links", "demo_status", "waitlist_status", "checkout_status", "availability", "cancellation_or_guarantee_policy", "privacy_or_data_notes", "how_it_works", "routine_areas", "whatsapp_scope", "integration_scope", "comparison_spreadsheet", "comparison_management_system", "security_and_data", "availability_and_onboarding", "out_of_profile", "unsupported_claims"]}]
Usage: {"model": "gpt-5.4-mini", "input_tokens": 16250, "output_tokens": 656, "cost_usd": 0.01514}

## FAIL final-post-waitlist-product-question

Title: Post-waitlist product question answers without repeating waitlist status
Channel: whatsapp
Failures:
- runtime returned non-200 status: [200, 200, 500]

Lead 1: quero contratar, como faco para entrar?
Taliya 1.1: A contratação ainda depende de validação do time, e o caminho disponível agora é entrar na lista para seguir os próximos passos com o studio.
Taliya 1.2: Hoje a entrada acontece por uma lista para um numero pequeno de studios. Posso deixar o interesse registrado sem prometer checkout, data ou condicao especial.
Runtime: http=200 status=succeeded agent=taliya_commercial_spec011_waitlist_agent trace=trace_turn_whatsapp_a37f96f7806052f0_b999003b9964f38b
Decision: {"previous_state": "none", "current_state": "waitlist_offer_after_contract_intent", "next_state": "waitlist_pending_details", "route": "waitlist", "opening_type": "none", "detected_intents": ["contract_intent", "buy_intent"], "direct_question_present": false, "direct_question_answered_first": true, "diagnostic_action": "none", "diagnostic_allowed_now": false, "waitlist_allowed_now": true, "demo_status": "not_offered", "demo_next_step": "none", "profile_name_usage": "not_available", "facts_used": ["metadata.page_path", "sender.whatsapp_phone"], "facts_missing": [], "template_ids": ["waitlist.offer_after_contract_intent"], "template_variables": {"waitlist.offer_after_contract_intent": {"waitlist_context_summary": {"kind": "long_text", "value": "A contratação ainda depende de validação do time, e o caminho disponível agora é entrar na lista para seguir os próximos passos com o studio.", "source": "diagnostic_ledger", "evidence": ["quero contratar, como faco para entrar?"], "max_length": 220}}}, "render_plan": [{"template_id": "waitlist.offer_after_contract_intent", "channel": "whatsapp", "variables": {"waitlist_context_summary": {"kind": "long_text", "value": "A contratação ainda depende de validação do time, e o caminho disponível agora é entrar na lista para seguir os próximos passos com o studio.", "source": "diagnostic_ledger", "evidence": ["quero contratar, como faco para entrar?"], "max_length": 220}}}], "diagnostic_ledger_status": "not_started", "next_question_kind": "none", "policy_checks": {"direct_question_answered_first": true, "diagnostic_timing_ok": true, "waitlist_timing_ok": true, "official_facts_only": true, "no_early_contact_capture": true, "no_whatsapp_phone_request": true, "no_fake_certainty": true, "no_human_overlap": true, "channel_brevity_ok": true}}
Waitlist: {"status": "offered", "reason": null, "missing_fields": []}
Handoff: {"status": "none", "reason": null}
Sources: [{"type": "product_knowledge", "version": "taliya-commercial-2026-05-22", "keys": ["plans", "prices", "plan_comparison", "links", "demo_status", "waitlist_status", "checkout_status", "availability", "cancellation_or_guarantee_policy", "privacy_or_data_notes", "how_it_works", "routine_areas", "whatsapp_scope", "integration_scope", "comparison_spreadsheet", "comparison_management_system", "security_and_data", "availability_and_onboarding", "out_of_profile", "unsupported_claims"]}]
Usage: {"model": "gpt-5.4-mini", "input_tokens": 15850, "output_tokens": 511, "cost_usd": 0.014187}

Lead 2: pode colocar o Studio Viva em Vitoria ES
Taliya 2.1: E de qual cidade e estado e o studio?
Runtime: http=200 status=succeeded agent=taliya_commercial_spec011_waitlist_agent trace=trace_turn_whatsapp_4a685c8c4900f0db_ed88f0267189d92f
Decision: {"previous_state": "waitlist.offered", "current_state": "waitlist.offered", "next_state": "waitlist.pending_details", "route": "waitlist", "opening_type": "none", "detected_intents": ["waitlist_update", "studio_location_provided"], "direct_question_present": false, "direct_question_answered_first": false, "diagnostic_action": "none", "diagnostic_allowed_now": false, "waitlist_allowed_now": true, "demo_status": "not_offered", "demo_next_step": "none", "profile_name_usage": "not_available", "facts_used": ["\"pode colocar o Studio Viva em Vitoria ES\"", "\"/pilates\""], "facts_missing": ["Treat the user message as providing studio name and city/state together; do not mark city_state missing if grounded as Vitória/ES.", "Keep waitlist status aligned with the validated state only when details are actually complete."], "template_ids": ["waitlist.ask_missing_city"], "template_variables": {"waitlist.ask_missing_city": {"missing_detail_label": {"kind": "enum", "value": "city_state", "source": "runtime_state", "evidence": ["\"pode colocar o Studio Viva em Vitoria ES\""], "max_length": 0}}}, "render_plan": [{"template_id": "waitlist.ask_missing_city", "channel": "whatsapp", "variables": {"missing_detail_label": {"kind": "enum", "value": "city_state", "source": "runtime_state", "evidence": ["\"pode colocar o Studio Viva em Vitoria ES\""], "max_length": 0}}}], "diagnostic_ledger_status": "not_started", "next_question_kind": "none", "policy_checks": {"direct_question_answered_first": true, "diagnostic_timing_ok": true, "waitlist_timing_ok": true, "official_facts_only": true, "no_early_contact_capture": true, "no_whatsapp_phone_request": true, "no_fake_certainty": true, "no_human_overlap": true, "channel_brevity_ok": true}}
Waitlist: {"status": "pending_details", "reason": null, "missing_fields": ["city_state"]}
Handoff: {"status": "none", "reason": null}
Sources: [{"type": "product_knowledge", "version": "taliya-commercial-2026-05-22", "keys": ["plans", "prices", "plan_comparison", "links", "demo_status", "waitlist_status", "checkout_status", "availability", "cancellation_or_guarantee_policy", "privacy_or_data_notes", "how_it_works", "routine_areas", "whatsapp_scope", "integration_scope", "comparison_spreadsheet", "comparison_management_system", "security_and_data", "availability_and_onboarding", "out_of_profile", "unsupported_claims"]}]
Usage: {"model": "gpt-5.4-mini", "input_tokens": 16215, "output_tokens": 540, "cost_usd": 0.014591}

Lead 3: quanto custa o Completo?
Taliya: [sem resposta automatica]
Runtime: http=500 status=None agent=None trace=None
