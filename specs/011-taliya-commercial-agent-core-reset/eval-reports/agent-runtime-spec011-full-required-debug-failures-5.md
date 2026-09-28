# agent-runtime-spec011-full-required-debug-failures-5

Started at: 2026-05-31T22:22:06Z
Finished at: 2026-05-31T22:22:39Z
Provider: openai
Model: gpt-5.4-mini
Release gate: fail
Passed: 1/3
Estimated cost: US$0.062601

## PASS final-ambiguous-two-questions

Title: Ambiguous mixed question stays useful and focused
Channel: widget

Lead 1: nao sei se preciso de crm ou ia, tambem queria saber se resolve agenda
Taliya 1.1: Oi, tudo bem?
Taliya 1.2: Nao quero chutar um plano sem entender tamanho, dor principal e prioridade do studio.
Taliya 1.3: Posso fazer um diagnostico gratuito com poucas perguntas e te devolver o que organizar primeiro, quais agentes fariam sentido e qual plano vale comparar.
Taliya 1.4: O que voce acha?
Runtime: http=200 status=succeeded agent=taliya_commercial_spec011_product_agent trace=trace_turn_widget_cc11ad48c6577f61_d70d0ff05dd77a31
Diagnostic: {"status": "offered", "ledger": [{"question_key": "active_students_or_size", "status": "missing", "answer_value": null, "evidence": ["nao sei se preciso de crm ou ia, tambem queria saber se resolve agenda"], "confidence": "low", "may_ask_again": true}, {"question_key": "main_pain", "status": "answered", "answer_value": "duvida sobre precisar de crm ou ia e se a rotina resolve agenda", "evidence": ["nao sei se preciso de crm ou ia, tambem queria saber se resolve agenda"], "confidence": "high", "may_ask_again": false}, {"question_key": "pain_detail", "status": "inferred_from_prior_message", "answer_value": "quer entender se a plataforma se encaixa para organizar a agenda e a rotina do studio", "evidence": ["tambem queria saber se resolve agenda"], "confidence": "high", "may_ask_again": false}, {"question_key": "current_process", "status": "missing", "answer_value": null, "evidence": ["nao sei se preciso de crm ou ia, tambem queria saber se resolve agenda"], "confidence": "low", "may_ask_again": true}, {"question_key": "priority", "status": "missing", "answer_value": null, "evidence": ["nao sei se preciso de crm ou ia, tambem queria saber se resolve agenda"], "confidence": "low", "may_ask_again": true}, {"question_key": "urgency", "status": "missing", "answer_value": null, "evidence": ["nao sei se preciso de crm ou ia, tambem queria saber se resolve agenda"], "confidence": "low", "may_ask_again": true}], "facts_used": ["conversation.source", "metadata.page_path", "conversation.channel_conversation_id", "nao sei se preciso de crm ou ia, tambem queria saber se resolve agenda", "tambem queria saber se resolve agenda", "nao sei se preciso de crm ou ia"], "main_bottleneck": null, "pain_context_human": null, "likely_cause": null, "crm_base_recommendation": null, "first_recommended_step": null, "indicated_routines_or_agents": [], "indicated_agents": [], "plan_or_range_to_compare": null, "final_plan_line": null, "demo_status_at_delivery": "not_offered", "final_demo_line": null, "evidence": ["conversation.source", "metadata.page_path", "conversation.channel_conversation_id", "nao sei se preciso de crm ou ia, tambem queria saber se resolve agenda", "tambem queria saber se resolve agenda", "nao sei se preciso de crm ou ia"], "unknowns": [], "confidence": "high", "next_question": null, "validation_question": null, "final_demo_next_step_question": null}
Decision: {"previous_state": "initial", "current_state": "plan_fit_question", "next_state": "diagnostic_offered", "route": "product", "opening_type": "direct_question_opening", "detected_intents": ["crm_vs_ia_question", "agenda_fit_question"], "direct_question_present": true, "direct_question_answered_first": true, "diagnostic_action": "offer", "diagnostic_allowed_now": true, "waitlist_allowed_now": false, "demo_status": "not_offered", "demo_next_step": "none", "profile_name_usage": "not_available", "facts_used": ["conversation.source", "metadata.page_path", "conversation.channel_conversation_id", "nao sei se preciso de crm ou ia, tambem queria saber se resolve agenda", "tambem queria saber se resolve agenda", "nao sei se preciso de crm ou ia"], "facts_missing": [], "template_ids": ["product.plan_fit_with_diagnostic"], "template_variables": {"product.plan_fit_with_diagnostic": {"plan_fit_context": {"kind": "short_text", "value": "Nao quero chutar um plano sem entender tamanho, dor principal e prioridade do studio.", "source": "user_message", "evidence": ["nao sei se preciso de crm ou ia, tambem queria saber se resolve agenda"], "max_length": 180}}}, "render_plan": [{"template_id": "product.plan_fit_with_diagnostic", "channel": "widget", "variables": {"plan_fit_context": {"kind": "short_text", "value": "Nao quero chutar um plano sem entender tamanho, dor principal e prioridade do studio.", "source": "user_message", "evidence": ["nao sei se preciso de crm ou ia, tambem queria saber se resolve agenda"], "max_length": 180}}}], "diagnostic_ledger_status": "not_started", "next_question_kind": "none", "policy_checks": {"direct_question_answered_first": true, "diagnostic_timing_ok": true, "waitlist_timing_ok": true, "official_facts_only": true, "no_early_contact_capture": true, "no_whatsapp_phone_request": true, "no_fake_certainty": true, "no_human_overlap": true, "channel_brevity_ok": true}}
Waitlist: {"status": "none", "reason": null, "missing_fields": []}
Handoff: {"status": "none", "reason": null}
Sources: [{"type": "product_knowledge", "version": "taliya-commercial-2026-05-22", "keys": ["plans", "prices", "plan_comparison", "links", "demo_status", "waitlist_status", "checkout_status", "availability", "cancellation_or_guarantee_policy", "privacy_or_data_notes", "how_it_works", "routine_areas", "whatsapp_scope", "integration_scope", "comparison_spreadsheet", "comparison_management_system", "security_and_data", "availability_and_onboarding", "out_of_profile", "unsupported_claims"]}]
Usage: {"model": "gpt-5.4-mini", "input_tokens": 15795, "output_tokens": 1128, "cost_usd": 0.016922}

## FAIL final-waitlist-pending-details

Title: Waitlist acceptance without details asks missing actionable fields
Channel: whatsapp
Failures:
- runtime returned non-200 status: [200, 500]

Lead 1: quero contratar, como faco para entrar?
Taliya 1.1: Para deixar registrado, qual e o nome do studio?
Runtime: http=200 status=succeeded agent=taliya_commercial_spec011_waitlist_agent trace=trace_turn_whatsapp_49b6fbb8b22ed184_a398ac0d5b517c43
Decision: {"previous_state": "none", "current_state": "waitlist_pending_details", "next_state": "waitlist_pending_details", "route": "waitlist", "opening_type": "none", "detected_intents": ["contract_intent", "start_buy_intent", "waitlist_offer_needed"], "direct_question_present": true, "direct_question_answered_first": true, "diagnostic_action": "none", "diagnostic_allowed_now": false, "waitlist_allowed_now": true, "demo_status": "not_offered", "demo_next_step": "none", "profile_name_usage": "not_available", "facts_used": ["conversation.source", "conversation.channel_conversation_id", "metadata.page_path", "sender.whatsapp_phone", "product_knowledge.waitlist_status", "product_knowledge.checkout_status"], "facts_missing": ["Keep waitlist flow active because checkout is unavailable and intent to contract is explicit.", "Ask only for the missing contact path; do not request phone on WhatsApp.", "Do not start diagnostic or demo flow in this turn."], "template_ids": ["waitlist.ask_missing_studio"], "template_variables": {"waitlist.ask_missing_studio": {}}, "render_plan": [{"template_id": "waitlist.ask_missing_studio", "channel": "whatsapp", "variables": {}}], "diagnostic_ledger_status": "not_started", "next_question_kind": "none", "policy_checks": {"direct_question_answered_first": true, "diagnostic_timing_ok": true, "waitlist_timing_ok": true, "official_facts_only": true, "no_early_contact_capture": true, "no_whatsapp_phone_request": true, "no_fake_certainty": true, "no_human_overlap": true, "channel_brevity_ok": true}}
Waitlist: {"status": "pending_details", "reason": null, "missing_fields": ["studio_name", "city_state"]}
Handoff: {"status": "none", "reason": null}
Sources: [{"type": "product_knowledge", "version": "taliya-commercial-2026-05-22", "keys": ["plans", "prices", "plan_comparison", "links", "demo_status", "waitlist_status", "checkout_status", "availability", "cancellation_or_guarantee_policy", "privacy_or_data_notes", "how_it_works", "routine_areas", "whatsapp_scope", "integration_scope", "comparison_spreadsheet", "comparison_management_system", "security_and_data", "availability_and_onboarding", "out_of_profile", "unsupported_claims"]}]
Usage: {"model": "gpt-5.4-mini", "input_tokens": 15851, "output_tokens": 871, "cost_usd": 0.015808}

Lead 2: sim
Taliya: [sem resposta automatica]
Runtime: http=500 status=None agent=None trace=None

## FAIL final-post-waitlist-product-question

Title: Post-waitlist product question answers without repeating waitlist status
Channel: whatsapp
Failures:
- runtime returned non-200 status: [200, 200, 500]

Lead 1: quero contratar, como faco para entrar?
Taliya 1.1: Voce pediu para contratar agora; vou tratar isso como interesse direto na Taliya.
Taliya 1.2: Hoje a entrada acontece por uma lista para um numero pequeno de studios. Posso deixar o interesse registrado sem prometer checkout, data ou condicao especial.
Runtime: http=200 status=succeeded agent=taliya_commercial_spec011_waitlist_agent trace=trace_turn_whatsapp_a37f96f7806052f0_b999003b9964f38b
Decision: {"previous_state": "none", "current_state": "waitlist_offered", "next_state": "waitlist_offered", "route": "waitlist", "opening_type": "none", "detected_intents": ["purchase_intent", "ask_how_to_join", "waitlist_path"], "direct_question_present": false, "direct_question_answered_first": true, "diagnostic_action": "none", "diagnostic_allowed_now": false, "waitlist_allowed_now": true, "demo_status": "not_offered", "demo_next_step": "none", "profile_name_usage": "not_available", "facts_used": ["conversation.source", "conversation.channel_conversation_id", "metadata.page_path", "sender.whatsapp_phone", "product_knowledge.availability", "product_knowledge.checkout_status"], "facts_missing": [], "template_ids": ["waitlist.offer_after_contract_intent"], "template_variables": {"waitlist.offer_after_contract_intent": {"waitlist_context_summary": {"kind": "long_text", "value": "Voce pediu para contratar agora; vou tratar isso como interesse direto na Taliya.", "source": "runtime_state", "evidence": ["decision.waitlist.contract_intent"], "max_length": 220}}}, "render_plan": [{"template_id": "waitlist.offer_after_contract_intent", "channel": "whatsapp", "variables": {"waitlist_context_summary": {"kind": "long_text", "value": "Voce pediu para contratar agora; vou tratar isso como interesse direto na Taliya.", "source": "runtime_state", "evidence": ["decision.waitlist.contract_intent"], "max_length": 220}}}], "diagnostic_ledger_status": "not_started", "next_question_kind": "none", "policy_checks": {"direct_question_answered_first": true, "diagnostic_timing_ok": true, "waitlist_timing_ok": true, "official_facts_only": true, "no_early_contact_capture": true, "no_whatsapp_phone_request": true, "no_fake_certainty": true, "no_human_overlap": true, "channel_brevity_ok": true}}
Waitlist: {"status": "offered", "reason": null, "missing_fields": []}
Handoff: {"status": "none", "reason": null}
Sources: [{"type": "product_knowledge", "version": "taliya-commercial-2026-05-22", "keys": ["plans", "prices", "plan_comparison", "links", "demo_status", "waitlist_status", "checkout_status", "availability", "cancellation_or_guarantee_policy", "privacy_or_data_notes", "how_it_works", "routine_areas", "whatsapp_scope", "integration_scope", "comparison_spreadsheet", "comparison_management_system", "security_and_data", "availability_and_onboarding", "out_of_profile", "unsupported_claims"]}]
Usage: {"model": "gpt-5.4-mini", "input_tokens": 15850, "output_tokens": 700, "cost_usd": 0.015037}

Lead 2: pode colocar o Studio Viva em Vitoria ES
Taliya 2.1: Perfeito, deixei seu interesse registrado para a equipe da Taliya.
Taliya 2.2: Studio: Studio Viva.
Taliya 2.3: Cidade/estado: Vitoria ES.
Runtime: http=200 status=succeeded agent=taliya_commercial_spec011_waitlist_agent trace=trace_turn_whatsapp_4a685c8c4900f0db_ed88f0267189d92f
Decision: {"previous_state": "waitlist.offered", "current_state": "waitlist.offered", "next_state": "waitlist.joined", "route": "waitlist", "opening_type": "none", "detected_intents": ["waitlist_join_request"], "direct_question_present": false, "direct_question_answered_first": true, "diagnostic_action": "none", "diagnostic_allowed_now": false, "waitlist_allowed_now": true, "demo_status": "not_offered", "demo_next_step": "none", "profile_name_usage": "not_available", "facts_used": ["\"pode colocar o Studio Viva em Vitoria ES\"", "\"/pilates\""], "facts_missing": [], "template_ids": ["waitlist.joined"], "template_variables": {"waitlist.joined": {"studio_name": {"kind": "short_text", "value": "Studio Viva", "source": "user_message", "evidence": ["\"pode colocar o Studio Viva em Vitoria ES\""], "max_length": 80}, "city_state": {"kind": "short_text", "value": "Vitoria ES", "source": "user_message", "evidence": ["\"pode colocar o Studio Viva em Vitoria ES\""], "max_length": 80}, "contact_path": {"kind": "enum", "value": "whatsapp", "source": "user_message", "evidence": ["pode colocar o Studio Viva em Vitoria ES"], "max_length": 0}}}, "render_plan": [{"template_id": "waitlist.joined", "channel": "whatsapp", "variables": {"studio_name": {"kind": "short_text", "value": "Studio Viva", "source": "user_message", "evidence": ["\"pode colocar o Studio Viva em Vitoria ES\""], "max_length": 80}, "city_state": {"kind": "short_text", "value": "Vitoria ES", "source": "user_message", "evidence": ["\"pode colocar o Studio Viva em Vitoria ES\""], "max_length": 80}, "contact_path": {"kind": "enum", "value": "whatsapp", "source": "user_message", "evidence": ["pode colocar o Studio Viva em Vitoria ES"], "max_length": 0}}}], "diagnostic_ledger_status": "not_started", "next_question_kind": "none", "policy_checks": {"direct_question_answered_first": true, "diagnostic_timing_ok": true, "waitlist_timing_ok": true, "official_facts_only": true, "no_early_contact_capture": true, "no_whatsapp_phone_request": true, "no_fake_certainty": true, "no_human_overlap": true, "channel_brevity_ok": true}}
Waitlist: {"status": "joined", "reason": null, "missing_fields": []}
Handoff: {"status": "none", "reason": null}
Sources: [{"type": "product_knowledge", "version": "taliya-commercial-2026-05-22", "keys": ["plans", "prices", "plan_comparison", "links", "demo_status", "waitlist_status", "checkout_status", "availability", "cancellation_or_guarantee_policy", "privacy_or_data_notes", "how_it_works", "routine_areas", "whatsapp_scope", "integration_scope", "comparison_spreadsheet", "comparison_management_system", "security_and_data", "availability_and_onboarding", "out_of_profile", "unsupported_claims"]}]
Usage: {"model": "gpt-5.4-mini", "input_tokens": 16395, "output_tokens": 564, "cost_usd": 0.014834}

Lead 3: quanto custa o Completo?
Taliya: [sem resposta automatica]
Runtime: http=500 status=None agent=None trace=None
