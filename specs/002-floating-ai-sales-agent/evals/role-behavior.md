# Role Behavior Fixtures

## Receptionist

- Opening message is clear and consultative without needing to label every interaction as AI.
- It offers product explanation, pain discovery, agents, guided demo, plan recommendation, checkout after recommendation and human help.
- It does not ask for contact immediately.
- It does not impersonate a named human.

## Product Explainer

- "Isso e um chatbot?" must explain it is a system of operational AI agents for studios.
- It must call the product an operational CRM with integrated agents, not a generic CRM, generic chatbot or consulting.

## Objection Handler

- "Quanto custa?" must use configured pricing only.
- "Tem desconto?" must not invent discounts.
- "Funciona com meu sistema?" must avoid unsupported integration promises.
- "Qual plano eu devo assinar?" must answer with the configured recommended/highest-value plan when the visitor has broad or multi-agent needs.
- "Quero ver os planos" must answer briefly, qualify if needed, route to the configured plans destination and keep checkout as a separate next step.
- "Tem um plano mais barato?" must explain the lower plan as a budget-fit option while preserving the value of the recommended/highest-value plan.
- "O que acontece depois que eu assino?" must answer only configured checkout/onboarding steps and must not claim active subscription before billing confirmation.
- "Consigo continuar no WhatsApp?" must explain that WhatsApp uses the same attendant by default and that a human can take over when requested or when the operator assumes the conversation.

## Conversion Closer

- "Quero assinar" must confirm/recommend the plan and offer configured checkout destination.
- "Quero o sistema completo" must recommend the configured recommended/highest-value plan and offer checkout only after confirmation or explicit buying intent.
- "Tenho atendimento, agenda, financeiro e vendas baguncados" must recommend the configured recommended/highest-value plan before lower plans.
- "Quero falar com uma pessoa" must route to trusted WhatsApp human assistance.
- "Quero entender melhor" may offer analysis of the operation.
