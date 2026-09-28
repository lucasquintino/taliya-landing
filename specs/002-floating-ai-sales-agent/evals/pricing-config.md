# Pricing And Config Alignment Fixtures

## Price Answers

- If `subscription.plans` contains Base, 1 Agente, 3 Agentes and 7 Agentes, the agent may quote their configured labels.
- If the recommended plan changes in config, the plan recommendation and checkout CTA must use the new recommended plan.
- If the visitor has broad pain, multiple relevant agents or asks for the complete system, the agent must recommend the configured recommended/highest-value plan before lower plans.
- If the visitor asks to see or compare plans, the agent must route to the configured plans destination and must not treat that as active subscription.
- If the visitor asks for the cheapest or narrowest option, the agent may explain a lower plan but must frame it as budget-fit/narrow-scope instead of the default best recommendation.
- Lower plans must be used for comparison, objection handling or fallback, not as equal default outcomes when the recommended/highest-value plan fits.
- If a checkout URL changes in config, the agent response must use the changed trusted destination.
- If pricing is missing from config, the agent must not invent a price and should offer analysis or human WhatsApp assistance.

## Negative Checks

- No prompt or component fallback text may hardcode plan prices.
- No model-generated arbitrary checkout URL is accepted.
- No model-generated arbitrary plans page URL is accepted.
- WhatsApp human destination must come from `assistedConversion.humanWhatsAppDestination`.
