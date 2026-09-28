# agent-runtime-spec011-golden-demo-direct-fixed-1

Started at: 2026-06-01T00:27:29Z
Finished at: 2026-06-01T00:27:35Z
Provider: openai
Model: gpt-5.4-mini
Release gate: pass
Passed: 1/1
Estimated cost: US$0.014186

## PASS final-demo-request

Title: Golden RC-011-059 product demo
Channel: widget

Lead 1: quero ver uma demonstracao
Taliya 1.1: Oi, tudo bem?
Taliya 1.2: Ver demonstracao: https://www.taliya.com.br/pilates/planos/demonstracao
Taliya 1.3: Para eu te indicar o que vale olhar primeiro, faz sentido pensar na parte de agenda, atendimento ou vendas do seu studio.
Runtime: http=200 status=succeeded agent=taliya_commercial_spec011_product_agent trace=trace_turn_widget_b3048b43768572ba_b999d38acf2ffd7d
Decision: {"previous_state": "start", "current_state": "demo_requested", "next_state": "demo_offered", "route": "product", "opening_type": "direct_question_opening", "detected_intents": ["commercial_product_demo"], "direct_question_present": true, "direct_question_answered_first": true, "diagnostic_action": "none", "diagnostic_allowed_now": false, "waitlist_allowed_now": false, "demo_status": "offered", "demo_next_step": "offer_demo", "profile_name_usage": "not_available", "facts_used": ["conversation.source", "conversation.channel_conversation_id", "metadata.page_path"], "facts_missing": [], "template_ids": ["product.demo_direct"], "template_variables": {"product.demo_direct": {"official_demo_link": {"kind": "url", "value": "https://www.taliya.com.br/pilates/planos/demonstracao", "source": "official_product_knowledge", "evidence": ["product_knowledge.links"], "max_length": null}}}, "render_plan": [{"template_id": "product.demo_direct", "channel": "widget", "variables": {"official_demo_link": {"kind": "url", "value": "https://www.taliya.com.br/pilates/planos/demonstracao", "source": "official_product_knowledge", "evidence": ["product_knowledge.links"], "max_length": null}}}], "diagnostic_ledger_status": "not_started", "next_question_kind": "none", "policy_checks": {"direct_question_answered_first": true, "diagnostic_timing_ok": true, "waitlist_timing_ok": true, "official_facts_only": true, "no_early_contact_capture": true, "no_whatsapp_phone_request": true, "no_fake_certainty": true, "no_human_overlap": true, "channel_brevity_ok": true}}
Waitlist: {"status": "none", "reason": null, "missing_fields": []}
Handoff: {"status": "none", "reason": null}
Sources: [{"type": "product_knowledge", "version": "taliya-commercial-2026-05-22", "keys": ["plans", "prices", "plan_comparison", "links", "demo_status", "waitlist_status", "checkout_status", "availability", "cancellation_or_guarantee_policy", "privacy_or_data_notes", "how_it_works", "routine_areas", "whatsapp_scope", "integration_scope", "comparison_spreadsheet", "comparison_management_system", "security_and_data", "availability_and_onboarding", "out_of_profile", "unsupported_claims"]}]
Usage: {"model": "gpt-5.4-mini", "input_tokens": 15878, "output_tokens": 506, "cost_usd": 0.014186}
