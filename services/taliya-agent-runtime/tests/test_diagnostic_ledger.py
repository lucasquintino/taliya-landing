from app.domains.taliya_commercial.diagnostic_ledger import (
    REQUIRED_QUESTION_KEYS,
    apply_diagnostic_answer_interpretation,
    empty_ledger,
    infer_ledger_from_text,
    ledger_is_complete,
    missing_or_unresolved_keys,
    next_question_key,
)


def test_empty_ledger_contains_all_required_questions():
    ledger = empty_ledger()

    assert [item["question_key"] for item in ledger] == list(REQUIRED_QUESTION_KEYS)
    assert ledger_is_complete(ledger) is False
    assert list(REQUIRED_QUESTION_KEYS) == [
        "active_students_or_size",
        "main_pain",
        "pain_detail",
        "current_process",
        "priority",
        "urgency",
    ]


def test_pre_answered_fact_is_marked_and_not_repeated():
    ledger = infer_ledger_from_text(
        "Tenho 120 alunos e perco interessados no WhatsApp porque o retorno demora.",
        evidence_id="msg_1",
    )

    answered = {item["question_key"]: item for item in ledger}
    assert answered["active_students_or_size"]["status"] == "inferred_from_prior_message"
    assert answered["main_pain"]["status"] == "missing"
    assert next_question_key(ledger) == "main_pain"


def test_rich_diagnostic_message_only_answers_pending_question():
    ledger = infer_ledger_from_text(
        "Tenho 100 alunos ativos, agenda e reposicoes se perdem, hoje controlo em planilha, "
        "a dor principal e agenda, a prioridade e organizar reposicoes, e urgente para esse mes.",
        evidence_id="msg_rich",
    )

    answered = {item["question_key"]: item for item in ledger}
    assert answered["active_students_or_size"]["status"] == "inferred_from_prior_message"
    assert answered["main_pain"]["status"] == "missing"
    assert answered["pain_detail"]["status"] == "missing"
    assert answered["urgency"]["status"] == "missing"
    assert next_question_key(ledger) == "main_pain"
    assert ledger_is_complete(ledger) is False


def test_agenda_pain_does_not_answer_current_process_by_itself():
    ledger = infer_ledger_from_text("tenho 90 alunos ativos", evidence_id="msg_size")
    ledger = infer_ledger_from_text(
        "agenda e reposicoes dao mais trabalho",
        previous_ledger=ledger,
        evidence_id="msg_pain",
    )

    answered = {item["question_key"]: item for item in ledger}
    assert answered["main_pain"]["status"] == "inferred_from_prior_message"
    assert answered["current_process"]["status"] == "missing"
    assert next_question_key(ledger) == "pain_detail"


def test_whatsapp_pain_with_fica_baguncada_does_not_answer_current_process():
    ledger = infer_ledger_from_text("tenho 90 alunos ativos", evidence_id="msg_size")
    ledger = infer_ledger_from_text(
        "perco interessados no whatsapp e a agenda fica baguncada",
        previous_ledger=ledger,
        evidence_id="msg_pain",
    )

    answered = {item["question_key"]: item for item in ledger}
    assert answered["main_pain"]["status"] == "inferred_from_prior_message"
    assert answered["pain_detail"]["status"] == "missing"
    assert answered["current_process"]["status"] == "missing"
    assert next_question_key(ledger) == "pain_detail"


def test_pain_mentions_sales_without_explicit_priority_does_not_answer_priority():
    ledger = infer_ledger_from_text("tenho 90 alunos ativos", evidence_id="msg_size")
    ledger = infer_ledger_from_text(
        "WhatsApp e vendas, muita gente chama e a equipe demora pra responder",
        previous_ledger=ledger,
        evidence_id="msg_pain",
    )
    ledger = infer_ledger_from_text(
        "Hoje fica tudo no WhatsApp e numa planilha, não tenho controle bom de follow-up",
        previous_ledger=ledger,
        evidence_id="msg_pain_detail",
    )
    ledger = infer_ledger_from_text(
        "Uso WhatsApp e planilha para controlar isso hoje",
        previous_ledger=ledger,
        evidence_id="msg_process",
    )

    answered = {item["question_key"]: item for item in ledger}
    assert answered["main_pain"]["status"] == "inferred_from_prior_message"
    assert answered["pain_detail"]["status"] == "inferred_from_prior_message"
    assert answered["current_process"]["status"] == "inferred_from_prior_message"
    assert answered["priority"]["status"] == "missing"
    assert next_question_key(ledger) == "priority"


def test_explicit_priority_answer_can_close_priority():
    ledger = [
        {
            "question_key": key,
            "status": "answered" if key not in {"priority", "urgency"} else "missing",
            "answer_value": f"answer:{key}" if key not in {"priority", "urgency"} else None,
            "evidence": ["msg"] if key not in {"priority", "urgency"} else [],
            "confidence": "medium" if key not in {"priority", "urgency"} else "low",
            "may_ask_again": key in {"priority", "urgency"},
        }
        for key in REQUIRED_QUESTION_KEYS
    ]

    ledger = infer_ledger_from_text(
        "minha prioridade é vendas e follow-up primeiro",
        previous_ledger=ledger,
        evidence_id="msg_priority",
    )

    answered = {item["question_key"]: item for item in ledger}
    assert answered["priority"]["status"] == "inferred_from_prior_message"
    assert next_question_key(ledger) == "urgency"


def test_llm_diagnostic_answer_interpretation_answers_pending_priority():
    ledger = [
        {
            "question_key": key,
            "status": "answered" if key not in {"priority", "urgency"} else "missing",
            "answer_value": f"answer:{key}" if key not in {"priority", "urgency"} else None,
            "evidence": ["msg"] if key not in {"priority", "urgency"} else [],
            "confidence": "medium" if key not in {"priority", "urgency"} else "low",
            "may_ask_again": key in {"priority", "urgency"},
        }
        for key in REQUIRED_QUESTION_KEYS
    ]

    next_ledger, applied = apply_diagnostic_answer_interpretation(
        {
            "current_question": "priority",
            "answer_status": "answered",
            "answer_value": "controle de pagamentos e reposições",
            "areas": ["financeiro", "reposicoes"],
            "confidence": "high",
            "evidence": ["pagamentos e reposicao"],
        },
        previous_ledger=ledger,
        evidence_id="msg_priority",
    )

    answered = {item["question_key"]: item for item in next_ledger}
    assert applied is True
    assert answered["priority"]["answer_value"] == "controle de pagamentos e reposições"
    assert answered["priority"]["areas"] == ["financeiro", "agenda_reposicoes"]
    assert answered["priority"]["confidence"] == "high"
    assert next_question_key(next_ledger) == "urgency"


def test_unclear_llm_diagnostic_answer_does_not_advance_ledger():
    ledger = empty_ledger()

    next_ledger, applied = apply_diagnostic_answer_interpretation(
        {
            "current_question": "active_students_or_size",
            "answer_status": "unclear",
            "answer_value": None,
            "confidence": "low",
            "evidence": [],
            "needs_clarification": True,
        },
        previous_ledger=ledger,
        evidence_id="msg_unclear",
    )

    assert applied is False
    assert next_ledger == ledger
    assert next_question_key(next_ledger) == "active_students_or_size"


def test_current_process_answer_does_not_count_as_urgency():
    ledger = [
        {
            "question_key": key,
            "status": "answered" if key != "urgency" else "missing",
            "answer_value": f"answer:{key}" if key != "urgency" else None,
            "evidence": ["msg"] if key != "urgency" else [],
            "confidence": "medium" if key != "urgency" else "low",
            "may_ask_again": key == "urgency",
        }
        for key in REQUIRED_QUESTION_KEYS
    ]

    ledger = infer_ledger_from_text(
        "hoje controlo em planilha e no caderno",
        previous_ledger=ledger,
        evidence_id="msg_process_late",
    )

    answered = {item["question_key"]: item for item in ledger}
    assert answered["urgency"]["status"] == "missing"
    assert ledger_is_complete(ledger) is False


def test_explicit_urgency_text_before_official_question_does_not_close_urgency():
    ledger = [
        {
            "question_key": key,
            "status": "answered" if key not in {"priority", "urgency"} else "missing",
            "answer_value": f"answer:{key}" if key not in {"priority", "urgency"} else None,
            "evidence": ["msg"] if key not in {"priority", "urgency"} else [],
            "confidence": "medium" if key not in {"priority", "urgency"} else "low",
            "may_ask_again": key in {"priority", "urgency"},
        }
        for key in REQUIRED_QUESTION_KEYS
    ]

    ledger = infer_ledger_from_text(
        "Primeiro quero organizar reposições, é urgente para esse mês.",
        previous_ledger=ledger,
        evidence_id="msg_priority_with_early_urgency",
    )

    answered = {item["question_key"]: item for item in ledger}
    assert answered["priority"]["status"] == "inferred_from_prior_message"
    assert answered["urgency"]["status"] == "missing"
    assert next_question_key(ledger) == "urgency"
    assert ledger_is_complete(ledger) is False


def test_llm_interpretation_does_not_infer_urgency_from_pain_consequences():
    ledger = [
        {
            "question_key": key,
            "status": "answered" if key not in {"priority", "urgency"} else "missing",
            "answer_value": f"answer:{key}" if key not in {"priority", "urgency"} else None,
            "evidence": ["msg"] if key not in {"priority", "urgency"} else [],
            "confidence": "medium" if key not in {"priority", "urgency"} else "low",
            "may_ask_again": key in {"priority", "urgency"},
        }
        for key in REQUIRED_QUESTION_KEYS
    ]

    next_ledger, applied = apply_diagnostic_answer_interpretation(
        {
            "current_question": "priority",
            "answer_status": "answered",
            "answer_value": "atendimento no WhatsApp e controle dos pagamentos",
            "confidence": "high",
            "evidence": ["Primeiro quero deixar mais leve o atendimento no WhatsApp e o controle dos pagamentos."],
            "areas": ["atendimento", "financeiro"],
            "additional_answers": [
                {
                    "question_key": "urgency",
                    "answer_status": "answered",
                    "answer_value": "O problema aparece quando alguém cobra, quando uma reposição vira problema ou quando um pagamento ficou para trás",
                    "confidence": "high",
                    "evidence": [
                        "fica tudo espalhado",
                        "eu só vejo quando alguém cobra",
                        "quando uma reposição vira problema",
                        "quando percebo que algum pagamento ficou para trás",
                    ],
                    "areas": ["atendimento", "agenda_reposicoes", "financeiro"],
                }
            ],
        },
        previous_ledger=ledger,
        evidence_id="msg_priority",
    )

    answered = {item["question_key"]: item for item in next_ledger}
    assert applied is True
    assert answered["priority"]["status"] == "inferred_from_prior_message"
    assert answered["urgency"]["status"] == "missing"
    assert next_question_key(next_ledger) == "urgency"
    assert ledger_is_complete(next_ledger) is False


def test_llm_interpretation_does_not_answer_urgency_before_official_question():
    ledger = [
        {
            "question_key": key,
            "status": "answered" if key not in {"priority", "urgency"} else "missing",
            "answer_value": f"answer:{key}" if key not in {"priority", "urgency"} else None,
            "evidence": ["msg"] if key not in {"priority", "urgency"} else [],
            "confidence": "medium" if key not in {"priority", "urgency"} else "low",
            "may_ask_again": key in {"priority", "urgency"},
        }
        for key in REQUIRED_QUESTION_KEYS
    ]

    next_ledger, applied = apply_diagnostic_answer_interpretation(
        {
            "current_question": "priority",
            "answer_status": "answered",
            "answer_value": "atendimento no WhatsApp",
            "confidence": "high",
            "evidence": ["Primeiro quero melhorar o atendimento no WhatsApp."],
            "areas": ["atendimento"],
            "additional_answers": [
                {
                    "question_key": "urgency",
                    "answer_status": "answered",
                    "answer_value": "Quero resolver agora",
                    "confidence": "high",
                    "evidence": ["Quero resolver agora porque estou perdendo dinheiro."],
                    "areas": ["atendimento"],
                }
            ],
        },
        previous_ledger=ledger,
        evidence_id="msg_priority_with_urgency",
    )

    answered = {item["question_key"]: item for item in next_ledger}
    assert applied is True
    assert answered["priority"]["status"] == "inferred_from_prior_message"
    assert answered["urgency"]["status"] == "missing"
    assert next_question_key(next_ledger) == "urgency"
    assert ledger_is_complete(next_ledger) is False


def test_plain_name_does_not_answer_pending_size_question():
    ledger = infer_ledger_from_text(
        "Lucas",
        previous_ledger=empty_ledger(),
        evidence_id="msg_name",
    )

    answered = {item["question_key"]: item for item in ledger}
    assert answered["active_students_or_size"]["status"] == "missing"
    assert next_question_key(ledger) == "active_students_or_size"


def test_plain_number_answers_pending_size_question():
    ledger = infer_ledger_from_text(
        "100",
        previous_ledger=empty_ledger(),
        evidence_id="msg_size",
    )

    answered = {item["question_key"]: item for item in ledger}
    assert answered["active_students_or_size"]["status"] == "inferred_from_prior_message"
    assert next_question_key(ledger) == "main_pain"


def test_unresolved_or_missing_keys_block_completion():
    ledger = empty_ledger()
    assert missing_or_unresolved_keys(ledger)
    assert ledger_is_complete(ledger) is False


def test_complete_ledger_allows_diagnostic_completion():
    ledger = [
        {
            "question_key": key,
            "status": "answered",
            "answer_value": f"answer:{key}",
            "evidence": ["msg"],
            "confidence": "medium",
            "may_ask_again": False,
        }
        for key in REQUIRED_QUESTION_KEYS
    ]

    assert ledger_is_complete(ledger) is True
