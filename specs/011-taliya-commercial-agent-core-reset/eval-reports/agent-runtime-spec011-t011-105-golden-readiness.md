# agent-runtime-spec011-t011-105-golden-readiness

Release gate: fail
Passed: 7/9
Runtime evidence cost: US$0.424509

## PASS final-price-first

Cases: RC-011-052
Evidence: specs\011-taliya-commercial-agent-core-reset\eval-reports\agent-runtime-spec011-full-required-final-matrix-budgeted-1.json

## PASS final-price-plus-pain

Cases: RC-011-053
Evidence: specs\011-taliya-commercial-agent-core-reset\eval-reports\agent-runtime-spec011-full-required-final-matrix-budgeted-1.json

## FAIL final-pain-first

Cases: RC-011-053A
Evidence: specs\011-taliya-commercial-agent-core-reset\eval-reports\agent-runtime-spec011-full-required-final-matrix-budgeted-1.json
Failures:
- no candidate evidence satisfied fixture expectations across 1 passing runtime report(s)
- forbidden rendered text present: lead loses
- forbidden rendered text present: interested leads
- forbidden rendered text present: team takes too long

## PASS final-instagram-interest

Cases: RC-011-054
Evidence: specs\011-taliya-commercial-agent-core-reset\eval-reports\agent-runtime-spec011-full-required-final-matrix-budgeted-1.json

## PASS final-whatsapp-question

Cases: RC-011-055
Evidence: specs\011-taliya-commercial-agent-core-reset\eval-reports\agent-runtime-spec011-full-required-final-matrix-budgeted-1.json

## FAIL step3g-long-conversation

Cases: RC-011-056, RC-011-060
Evidence: specs\011-taliya-commercial-agent-core-reset\eval-reports\agent-runtime-spec011-golden-long-conversation-16.json
Failures:
- no passing evidence report; failures: expected completed diagnostic, got None; price objection did not validate the value concern naturally

## PASS final-waitlist-joined

Cases: RC-011-057
Evidence: specs\011-taliya-commercial-agent-core-reset\eval-reports\agent-runtime-spec011-full-required-final-matrix-budgeted-1.json

## PASS final-human-request-silent-after

Cases: RC-011-058
Evidence: specs\011-taliya-commercial-agent-core-reset\eval-reports\agent-runtime-spec011-full-required-remaining-budgeted-1.json

## PASS final-demo-request

Cases: RC-011-059
Evidence: specs\011-taliya-commercial-agent-core-reset\eval-reports\agent-runtime-spec011-golden-demo-direct-fixed-1.json
