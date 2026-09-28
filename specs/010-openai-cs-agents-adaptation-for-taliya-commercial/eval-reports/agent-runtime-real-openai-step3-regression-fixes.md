# agent-runtime-real-openai-step3-regression-fixes

Started at: 2026-05-26T17:51:42Z
Finished at: 2026-05-26T17:51:49Z
Provider: openai
Model: gpt-5.4-mini
Release gate: fail
Passed: 0/1
Estimated cost: US$0.005213

## FAIL fix-small-studio-valid

Title: Small studio is valid Pilates studio profile and should get diagnostic path
Channel: widget
Failures:
- expected diagnostic offer/start, got None

Lead 1: sou studio pequeno
Taliya 1.1: Oi, tudo bem?
Taliya 1.2: Em que posso ajudar?
Taliya 1.3: Se fizer sentido pra você, estamos oferecendo um diagnóstico gratuito pro seu studio. O que você acha?
Runtime: http=200 status=succeeded agent=taliya_commercial_entry_agent trace=trace_630ced45b0b44e9b8c8b72242aaa1b93
Decision: {"previous_state": "new_lead", "current_state": "general_interest", "next_state": "general_interest", "route": "entry", "opening_type": "widget_opening", "detected_intents": ["general_interest"], "direct_question_present": false, "direct_question_answered_first": true, "diagnostic_action": "none", "diagnostic_allowed_now": false, "waitlist_allowed_now": false, "demo_status": "not_offered", "demo_next_step": "none", "profile_name_usage": "used_reliable_name", "facts_used": ["lead said they are a small studio", "reliable profile name available: Ana"], "facts_missing": [], "template_ids": ["opening.widget_empty_diagnostic"], "template_variables": {"diagnostic.offer_soft": {"pain_context": "Para te orientar sem chutar, preciso entender um pouco da rotina do studio."}, "diagnostic.price_hook_with_context": {"pain_context": "Para te orientar sem chutar, preciso entender um pouco da rotina do studio."}}, "render_plan": [{"template_id": "opening.widget_empty_diagnostic", "channel": "widget"}], "diagnostic_ledger_status": "not_started", "next_question_kind": "clarification", "policy_checks": {"direct_question_answered_first": true, "diagnostic_timing_ok": true, "waitlist_timing_ok": true, "official_facts_only": true, "no_early_contact_capture": true, "no_whatsapp_phone_request": true, "no_fake_certainty": true, "no_human_overlap": true, "channel_brevity_ok": true}}
Sources: [{"type": "product_knowledge", "version": "taliya-commercial-2026-05-22", "keys": ["user_message.text", "profile_name_assessment.first_name", "initial_policy_read", "product_knowledge.facts.waitlist_status"]}]
Usage: {"model": "gpt-5.4-mini", "input_tokens": 4815, "output_tokens": 356, "cost_usd": 0.005213}
