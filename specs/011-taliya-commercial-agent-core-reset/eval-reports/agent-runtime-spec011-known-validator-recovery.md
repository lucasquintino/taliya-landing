# agent-runtime-spec011-known-validator-recovery

Release gate: pass
Paid OpenAI spend: US$0
Passed: 9/9

## Covered Validator Codes

- `demo_direct_question_flags_missing`
- `diagnostic_final_demo_stage_missing`
- `diagnostic_final_staged_order_invalid`
- `diagnostic_next_question_invalid`
- `diagnostic_next_question_not_missing`
- `diagnostic_start_must_ask_active_students`
- `diagnostic_urgency_answer_not_captured`
- `pain_first_diagnostic_offer_must_use_diagnostic_route`
- `pain_first_must_offer_diagnostic`
- `price_question_missing_diagnostic_hook`
- `price_question_missing_diagnostic_offer`
- `price_question_missing_price_answer`
- `sales_inbox_diagnostic_status_mismatch`
- `stale_demo_direct_without_current_request`
- `unsupported_schema_version`

## PASS pain_first_question_only_no_500

```json
{
  "validatorCodes": [
    "pain_first_must_offer_diagnostic"
  ],
  "recovery": "structural_repair",
  "command": "python -m pytest services\\taliya-agent-runtime\\tests\\test_spec011_widget_runtime_adapter.py::test_runtime_adapter_repairs_pain_first_question_only_without_500 -q",
  "output": ".                                                                        [100%]\r\n1 passed in 1.25s"
}
```

## PASS pain_first_schema_alias_no_500

```json
{
  "validatorCodes": [
    "unsupported_schema_version",
    "diagnostic_start_must_ask_active_students"
  ],
  "recovery": "structural_repair",
  "command": "python -m pytest services\\taliya-agent-runtime\\tests\\test_spec011_widget_runtime_adapter.py::test_runtime_adapter_repairs_known_schema_alias_on_pain_first_without_500 -q",
  "output": ".                                                                        [100%]\r\n1 passed in 1.21s"
}
```

## PASS pain_first_product_route_no_500

```json
{
  "validatorCodes": [
    "pain_first_diagnostic_offer_must_use_diagnostic_route",
    "diagnostic_start_must_ask_active_students"
  ],
  "recovery": "structural_repair",
  "command": "python -m pytest services\\taliya-agent-runtime\\tests\\test_spec011_widget_runtime_adapter.py::test_runtime_adapter_repairs_pain_first_product_route_without_paid_repair -q",
  "output": ".                                                                        [100%]\r\n1 passed in 1.29s"
}
```

## PASS pending_urgency_answer_llm_repair

```json
{
  "validatorCodes": [
    "diagnostic_urgency_answer_not_captured"
  ],
  "recovery": "one_call_llm_repair",
  "command": "python -m pytest services\\taliya-agent-runtime\\tests\\test_spec011_repair_loop.py::test_repair_loop_sends_pending_urgency_answer_to_llm_repair -q",
  "output": ".                                                                        [100%]\r\n1 passed in 0.42s"
}
```

## PASS invalid_diagnostic_next_question_llm_repair

```json
{
  "validatorCodes": [
    "diagnostic_next_question_invalid"
  ],
  "recovery": "one_call_llm_repair",
  "command": "python -m pytest services\\taliya-agent-runtime\\tests\\test_spec011_repair_loop.py::test_repair_loop_sends_invalid_diagnostic_next_question_to_llm_repair -q",
  "output": ".                                                                        [100%]\r\n1 passed in 0.42s"
}
```

## PASS long_conversation_stale_state_no_500

```json
{
  "validatorCodes": [
    "stale_demo_direct_without_current_request",
    "sales_inbox_diagnostic_status_mismatch"
  ],
  "recovery": "state_projection_repair",
  "command": "python -m pytest services\\taliya-agent-runtime\\tests\\test_spec011_widget_runtime_adapter.py::test_runtime_adapter_long_conversation_preflight_covers_last_real_gate_failures -q",
  "output": ".                                                                        [100%]\r\n1 passed in 1.19s"
}
```

## PASS final_diagnostic_last_pending_answer_no_500

```json
{
  "validatorCodes": [
    "diagnostic_next_question_not_missing",
    "diagnostic_final_demo_stage_missing",
    "diagnostic_final_staged_order_invalid"
  ],
  "recovery": "structural_final_diagnostic_repair",
  "command": "python -m pytest services\\taliya-agent-runtime\\tests\\test_spec011_repair_loop.py::test_repair_loop_completes_final_diagnostic_when_last_pending_answer_captured -q",
  "output": ".                                                                        [100%]\r\n1 passed in 0.40s"
}
```

## PASS current_demo_request_stale_price_intent_no_500

```json
{
  "validatorCodes": [
    "price_question_missing_price_answer",
    "price_question_missing_diagnostic_hook",
    "price_question_missing_diagnostic_offer",
    "demo_direct_question_flags_missing"
  ],
  "recovery": "structural_demo_direct_repair",
  "command": "python -m pytest services\\taliya-agent-runtime\\tests\\test_spec011_repair_loop.py::test_repair_loop_clears_stale_price_intent_for_current_demo_request -q",
  "output": ".                                                                        [100%]\r\n1 passed in 0.40s"
}
```

## PASS long_conversation_latest_paid_500s_adapter_no_500

```json
{
  "validatorCodes": [
    "diagnostic_next_question_not_missing",
    "diagnostic_final_demo_stage_missing",
    "diagnostic_final_staged_order_invalid",
    "price_question_missing_price_answer",
    "demo_direct_question_flags_missing"
  ],
  "recovery": "adapter_sequential_structural_repair",
  "command": "python -m pytest services\\taliya-agent-runtime\\tests\\test_spec011_widget_runtime_adapter.py::test_runtime_adapter_long_conversation_preflight_covers_latest_paid_500s -q",
  "output": ".                                                                        [100%]\r\n1 passed in 1.22s"
}
```
