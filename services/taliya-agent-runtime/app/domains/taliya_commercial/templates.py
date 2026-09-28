from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal


ChannelSupport = Literal["widget", "whatsapp", "both"]


@dataclass(frozen=True)
class MessageTemplate:
    template_id: str
    category: str
    allowed_states: tuple[str, ...]
    channel_support: ChannelSupport = "both"
    required_variables: tuple[str, ...] = ()
    optional_variables: tuple[str, ...] = ()
    product_keys: tuple[str, ...] = ()
    max_messages: int = 1
    max_chars_per_chunk: int = 320
    buttons_allowed: bool = False
    official_links_allowed: bool = False
    body: tuple[str, ...] = field(default_factory=tuple)


ANY_STATE = ("*",)
DIAGNOSTIC_STATES = ("diagnostic_requested", "diagnostic_offered", "diagnostic_in_progress", "diagnostic_waiting_answer")
PRODUCT_STATES = ("product_question", "price_question", "plan_question", "demo_question", "general_interest")
WAITLIST_STATES = ("buying_intent_detected", "waitlist_eligible", "waitlist_offered", "waitlist_pending_data")


TEMPLATE_REGISTRY: dict[str, MessageTemplate] = {
    "opening.cold_greeting": MessageTemplate(
        "opening.cold_greeting",
        "opening",
        ("new_lead", "greeting_only"),
        body=("Oi, tudo bem?", "Em que posso te ajudar?"),
        max_messages=2,
    ),
    "opening.cold_greeting_named": MessageTemplate(
        "opening.cold_greeting_named",
        "opening",
        ("new_lead", "greeting_only"),
        required_variables=("first_name",),
        body=("Oi, {first_name}, tudo bem?", "Em que posso te ajudar?"),
        max_messages=2,
    ),
    "opening.general_interest": MessageTemplate(
        "opening.general_interest",
        "opening",
        ("general_interest", "new_lead"),
        body=(
            "A Taliya é a IA do seu studio de Pilates.",
            "Você cuida dos alunos; ela ajuda a cuidar da rotina que faz o studio girar: agenda, reposições, cobranças, gestão, atendimento e acompanhamento em um só lugar.",
            "Você quer entender a ideia geral primeiro ou tem alguma rotina específica pesando hoje?",
        ),
        max_messages=3,
    ),
    "opening.widget_empty_diagnostic": MessageTemplate(
        "opening.widget_empty_diagnostic",
        "opening",
        ("general_interest", "diagnostic_offered", "new_lead"),
        channel_support="widget",
        body=(
            "Oi, tudo bem?",
            "Em que posso ajudar?",
            "Se fizer sentido pra você, estamos oferecendo um diagnóstico gratuito pro seu studio. O que você acha?",
        ),
        max_messages=3,
    ),
    "opening.instagram_source": MessageTemplate(
        "opening.instagram_source",
        "opening",
        ("source_instagram", "general_interest"),
        body=(
            "A Taliya é a IA do seu studio de Pilates.",
            "Você cuida dos alunos; ela ajuda a cuidar da rotina que faz o studio girar: agenda, reposições, cobranças, gestão, atendimento e acompanhamento em um só lugar.",
            "Se fizer sentido para você, estamos oferecendo um diagnóstico gratuito para o seu studio. Assim podemos entender se conseguimos te atender ou não. O que você acha?",
        ),
        max_messages=3,
    ),
    "opening.site_cta": MessageTemplate(
        "opening.site_cta",
        "opening",
        ("general_interest", "new_lead"),
        body=(
            "Claro, posso te ajudar com isso sim.",
            "Resumindo... A Taliya é a IA do seu studio de Pilates: você cuida dos alunos, e ela ajuda na rotina que faz o studio girar: agenda, reposições, cobranças, gestão, atendimento e acompanhamento.",
            "Pra te orientar sem chutar, posso fazer um diagnóstico gratuito com poucas perguntas e te devolver por onde começar. O que você acha?",
        ),
        max_messages=3,
    ),
    "opening.diagnostic_cta": MessageTemplate(
        "opening.diagnostic_cta",
        "opening",
        ("diagnostic_requested", "diagnostic_offered", "diagnostic_in_progress"),
        body=("Claro, faço sim.", "Pra te devolver algo útil, vou entender rapidinho como está a rotina do studio hoje."),
        max_messages=2,
    ),
    "product.overview_short": MessageTemplate(
        "product.overview_short",
        "product",
        PRODUCT_STATES,
        product_keys=("overview",),
        body=("A Taliya é a IA do seu studio de Pilates: ela ajuda a organizar agenda, reposições, cobranças, gestão, atendimento e acompanhamento em um só lugar.",),
    ),
    "product.price_direct": MessageTemplate(
        "product.price_direct",
        "product",
        PRODUCT_STATES,
        product_keys=("plans", "prices"),
        body=("Hoje os planos são Base R$ 197/mês, Essencial R$ 497/mês, Avance R$ 897/mês e Completo R$ 1.497/mês.",),
    ),
    "product.price_complete_direct": MessageTemplate(
        "product.price_complete_direct",
        "product",
        PRODUCT_STATES,
        product_keys=("plans", "prices"),
        body=("O Completo fica em R$ 1.497/mês.",),
    ),
    "product.price_objection_value": MessageTemplate(
        "product.price_objection_value",
        "product",
        ANY_STATE,
        required_variables=("value_context", "next_step"),
        product_keys=("plans", "prices", "plan_comparison"),
        body=(
            "Entendo. É um valor para olhar com calma mesmo. {value_context}",
            "{next_step}",
        ),
        max_messages=3,
    ),
    "product.plan_direct": MessageTemplate(
        "product.plan_direct",
        "product",
        PRODUCT_STATES,
        product_keys=("plans", "prices"),
        body=("Base organiza a rotina, Essencial resolve uma dor clara primeiro, Avance cobre algumas rotinas prioritárias e Completo é para quem quer a Taliya mais completa.",),
    ),
    "product.post_diagnostic_plan_recap": MessageTemplate(
        "product.post_diagnostic_plan_recap",
        "product",
        (*PRODUCT_STATES, "post_diagnostic_questions", "diagnostic_delivered"),
        required_variables=("recommended_plan_or_range",),
        product_keys=("plans", "prices"),
        body=("Pelo diagnóstico, eu recomendaria pra você olhar o plano {recommended_plan_or_range}.",),
    ),
    "product.plan_fit_with_diagnostic": MessageTemplate(
        "product.plan_fit_with_diagnostic",
        "product",
        PRODUCT_STATES,
        required_variables=("plan_fit_context",),
        product_keys=("plans", "prices"),
        body=(
            "{plan_fit_context}",
            "Posso fazer um diagnóstico gratuito com poucas perguntas e te devolver o que organizar primeiro, quais agentes fariam sentido e qual plano vale comparar.",
            "O que você acha?",
        ),
        max_messages=3,
    ),
    "product.demo_direct": MessageTemplate(
        "product.demo_direct",
        "product",
        PRODUCT_STATES,
        product_keys=("demo", "links"),
        buttons_allowed=True,
        official_links_allowed=True,
        required_variables=("demo_contextual_next_step",),
        body=(
            "Ver demonstração: https://www.taliya.com.br/pilates/planos/demonstracao",
            "{demo_contextual_next_step}",
        ),
        max_messages=2,
    ),
    "product.whatsapp_direct": MessageTemplate(
        "product.whatsapp_direct",
        "product",
        PRODUCT_STATES,
        product_keys=("links",),
        official_links_allowed=True,
        body=(
            "O aluno não precisa baixar aplicativo nem criar senha. Ele conversa no WhatsApp; a Taliya registra a ação, atualiza o painel e avisa o responsável.",
            "Temos uma demonstração para você entender melhor: https://www.taliya.com.br/pilates/planos/demonstracao",
        ),
        max_messages=2,
    ),
    "product.how_it_works_direct": MessageTemplate(
        "product.how_it_works_direct",
        "product",
        (*PRODUCT_STATES, "diagnostic_in_progress", "diagnostic_delivered", "waitlist_joined"),
        required_variables=("contextual_next_step",),
        optional_variables=("recommended_area",),
        product_keys=("how_it_works", "routine_areas", "whatsapp_scope"),
        body=(
            "Funciona assim: a Taliya ajuda o studio a organizar o que acontece no dia a dia.",
            "Ela junta conversas, alunos, agenda, reposições, cobranças, interessados e acompanhamentos para a equipe enxergar melhor o que precisa de ação.",
            "Quando o WhatsApp Business do studio está conectado, os agentes podem apoiar conversas com alunos e interessados, sempre com a equipe podendo acompanhar e assumir quando precisar.",
            "{contextual_next_step}",
        ),
        max_messages=5,
    ),
    "product.comparison_current_tool": MessageTemplate(
        "product.comparison_current_tool",
        "product",
        (*PRODUCT_STATES, "diagnostic_delivered", "waitlist_joined"),
        required_variables=("current_tool_context",),
        product_keys=("comparison_spreadsheet", "comparison_management_system", "routine_areas"),
        body=(
            "Se hoje vocês usam {current_tool_context}, faz sentido manter o que funciona.",
            "A diferença da Taliya é ajudar a organizar o que costuma ficar espalhado: conversas, agenda, reposições, cobranças, interessados e acompanhamento dos alunos.",
            "Para comparar sem chute, vale olhar onde a rotina do seu studio mais perde tempo hoje.",
        ),
        max_messages=3,
    ),
    "product.integration_scope_direct": MessageTemplate(
        "product.integration_scope_direct",
        "product",
        (*PRODUCT_STATES, "diagnostic_delivered", "waitlist_joined"),
        required_variables=("integration_topic",),
        product_keys=("whatsapp_scope", "integration_scope", "unsupported_claims"),
        body=(
            "Sobre {integration_topic}, eu não quero te prometer uma integração sem confirmar com a equipe.",
            "Mas mesmo quando o studio já usa outro sistema, a Taliya entra para organizar a rotina que acontece no dia a dia: conversas, agenda, reposições, cobranças, atendimento e acompanhamento.",
            "Se {integration_topic} é importante na sua operação, eu deixo esse ponto anotado e posso te mostrar o que a Taliya faria por fora ou junto da rotina atual.",
        ),
        max_messages=3,
    ),
    "product.whatsapp_business_requirement": MessageTemplate(
        "product.whatsapp_business_requirement",
        "product",
        (*PRODUCT_STATES, "diagnostic_delivered", "waitlist_joined"),
        product_keys=("whatsapp_scope",),
        body=(
            "Sim. Para os agentes atuarem no WhatsApp dos alunos e interessados, o studio precisa ter WhatsApp Business.",
            "A ideia é que o aluno continue conversando pelo WhatsApp, sem baixar app nem criar senha, e a Taliya ajude a registrar, organizar e avisar a equipe quando precisar.",
            "Se quiser, posso te mostrar uma demonstração desse fluxo na prática.",
        ),
        max_messages=3,
    ),
    "product.security_data_direct": MessageTemplate(
        "product.security_data_direct",
        "product",
        (*PRODUCT_STATES, "diagnostic_delivered", "waitlist_joined"),
        product_keys=("security_and_data", "privacy_or_data_notes"),
        body=(
            "Sim, esse é um ponto importante.",
            "Por aqui eu não preciso que você envie dados sensíveis dos alunos. A conversa pode ficar no nível da rotina do studio.",
            "Sobre segurança, privacidade e LGPD, a Taliya deve tratar esses dados com cuidado e seguir as informações oficiais do produto. Se você quiser validar algum ponto específico, eu deixo isso anotado para a equipe responder com precisão.",
        ),
        max_messages=3,
    ),
    "product.out_of_profile_redirect": MessageTemplate(
        "product.out_of_profile_redirect",
        "product",
        ANY_STATE,
        product_keys=("out_of_profile",),
        body=(
            "Hoje a Taliya é pensada principalmente para studios de Pilates.",
            "Se você é aluno, professor autônomo ou está falando de outro tipo de negócio, me conta rapidinho o contexto para eu não te orientar errado.",
        ),
        max_messages=2,
    ),
    "product.crm_direct": MessageTemplate(
        "product.crm_direct",
        "product",
        PRODUCT_STATES,
        body=("A Taliya funciona como CRM para organizar leads, alunos, conversas, agenda e rotinas comerciais do studio.",),
    ),
    "product.agents_direct": MessageTemplate(
        "product.agents_direct",
        "product",
        PRODUCT_STATES,
        body=("Os agentes entram para apoiar rotinas como atendimento, vendas, agenda, financeiro e retenção, sempre com regras e contexto do studio.",),
    ),
    "diagnostic.price_hook": MessageTemplate(
        "diagnostic.price_hook",
        "diagnostic",
        ("product_question", "price_question", "plan_question", "general_interest"),
        body=(
            "Se fizer sentido para você, estamos oferecendo um diagnóstico gratuito para o seu studio. Assim você entende se algum dos nossos planos te atenderia. O que você acha?",
        ),
        max_messages=1,
    ),
    "diagnostic.price_hook_with_context": MessageTemplate(
        "diagnostic.price_hook_with_context",
        "diagnostic",
        ("product_question", "price_question", "plan_question", "general_interest"),
        required_variables=("pain_context",),
        body=(
            "{pain_context}",
            "Se fizer sentido, faço um diagnóstico gratuito para entender se algum dos nossos planos te atenderia. O que você acha?",
        ),
        max_messages=2,
    ),
    "diagnostic.offer_soft": MessageTemplate(
        "diagnostic.offer_soft",
        "diagnostic",
        ("general_interest", "pain_detected", "product_question", "price_question", "plan_question", "diagnostic_offered", "diagnostic_in_progress"),
        required_variables=("pain_context",),
        body=("{pain_context}", "Posso fazer um diagnóstico gratuito com poucas perguntas e te devolver o que organizar primeiro, quais agentes fariam sentido e qual plano vale comparar.", "O que você acha?"),
        max_messages=3,
    ),
    "diagnostic.start": MessageTemplate(
        "diagnostic.start",
        "diagnostic",
        DIAGNOSTIC_STATES,
        body=("Claro, faço sim. Pra te devolver algo útil, vou entender rapidinho como está a rotina do studio hoje.",),
    ),
    "diagnostic.ask_active_students": MessageTemplate("diagnostic.ask_active_students", "diagnostic", DIAGNOSTIC_STATES, optional_variables=("answer_feedback",), body=("Hoje seu studio tem mais ou menos quantos alunos ativos?",), max_messages=2),
    "diagnostic.ask_main_pain": MessageTemplate("diagnostic.ask_main_pain", "diagnostic", DIAGNOSTIC_STATES, optional_variables=("answer_feedback",), body=("Quais partes mais dão trabalho hoje: WhatsApp, agenda/reposições, vendas, financeiro ou acompanhamento dos alunos?",), max_messages=2),
    "diagnostic.ask_current_process": MessageTemplate("diagnostic.ask_current_process", "diagnostic", DIAGNOSTIC_STATES, optional_variables=("answer_feedback",), body=("Hoje isso fica em algum sistema ou mais em WhatsApp, planilha e caderno?",), max_messages=2),
    "diagnostic.ask_pain_detail": MessageTemplate("diagnostic.ask_pain_detail", "diagnostic", DIAGNOSTIC_STATES, optional_variables=("answer_feedback",), body=("Hoje você consegue ver facilmente o que precisa ser resolvido no dia?",), max_messages=2),
    "diagnostic.ask_priority": MessageTemplate("diagnostic.ask_priority", "diagnostic", DIAGNOSTIC_STATES, optional_variables=("answer_feedback",), body=("Pensando na rotina do studio, qual tarefa você mais gostaria de deixar mais leve primeiro?",), max_messages=2),
    "diagnostic.ask_urgency": MessageTemplate("diagnostic.ask_urgency", "diagnostic", DIAGNOSTIC_STATES, optional_variables=("answer_feedback",), body=("Vocês estão buscando resolver isso agora ou só pesquisando por enquanto?",), max_messages=2),
    "diagnostic.partial_progress": MessageTemplate("diagnostic.partial_progress", "diagnostic", DIAGNOSTIC_STATES, body=("Já tenho parte do contexto. Falta só um ponto para não te devolver um diagnóstico chutado.",)),
    "diagnostic.deliver": MessageTemplate("diagnostic.deliver", "diagnostic", ("diagnostic_ready", "diagnostic_delivered"), body=("Diagnóstico pronto.",), required_variables=("legacy_blocked",), max_messages=1),
    "diagnostic.deliver_hold": MessageTemplate("diagnostic.deliver_hold", "diagnostic", ("diagnostic_ready", "diagnostic_delivered"), body=("Perfeito. Já dá pra te devolver uma leitura prática. Vou organizar em partes.",)),
    "diagnostic.deliver_context": MessageTemplate("diagnostic.deliver_context", "diagnostic", ("diagnostic_ready", "diagnostic_delivered"), required_variables=("pain_context_human",), body=("{pain_context_human}",)),
    "diagnostic.deliver_crm_base": MessageTemplate("diagnostic.deliver_crm_base", "diagnostic", ("diagnostic_ready", "diagnostic_delivered"), required_variables=("crm_base_recommendation",), body=("{crm_base_recommendation}",)),
    "diagnostic.deliver_operational_step": MessageTemplate("diagnostic.deliver_operational_step", "diagnostic", ("diagnostic_ready", "diagnostic_delivered"), required_variables=("operational_first_step",), body=("{operational_first_step}",)),
    "diagnostic.deliver_agent_recommendation": MessageTemplate(
        "diagnostic.deliver_agent_recommendation",
        "diagnostic",
        ("diagnostic_ready", "diagnostic_delivered"),
        required_variables=("agent_name", "agent_fit_phrase", "agent_pain_resolved", "agent_recommendation_reason", "agent_practical_action"),
        body=("Agente {agent_name} {agent_fit_phrase}: ele ajuda com {agent_pain_resolved}. Faz sentido aqui porque {agent_recommendation_reason}; na prática, {agent_practical_action}.",),
    ),
    "diagnostic.deliver_plan_recommendation": MessageTemplate(
        "diagnostic.deliver_plan_recommendation",
        "diagnostic",
        ("diagnostic_ready", "diagnostic_delivered"),
        required_variables=("recommended_plan_or_range",),
        body=("Pelo tamanho, momento do studio e todo o contexto acima, eu recomendaria pra você o plano {recommended_plan_or_range}.",),
    ),
    "diagnostic.deliver_demo_not_offered": MessageTemplate("diagnostic.deliver_demo_not_offered", "diagnostic", ("diagnostic_ready", "diagnostic_delivered"), body=("Temos algumas demonstrações que mostram o funcionamento na prática. Quer que eu te mande?",)),
    "diagnostic.deliver_demo_already_offered": MessageTemplate("diagnostic.deliver_demo_already_offered", "diagnostic", ("diagnostic_ready", "diagnostic_delivered"), body=("Chegou a olhar as demonstrações? O que você achou?",)),
    "diagnostic.insufficient_evidence": MessageTemplate("diagnostic.insufficient_evidence", "diagnostic", DIAGNOSTIC_STATES, body=("Ainda não tenho informação suficiente para fechar um diagnóstico sem chutar.", "Qual é a principal dor ou rotina que você quer melhorar primeiro?"), max_messages=2),
    "post_diagnostic.thinking": MessageTemplate("post_diagnostic.thinking", "product", ("product_question", "diagnostic_delivered"), product_keys=("demo", "links"), body=("Claro, sem pressa.", "Se ajudar, posso te mandar a demonstração para você olhar com calma junto com o diagnóstico que fizemos."), max_messages=2),
    "post_diagnostic.priority_update": MessageTemplate(
        "post_diagnostic.priority_update",
        "product",
        ("product_question", "diagnostic_delivered"),
        required_variables=("priority_area", "demo_area"),
        body=(
            "Faz sentido. Então eu manteria {priority_area} como prioridade principal.",
            "Nesse caso, o primeiro olhar seria para {demo_area}.",
            "Com isso, a demonstração mais útil para você é essa parte funcionando na prática.",
        ),
        max_messages=3,
    ),
    "waitlist.offer_after_contract_intent": MessageTemplate("waitlist.offer_after_contract_intent", "waitlist", WAITLIST_STATES, product_keys=("waitlist_status", "checkout_status"), body=("Estamos trabalhando com um número pequeno de studios agora.", "Se fizer sentido, posso colocar seu studio na lista de espera e chamar assim que abrir uma próxima janela."), max_messages=2),
    "waitlist.ask_missing_studio": MessageTemplate("waitlist.ask_missing_studio", "waitlist", ("waitlist_pending_data", "waitlist_offered"), body=("Combinado. Estamos trabalhando com um número pequeno de studios agora. Para registrar certinho, qual é o nome do studio?",)),
    "waitlist.ask_missing_city": MessageTemplate("waitlist.ask_missing_city", "waitlist", ("waitlist_pending_data", "waitlist_offered"), body=("E de qual cidade/estado ele é?",)),
    "waitlist.ask_missing_contact_path": MessageTemplate("waitlist.ask_missing_contact_path", "waitlist", ("waitlist_pending_data",), body=("Qual o melhor caminho para a equipe te chamar quando abrir a próxima janela?",)),
    "waitlist.joined": MessageTemplate("waitlist.joined", "waitlist", ("waitlist_joined", "waitlist_pending_data"), body=("Perfeito, deixei seu studio na lista de espera da Taliya.", "Quando abrir uma próxima janela, a equipe chama com o contexto dessa conversa."), max_messages=2),
    "waitlist.pause_decision": MessageTemplate(
        "waitlist.pause_decision",
        "waitlist",
        ("waitlist_offered", "waitlist_pending_data"),
        body=("Claro. O que você quer entender melhor antes de decidir?",),
    ),
    "waitlist.status_preserved": MessageTemplate(
        "waitlist.status_preserved",
        "waitlist",
        ("product_question", "waitlist_joined"),
        product_keys=("waitlist_status",),
        body=("Seu studio continua registrado na lista de espera.",),
    ),
    "waitlist.resume_missing_studio": MessageTemplate(
        "waitlist.resume_missing_studio",
        "waitlist",
        ("product_question", "waitlist_pending_data"),
        product_keys=("waitlist_status",),
        body=("E para deixar sua lista certinha, ainda preciso do nome do studio.",),
    ),
    "handoff.acknowledge": MessageTemplate("handoff.acknowledge", "handoff", ("human_requested", "human_handoff"), body=("Claro. Vou deixar uma pessoa assumir daqui.", "Também deixo o contexto salvo para você não precisar repetir tudo."), max_messages=2),
    "handoff.paused": MessageTemplate("handoff.paused", "handoff", ("human_handoff", "paused_by_human"), body=()),
    "fallback.invalid_json": MessageTemplate("fallback.invalid_json", "fallback", ANY_STATE, body=("Tive uma instabilidade para organizar a resposta. Vou deixar sua mensagem registrada para a equipe continuar com seguranca.",)),
    "fallback.provider_timeout": MessageTemplate("fallback.provider_timeout", "fallback", ANY_STATE, body=("Estou com uma instabilidade aqui. Sua mensagem ficou registrada para a equipe da Taliya continuar com seguranca.",)),
    "fallback.product_knowledge_missing": MessageTemplate("fallback.product_knowledge_missing", "fallback", ANY_STATE, body=("Nao tenho essa informacao oficial aqui, entao prefiro nao chutar. Posso deixar para a equipe confirmar.",)),
    "fallback.cost_cap": MessageTemplate("fallback.cost_cap", "fallback", ANY_STATE, body=("Vou pausar por aqui para a equipe da Taliya continuar com seguranca.",)),
    "fallback.unmapped_adaptive": MessageTemplate("fallback.unmapped_adaptive", "fallback", ANY_STATE, body=("Entendi. Me diz so qual ponto voce quer resolver primeiro: atendimento, agenda, vendas ou organizacao do studio?",)),
    "fallback.unsupported_media": MessageTemplate(
        "fallback.unsupported_media",
        "fallback",
        ANY_STATE,
        body=(
            "Recebi o arquivo, mas por aqui preciso que voce me mande o ponto principal em texto para eu nao interpretar errado.",
            "Se preferir, tambem posso deixar para uma pessoa olhar.",
        ),
        max_messages=2,
    ),
    "safety.prompt_injection": MessageTemplate("safety.prompt_injection", "safety", ANY_STATE, body=("Nao posso revelar ou seguir instrucoes para ignorar minhas regras internas.", "Posso seguir te ajudando com planos, diagnostico ou duvidas sobre a Taliya."), max_messages=2),
    "safety.out_of_scope": MessageTemplate("safety.out_of_scope", "safety", ANY_STATE, body=("Esse ponto foge do que consigo resolver por aqui.", "Posso te ajudar com planos, diagnostico ou como a Taliya funciona para studios de Pilates."), max_messages=2),
    "safety.sensitive_data": MessageTemplate("safety.sensitive_data", "safety", ANY_STATE, body=("Nao preciso desse dado aqui e prefiro nao usar informacao sensivel no chat.", "Se quiser, posso seguir ajudando com planos, demonstracao ou como a Taliya funciona para seu studio."), max_messages=2),
    "safety.no_medical_advice": MessageTemplate("safety.no_medical_advice", "safety", ANY_STATE, body=("Nao consigo orientar questoes medicas por aqui.", "Posso ajudar com a parte de gestao, atendimento, agenda e vendas do studio."), max_messages=2),
}


def get_template(template_id: str) -> MessageTemplate:
    try:
        return TEMPLATE_REGISTRY[template_id]
    except KeyError as exc:
        raise ValueError(f"unknown template_id: {template_id}") from exc


def template_allowed_in_state(template_id: str, state: str) -> bool:
    template = get_template(template_id)
    return "*" in template.allowed_states or state in template.allowed_states


def required_template_ids() -> set[str]:
    return set(TEMPLATE_REGISTRY)
