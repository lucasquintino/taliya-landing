# Spec 012 Manual Transcript Review Package

- Schema: 012.manual_transcript_review.v1
- Scenario: t012-047-mocked-manual-transcript-review
- Proof mode: mocked_no_cost
- Review status: pending_manual_review
- Manual decision: pending
- Turn count: 4
- Delivered turns: 3
- Suppressed turns: 1
- Total model operations: 5
- Total cost USD: 0.0

## Checklist

- [ ] answers_direct_questions_first: Direct questions are answered before steering (status: pending)
- [ ] studio_owner_language: Language sounds natural for a Pilates studio owner (status: pending)
- [ ] official_facts_only: Prices, demo link, availability, and product claims use official facts (status: pending)
- [ ] diagnostic_flow_quality: Diagnostic questions progress naturally without repeats (status: pending)
- [ ] final_diagnostic_quality: Final diagnostic is complete, practical, and not truncated (status: pending)
- [ ] handoff_and_suppression: Human handoff pauses AI replies after acknowledgement (status: pending)
- [ ] no_unsafe_promises: No checkout, discount, VIP, date, or integration promises are invented (status: pending)

## Transcript

**USER:** quanto custa?

**ASSISTANT:** Oi, tudo bem?

Base: R$ 197/mes. Essencial: R$ 497/mes. Avance: R$ 897/mes. Completo: R$ 1.497/mes.

**ASSISTANT:** Se fizer sentido para voce, estamos oferecendo um diagnostico gratuito para o seu studio. Assim voce entende se algum dos nossos planos te atenderia.

Com poucas perguntas, eu entendo a rotina do studio e te devolvo o que organizar primeiro, quais agentes fariam sentido e qual plano vale comparar.

**ASSISTANT:** O que voce acha?

**USER:** quero fazer o diagnostico gratuito

**ASSISTANT:** Claro, faco sim. Pra te devolver algo util, vou entender rapidinho como esta a rotina do studio hoje.

**ASSISTANT:** Hoje seu studio tem mais ou menos quantos alunos ativos?

**USER:** prefiro falar com uma pessoa

**ASSISTANT:** Claro. Vou deixar uma pessoa assumir daqui.

**ASSISTANT:** Tambem deixo o contexto salvo para voce nao precisar repetir tudo.

## Turn Summary

- Turn 0: delivered / entry / answer_direct_product_question / product.price_direct, diagnostic.price_hook / trace=True / projection=True
- Turn 1: delivered / entry / start_requested_diagnostic / diagnostic.start, diagnostic.ask_active_students / trace=True / projection=True
- Turn 2: delivered / diagnostic / handoff_requested / handoff.acknowledge / trace=True / projection=True
- Turn 3: suppressed / handoff /  /  / trace=False / projection=False
