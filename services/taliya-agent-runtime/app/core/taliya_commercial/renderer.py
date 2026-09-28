from __future__ import annotations

import re
from collections.abc import Mapping
from dataclasses import dataclass
from string import Formatter
from typing import Any

from app.core.taliya_commercial.schemas import (
    Channel,
    RenderedMessage,
    RenderPlan,
    RenderPlanItem,
    ValidatorResult,
)
from app.core.taliya_commercial.template_registry import (
    TEMPLATE_REGISTRY,
    VARIABLE_REGISTRY,
    normalize_template_id,
    validate_render_plan_item_variables,
)


class RenderError(ValueError):
    pass


@dataclass(frozen=True, slots=True)
class TemplateBodyLine:
    text: str
    required_variables: frozenset[str] = frozenset()
    optional: bool = False


_APPROVED_TEMPLATE_BODIES: dict[str, tuple[TemplateBodyLine, ...]] = {
    "opening.cold_greeting": (
        TemplateBodyLine("Oi, tudo bem?"),
        TemplateBodyLine("Em que posso ajudar?"),
    ),
    "opening.cold_greeting_named": (
        TemplateBodyLine(
            "Oi, {first_name}, tudo bem?",
            required_variables=frozenset({"first_name"}),
        ),
        TemplateBodyLine("Em que posso ajudar?"),
    ),
    "opening.contextual_ack": (
        TemplateBodyLine("Oi, tudo bem?"),
        TemplateBodyLine("Entendi."),
    ),
    "opening.widget_empty_diagnostic": (
        TemplateBodyLine("Oi, tudo bem?"),
        TemplateBodyLine("Em que posso ajudar?"),
        TemplateBodyLine(
            "Se fizer sentido para você, estamos oferecendo um diagnóstico "
            "gratuito para o seu studio. O que você acha?"
        ),
    ),
    "opening.general_interest": (
        TemplateBodyLine("Oi, tudo bem?"),
        TemplateBodyLine(
            "A Taliya é a IA do seu studio de Pilates para organizar a rotina "
            "que faz o studio girar: agenda, reposições, cobranças, gestão, "
            "atendimento e acompanhamento."
        ),
        TemplateBodyLine(
            "Se fizer sentido, posso fazer um diagnóstico gratuito com poucas "
            "perguntas para entender a rotina, os gargalos e a prioridade do "
            "seu studio. O que você acha?"
        ),
    ),
    "opening.instagram_source": (
        TemplateBodyLine("Oi, tudo bem?"),
        TemplateBodyLine(
            "A Taliya é a IA do seu studio de Pilates para organizar agenda, "
            "reposições, cobranças, gestão, atendimento e acompanhamento em "
            "um só lugar."
        ),
        TemplateBodyLine(
            "Se fizer sentido, posso fazer um diagnóstico gratuito com poucas "
            "perguntas para entender a rotina, os gargalos e a prioridade do "
            "seu studio. O que você acha?"
        ),
    ),
    "opening.site_cta": (
        TemplateBodyLine("Oi, tudo bem?"),
        TemplateBodyLine(
            "A Taliya é a IA do seu studio de Pilates para ajudar no dia a dia: "
            "agenda, reposições, cobranças, gestão, atendimento e acompanhamento."
        ),
        TemplateBodyLine(
            "Se fizer sentido, posso fazer um diagnóstico gratuito com poucas "
            "perguntas para entender a rotina, os gargalos e a prioridade do "
            "seu studio. O que você acha?"
        ),
    ),
    "product.price_direct": (
        TemplateBodyLine("Oi, tudo bem?"),
        TemplateBodyLine(
            "{plan_price_summary}",
            required_variables=frozenset({"plan_price_summary"}),
        ),
    ),
    "product.price_complete_direct": (
        TemplateBodyLine("Oi, tudo bem?"),
        TemplateBodyLine(
            "{plan_price_summary}",
            required_variables=frozenset({"plan_price_summary"}),
        ),
    ),
    "product.price_objection_value": (
        TemplateBodyLine("Entendo. É um valor para olhar com calma mesmo."),
        TemplateBodyLine(
            "O ponto é que a Taliya não é só mais uma ferramenta: ela ajuda nas "
            "rotinas que fazem o studio girar, como WhatsApp, retorno de "
            "interessados, agenda, reposições, cobranças e acompanhamento."
        ),
        TemplateBodyLine(
            "Para decidir sem pressa, podemos usar o diagnóstico gratuito para "
            "comparar prioridade e plano, ou deixar seu interesse na lista de "
            "espera se você já quiser seguir."
        ),
    ),
    "product.overview_short": (
        TemplateBodyLine(
            "{product_fact_summary}",
            required_variables=frozenset({"product_fact_summary"}),
            optional=True,
        ),
        TemplateBodyLine(
            "A Taliya ajuda o studio de Pilates a organizar agenda, reposições, "
            "cobranças, vendas, atendimento e acompanhamento em um só lugar."
        ),
    ),
    "product.plan_direct": (
        TemplateBodyLine(
            "{plan_price_summary}",
            required_variables=frozenset({"plan_price_summary"}),
        ),
    ),
    "product.demo_direct": (
        TemplateBodyLine("Oi, tudo bem?"),
        TemplateBodyLine(
            "Ver demonstração: {official_demo_link}",
            required_variables=frozenset({"official_demo_link"}),
        ),
        TemplateBodyLine(
            "Depois que você olhar, retorna aqui se fez sentido para você, "
            "ou se não entendeu alguma coisa, pode ser?"
        ),
    ),
    "product.whatsapp_direct": (
        TemplateBodyLine("Oi, tudo bem?"),
        TemplateBodyLine(
            "O aluno não precisa baixar aplicativo nem criar senha. Ele conversa "
            "no WhatsApp; a Taliya registra a ação, atualiza o painel e avisa "
            "o responsável."
        ),
        TemplateBodyLine(
            "Se quiser ver isso funcionando na prática, aqui está uma "
            "demonstração: {official_demo_link}",
            required_variables=frozenset({"official_demo_link"}),
            optional=True,
        ),
    ),
    "product.crm_direct": (
        TemplateBodyLine(
            "{product_fact_summary}",
            required_variables=frozenset({"product_fact_summary"}),
        ),
    ),
    "product.agents_direct": (
        TemplateBodyLine(
            "{product_fact_summary}",
            required_variables=frozenset({"product_fact_summary"}),
        ),
    ),
    "product.how_it_works_direct": (
        TemplateBodyLine(
            "Funciona assim: a Taliya ajuda o studio a organizar o que "
            "acontece no dia a dia."
        ),
        TemplateBodyLine(
            "Ela junta conversas, alunos, agenda, reposições, cobranças, "
            "interessados e acompanhamentos para a equipe enxergar melhor "
            "o que precisa de ação."
        ),
        TemplateBodyLine(
            "Quando o WhatsApp Business do studio está conectado, os agentes "
            "podem apoiar conversas com alunos e interessados, sempre com a "
            "equipe podendo acompanhar e assumir quando precisar. "
            "{contextual_next_step}",
            required_variables=frozenset({"contextual_next_step"}),
        ),
    ),
    "product.plan_fit_with_diagnostic": (
        TemplateBodyLine("Oi, tudo bem?"),
        TemplateBodyLine(
            "{plan_fit_context}",
            required_variables=frozenset({"plan_fit_context"}),
        ),
        TemplateBodyLine(
            "Posso fazer um diagnóstico gratuito com poucas perguntas e te "
            "devolver o que organizar primeiro, quais agentes fariam sentido "
            "e qual plano vale comparar."
        ),
        TemplateBodyLine("O que você acha?"),
    ),
    "product.comparison_current_tool": (
        TemplateBodyLine(
            "Se hoje vocês usam {current_tool_context}, faz sentido manter o "
            "que funciona.",
            required_variables=frozenset({"current_tool_context"}),
        ),
        TemplateBodyLine(
            "Para comparar sem chute, vale olhar onde a rotina do seu studio "
            "mais perde tempo hoje."
        ),
    ),
    "product.integration_scope_direct": (
        TemplateBodyLine(
            "Sobre {integration_topic}, eu prefiro confirmar com a equipe "
            "antes de prometer uma integração.",
            required_variables=frozenset({"integration_topic"}),
        ),
        TemplateBodyLine(
            "Se esse ponto for importante na sua operação, deixo isso marcado "
            "para validarem com precisão."
        ),
    ),
    "product.security_data_direct": (
        TemplateBodyLine(
            "Sobre dados e segurança, eu sigo apenas o que estiver confirmado "
            "nas informações oficiais."
        ),
        TemplateBodyLine(
            "O caminho seguro aqui é não mandar CPF, pagamento ou dados sensíveis "
            "dos alunos pelo chat. Se esse ponto for decisivo, a equipe confirma "
            "com você."
        ),
    ),
    "product.out_of_profile_redirect": (
        TemplateBodyLine(
            "Hoje a Taliya é pensada principalmente para studios de Pilates."
        ),
        TemplateBodyLine(
            "Se você e aluno, professor autônomo ou esta em outro tipo de negócio, "
            "melhor confirmar com a equipe antes de prometer encaixe."
        ),
    ),
    "diagnostic.price_hook": (
        TemplateBodyLine(
            "Se fizer sentido para você, estamos oferecendo um diagnóstico "
            "gratuito para o seu studio. Assim você entende se algum dos "
            "nossos planos te atenderia."
        ),
        TemplateBodyLine(
            "Com poucas perguntas, eu entendo a rotina do studio e te devolvo "
            "o que organizar primeiro, quais agentes fariam sentido e qual "
            "plano vale comparar."
        ),
        TemplateBodyLine("O que você acha?"),
    ),
    "diagnostic.price_hook_with_context": (
        TemplateBodyLine(
            "Como você ja trouxe um ponto da rotina que está te incomodando, "
            "vale olhar com um pouco mais de calma para entender o que está "
            "travando hoje."
        ),
        TemplateBodyLine(
            "Posso fazer um diagnóstico gratuito com poucas perguntas e te "
            "devolver o que organizar primeiro, quais agentes fariam sentido "
            "e qual plano vale comparar."
        ),
        TemplateBodyLine("O que você acha?"),
    ),
    "opening.diagnostic_cta": (
        TemplateBodyLine("Claro, faço sim."),
        TemplateBodyLine(
            "Para te devolver algo útil, vou entender rapidinho como está a "
            "rotina do studio hoje."
        ),
    ),
    "diagnostic.offer_soft": (
        TemplateBodyLine(
            "{pain_context_human}",
            required_variables=frozenset({"pain_context_human"}),
            optional=True,
        ),
        TemplateBodyLine(
            "Posso fazer um diagnóstico gratuito com poucas perguntas e te "
            "devolver o que organizar primeiro, quais agentes fariam sentido "
            "e qual plano vale comparar."
        ),
        TemplateBodyLine("O que você acha?"),
    ),
    "diagnostic.start": (
        TemplateBodyLine(
            "Claro, faço sim. Para te devolver algo útil, vou entender rapidinho "
            "como está a rotina do studio hoje."
        ),
    ),
    "diagnostic.start_named": (
        TemplateBodyLine(
            "Claro, {first_name}. Para te devolver algo útil, vou entender "
            "rapidinho como está a rotina do studio hoje.",
            required_variables=frozenset({"first_name"}),
        ),
    ),
    "diagnostic.ask_active_students": (
        TemplateBodyLine(
            "{answer_feedback}",
            required_variables=frozenset({"answer_feedback"}),
            optional=True,
        ),
        TemplateBodyLine("Hoje seu studio tem mais ou menos quantos alunos ativos?"),
    ),
    "diagnostic.ask_main_pain": (
        TemplateBodyLine(
            "{answer_feedback}",
            required_variables=frozenset({"answer_feedback"}),
            optional=True,
        ),
        TemplateBodyLine(
            "Quais partes mais dão trabalho hoje: WhatsApp, agenda/reposições, "
            "vendas, financeiro ou acompanhamento dos alunos?"
        ),
    ),
    "diagnostic.ask_current_process": (
        TemplateBodyLine(
            "{answer_feedback}",
            required_variables=frozenset({"answer_feedback"}),
            optional=True,
        ),
        TemplateBodyLine(
            "Hoje isso fica em algum sistema ou mais em WhatsApp, planilha e "
            "caderno?"
        ),
    ),
    "diagnostic.ask_pain_detail": (
        TemplateBodyLine(
            "{answer_feedback}",
            required_variables=frozenset({"answer_feedback"}),
            optional=True,
        ),
        TemplateBodyLine(
            "Hoje você consegue ver facilmente o que precisa ser resolvido no dia?"
        ),
    ),
    "diagnostic.ask_priority": (
        TemplateBodyLine(
            "{answer_feedback}",
            required_variables=frozenset({"answer_feedback"}),
            optional=True,
        ),
        TemplateBodyLine(
            "Pensando na rotina do studio, qual tarefa você mais gostaria de "
            "deixar mais leve primeiro?"
        ),
    ),
    "diagnostic.ask_urgency": (
        TemplateBodyLine(
            "{answer_feedback}",
            required_variables=frozenset({"answer_feedback"}),
            optional=True,
        ),
        TemplateBodyLine(
            "Vocês estão buscando resolver isso agora ou só pesquisando por "
            "enquanto?"
        ),
    ),
    "diagnostic.partial_progress": (
        TemplateBodyLine(
            "{answer_feedback}",
            required_variables=frozenset({"answer_feedback"}),
        ),
        TemplateBodyLine(
            "Já tenho parte do contexto. Falta só um ponto para não te devolver "
            "um diagnóstico chutado."
        ),
    ),
    "diagnostic.deliver_hold": (
        TemplateBodyLine(
            "Perfeito. Já dá para te devolver uma leitura prática. Vou organizar "
            "em partes."
        ),
    ),
    "diagnostic.deliver_context": (
        TemplateBodyLine(
            "{pain_context_human}",
            required_variables=frozenset({"pain_context_human"}),
        ),
    ),
    "diagnostic.deliver_crm_base": (
        TemplateBodyLine(
            "{crm_base_recommendation}",
            required_variables=frozenset({"crm_base_recommendation"}),
        ),
    ),
    "diagnostic.deliver_operational_step": (
        TemplateBodyLine(
            "{operational_first_step}",
            required_variables=frozenset({"operational_first_step"}),
        ),
    ),
    "diagnostic.deliver_agent_recommendation": (
        TemplateBodyLine(
            "Agente de {agent_name}: organiza interessados, aulas experimentais, "
            "próximos passos e follow-up.",
            required_variables=frozenset(
                {
                    "agent_name",
                }
            ),
        ),
        TemplateBodyLine(
            "Na prática, a equipe enxerga o que precisa resolver primeiro."
        ),
    ),
    "diagnostic.deliver_plan_recommendation": (
        TemplateBodyLine(
            "Pelo tamanho, momento do studio e contexto acima, eu recomendaria "
            "para você o plano {recommended_plan_or_range}.",
            required_variables=frozenset({"recommended_plan_or_range"}),
        ),
    ),
    "diagnostic.deliver_demo_not_offered": (
        TemplateBodyLine(
            "Também posso te mandar uma demonstração para você ver isso "
            "funcionando na prática. Quer que eu te envie?"
        ),
    ),
    "diagnostic.deliver_demo_already_offered": (
        TemplateBodyLine(
            "{demo_status}. Chegou a olhar as demonstrações? O que você achou?",
            required_variables=frozenset({"demo_status"}),
        ),
    ),
    "diagnostic.insufficient_evidence": (
        TemplateBodyLine(
            "Ainda não tenho informação suficiente para fechar um diagnóstico "
            "sem chutar."
        ),
        TemplateBodyLine(
            "{clarification_question}",
            required_variables=frozenset({"clarification_question"}),
            optional=True,
        ),
    ),
    "waitlist.offer_after_contract_intent": (
        TemplateBodyLine(
            "Perfeito. Posso deixar seu interesse registrado na lista."
        ),
        TemplateBodyLine(
            "Hoje a entrada acontece por uma lista para um número pequeno de "
            "studios. Posso deixar o interesse registrado sem prometer entrada "
            "imediata, data ou condição especial."
        ),
    ),
    "waitlist.answer_question": (
        TemplateBodyLine(
            "{answer_feedback}",
            required_variables=frozenset({"answer_feedback"}),
        ),
    ),
    "waitlist.ask_missing_studio": (
        TemplateBodyLine("Para deixar registrado, qual é o nome do studio?"),
    ),
    "waitlist.ask_missing_city": (
        TemplateBodyLine("E de qual cidade e estado é o studio?"),
    ),
    "waitlist.ask_missing_contact_path": (
        TemplateBodyLine(
            "Para a equipe continuar com segurança, prefere seguir por esta "
            "conversa ou por e-mail?"
        ),
    ),
    "waitlist.current_path_explained": (
        TemplateBodyLine(
            "Funciona assim: hoje a entrada acontece por uma lista para um "
            "número pequeno de studios, sem promessa de vaga imediata, data, "
            "desconto ou condição especial."
        ),
    ),
    "waitlist.joined": (
        TemplateBodyLine(
            "Perfeito, deixei seu interesse registrado para a equipe da Taliya."
        ),
        TemplateBodyLine(
            "Studio: {studio_name}.",
            required_variables=frozenset({"studio_name"}),
            optional=True,
        ),
        TemplateBodyLine(
            "Cidade/estado: {city_state}.",
            required_variables=frozenset({"city_state"}),
            optional=True,
        ),
    ),
    "waitlist.pause_decision": (
        TemplateBodyLine("Claro. O que você quer entender melhor antes de decidir?"),
    ),
    "waitlist.status_preserved": (
        TemplateBodyLine(
            "{waitlist_context_summary}",
            required_variables=frozenset({"waitlist_context_summary"}),
            optional=True,
        ),
        TemplateBodyLine(
            "Seu interesse segue registrado; posso responder a dúvida sem mexer "
            "nisso."
        ),
    ),
    "fallback.provider_timeout": (
        TemplateBodyLine(
            "Estou com uma instabilidade aqui. Sua mensagem ficou registrada "
            "para a equipe da Taliya continuar com segurança."
        ),
    ),
    "fallback.invalid_json": (
        TemplateBodyLine(
            "Tive uma instabilidade para organizar a resposta. Vou deixar sua "
            "mensagem registrada para a equipe continuar com segurança."
        ),
    ),
    "fallback.product_knowledge_missing": (
        TemplateBodyLine(
            "Não tenho essa informação oficial fechada aqui, então prefiro não "
            "te prometer algo no chute."
        ),
        TemplateBodyLine(
            "Posso deixar esse ponto para a equipe da Taliya confirmar com "
            "precisão."
        ),
    ),
    "fallback.cost_cap": (
        TemplateBodyLine(
            "Para manter segurança e custo sob controle, vou deixar sua mensagem "
            "registrada para a equipe continuar daqui."
        ),
    ),
    "fallback.unmapped_adaptive": (
        TemplateBodyLine(
            "{clarification_question}",
            required_variables=frozenset({"clarification_question"}),
        ),
    ),
    "fallback.unsupported_media": (
        TemplateBodyLine(
            "Não consigo analisar esse tipo de arquivo por aqui."
        ),
        TemplateBodyLine(
            "Me manda um resumo em texto ou, se preferir, deixo para uma pessoa "
            "da Taliya olhar."
        ),
    ),
    "safety.unsupported_media": (
        TemplateBodyLine(
            "Não consigo analisar esse tipo de arquivo por aqui."
        ),
        TemplateBodyLine(
            "Me manda um resumo em texto ou, se preferir, deixo para uma pessoa "
            "da Taliya olhar."
        ),
    ),
    "safety.prompt_injection": (
        TemplateBodyLine(
            "Não posso mostrar instruções internas ou regras do sistema."
        ),
        TemplateBodyLine(
            "Posso seguir te ajudando com dúvidas sobre a Taliya para studios "
            "de Pilates."
        ),
    ),
    "safety.out_of_scope": (
        TemplateBodyLine(
            "Não consigo ajudar com esse pedido por aqui."
        ),
        TemplateBodyLine(
            "Se quiser, posso voltar para as dúvidas sobre a Taliya é a rotina "
            "do seu studio."
        ),
    ),
    "safety.sensitive_data": (
        TemplateBodyLine(
            "Não preciso desse dado sensível para te ajudar aqui."
        ),
        TemplateBodyLine(
            "Para sua segurança, melhor não enviar CPF, pagamento ou dados "
            "sensíveis dos alunos pelo chat."
        ),
    ),
    "safety.no_medical_advice": (
        TemplateBodyLine(
            "Não consigo orientar caso médico ou de saúde por aqui."
        ),
        TemplateBodyLine(
            "Posso seguir pela parte comercial e operacional da Taliya se fizer "
            "sentido."
        ),
    ),
    "handoff.acknowledge": (
        TemplateBodyLine("Claro. Vou deixar uma pessoa assumir daqui."),
        TemplateBodyLine(
            "Vou deixar o contexto da conversa salvo para você não precisar "
            "repetir tudo."
        ),
    ),
    "handoff.paused": (
        TemplateBodyLine(
            "A conversa segue com uma pessoa da Taliya; mantive sua mensagem "
            "registrada."
        ),
    ),
}
_ENUM_RENDER_LABELS: dict[str, dict[str, str]] = {
    "contextual_next_step": {
        "diagnostic_offer_with_pain": (
            "Se fizer sentido, posso fazer um diagnóstico gratuito para entender "
            "como isso encaixaria na rotina do seu studio. O que você acha?"
        ),
        "diagnostic_offer_generic": (
            "Se fizer sentido, posso fazer um diagnóstico gratuito para entender "
            "se a Taliya encaixa na rotina do seu studio. O que você acha?"
        ),
        "continue_diagnostic": (
            "Para comparar com menos chute, seguimos pelo diagnóstico e eu te "
            "devolvo o próximo passó mais prático."
        ),
        "no_cta": (
            "Como seu diagnóstico já ficou fechado, não vou reiniciar as "
            "perguntas."
        ),
    },
    "demo_status": {
        "not_offered": "Como eu ainda não tinha te enviado a demonstração",
        "offered": "Como a demonstração já ficou no seu caminho",
        "viewed_or_asked": "Como você já tinha visto a demonstração",
        "reacted_positive": "Como você gostou da demonstração",
    },
}

_URL_RE = re.compile(r"https?://\S+")
_PT_BR_PUBLIC_REPLACEMENTS: tuple[tuple[str, str], ...] = (
    ("A Taliya e", "A Taliya é"),
    ("a Taliya e", "a Taliya é"),
    ("O ponto e", "O ponto é"),
    ("o ponto e", "o ponto é"),
    ("O caminho seguro aqui e", "O caminho seguro aqui é"),
    ("o caminho seguro aqui e", "o caminho seguro aqui é"),
    ("O caminho seguro e", "O caminho seguro é"),
    ("o caminho seguro e", "o caminho seguro é"),
    ("qual e", "qual é"),
    ("estado e o studio", "estado é o studio"),
    ("Ja da", "Já dá"),
    ("ja da", "já dá"),
    ("aqui esta", "aqui está"),
    ("como esta", "como está"),
    ("que esta", "que está"),
    ("studio esta", "studio está"),
    ("WhatsApp esta", "WhatsApp está"),
    ("Voces estao", "Vocês estão"),
    ("voces estao", "vocês estão"),
    ("passo prático e", "passo prático é"),
    ("primeiro passo prático e", "primeiro passo prático é"),
    ("pra", "para"),
    ("pro", "para o"),
    ("voce", "você"),
    ("Voce", "Você"),
    ("voces", "vocês"),
    ("Voces", "Vocês"),
    ("diagnostico", "diagnóstico"),
    ("Diagnostico", "Diagnóstico"),
    ("demonstracao", "demonstração"),
    ("Demonstracao", "Demonstração"),
    ("demonstracoes", "demonstrações"),
    ("pratica", "prática"),
    ("Pratica", "Prática"),
    ("pratico", "prático"),
    ("proximo", "próximo"),
    ("proximos", "próximos"),
    ("Tambem", "Também"),
    ("tambem", "também"),
    ("nao", "não"),
    ("Nao", "Não"),
    ("acao", "ação"),
    ("responsavel", "responsável"),
    ("seguranca", "segurança"),
    ("sensivel", "sensível"),
    ("sensiveis", "sensíveis"),
    ("saude", "saúde"),
    ("medico", "médico"),
    ("instrucao", "instrução"),
    ("instrucoes", "instruções"),
    ("duvida", "dúvida"),
    ("duvidas", "dúvidas"),
    ("ate", "até"),
    ("mes", "mês"),
    ("cobranca", "cobrança"),
    ("cobrancas", "cobranças"),
    ("reposicao", "reposição"),
    ("reposicoes", "reposições"),
    ("organizacao", "organização"),
    ("visivel", "visível"),
    ("areas", "áreas"),
    ("condicao", "condição"),
    ("operacao", "operação"),
    ("integracao", "integração"),
    ("informacao", "informação"),
    ("informacoes", "informações"),
    ("precisao", "precisão"),
    ("util", "útil"),
    ("rapida", "rápida"),
    ("rapido", "rápido"),
    ("diaria", "diária"),
    ("intencao", "intenção"),
    ("faco", "faço"),
    ("so", "só"),
    ("ja", "já"),
    ("Ja", "Já"),
    ("comecam", "começam"),
    ("comecar", "começar"),
    ("criterio", "critério"),
    ("visao", "visão"),
)


def validate_renderer_template_bodies(
    bodies: Mapping[str, tuple[TemplateBodyLine, ...]] | None = None,
) -> list[str]:
    body_map = bodies or _APPROVED_TEMPLATE_BODIES
    errors: list[str] = []

    for raw_template_id, body in body_map.items():
        template_id = normalize_template_id(raw_template_id)
        template = TEMPLATE_REGISTRY.get(template_id)
        if template is None:
            errors.append(f"unknown_body_template_id:{raw_template_id}")
            continue

        required = set(template.required_variables)
        optional = set(template.optional_variables)
        allowed = required | optional
        rendered_required: set[str] = set()

        for line in body:
            placeholders = _placeholder_names(line.text)
            declared = set(line.required_variables)

            for variable_name in sorted(placeholders - declared):
                errors.append(
                    f"undeclared_body_placeholder:{template_id}:{variable_name}"
                )
            for variable_name in sorted(declared - placeholders):
                errors.append(
                    f"unused_required_body_variable:{template_id}:{variable_name}"
                )
            for variable_name in sorted(placeholders):
                if variable_name not in VARIABLE_REGISTRY:
                    errors.append(f"unknown_body_variable:{template_id}:{variable_name}")
                if variable_name not in allowed:
                    errors.append(
                        f"body_variable_not_allowed:{template_id}:{variable_name}"
                    )
            if line.optional:
                for variable_name in sorted(declared & required):
                    errors.append(
                        f"required_variable_on_optional_line:"
                        f"{template_id}:{variable_name}"
                    )
            else:
                rendered_required.update(declared & required)

        for variable_name in sorted(required - rendered_required):
            errors.append(
                f"required_template_variable_not_rendered:{template_id}:{variable_name}"
            )

    return errors


def render_validated_template_plan(
    render_plan: RenderPlan,
    validator_result: ValidatorResult,
    *,
    channel: Channel,
) -> list[RenderedMessage]:
    _ensure_validated_plan(render_plan, validator_result)

    messages: list[RenderedMessage] = []
    for item in render_plan.items:
        messages.extend(
            _render_item(
                item,
                channel=channel,
                starting_sequence=len(messages) + 1,
            )
        )

    return _apply_channel_policy(messages, render_plan=render_plan, channel=channel)


def _ensure_validated_plan(
    render_plan: RenderPlan,
    validator_result: ValidatorResult,
) -> None:
    if not isinstance(render_plan, RenderPlan):
        raise RenderError("renderer requires a RenderPlan")
    if not isinstance(validator_result, ValidatorResult):
        raise RenderError("renderer requires a ValidatorResult")
    if validator_result.status != "passed" or validator_result.final_disposition not in {
        "accepted",
        "repaired",
    }:
        raise RenderError("renderer requires a validated render plan")
    if not render_plan.items:
        raise RenderError("renderer requires a non-empty validated render plan")


def _render_item(
    item: RenderPlanItem,
    *,
    channel: Channel,
    starting_sequence: int,
) -> list[RenderedMessage]:
    if item.channel is not None and item.channel != channel:
        raise RenderError("template channel mismatch")

    registry_errors = validate_render_plan_item_variables(item)
    if registry_errors:
        raise RenderError(";".join(registry_errors))

    template_id = normalize_template_id(item.template_id)
    body = _APPROVED_TEMPLATE_BODIES.get(template_id)
    if body is None:
        raise RenderError(f"template body not approved for renderer: {template_id}")
    body_errors = validate_renderer_template_bodies({template_id: body})
    if body_errors:
        raise RenderError(";".join(body_errors))

    values = _variable_values(item)
    messages: list[RenderedMessage] = []
    for line in body:
        rendered = _render_line(line, values)
        if rendered is None:
            continue
        messages.append(
            RenderedMessage(
                text=rendered,
                template_id=item.template_id,
                channel=channel,
                sequence=starting_sequence + len(messages),
            )
        )
    return messages


def _apply_channel_policy(
    messages: list[RenderedMessage],
    *,
    render_plan: RenderPlan,
    channel: Channel,
) -> list[RenderedMessage]:
    if channel == "whatsapp" and render_plan.chunk_policy == "whatsapp_max_3":
        return _coalesce_whatsapp_messages(messages, max_chunks=3)
    if (
        channel == "whatsapp"
        and render_plan.chunk_policy == "staged_diagnostic"
        and len(messages) > 3
    ):
        return _coalesce_whatsapp_messages(messages, max_chunks=3)
    return messages


def _coalesce_whatsapp_messages(
    messages: list[RenderedMessage],
    *,
    max_chunks: int,
) -> list[RenderedMessage]:
    if len(messages) <= max_chunks:
        return messages

    groups: list[list[RenderedMessage]] = [[] for _ in range(max_chunks)]
    for index, message in enumerate(messages):
        group_index = min(index * max_chunks // len(messages), max_chunks - 1)
        groups[group_index].append(message)

    coalesced: list[RenderedMessage] = []
    for group in groups:
        if not group:
            continue
        coalesced.append(
            RenderedMessage(
                text="\n\n".join(message.text for message in group),
                template_id=group[0].template_id,
                channel="whatsapp",
                sequence=len(coalesced) + 1,
            )
        )
    return coalesced


def _render_line(line: TemplateBodyLine, values: dict[str, Any]) -> str | None:
    missing = [
        variable_name
        for variable_name in line.required_variables
        if _is_missing(values.get(variable_name))
    ]
    if missing and line.optional:
        return None
    if missing:
        raise RenderError(f"missing template variables: {', '.join(sorted(missing))}")

    try:
        rendered = line.text.format(**values)
    except KeyError as error:
        if line.optional:
            return None
        raise RenderError(f"missing template variable: {error.args[0]}") from error

    rendered = _normalize_public_pt_br(" ".join(rendered.split()))
    return rendered or None


def _normalize_public_pt_br(text: str) -> str:
    parts: list[str] = []
    last_end = 0
    for match in _URL_RE.finditer(text):
        parts.append(_replace_public_pt_br_words(text[last_end : match.start()]))
        parts.append(match.group(0))
        last_end = match.end()
    parts.append(_replace_public_pt_br_words(text[last_end:]))
    return "".join(parts)


def _replace_public_pt_br_words(text: str) -> str:
    normalized = text
    for raw, replacement in _PT_BR_PUBLIC_REPLACEMENTS:
        normalized = re.sub(rf"\b{re.escape(raw)}\b", replacement, normalized)
    return normalized


def _variable_values(item: RenderPlanItem) -> dict[str, Any]:
    return {
        variable_name: _render_variable_value(variable_name, variable.value)
        for variable_name, variable in item.variables.items()
    }


def _render_variable_value(variable_name: str, value: Any) -> Any:
    enum_labels = _ENUM_RENDER_LABELS.get(variable_name)
    if enum_labels is None:
        return value

    key = str(value)
    try:
        return enum_labels[key]
    except KeyError as error:
        raise RenderError(
            f"unsupported enum value for renderer: {variable_name}={key}"
        ) from error


def _placeholder_names(text: str) -> set[str]:
    names: set[str] = set()
    for _, field_name, _, _ in Formatter().parse(text):
        if not field_name:
            continue
        names.add(_root_field_name(field_name))
    return names


def _root_field_name(field_name: str) -> str:
    return field_name.split(".", 1)[0].split("[", 1)[0]


def _is_missing(value: Any) -> bool:
    if value is None:
        return True
    if isinstance(value, str):
        return not value.strip()
    if isinstance(value, list | tuple | set | dict):
        return not value
    return False
