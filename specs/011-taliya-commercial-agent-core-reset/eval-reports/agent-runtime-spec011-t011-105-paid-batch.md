# agent-runtime-spec011-t011-105-paid-batch

Release gate: fail_stopped_after_pain_first
Estimated paid cost: US$0.005045
Paid commands started: 1
Source fingerprint: b6bc712960ac06a93f80eff575a732cfb7e3d86f22cc0e7a6cbfce54fe159c9b

## PASS readiness_gate_before_paid_batch

```text
node scripts\eval-agent-runtime-spec011-t011-105-readiness.mjs
```

Output:
```text
agent-runtime-spec011-t011-105-readiness: 13/13 passed
Release gate: ready_for_paid_batch
Report JSON: C:\Users\lucas\agentes-landing-system\specs\011-taliya-commercial-agent-core-reset\eval-reports\agent-runtime-spec011-t011-105-readiness.json
Report MD: C:\Users\lucas\agentes-landing-system\specs\011-taliya-commercial-agent-core-reset\eval-reports\agent-runtime-spec011-t011-105-readiness.md
```

## PASS source_stable_after_readiness

```text
source fingerprint stability check
```

Output:
```text
Source fingerprint stable: b6bc712960ac06a93f80eff575a732cfb7e3d86f22cc0e7a6cbfce54fe159c9b
```

## FAIL paid_pain_first

```text
python scripts\eval-agent-runtime-spec011.py --fixture scripts\fixtures\agent-runtime\spec-011-golden-transcripts.json --scenario-id final-pain-first --max-scenarios 1 --max-model-calls 1 --max-cost-usd 0.03 --report-name agent-runtime-spec011-golden-pain-first-1
```

Output:
```text
agent-runtime-real-openai: 0/1 passed
Report JSON: C:\Users\lucas\agentes-landing-system\specs\011-taliya-commercial-agent-core-reset\eval-reports\agent-runtime-spec011-golden-pain-first-1.json
Transcript MD: C:\Users\lucas\agentes-landing-system\specs\011-taliya-commercial-agent-core-reset\eval-reports\agent-runtime-spec011-golden-pain-first-1.md
- final-pain-first: did not reuse lead context terms: ['whatsapp', 'interessado']
```

## PASS source_stable_after_pain_first

```text
source fingerprint stability check
```

Output:
```text
Source fingerprint stable: b6bc712960ac06a93f80eff575a732cfb7e3d86f22cc0e7a6cbfce54fe159c9b
```
