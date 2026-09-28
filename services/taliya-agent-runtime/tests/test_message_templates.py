import pytest

from app.domains.taliya_commercial.templates import (
    get_template,
    required_template_ids,
    template_allowed_in_state,
)


def test_required_template_registry_contains_contract_ids():
    required = required_template_ids()

    assert "opening.cold_greeting" in required
    assert "opening.widget_empty_diagnostic" in required
    assert "product.price_direct" in required
    assert "product.price_complete_direct" in required
    assert "diagnostic.price_hook" in required
    assert "diagnostic.price_hook_with_context" in required
    assert "diagnostic.ask_main_pain" in required
    assert "waitlist.offer_after_contract_intent" in required
    assert "waitlist.status_preserved" in required
    assert "fallback.unmapped_adaptive" in required


def test_product_followup_delta_templates_are_registered_with_sources():
    required = required_template_ids()

    for template_id in (
        "product.how_it_works_direct",
        "product.comparison_current_tool",
        "product.integration_scope_direct",
        "product.security_data_direct",
        "product.out_of_profile_redirect",
    ):
        assert template_id in required

    assert "how_it_works" in get_template("product.how_it_works_direct").product_keys
    assert "comparison_spreadsheet" in get_template("product.comparison_current_tool").product_keys
    assert "integration_scope" in get_template("product.integration_scope_direct").product_keys
    assert "security_and_data" in get_template("product.security_data_direct").product_keys
    assert "out_of_profile" in get_template("product.out_of_profile_redirect").product_keys


def test_template_allowed_states_are_enforced():
    assert template_allowed_in_state("opening.cold_greeting", "greeting_only")
    assert not template_allowed_in_state("waitlist.offer_after_contract_intent", "greeting_only")
    assert template_allowed_in_state("waitlist.status_preserved", "product_question")


def test_unknown_template_id_is_rejected():
    with pytest.raises(ValueError):
        get_template("not.real")


def test_price_template_requires_product_knowledge():
    template = get_template("product.price_direct")

    assert "prices" in template.product_keys
    assert template.max_chars_per_chunk <= 320


def test_widget_empty_opening_template_matches_product_owner_copy():
    template = get_template("opening.widget_empty_diagnostic")

    assert template.channel_support == "widget"
    assert template.max_messages == 3
    assert template.body == (
        "Oi, tudo bem?",
        "Em que posso ajudar?",
        "Se fizer sentido pra você, estamos oferecendo um diagnóstico gratuito pro seu studio. O que você acha?",
    )


def test_plan_fit_template_matches_product_owner_copy_without_repetition():
    template = get_template("product.plan_fit_with_diagnostic")

    assert template.max_messages == 3
    assert template.required_variables == ("plan_fit_context",)
    assert template.body == (
        "{plan_fit_context}",
        "Posso fazer um diagnóstico gratuito com poucas perguntas e te devolver o que organizar primeiro, quais agentes fariam sentido e qual plano vale comparar.",
        "O que você acha?",
    )


def test_demo_and_whatsapp_templates_use_official_full_link():
    demo = get_template("product.demo_direct")
    whatsapp = get_template("product.whatsapp_direct")

    assert "https://www.taliya.com.br/pilates/planos/demonstracao" in "\n".join(demo.body)
    assert "demo_contextual_next_step" in "\n".join(demo.body)
    assert "não precisa baixar aplicativo" in "\n".join(whatsapp.body)
    assert "https://www.taliya.com.br/pilates/planos/demonstracao" in "\n".join(whatsapp.body)


def test_product_followup_templates_do_not_use_crm_as_lay_explanation():
    for template_id in (
        "product.how_it_works_direct",
        "product.comparison_current_tool",
        "product.integration_scope_direct",
        "product.security_data_direct",
        "product.out_of_profile_redirect",
        "product.price_objection_value",
    ):
        assert "crm" not in "\n".join(get_template(template_id).body).lower()
