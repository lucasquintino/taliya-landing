import { assert, readText, writeReport } from "./eval-agent-runtime-utils.mjs";

const floatingAgent = readText("lib/landing/floating-agent.ts");
const widgetRoute = readText("app/api/landing/ai-attendant/route.ts");
const whatsappRoute = readText("app/api/landing/ai-attendant/whatsapp/route.ts");
const runtimeClient = readText("lib/landing/ai-attendant/runtime-client.ts");
const v2Loop = readText("lib/landing/ai-attendant/agent-v2-loop.ts");
const productSource = readText("services/taliya-agent-runtime/app/shared/product_knowledge/source.py");
const validators = readText("services/taliya-agent-runtime/app/shared/guardrails/validators.py");
const runner = readText("services/taliya-agent-runtime/app/runtime/runner.py");
const state = readText("services/taliya-agent-runtime/app/domains/taliya_commercial/state.py");
const templates = readText("services/taliya-agent-runtime/app/domains/taliya_commercial/templates.py");
const ledger = readText("services/taliya-agent-runtime/app/domains/taliya_commercial/diagnostic_ledger.py");

const results = [
  assert(floatingAgent.includes("runTaliyaCommercialRuntimeTurn"), "floating-agent delegates to runtime client"),
  assert(!floatingAgent.includes("runAiAttendantTurnV2"), "floating-agent does not import old v2 loop"),
  assert(!floatingAgent.includes("legacyTurn"), "floating-agent has no legacy fallback hook"),
  assert(widgetRoute.includes("runtime-client"), "widget route imports runtime client"),
  assert(whatsappRoute.includes("runtime-client"), "WhatsApp route imports runtime client"),
  assert(runtimeClient.includes("x-taliya-agent-signature"), "runtime client signs HMAC requests"),
  assert(runtimeClient.includes("createOperationalFallbackResponse"), "runtime client has operational fallback"),
  assert(!runtimeClient.includes("agent-v2-loop"), "runtime client does not import old v2 loop"),
  assert(!runtimeClient.includes("runAiAttendantTurnLegacy"), "runtime client does not call legacy turn"),
  assert(v2Loop.includes("Quarantined legacy runtime"), "old v2 loop is explicitly quarantined"),
  assert(
    productSource.includes("\"demonstration\": \"https://www.taliya.com.br/pilates/planos/demonstracao\""),
    "official demo link is product-sourced",
  ),
  assert(productSource.includes("checkout_status: str = \"unavailable\""), "checkout unavailable is product-sourced"),
  assert(validators.includes("invented_checkout"), "output validators block invented checkout"),
  assert(validators.includes("missing_product_source"), "output validators require product source"),
  assert(runner.includes("Runner.run"), "non-mock runtime path invokes OpenAI Agents SDK Runner"),
  assert(runner.includes("output_type=AgentOutputSchema(LLMStructuredDraft"), "non-mock runtime path requests structured LLM output"),
  assert(runner.includes("render_template_plan"), "non-mock runtime path renders selected template IDs"),
  assert(state.includes("ConversationState"), "canonical conversation states are implemented"),
  assert(templates.includes("TEMPLATE_REGISTRY"), "approved template registry is implemented"),
  assert(templates.includes("product.how_it_works_direct"), "product how-it-works template is registered"),
  assert(templates.includes("product.comparison_current_tool"), "current-tool comparison template is registered"),
  assert(templates.includes("product.integration_scope_direct"), "integration scope template is registered"),
  assert(templates.includes("product.security_data_direct"), "security/data template is registered"),
  assert(templates.includes("product.out_of_profile_redirect"), "out-of-profile template is registered"),
  assert(productSource.includes("how_it_works"), "product knowledge includes how-it-works facts"),
  assert(productSource.includes("integration_scope"), "product knowledge includes integration scope facts"),
  assert(productSource.includes("security_and_data"), "product knowledge includes security/data facts"),
  assert(runner.includes("product_how_it_works"), "runner supports LLM-selected product-followup intents"),
  assert(runner.includes("post_diagnostic_context"), "runner passes compact post-diagnostic context to the LLM"),
  assert(runner.includes("Runner.run") && runner.includes("product_how_it_works"), "product-followup commercial routes stay on the LLM runner path"),
  assert(ledger.includes("REQUIRED_QUESTION_KEYS"), "diagnostic ledger required questions are implemented"),
  assert(validators.includes("diagnostic_ledger_incomplete"), "validators block completed diagnostics with incomplete ledger"),
  assert(validators.includes("message_template_mismatch"), "validators block messages outside selected templates"),
];

writeReport("agent-runtime-invariants", results);
