# agent-runtime-spec011-golden-transcripts-preflight

Release gate: fail
Passed: 3/8
Runtime evidence cost: US$0.115717

## PASS final-price-first

Cases: RC-011-052
Evidence: specs\011-taliya-commercial-agent-core-reset\eval-reports\agent-runtime-spec011-full-required-final-matrix-budgeted-1.json

## PASS final-price-plus-pain

Cases: RC-011-053
Evidence: specs\011-taliya-commercial-agent-core-reset\eval-reports\agent-runtime-spec011-full-required-final-matrix-budgeted-1.json

## FAIL final-instagram-interest

Cases: RC-011-054
Evidence: specs\011-taliya-commercial-agent-core-reset\eval-reports\agent-runtime-spec011-full-required-final-matrix-budgeted-1.json
Failures:
- missing required rendered text: Instagram

## FAIL final-whatsapp-question

Cases: RC-011-055
Evidence: specs\011-taliya-commercial-agent-core-reset\eval-reports\agent-runtime-spec011-full-required-final-matrix-budgeted-1.json
Failures:
- template id missing from final decision: product.demo_direct
- missing required rendered text: alunos
- missing required rendered text: nao precisam baixar aplicativo

## FAIL step3g-long-conversation

Cases: RC-011-056, RC-011-060
Evidence: null
Failures:
- missing scenario evidence report

## PASS final-waitlist-joined

Cases: RC-011-057
Evidence: specs\011-taliya-commercial-agent-core-reset\eval-reports\agent-runtime-spec011-full-required-final-matrix-budgeted-1.json

## FAIL final-human-request-silent-after

Cases: RC-011-058
Evidence: specs\011-taliya-commercial-agent-core-reset\eval-reports\agent-runtime-spec011-full-required-remaining-budgeted-1.json
Failures:
- handoff status expected requested, got active

## FAIL final-demo-request

Cases: RC-011-059
Evidence: specs\011-taliya-commercial-agent-core-reset\eval-reports\agent-runtime-spec011-full-required-final-matrix-budgeted-1.json
Failures:
- direct_question_answered_first expected true, got false
