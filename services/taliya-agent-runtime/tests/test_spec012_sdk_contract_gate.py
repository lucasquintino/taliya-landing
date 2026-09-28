"""T012-041: no-cost SDK contract gate manifest."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
TESTS = ROOT / "services" / "taliya-agent-runtime" / "tests"

REQUIRED_CONTRACT_FILES: dict[str, tuple[str, ...]] = {
    "test_spec012_conductor_decision.py": (
        "test_conductor_decision_is_strict_sdk_output_compatible",
        "test_conductor_decision_rejects_superseded_boundary_fields",
        "test_conductor_decision_rejects_invented_actions_and_slot_keys",
        "test_action_menus_preserve_011_contract_with_012_delta_actions",
        "test_turn_action_literal_and_menus_are_consistent",
        "test_composition_set_excludes_official_only_variables",
        "test_validate_action_decision_form_checks",
    ),
    "test_spec012_action_agents.py": (
        "test_action_first_agents_use_conductor_decision_and_no_tools",
        "test_starting_agent_is_deterministic_from_mode",
        "test_instructions_carry_the_action_first_contract",
        "test_instructions_carry_delta_refusal_objection_and_resume_policy",
        "test_no_cost_end_to_end_board_to_compiled_turn",
    ),
    "test_spec012_sdk_output_adapter.py": (
        "test_spec012_turn_proposal_schema_accepts_structured_proposal",
        "test_spec012_output_adapter_adds_runtime_identity_fields",
        "test_spec012_output_adapter_extracts_basic_sdk_run_items_when_agent_path_missing",
        "test_spec012_output_adapter_rejects_freeform_final_output",
        "test_spec012_turn_proposal_rejects_direct_output_fields",
        "test_spec012_turn_proposal_rejects_product_claim_without_fact_ref",
        "test_spec012_output_adapter_does_not_import_public_runtime_endpoint",
    ),
    "test_spec012_sdk_agents.py": (
        "test_spec012_minimal_sdk_agent_topology_matches_design_lock",
        "test_spec012_agent_instructions_preserve_llm_first_boundaries",
        "test_spec012_builds_real_sdk_agents_with_sdk_tools_and_without_paid_run",
        "test_spec012_sdk_tool_catalog_matches_read_only_and_proposal_only_lock",
        "test_spec012_sdk_tools_return_non_committing_envelopes",
        "test_spec012_sdk_tools_do_not_contain_commercial_shortcut_parser",
        "test_spec012_sdk_agents_are_not_imported_by_public_runtime_endpoint",
    ),
    "test_spec012_sdk_preflight.py": (
        "test_preflight_every_template_variable_has_a_registry_spec",
        "test_preflight_golden_templates_are_in_the_final_agents_embedded_catalog",
        "test_preflight_golden_variables_conform_to_registry_specs",
        "test_preflight_canary_subset_covers_observed_failure_classes",
        "test_preflight_persisted_current_agents_are_valid_agent_names",
        "test_preflight_embedded_catalogs_only_list_registry_templates",
    ),
    "test_spec012_sdk_spike_isolation.py": (
        "test_spec012_sdk_spike_package_is_not_public_endpoint_cutover",
        "test_spec012_sdk_spike_blocks_paid_calls_without_approval",
        "test_spec012_sdk_spike_runs_with_mocked_no_cost_runner",
    ),
    "test_spec012_sdk_paid_harness_dry_run.py": (
        "test_spec012_strict_output_schema_is_sdk_compatible",
        "test_spec012_agents_declare_strict_structured_output_type",
        "test_spec012_frozen_scenarios_match_approval_packet",
        "test_spec012_dry_run_full_real_runner_path",
        "test_spec012_dry_run_state_snapshot_reaches_tools_via_run_context",
        "test_spec012_dry_run_single_repair_operation_recovers_validator_failure",
        "test_spec012_dry_run_repair_respects_per_scenario_operation_cap",
        "test_spec012_validator_allows_unanswered_question_during_delivery_deferral",
        "test_spec012_diagnostic_sequence_guardrail_is_deterministic",
        "test_spec012_dry_run_free_form_output_aborts_run",
        "test_spec012_dry_run_budget_meter_stops_before_ceiling",
        "test_spec012_paid_run_remains_blocked_without_explicit_approval",
        "test_spec012_paid_run_preconditions_block_unpriced_model_and_missing_key",
        "test_spec012_agent_instructions_embed_official_template_catalog",
        "test_spec012_template_variables_normalize_to_official_registry_spec",
        "test_spec012_harness_keeps_public_runtime_isolated",
    ),
    "test_spec012_sdk_validators_adapter.py": (
        "test_spec012_spike_validator_renders_approved_template_preview_only",
        "test_spec012_spike_validator_blocks_unanswered_direct_question",
        "test_spec012_spike_validator_blocks_missing_required_template_variable",
        "test_spec012_spike_validator_blocks_unknown_template",
        "test_spec012_spike_validator_adapter_does_not_parse_commercial_text",
        "test_spec012_spike_validator_adapter_is_not_public_endpoint_cutover",
    ),
    "test_spec012_turn_situation.py": (
        "test_builder_signature_has_no_lead_text_parameter",
        "test_empty_state_is_entry_mode_first_contact",
        "test_diagnostic_in_progress_pending_key_and_completion_gate",
        "test_diagnostic_last_key_pending_allows_completion",
        "test_operational_precedence_over_canonical_state",
        "test_canonical_states_map_to_modes",
        "test_post_diagnostic_with_joined_waitlist_blocks_reoffer",
        "test_post_diagnostic_preamble_carries_compact_delta_context",
        "test_profile_name_context_marks_reliable_and_unreliable_names",
        "test_preamble_carries_compact_memory",
    ),
    "test_spec012_action_turn_runner.py": (
        "test_official_facts_resolver_formats_from_real_knowledge",
        "test_official_facts_resolver_selects_delta_product_summary",
        "test_official_facts_resolver_selects_routine_areas_summary",
        "test_paid_calls_stay_blocked_without_approval",
        "test_full_funnel_segment_with_state_evolution",
        "test_adequacy_failure_is_repaired_in_one_operation",
        "test_conversation_cost_cap_defers_next_turn_without_calling_sdk",
        "test_conversation_cost_cap_can_be_disabled_for_local_harnesses",
        "test_routine_areas_question_uses_official_delta_fact_without_paid_call",
        "test_post_diagnostic_messy_price_resume_does_not_restart_diagnostic",
        "test_diagnostic_interruption_availability_answers_then_resumes_pending_question",
        "test_diagnostic_correction_replaces_previous_number_in_committed_state",
        "test_diagnostic_multiple_answers_in_one_message_commits_both_slots",
        "test_diagnostic_price_objection_answers_then_resumes_pending_question",
        "test_waitlist_pending_product_question_answers_then_asks_missing_studio",
        "test_post_diagnostic_demo_resume_after_days_does_not_restart_diagnostic",
        "test_diagnostic_refusal_price_question_answers_without_reoffering_diagnostic",
        "test_post_waitlist_product_resume_preserves_joined_status",
        "test_parroting_composition_is_blocked",
    ),
    "test_spec012_runtime_adapter.py": (
        "test_t012_031_runtime_adapter_returns_agent_run_response_with_no_cost_model",
        "test_t012_031_runtime_adapter_persists_action_first_state_fields",
        "test_t012_050_shadow_mode_suppresses_delivery_and_does_not_mutate_state",
        "test_t012_036_runtime_adapter_cost_cap_blocks_before_sdk_call",
        "test_t012_055_runtime_adapter_runs_openai_provider_after_public_activation",
    ),
    "test_spec012_canonical_fixture_port.py": (
        "test_t012_038_canonical_fixture_map_matches_spec011_sources",
        "test_t012_038_canonical_fixture_regression_ids_exist",
        "test_t012_038_every_ported_fixture_has_action_first_owner_and_proof_mode",
        "test_t012_038_map_keeps_paid_real_model_work_explicitly_deferred",
    ),
    "test_spec012_canonical_action_first_mocked.py": (
        "test_t012_038_mocked_canonical_price_first_runs_action_pipeline",
        "test_t012_038_mocked_canonical_price_plus_pain_uses_context_hook",
        "test_t012_038_mocked_canonical_pain_first_offers_before_starting_diagnostic",
        "test_t012_038_mocked_canonical_instagram_source_opening",
        "test_t012_038_mocked_canonical_whatsapp_question_uses_scope",
        "test_t012_038_mocked_canonical_demo_request_uses_official_link",
        "test_t012_038_mocked_canonical_waitlist_joined_keeps_no_checkout",
        "test_t012_038_mocked_canonical_step3g_long_conversation_stateful",
        "test_t012_038_mocked_canonical_human_request_suppresses_next_turn",
        "test_t012_038_mocked_canonical_simple_number_advances_diagnostic",
    ),
    "test_spec012_canonical_do_not_do_mocked.py": (
        "test_t012_038_do_not_do_early_phone_capture_answers_price_only",
        "test_t012_038_do_not_do_checkout_buy_intent_goes_to_waitlist",
        "test_t012_038_do_not_do_date_vip_discount_uses_waitlist_safely",
        "test_t012_038_do_not_do_integration_scope_no_invented_integration",
        "test_t012_038_do_not_do_security_data_no_certification_promise",
        "test_t012_038_do_not_do_studio_whatsapp_connection_capture",
        "test_t012_038_do_not_do_wrong_student_language",
        "test_t012_038_do_not_do_price_497_not_student_count",
    ),
    "test_spec012_canonical_p0_mocked.py": (
        "test_t012_038_p0_internal_metadata_leak_is_not_rendered",
        "test_t012_038_p0_urgency_timing_is_captured_before_final",
        "test_t012_038_p0_valid_short_answer_advances_diagnostic",
        "test_t012_038_p0_final_diagnostic_not_truncated",
        "test_t012_038_p0_final_diagnostic_plain_studio_language",
        "test_t012_038_p0_sales_inbox_consistency_price_plus_pain",
        "test_t012_038_p0_false_pass_requires_model_and_rendered_behavior",
    ),
    "test_spec012_sdk_mocked_contracts.py": (
        "test_spec012_mocked_sdk_contract_scenarios_validate_and_render",
        "test_spec012_mocked_contract_covers_required_spike_scenarios",
        "test_spec012_mocked_contract_keeps_497_as_plan_price_not_student_count",
        "test_spec012_mocked_contract_does_not_offer_waitlist_for_curiosity",
        "test_spec012_mocked_contract_persists_handoff_pause_as_proposal_only",
        "test_spec012_mocked_contract_defers_delivery_concurrency_without_public_delivery",
        "test_spec012_mocked_contract_tests_do_not_call_real_sdk_runner",
    ),
    "test_spec012_sdk_ideal_conversation.py": (
        "test_ideal_conversation_script_covers_the_full_funnel",
        "test_ideal_conversation_commits_state_between_turns_no_cost",
        "test_ideal_conversation_stops_at_first_failed_turn",
    ),
    "test_spec012_decision_compiler.py": (
        "test_compiler_signature_has_no_lead_text_parameter",
        "test_answer_price_compiles_with_compiler_owned_official_variable",
        "test_t011_105_regression_action_without_composition_fails",
        "test_capture_answer_merges_ledger_and_asks_next",
        "test_complete_diagnostic_derives_full_staged_sequence",
        "test_handoff_compiles_pause_patch_and_requires_reason",
        "test_delta_contract_compiles_how_it_works_with_state_next_step",
        "test_delta_contract_compiles_comparison_only_with_lead_context",
        "test_delta_contract_compiles_security_and_integration_safe_templates",
        "test_delta_contract_compiles_availability_without_checkout_or_date_promise",
        "test_delta_contract_compiles_out_of_profile_without_diagnostic_offer",
        "test_038b_fixture_correction_replaces_previous_diagnostic_number",
        "test_038b_fixture_multiple_diagnostic_answers_in_one_message",
        "test_038b_fixture_messy_price_interruption_answers_then_resumes_diagnostic",
        "test_038b_fixture_messy_demo_request_uses_official_demo_link",
        "test_038b_fixture_price_objection_mid_diagnostic_answers_then_resumes",
        "test_038b_interruption_matrix_answers_product_question_then_resumes_diagnostic",
        "test_038b_fixture_resume_after_days_uses_post_diagnostic_memory",
        "test_032b_post_diagnostic_price_resume_does_not_restart_diagnostic",
        "test_038b_fixture_waitlist_resume_answers_question_then_missing_studio",
        "test_038b_fixture_demo_resume_after_days_does_not_restart_diagnostic",
        "test_032b_diagnostic_refusal_answers_price_without_reoffering_diagnostic",
        "test_032b_reliable_profile_name_personalizes_cold_greeting_only",
        "test_032b_reliable_profile_name_personalizes_diagnostic_start",
        "test_032b_diagnostic_start_still_works_after_name_was_skipped",
        "test_every_turn_action_is_explicitly_compiled",
        "test_template_group_boundary_flags_out_of_mode_templates",
    ),
    "test_spec012_renderer_compiler.py": (
        "test_033_renderer_starts_diagnostic_without_name_question",
        "test_033_renderer_accepts_compiler_owned_how_it_works_enum_variable",
        "test_033_renderer_accepts_compiler_staged_final_diagnostic_plan",
    ),
    "test_spec012_action_validators.py": (
        "test_action_validator_ports_spec011_price_hook_requirement",
        "test_action_validator_blocks_invented_demo_link",
        "test_action_validator_blocks_waitlist_from_demo_curiosity",
        "test_action_validator_blocks_internal_label_leak_in_composition",
    ),
    "test_spec012_action_validators_ported.py": (
        "test_action_validator_blocks_waitlist_offer_from_demo_curiosity",
        "test_action_validator_starts_diagnostic_without_name_question",
        "test_action_validator_ports_internal_source_label_leak_block",
        "test_action_validator_blocks_crm_jargon_for_lay_lead",
        "test_action_validator_allows_crm_term_when_lead_used_it",
        "test_action_validator_blocks_rejected_final_diagnostic_phrase",
        "test_action_validator_blocks_thin_context_pelo_que_voce_contou",
        "test_action_validator_blocks_waitlist_checkout_discount_promise",
        "test_action_validator_ports_price_answer_adequacy_map",
        "test_action_validator_ports_integration_scope_before_handoff_contract",
        "test_action_validator_accepts_waitlist_offer_for_contract_intent",
        "test_action_validator_blocks_demo_offer_without_demo_template",
        "test_action_validator_requires_handoff_reason_and_ack_template",
        "test_action_validator_accepts_handoff_with_reason_and_pause_patch",
    ),
    "test_spec012_action_safety.py": (
        "test_safety_guardrail_blocks_prompt_injection",
        "test_safety_guardrail_blocks_unsupported_media",
        "test_safety_guardrail_blocks_sensitive_data",
        "test_safety_guardrail_allows_security_policy_question",
        "test_safety_guardrail_blocks_medical_advice",
        "test_safety_guardrail_does_not_classify_commercial_price_question",
        "test_action_runner_safety_guardrail_skips_sdk_and_renders_template",
    ),
    "test_spec012_action_trace_export.py": (
        "test_trace_export_packages_required_sections_without_external_export",
        "test_trace_export_includes_safety_turn_as_zero_cost_no_llm_trace",
    ),
    "test_spec012_sales_inbox_projection.py": (
        "test_t012_035_sales_inbox_projection_for_price_turn",
        "test_t012_035_sales_inbox_projection_for_completed_diagnostic",
        "test_t012_046_exports_sales_inbox_projection_evidence_package",
        "test_t012_046_exports_joined_waitlist_projection_history",
    ),
    "test_spec012_quality_judge.py": (
        "test_t012_039_mocked_quality_judge_cannot_release",
        "test_t012_039_real_quality_judge_passes_when_thresholds_hold",
        "test_t012_039_quality_judge_blocks_average_below_gate",
        "test_t012_039_quality_judge_blocks_any_dimension_below_four",
        "test_t012_039_blocking_failures_override_judge_score",
        "test_t012_039_quality_judge_requires_all_contract_dimensions",
        "test_t012_039_exports_eval_contract_evidence_package_without_release",
    ),
    "test_spec012_manual_review_package.py": (
        "test_t012_047_exports_manual_transcript_review_package",
    ),
    "test_spec012_sdk_run_items_mocked.py": (
        "test_t012_042_router_handoff_run_items_are_structural",
        "test_t012_042_specialist_direct_run_items_skip_router",
        "test_t012_042_repair_trace_records_validator_feedback_and_repair_items",
        "test_t012_042_safety_boundary_has_no_sdk_run_items",
    ),
    "test_spec012_static_audit.py": (
        "test_t012_037_next_runtime_turn_has_no_old_runner_public_fallback",
        "test_t012_037_whatsapp_route_delegates_to_runtime_not_ts_v2_engine",
        "test_t012_040_blocks_regex_as_commercial_brain_in_action_core",
        "test_t012_040_sdk_tools_remain_read_only_or_proposal_only",
        "test_t012_040_sdk_tools_cannot_commit_or_deliver_during_reasoning",
        "test_t012_040_sdk_output_cannot_deliver_free_text_directly",
        "test_t012_040_isolated_runner_has_no_public_old_runner_fallback",
        "test_t012_040_sdk_path_is_the_only_public_commercial_runtime",
        "test_t012_040_prompts_and_templates_do_not_hardcode_unsafe_promises",
        "test_t012_040_sdk_external_tracing_stays_disabled",
        "test_t012_040_sdk_trace_export_does_not_claim_public_delivery",
    ),
}


def test_t012_041_contract_gate_manifest_files_and_anchors_exist() -> None:
    missing: list[str] = []
    for file_name, anchors in REQUIRED_CONTRACT_FILES.items():
        path = TESTS / file_name
        if not path.exists():
            missing.append(f"{file_name}:missing_file")
            continue
        source = path.read_text(encoding="utf-8")
        for anchor in anchors:
            if f"def {anchor}" not in source and f"async def {anchor}" not in source:
                missing.append(f"{file_name}:{anchor}")

    assert missing == []


def test_t012_041_contract_gate_is_no_cost_and_isolated() -> None:
    source = "\n".join(
        (TESTS / file_name).read_text(encoding="utf-8")
        for file_name in REQUIRED_CONTRACT_FILES
    )
    forbidden_cost_fragments = (
        "paid_openai_approved=True",
        "OPENAI_API_KEY",
    )
    non_static_audit_source = "\n".join(
        (TESTS / file_name).read_text(encoding="utf-8")
        for file_name in REQUIRED_CONTRACT_FILES
        if file_name != "test_spec012_static_audit.py"
    )
    forbidden_runtime_path_fragments = (
        "app/api/landing",
        "lib/landing/ai-attendant",
    )

    assert [fragment for fragment in forbidden_cost_fragments if fragment in source] == []
    assert [
        fragment
        for fragment in forbidden_runtime_path_fragments
        if fragment in non_static_audit_source
    ] == []
    assert "ScriptedFakeModel" in source
    assert "SdkSpikePaidCallBlocked" in source
