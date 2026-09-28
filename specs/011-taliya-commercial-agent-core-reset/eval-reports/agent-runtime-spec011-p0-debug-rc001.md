# agent-runtime-spec011-p0-debug-rc001

Started at: 2026-05-31T14:36:22Z
Finished at: 2026-05-31T14:36:29Z
Provider: openai
Model: gpt-5.4-mini
Release gate: pass
Passed: 1/1
Estimated cost: US$0.013341

## PASS spec011-rc001-rc002-internal-metadata-leak

Title: Spec 011 RC-011-001/002 internal profile/source metadata never reaches user text
Channel: whatsapp

Lead 1: como funciona a Taliya na pratica?
Taliya 1.1: Funciona assim: a Taliya ajuda o studio a organizar o que acontece no dia a dia.
Taliya 1.2: Ela junta conversas, alunos, agenda, reposicoes, cobrancas, interessados e acompanhamentos para a equipe enxergar melhor o que precisa de acao.
Taliya 1.3: Quando o WhatsApp Business do studio esta conectado, os agentes podem apoiar conversas com alunos e interessados, sempre com a equipe podendo acompanhar e assumir quando precisar. Se fizer sentido, posso fazer um diagnostico gratuito para entender se a Taliya encaixa na rotina do seu studio. O que voce acha?
Runtime: http=200 status=succeeded agent=taliya_commercial_spec011_product_agent trace=trace_turn_whatsapp_e433e54c79c706b4_aa77c0b89fda514b
Diagnostic: {"status": "offered", "ledger": [{"question_key": "main_pain", "status": "missing", "answer_value": null, "evidence": ["inbound text: como funciona a Taliya na pratica?"], "confidence": "high", "may_ask_again": true}], "facts_used": ["source: lead came from the site", "page_path: /pilates", "profile_name: Reliable profile first name: Marina"], "main_bottleneck": null, "pain_context_human": null, "likely_cause": null, "crm_base_recommendation": null, "first_recommended_step": null, "indicated_routines_or_agents": [], "indicated_agents": [], "plan_or_range_to_compare": null, "final_plan_line": null, "demo_status_at_delivery": "not_offered", "final_demo_line": null, "evidence": ["source: lead came from the site", "page_path: /pilates", "profile_name: Reliable profile first name: Marina"], "unknowns": [], "confidence": "high", "next_question": "main_pain", "validation_question": null, "final_demo_next_step_question": null}
Decision: {"previous_state": "entry", "current_state": "product_answered_practical", "next_state": "diagnostic_offer", "route": "product", "opening_type": "none", "detected_intents": ["product_how_it_works", "pricing_context_request"], "direct_question_present": true, "direct_question_answered_first": true, "diagnostic_action": "offer", "diagnostic_allowed_now": true, "waitlist_allowed_now": false, "demo_status": "not_offered", "demo_next_step": "none", "profile_name_usage": "not_needed", "facts_used": ["source: lead came from the site", "page_path: /pilates", "profile_name: Reliable profile first name: Marina"], "facts_missing": ["Do not expose internal metadata such as channel_conversation_id or whatsapp_phone in customer-facing fields.", "Keep language practical and avoid CRM unless the lead used it.", "Answer the direct 'como funciona na pratica' question with official product facts before the diagnostic question."], "template_ids": ["product.how_it_works_direct"], "template_variables": {"product.how_it_works_direct": {"contextual_next_step": {"kind": "enum", "value": "diagnostic_offer_generic", "source": "model_decision", "evidence": ["detected_intents.how_it_works"], "max_length": null}}}, "render_plan": [{"template_id": "product.how_it_works_direct", "channel": "whatsapp", "variables": {"contextual_next_step": {"kind": "enum", "value": "diagnostic_offer_generic", "source": "model_decision", "evidence": ["detected_intents.how_it_works"], "max_length": null}}}], "diagnostic_ledger_status": "not_started", "next_question_kind": "pain", "policy_checks": {"direct_question_answered_first": true, "diagnostic_timing_ok": true, "waitlist_timing_ok": true, "official_facts_only": true, "no_early_contact_capture": true, "no_whatsapp_phone_request": true, "no_fake_certainty": true, "no_human_overlap": true, "channel_brevity_ok": true}}
Waitlist: {"status": "none", "reason": null, "missing_fields": []}
Handoff: {"status": "none", "reason": null}
Sources: [{"type": "product_knowledge", "version": "taliya-commercial-2026-05-22", "keys": ["plans", "prices", "plan_comparison", "links", "demo_status", "waitlist_status", "checkout_status", "availability", "unsupported_claims"]}]
Usage: {"model": "gpt-5.4-mini", "input_tokens": 13576, "output_tokens": 702, "cost_usd": 0.013341}
