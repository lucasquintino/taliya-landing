# Coverage Heatmap - Taliya Product Mapping

> Status: exploratory. This heatmap shows coverage quality by area and dimension.

## Legend

| Mark | Meaning |
| --- | --- |
| Green | Mapped well enough for product discussion. |
| Yellow | Partially mapped; needs detail. |
| Red | Missing or risky gap. |
| Gray | Not needed or intentionally limited. |

## Current Coverage

| Area | Use Cases | Routes | Manual | Copilot | Auto | Web | Mobile | WhatsApp | Data | Gates | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Setup/Governance | Green | Green | Green | Yellow | Gray | Green | Gray | Gray | Yellow | Yellow | Needs final RBAC and support-access detail. |
| Daily Command | Green | Green | Green | Green | Green | Green | Yellow | Gray | Yellow | Yellow | Needs screen composition. |
| Inbox/Contacts | Green | Green | Green | Green | Green | Green | Green | Green | Green | Yellow | LGPD execution route needs decision. |
| Sales | Green | Green | Green | Green | Green | Green | Yellow | Green | Green | Yellow | Campaign/segment depth still candidate. |
| Agenda | Green | Green | Green | Green | Green | Green | Green | Green | Green | Yellow | Resources/closures are candidate additions. |
| Finance | Green | Green | Green | Green | Yellow | Green | Yellow | Green | Yellow | Red | Financial exceptions/disputes need strict gates. |
| Retention | Green | Green | Green | Green | Yellow | Green | Green | Green | Green | Yellow | First-week journey and complaint escalation need detail. |
| History/Teacher | Green | Green | Green | Green | Yellow | Green | Green | Yellow | Green | Red | Sensitive visibility and intake gate need detail. |
| Agents/Runtime | Green | Green | Green | Green | Yellow | Green | Yellow | Yellow | Yellow | Red | Autonomy, quota and incident gates must be exact. |
| Reports/Admin | Green | Yellow | Green | Yellow | Yellow | Green | Gray | Gray | Yellow | Yellow | Exports/backups/support access are candidate. |

## Biggest Red/Yellow Risks

| Risk | Impact |
| --- | --- |
| Financial exceptions gates | Refunds, blocks, disputes and agreements cannot be loose. |
| Sensitive history permissions | Teachers/finance/reception must not see the wrong data. |
| Autonomy gates | Agents cannot bypass consent, quota, risk, data quality or approvals. |
| Policy versioning | Rule changes affect many future automations. |
| Mobile scope | App must support daily action without becoming full admin. |
| Data quality | Bad setup will make agents look broken. |

## Use This Heatmap For

- deciding where to detail next;
- deciding what requires evals/security review;
- deciding what must be web-only;
- spotting places where routes exist but behavior is not deep enough.
