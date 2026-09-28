from app.domains.taliya_commercial.state import (
    ALL_STATES,
    ConversationState,
    allowed_next_states,
    is_high_impact_transition,
    is_transition_allowed,
    next_state_after_response,
    state_for_route,
)


def test_contract_contains_canonical_states():
    assert "greeting_only" in ALL_STATES
    assert "diagnostic_delivered" in ALL_STATES
    assert "waitlist_pending_data" in ALL_STATES
    assert "paused_by_human" in ALL_STATES


def test_cold_greeting_cannot_jump_to_diagnostic_or_waitlist():
    allowed = allowed_next_states("greeting_only")

    assert "diagnostic_offered" not in allowed
    assert "waitlist_offered" not in allowed
    assert "waitlist_joined" not in allowed


def test_product_and_price_states_trend_to_diagnostic_after_direct_answer():
    assert is_transition_allowed("price_question", "diagnostic_offered")
    assert is_transition_allowed("product_question", "diagnostic_offered")


def test_state_helpers_map_routes_to_expected_states():
    assert state_for_route("diagnostic", diagnostic_action="offer") == ConversationState.DIAGNOSTIC_OFFERED
    assert state_for_route("waitlist", waitlist_status="pending_details") == ConversationState.WAITLIST_PENDING_DATA
    assert next_state_after_response("human_handoff") == ConversationState.PAUSED_BY_HUMAN


def test_high_impact_transitions_require_validation():
    assert is_high_impact_transition("diagnostic_delivered")
    assert is_high_impact_transition("waitlist_joined")
    assert not is_high_impact_transition("general_interest")
