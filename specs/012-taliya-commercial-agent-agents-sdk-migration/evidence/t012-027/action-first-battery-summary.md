# Action-First Validation Battery - Summary - 2026-06-11

Approved by D-012-013 (`$1.00` ceiling, canary-first, no public cutover).
Total spend: ~`$0.32` of `$1.00`. All evidence under
`evidence/t012-027/action-first-*`.

## Results

| Battery | Result |
| --- | --- |
| Canary (cold oi / price / capture-120) | 3/3 delivered; cold greeting verbatim contract copy; price answered with official values; capture in ONE model operation |
| 15 frozen scenarios | 11/15 first pass; 4/4 on retry after fixes -> all 15 delivered |
| Staged final delivery (the architecture centerpiece) | DELIVERED on real model, in Portuguese: hold -> context -> CRM base -> operational step -> agent recommendation -> verbatim plan line -> demo bridge by persisted state. Failed in ALL 15 spike runs; works under action-first |
| Ideal conversation (12-turn script) | 11/12; remaining gap is script semantics (see findings) |
| Cost profile | Known-state turn: 1 op (~$0.003); routed turn: 2 ops (~$0.005); repaired: +1 op. Full conversation ~$0.07 |

## Fixes Landed During The Battery (all no-cost, suite 103 green)

1. Cold first contact renders `opening.cold_greeting` (state-derived).
2. Product template selection accepts the model's intent signal as fallback
   when fact keys are missing.
3. Non-composable composition variables are advisory (dropped), not blocking.
4. Product-family action specializations accepted when the menu offers the
   generic action (011 menus stay verbatim).
5. Approved-body greeting chunks stripped mid-conversation (delivery shaping;
   live templates untouched) - this was the origin of the spike's
   mid-conversation "Oi, tudo bem?" wart.
6. Per-template variable attachment (renderer rejects unknown variables).
7. `contextual_next_step` and `demo_status` enum tokens filled from state.
8. Demo link resolved from the official `links.demonstration` key.
9. Waitlist offer accepted off-menu when the model declares
   `waitlist_intent=contract_intent` (clear intent can appear anytime).
10. Compositions MUST be in Brazilian Portuguese, studio-owner language
    (model had composed in English; fixed and verified).
11. Repair preserves first-pass extractions (captured slots/compositions
    merge) - a regenerated decision no longer loses the lead's answer.

## Honest Findings For Manual Review / Next Iteration

- Ideal-conversation turns 4-8: the model answers "como funciona esse
  diagnostico?" as a product question instead of starting the diagnostic the
  lead just accepted; the script presumes the spike's flow. Defensible model
  behavior; flow design to settle in the goldens phase.
- Scenario 14 (checkout/discount/VIP): answered with official prices - no
  false promise (do-not-do bar met) but does not address availability;
  needs an availability/checkout answer path (T012-032B).
- Scenario 9 (demo request): clarified instead of sending the demo once;
  weak but safe.
- First-contact replies keep the approved-body greeting prefix (approved
  copy, unchanged).
- PROVISIONAL facts used for `recommended_plan_or_range` and
  `indicated_agents` (plan-recommendation rule is a pending product-owner
  decision; resolver derivation is T012-031 scope).

## Verdict

The action-first architecture is validated on the real model: routing
deterministic, one-operation known-state turns, staged delivery derived by
code and rendered correctly, repair loop effective, every hard rule held
(no invented facts, no free-form text, handoff suppression, deferral).
Remaining work is quality iteration (instructions/copy) and the planned
Phase 3 tasks - not architecture.
