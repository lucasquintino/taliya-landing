from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class ProductPlan(BaseModel):
    id: str
    name: str
    monthly_price_brl: int
    price_label: str
    best_for: str
    included_agents: list[str] = Field(default_factory=list)
    whatsapp_availability: str
    usage_boundary: str


class ProductKnowledgeSource(BaseModel):
    source_key: str = "taliya-commercial-product-knowledge"
    scope: str = "taliya_commercial"
    version: str = "taliya-commercial-2026-05-22"
    last_reviewed_at: str = "2026-05-22T00:00:00Z"
    plans: list[ProductPlan]
    links: dict[str, str]
    demo_status: str = "available"
    waitlist_status: str = "limited_studios_waitlist"
    checkout_status: str = "unavailable"
    availability: str = "Limited rollout for a small number of studios."
    cancellation_or_guarantee_policy: str = (
        "14 days of guarantee on the first subscription. Monthly cancellation "
        "without penalty after that period, according to the current policy."
    )
    privacy_or_data_notes: str = (
        "Do not ask for payment data or sensitive student data in chat."
    )
    how_it_works: str = (
        "Taliya helps a Pilates studio organize the daily routine in one "
        "place: conversations, students, agenda, reposicoes, cobrancas, "
        "interested leads, and follow-ups. The team can see what needs action. "
        "When the studio WhatsApp Business is connected and configured, agents "
        "can support conversations with students and interested leads while "
        "the team follows and takes over when needed."
    )
    routine_areas: dict[str, str] = Field(
        default_factory=lambda: {
            "atendimento": "Mensagens e duvidas comuns nao ficam perdidas.",
            "vendas_interessados": (
                "Interessados, aulas experimentais, proximos passos e "
                "follow-up ficam organizados."
            ),
            "agenda": (
                "Aulas, horarios, faltas, encaixes e movimentos da agenda "
                "ficam mais claros."
            ),
            "reposicoes": "Pedidos e pendencias de reposicao ficam organizados.",
            "cobrancas_financeiro": (
                "Mensalidades, vencimentos, renovacoes e pendencias ficam "
                "mais visiveis."
            ),
            "acompanhamento_alunos": (
                "Alunos que somem, faltam ou precisam de retorno ficam no "
                "radar da equipe."
            ),
            "gestao_prioridades": "A equipe enxerga o que precisa resolver primeiro.",
        }
    )
    whatsapp_scope: str = (
        "O aluno nao precisa baixar aplicativo nem criar senha. Ele conversa "
        "no WhatsApp; a Taliya registra a acao, atualiza o painel e avisa o "
        "responsavel. Para atuar nas conversas de alunos, o WhatsApp Business "
        "do studio precisa estar conectado/configurado. Nao prometa "
        "configuracao automatica no chat comercial."
    )
    integration_scope: str = (
        "Do not promise Instagram integration, integration with the lead's "
        "current system, mass messaging, checkout, payment links, or automatic "
        "migration. If a specific integration is not officially known, say the "
        "limit and offer human confirmation."
    )
    comparison_spreadsheet: str = (
        "Spreadsheet, notebook, and manual WhatsApp can work while the routine "
        "is small. Taliya is different because it helps organize what gets "
        "spread out: conversations, agenda, reposicoes, cobrancas, interested "
        "leads, and student follow-up. Do not shame the current process or "
        "claim replacement before understanding the case."
    )
    comparison_management_system: str = (
        "If the current system solves part of the routine, acknowledge it. "
        "Compare Taliya by how it organizes the studio routine and how AI "
        "agents support actions. Do not attack Tecnofit, Next Fit, or "
        "competitors. Do not promise migration, integration, or feature parity "
        "without confirmation."
    )
    security_and_data: str = (
        "The chat should not request sensitive data. Do not ask for CPF, "
        "payment data, medical data, or sensitive student information. "
        "Privacy, LGPD, certifications, encryption, or access-to-conversation "
        "claims require official facts; if the fact is missing, offer human "
        "confirmation."
    )
    availability_and_onboarding: str = (
        "Taliya is working with a small number of studios. There is no open "
        "checkout for immediate broad entry. Do not promise an exact date or "
        "guaranteed opening window. Waitlist is the current path when there is "
        "real intent to start or contract. Setup details should be confirmed "
        "by the team."
    )
    out_of_profile: str = (
        "Taliya is currently intended mainly for Pilates studios. If the "
        "person is a student, autonomous teacher, gym, clinic, non-Pilates "
        "business, or not-yet-open studio, qualify gently. Do not force a "
        "studio diagnostic or promise fit for another niche."
    )
    unsupported_claims: list[str] = Field(default_factory=list)

    def query(self, requested_keys: list[str] | None = None) -> dict[str, Any]:
        requested = requested_keys or [
            "plans",
            "prices",
            "links",
            "demo_status",
            "waitlist_status",
            "checkout_status",
            "availability",
        ]
        available: dict[str, Any] = {
            "plans": [plan.model_dump() for plan in self.plans],
            "prices": {plan.id: plan.price_label for plan in self.plans},
            "plan_comparison": [f"{plan.name}: {plan.best_for}" for plan in self.plans],
            "links": self.links,
            "demo_status": self.demo_status,
            "waitlist_status": self.waitlist_status,
            "checkout_status": self.checkout_status,
            "availability": self.availability,
            "cancellation_or_guarantee_policy": self.cancellation_or_guarantee_policy,
            "privacy_or_data_notes": self.privacy_or_data_notes,
            "how_it_works": self.how_it_works,
            "routine_areas": self.routine_areas,
            "whatsapp_scope": self.whatsapp_scope,
            "integration_scope": self.integration_scope,
            "comparison_spreadsheet": self.comparison_spreadsheet,
            "comparison_management_system": self.comparison_management_system,
            "security_and_data": self.security_and_data,
            "availability_and_onboarding": self.availability_and_onboarding,
            "out_of_profile": self.out_of_profile,
            "unsupported_claims": self.unsupported_claims,
        }
        facts = {key: available[key] for key in requested if key in available}
        missing = [key for key in requested if key not in available]
        return {
            "source_version": self.version,
            "facts": facts,
            "missing_facts": missing,
            "unsupported_claims": self.unsupported_claims,
        }


def get_product_knowledge_source() -> ProductKnowledgeSource:
    return ProductKnowledgeSource(
        plans=[
            ProductPlan(
                id="base",
                name="Base",
                monthly_price_brl=197,
                price_label="R$ 197/mes",
                best_for="Studios that want to organize the routine before active AI.",
                included_agents=[],
                whatsapp_availability="No automatic WhatsApp AI replies.",
                usage_boundary="1 studio, 1 user, no AI message quota.",
            ),
            ProductPlan(
                id="one_agent",
                name="Essencial",
                monthly_price_brl=497,
                price_label="R$ 497/mes",
                best_for="Studios that want to solve one clear pain first.",
                included_agents=["1 main agent chosen during setup"],
                whatsapp_availability=(
                    "Requires the studio WhatsApp Business connected for that agent."
                ),
                usage_boundary="1 studio, up to 2 users, 1,500 AI messages/month with hard cap.",
            ),
            ProductPlan(
                id="three_agents",
                name="Avance",
                monthly_price_brl=897,
                price_label="R$ 897/mes",
                best_for="Studios that want help in some priority routines.",
                included_agents=["3 main agents chosen during setup"],
                whatsapp_availability=(
                    "Requires the studio WhatsApp Business connected for "
                    "included agents."
                ),
                usage_boundary="1 studio, up to 5 users, 5,000 AI messages/month with hard cap.",
            ),
            ProductPlan(
                id="seven_agents",
                name="Completo",
                monthly_price_brl=1497,
                price_label="R$ 1.497/mes",
                best_for="Studios that want the complete Taliya.",
                included_agents=[
                    "Atendimento",
                    "Agenda",
                    "Vendas",
                    "Financeiro",
                    "Retencao",
                    "Gestao",
                    "Historico/Evolucao",
                ],
                whatsapp_availability=(
                    "Requires the studio WhatsApp Business connected for the "
                    "complete team."
                ),
                usage_boundary="1 studio, up to 10 users, 15,000 AI messages/month with hard cap.",
            ),
        ],
        links={
            "landing": "https://www.taliya.com.br/pilates",
            "plans": "https://www.taliya.com.br/pilates/planos",
            "demonstration": "https://www.taliya.com.br/pilates/planos/demonstracao",
            "privacy": "https://www.taliya.com.br/privacidade",
        },
        unsupported_claims=[
            "checkout",
            "guaranteed ROI",
            "specific integration without confirmation",
            "exact broad availability date",
            "payment link while checkout is unavailable",
        ],
    )
