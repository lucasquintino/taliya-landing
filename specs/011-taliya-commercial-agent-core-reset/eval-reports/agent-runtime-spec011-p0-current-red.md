# agent-runtime-spec011-p0-current-red

Started at: 2026-05-30T01:03:12Z
Finished at: 2026-05-30T01:03:25Z
Provider: openai
Model: gpt-5.4-mini
Release gate: fail
Passed: 0/1
Estimated cost: US$0.007622

## FAIL spec011-rc001-rc002-internal-metadata-leak

Title: Spec 011 RC-011-001/002 internal profile/source metadata never reaches user text
Channel: whatsapp
Failures:
- internal metadata was persisted as lead fact: ['lead came from the site']
- metadata source was persisted as a high-confidence lead fact
- internal metadata was persisted as lead fact: ['reliable profile first name']
- internal profile-name label was treated as reliable sender name
- turn 1 has more than 3 WhatsApp chunks

Lead 1: como funciona a Taliya na pratica?
Taliya 1.1: Oi, tudo bem? Funciona assim: a Taliya ajuda o studio a organizar o que acontece no dia a dia.
Taliya 1.2: Ela junta conversas, alunos, agenda, reposições, cobranças, interessados e acompanhamentos para a equipe enxergar melhor o que precisa de ação.
Taliya 1.3: Quando o WhatsApp Business do studio está conectado, os agentes podem apoiar conversas com alunos e interessados, sempre com a equipe podendo acompanhar e assumir quando precisar.
Taliya 1.4: Se fizer sentido para você, estamos oferecendo um diagnóstico gratuito para o seu studio. Assim podemos entender como a Taliya encaixaria na sua rotina e por onde começar. O que você acha?
Runtime: http=200 status=succeeded agent=taliya_commercial_product_agent trace=trace_2d593e2443a6434491ff3fc90fc08c2a
Decision: {"previous_state": "new_lead", "current_state": "product_question", "next_state": "product_question", "route": "product", "opening_type": "none", "detected_intents": ["product_how_it_works"], "direct_question_present": true, "direct_question_answered_first": true, "diagnostic_action": "none", "diagnostic_allowed_now": true, "waitlist_allowed_now": false, "demo_status": "not_offered", "demo_next_step": "none", "profile_name_usage": "used_reliable_name", "facts_used": ["A lead veio do site (/pilates).", "O nome do perfil foi considerado confiável: Marina.", "A pergunta foi sobre como a Taliya funciona na prática."], "facts_missing": [], "template_ids": ["product.how_it_works_direct"], "template_variables": {"first_name": {"value": "Marina"}, "diagnostic.offer_soft": {"pain_context": "Entendi esse ponto: A lead veio do site (/pilates).."}, "diagnostic.price_hook_with_context": {"pain_context": "Entendi esse ponto: A lead veio do site (/pilates).."}, "product.how_it_works_direct": {"contextual_next_step": "Se fizer sentido para você, estamos oferecendo um diagnóstico gratuito para o seu studio. Assim podemos entender como a Taliya encaixaria na sua rotina e por onde começar. O que você acha?", "recommended_area": ""}}, "render_plan": [{"template_id": "product.how_it_works_direct", "channel": "whatsapp"}], "diagnostic_ledger_status": "not_started", "next_question_kind": "pain", "policy_checks": {"direct_question_answered_first": true, "diagnostic_timing_ok": true, "waitlist_timing_ok": true, "official_facts_only": true, "no_early_contact_capture": true, "no_whatsapp_phone_request": true, "no_fake_certainty": true, "no_human_overlap": true, "channel_brevity_ok": true}}
Sources: [{"type": "product_knowledge", "version": "taliya-commercial-2026-05-22", "keys": ["product_knowledge.how_it_works", "product_knowledge.routine_areas", "product_knowledge.whatsapp_scope", "how_it_works", "routine_areas", "whatsapp_scope"]}]
Usage: {"model": "gpt-5.4-mini", "input_tokens": 6028, "output_tokens": 689, "cost_usd": 0.007622}
