import pytest

from app.domains.taliya_commercial.renderer import RenderError, render_template, render_template_plan


def test_renderer_returns_template_tagged_messages():
    messages = render_template("product.price_direct", channel="widget")

    assert messages
    assert all(message.template_id == "product.price_direct" for message in messages)
    assert messages[0].requires_product_source is True


def test_renderer_caps_whatsapp_plan_to_three_chunks():
    messages = render_template_plan(
        ["opening.general_interest", "diagnostic.offer_soft"],
        channel="whatsapp",
        variables_by_template={
            "diagnostic.offer_soft": {
                "pain_context": "Para te orientar sem chutar, preciso entender um pouco da rotina do studio.",
            }
        },
    )

    assert 1 <= len(messages) <= 3
    assert all(message.channel_hint == "whatsapp" for message in messages)


def test_renderer_requires_template_variables():
    with pytest.raises(RenderError):
        render_template("diagnostic.deliver", channel="widget")


def test_renderer_fills_diagnostic_delivery_variables():
    messages = render_template_plan(
        [
            "diagnostic.deliver_hold",
            "diagnostic.deliver_context",
            "diagnostic.deliver_crm_base",
            "diagnostic.deliver_operational_step",
            "diagnostic.deliver_agent_recommendation",
            "diagnostic.deliver_plan_recommendation",
            "diagnostic.deliver_demo_not_offered",
        ],
        channel="widget",
        variables_by_template={
            "diagnostic.deliver_context": {
                "pain_context_human": "Então, Lucas, o que mais pesa hoje é perder interessados no WhatsApp antes da equipe responder.",
            },
            "diagnostic.deliver_crm_base": {
                "crm_base_recommendation": "Antes dos agentes, eu organizaria tudo em um só lugar: contatos, conversas, situação de cada interessado e próximos passos.",
            },
            "diagnostic.deliver_operational_step": {
                "operational_first_step": "O primeiro passo é separar novos interessados, retornos pendentes e conversas paradas.",
            },
            "diagnostic.deliver_agent_recommendation": {
                "agent_name": "Atendimento",
                "agent_fit_phrase": "faria sentido primeiro",
                "agent_pain_resolved": "demora no retorno",
                "agent_recommendation_reason": "essa foi a dor mais clara do diagnóstico",
                "agent_practical_action": "ele responde, registra contexto e avisa a equipe quando precisa de humano",
            },
            "diagnostic.deliver_plan_recommendation": {
                "recommended_plan_or_range": "Avance ou Completo",
            },
        },
    )

    rendered = "\n".join(message.text for message in messages)
    assert messages[0].template_id == "diagnostic.deliver_hold"
    assert "perder interessados" in rendered
    assert "Antes dos agentes" in rendered
    assert "Agente Atendimento faria sentido primeiro" in rendered
    assert "Pelo tamanho, momento do studio e todo o contexto acima" in rendered
    assert "eu recomendaria pra você o plano Avance ou Completo" in rendered
    assert "Temos algumas demonstrações que mostram o funcionamento na prática" in rendered
    assert "gargalo principal" not in rendered
    assert "Para plano, eu compararia" not in rendered
    assert "Isso faz sentido para o momento do seu studio" not in rendered


def test_renderer_preserves_widget_empty_opening_copy():
    messages = render_template("opening.widget_empty_diagnostic", channel="widget")

    assert [message.text for message in messages] == [
        "Oi, tudo bem?",
        "Em que posso ajudar?",
        "Se fizer sentido pra você, estamos oferecendo um diagnóstico gratuito pro seu studio. O que você acha?",
    ]
    assert all(message.template_id == "opening.widget_empty_diagnostic" for message in messages)


def test_renderer_marks_widget_demo_link_as_action():
    widget_messages = render_template("product.demo_direct", channel="widget")
    whatsapp_messages = render_template("product.demo_direct", channel="whatsapp")

    assert widget_messages[0].kind == "action"
    assert whatsapp_messages[0].kind == "text"


def test_renderer_allows_staged_completed_diagnostic_beyond_three_chunks():
    messages = render_template_plan(
        [
            "diagnostic.deliver_hold",
            "diagnostic.deliver_context",
            "diagnostic.deliver_crm_base",
            "diagnostic.deliver_operational_step",
            "diagnostic.deliver_agent_recommendation",
            "diagnostic.deliver_agent_recommendation",
            "diagnostic.deliver_plan_recommendation",
            "diagnostic.deliver_demo_already_offered",
        ],
        channel="whatsapp",
        variables_by_template={
            "diagnostic.deliver_context": {
                "pain_context_human": "Então, Lucas, o principal peso hoje parece ser agenda e reposições escapando.",
            },
            "diagnostic.deliver_crm_base": {
                "crm_base_recommendation": "Eu começaria organizando tudo em um só lugar: alunos, faltas e reposições.",
            },
            "diagnostic.deliver_operational_step": {
                "operational_first_step": "O primeiro passo é transformar faltas e reposições em fila clara de ação.",
            },
            "diagnostic.deliver_agent_recommendation": {
                "agent_name": "Agenda",
                "agent_fit_phrase": "faria sentido primeiro",
                "agent_pain_resolved": "reposições perdidas",
                "agent_recommendation_reason": "a agenda apareceu como prioridade",
                "agent_practical_action": "ele acompanha faltas e próximos encaixes",
            },
            "diagnostic.deliver_plan_recommendation": {
                "recommended_plan_or_range": "Avance",
            },
        },
    )

    assert len(messages) > 3
    assert messages[-1].text == "Chegou a olhar as demonstrações? O que você achou?"


def test_renderer_uses_occurrence_specific_variables_for_repeated_templates():
    messages = render_template_plan(
        [
            "diagnostic.deliver_agent_recommendation",
            "diagnostic.deliver_agent_recommendation",
        ],
        channel="widget",
        variables_by_template={
            "diagnostic.deliver_agent_recommendation": {
                "agent_name": "Atendimento",
                "agent_fit_phrase": "faria sentido primeiro",
                "agent_pain_resolved": "demora no retorno",
                "agent_recommendation_reason": "atendimento foi a dor mais clara",
                "agent_practical_action": "ele responde e registra contexto",
            },
            "diagnostic.deliver_agent_recommendation#2": {
                "agent_name": "Vendas",
                "agent_fit_phrase": "também faria sentido",
                "agent_pain_resolved": "follow-up",
                "agent_recommendation_reason": "vendas apareceu como prioridade",
                "agent_practical_action": "ele acompanha interessados",
            },
        },
    )

    assert "Atendimento" in messages[0].text
    assert "Vendas" in messages[1].text


def test_renderer_fills_product_how_it_works_contextual_next_step():
    messages = render_template(
        "product.how_it_works_direct",
        channel="whatsapp",
        variables={
            "contextual_next_step": "Se fizer sentido para você, estamos oferecendo um diagnóstico gratuito para entender como isso encaixaria na rotina do seu studio. O que você acha?",
        },
    )
    text = "\n".join(message.text for message in messages)

    assert len(messages) == 4
    assert "organizar o que acontece no dia a dia" in text
    assert "WhatsApp Business do studio" in text
    assert "diagnóstico gratuito" in text
    assert "CRM" not in text


def test_renderer_keeps_product_followup_templates_short_and_channel_safe():
    for template_id in (
        "product.comparison_current_tool",
        "product.integration_scope_direct",
        "product.security_data_direct",
        "product.out_of_profile_redirect",
    ):
        messages = render_template(template_id, channel="widget")
        assert 1 <= len(messages) <= 3
        assert all(len(message.text) <= 320 for message in messages)
        assert all(message.kind == "text" for message in messages)


def test_diagnostic_question_can_render_grounded_feedback_before_question():
    messages = render_template(
        "diagnostic.ask_priority",
        channel="widget",
        variables={
            "answer_feedback": "Boa, 90 alunos já mostram que a rotina precisa ser organizada sem depender de memória.",
        },
    )

    assert [message.text for message in messages] == [
        "Boa, 90 alunos já mostram que a rotina precisa ser organizada sem depender de memória.",
        "Pensando na rotina do studio, qual tarefa você mais gostaria de deixar mais leve primeiro?",
    ]
