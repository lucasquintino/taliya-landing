# Taliya Agent V2 Environment

## Runtime Flags

- `AI_ATTENDANT_V2_MODE` unset: defaults to `auto`. The v2 agent is the current production path.
- `AI_ATTENDANT_V2_MODE=legacy`: explicit rollback only. Existing legacy agent replies.
- `AI_ATTENDANT_V2_MODE=capture_only`: emergency/staging mode only. v2 normalizes, traces and stores state without sending automatic v2 replies.
- `AI_ATTENDANT_V2_MODE=auto`: v2 answers automatically.
- `AI_ATTENDANT_V2_KILL_SWITCH=true`: disables automatic v2 replies and keeps capture/logging safe.
- `AI_ATTENDANT_V2_DISABLED=true`: alias kill switch.
- `AI_ATTENDANT_V2_LEGACY_FALLBACK=true`: allows legacy fallback only with `capture_only` for rollback/debug. Leave unset in production v2.

## Cost Controls

- `AI_ATTENDANT_V2_HARD_COST_CAP_USD=0.15`
- `AI_ATTENDANT_V2_REVIEW_COST_USD=0.05`
- `AI_ATTENDANT_V2_HIGH_COST_USD=0.10`
- `AI_ATTENDANT_MODEL`: default low-cost generation model.
- `AI_ATTENDANT_V2_STRONG_MODEL`: optional escalation model.

## Production Behavior

Production should run v2 by leaving `AI_ATTENDANT_V2_MODE` unset or setting it to `auto`.

Use `AI_ATTENDANT_V2_KILL_SWITCH=true` for an emergency stop that preserves capture/logging, or `AI_ATTENDANT_V2_MODE=legacy` only as an explicit rollback.
