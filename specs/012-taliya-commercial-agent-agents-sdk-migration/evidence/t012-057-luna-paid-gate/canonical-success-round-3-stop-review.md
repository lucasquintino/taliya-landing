# T012-057 attempted canonical success round 3 stop review

## Result

- Automated result: `9/9` passed.
- Human review: failed.
- Model operations: `33`.
- Reported cost: `$0.122368`.
- Evidence: `canonical-success-round-3/20260805T012022Z/report.md`.

## Human-review failure

`final-whatsapp-question` first rendered the complete approved WhatsApp answer
and demo link, then added the generic how-it-works explanation and another
diagnostic offer. The reply was redundant and unnecessarily long even though
all deterministic fixture checks passed.

The structured decision selected both `whatsapp_scope` and `how_it_works`.
The compiler rendered one template per fact key and had no subsumption rule for
overlapping facts. This is an answer-adequacy gap, not a raw-text routing error.

## No-cost correction scope

- tell the product agent to choose the smallest sufficient official fact set;
- make the specific WhatsApp template suppress the generic how-it-works
  template when both structured fact keys are present;
- make specific direct product templates suppress the generic overview when
  both are present;
- add an exact compiler regression before any further paid call.

This attempted round does not count toward the required three consecutive
human-approved canonical rounds. Paid execution remains stopped until the
correction passes the no-cost gates.
