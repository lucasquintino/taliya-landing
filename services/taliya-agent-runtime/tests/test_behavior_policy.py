from app.domains.taliya_commercial.behavior_policy import assess_profile_name, is_cold_greeting_only, route_from_text


def test_cold_greeting_detection_is_narrow():
    assert is_cold_greeting_only("oi")
    assert is_cold_greeting_only("Bom dia!")
    assert not is_cold_greeting_only("oi, quero saber preco")


def test_profile_name_assessment_accepts_person_name_and_rejects_business_name():
    reliable = assess_profile_name("Mariana Costa")
    business = assess_profile_name("Studio Viva Pilates")

    assert reliable.status == "reliable"
    assert reliable.first_name == "Mariana"
    assert business.status == "unreliable"


def test_route_signal_keeps_mock_path_aligned_with_policy():
    assert route_from_text("quanto custa?") == "product"
    assert route_from_text("quero fazer diagnostico") == "diagnostic"
    assert route_from_text("quero falar com uma pessoa") == "handoff"
