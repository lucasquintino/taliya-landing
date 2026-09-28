# agent-runtime-spec011-full-required-debug-openings-1

Started at: 2026-05-31T17:02:55Z
Finished at: 2026-05-31T17:03:08Z
Provider: openai
Model: gpt-5.4-mini
Release gate: pass
Passed: 3/3
Estimated cost: US$0.041645

## PASS final-cold-oi

Title: Cold oi stays light
Channel: whatsapp

Lead 1: oi
Taliya 1.1: Oi, tudo bem?
Taliya 1.2: Em que posso ajudar?
Runtime: http=200 status=succeeded agent=taliya_commercial_spec011_entry_agent trace=trace_turn_whatsapp_0fdf3d420cbbeb1c_c11f1c6a1d17a675
Decision: {"previous_state": "start", "current_state": "opening", "next_state": "opening", "route": "entry", "opening_type": "cold_greeting_only", "detected_intents": ["greeting"], "direct_question_present": false, "direct_question_answered_first": false, "diagnostic_action": "none", "diagnostic_allowed_now": false, "waitlist_allowed_now": false, "demo_status": "not_offered", "demo_next_step": "none", "profile_name_usage": "not_available", "facts_used": ["conversation.source", "conversation.channel_conversation_id", "metadata.page_path", "sender.whatsapp_phone"], "facts_missing": [], "template_ids": ["opening.cold_greeting"], "template_variables": {"opening.cold_greeting": {}}, "render_plan": [{"template_id": "opening.cold_greeting", "channel": "whatsapp", "variables": {}}], "diagnostic_ledger_status": "not_started", "next_question_kind": "none", "policy_checks": {"direct_question_answered_first": true, "diagnostic_timing_ok": true, "waitlist_timing_ok": true, "official_facts_only": true, "no_early_contact_capture": true, "no_whatsapp_phone_request": true, "no_fake_certainty": true, "no_human_overlap": true, "channel_brevity_ok": true}}
Waitlist: {"status": "none", "reason": null, "missing_fields": []}
Handoff: {"status": "none", "reason": null}
Sources: [{"type": "product_knowledge", "version": "taliya-commercial-2026-05-22", "keys": ["plans", "prices", "plan_comparison", "links", "demo_status", "waitlist_status", "checkout_status", "availability", "cancellation_or_guarantee_policy", "privacy_or_data_notes", "how_it_works", "routine_areas", "whatsapp_scope", "integration_scope", "comparison_spreadsheet", "comparison_management_system", "security_and_data", "availability_and_onboarding", "out_of_profile", "unsupported_claims"]}]
Usage: {"model": "gpt-5.4-mini", "input_tokens": 15655, "output_tokens": 513, "cost_usd": 0.01405}

## PASS final-widget-empty-opening

Title: Empty widget opening softly offers free diagnostic
Channel: widget

Lead 1: [text]
Taliya 1.1: Oi, tudo bem?
Taliya 1.2: Em que posso ajudar?
Taliya 1.3: Se fizer sentido pra voce, estamos oferecendo um diagnostico gratuito pro seu studio. O que voce acha?
Runtime: http=200 status=succeeded agent=taliya_commercial_spec011_entry_agent trace=trace_turn_widget_b3d9dbf778f1ac8f_55754aafa1ad96c0
Diagnostic: {"status": "offered", "ledger": [], "facts_used": [], "main_bottleneck": null, "pain_context_human": null, "likely_cause": null, "crm_base_recommendation": null, "first_recommended_step": null, "indicated_routines_or_agents": [], "indicated_agents": [], "plan_or_range_to_compare": null, "final_plan_line": null, "demo_status_at_delivery": "not_offered", "final_demo_line": null, "evidence": [], "unknowns": [], "confidence": "high", "next_question": null, "validation_question": null, "final_demo_next_step_question": null}
Decision: {"previous_state": "unknown", "current_state": "widget_opening", "next_state": "diagnostic_offered", "route": "entry", "opening_type": "widget_opening", "detected_intents": ["widget_empty_opening", "diagnostic_offer"], "direct_question_present": false, "direct_question_answered_first": true, "diagnostic_action": "offer", "diagnostic_allowed_now": true, "waitlist_allowed_now": false, "demo_status": "not_offered", "demo_next_step": "none", "profile_name_usage": "not_available", "facts_used": [], "facts_missing": [], "template_ids": ["opening.widget_empty_diagnostic"], "template_variables": {"opening.widget_empty_diagnostic": {}}, "render_plan": [{"template_id": "opening.widget_empty_diagnostic", "channel": "widget", "variables": {}}], "diagnostic_ledger_status": "not_started", "next_question_kind": "none", "policy_checks": {"direct_question_answered_first": true, "diagnostic_timing_ok": true, "waitlist_timing_ok": true, "official_facts_only": true, "no_early_contact_capture": true, "no_whatsapp_phone_request": true, "no_fake_certainty": true, "no_human_overlap": true, "channel_brevity_ok": true}}
Waitlist: {"status": "none", "reason": null, "missing_fields": []}
Handoff: {"status": "none", "reason": null}
Sources: [{"type": "product_knowledge", "version": "taliya-commercial-2026-05-22", "keys": ["plans", "prices", "plan_comparison", "links", "demo_status", "waitlist_status", "checkout_status", "availability", "cancellation_or_guarantee_policy", "privacy_or_data_notes", "how_it_works", "routine_areas", "whatsapp_scope", "integration_scope", "comparison_spreadsheet", "comparison_management_system", "security_and_data", "availability_and_onboarding", "out_of_profile", "unsupported_claims"]}]
Usage: {"model": "gpt-5.4-mini", "input_tokens": 15586, "output_tokens": 465, "cost_usd": 0.013782}

## PASS final-site-cta-opening

Title: Site CTA opening gives short context
Channel: widget

Lead 1: gostaria de conhecer melhor
Taliya 1.1: Oi, tudo bem?
Taliya 1.2: A Taliya e uma IA para ajudar no dia a dia do seu studio de Pilates: agenda, reposicoes, cobrancas, gestao, atendimento e acompanhamento.
Taliya 1.3: Se fizer sentido, posso fazer um diagnostico gratuito com poucas perguntas para entender por onde comecar. O que voce acha?
Runtime: http=200 status=succeeded agent=taliya_commercial_spec011_entry_agent trace=trace_turn_widget_d919538c8f8472c1_31820160a99775f6
Decision: {"previous_state": "initial", "current_state": "opening.site_cta", "next_state": "opening.site_cta", "route": "entry", "opening_type": "site_forced_message", "detected_intents": ["general_interest", "site_cta_opening"], "direct_question_present": false, "direct_question_answered_first": false, "diagnostic_action": "none", "diagnostic_allowed_now": false, "waitlist_allowed_now": false, "demo_status": "not_offered", "demo_next_step": "none", "profile_name_usage": "not_available", "facts_used": ["conversation.source", "conversation.entry_intent", "metadata.page_path"], "facts_missing": [], "template_ids": ["opening.site_cta"], "template_variables": {"opening.site_cta": {}}, "render_plan": [{"template_id": "opening.site_cta", "channel": "widget", "variables": {}}], "diagnostic_ledger_status": "not_started", "next_question_kind": "none", "policy_checks": {"direct_question_answered_first": true, "diagnostic_timing_ok": true, "waitlist_timing_ok": true, "official_facts_only": true, "no_early_contact_capture": true, "no_whatsapp_phone_request": true, "no_fake_certainty": true, "no_human_overlap": true, "channel_brevity_ok": true}}
Waitlist: {"status": "none", "reason": null, "missing_fields": []}
Handoff: {"status": "none", "reason": null}
Sources: [{"type": "product_knowledge", "version": "taliya-commercial-2026-05-22", "keys": ["plans", "prices", "plan_comparison", "links", "demo_status", "waitlist_status", "checkout_status", "availability", "cancellation_or_guarantee_policy", "privacy_or_data_notes", "how_it_works", "routine_areas", "whatsapp_scope", "integration_scope", "comparison_spreadsheet", "comparison_management_system", "security_and_data", "availability_and_onboarding", "out_of_profile", "unsupported_claims"]}]
Usage: {"model": "gpt-5.4-mini", "input_tokens": 15652, "output_tokens": 461, "cost_usd": 0.013813}
