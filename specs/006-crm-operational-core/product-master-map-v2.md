# Product Master Map V2 - Decision-Oriented

> Status: exploratory decision table. This is generated from `product-master-map.csv`, `manager-use-case-catalog.md`, and `complete-manager-use-case-audit.md`.

## Counts

| Group | Count |
| --- | ---: |
| MUC rows | 132 |
| AUD candidate rows | 25 |
| Total rows | 157 |

## Column Notes

- `Priority`, `Decision`, `RouteType`, `Risk`, `MobileDepth`, and `WhatsApp` are review fields, not final decisions.
- `AgentFlowIds` comes from the current manager catalog/audit layer and may contain agent family references rather than only canonical flow IDs.
- Use this table to decide what becomes page, drawer, button, mobile action, automation or out of scope.

## Table

| ID | Area | Name | Priority | Decision | RouteType | Risk | MobileDepth | WhatsApp | PrimaryObject | RelatedObjects | Surface | UIPattern | Modes | AgentFlowIds | Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| MUC-001 | Setup | Claim paid workspace | P0/P1-review | candidate-review | page/form | low | web-only | none | Tenant |  | web | page/form | M | CRM core | candidate |
| MUC-002 | Setup | Complete studio profile | P0/P1-review | candidate-review | page/form | low | web-only | none | StudioProfile |  | web | page/form | M/C | CRM core | candidate |
| MUC-003 | Setup | Finish setup checklist | P0/P1-review | candidate-review | page/list | low | web-only | none | SetupChecklist |  | web | checklist/assistant | M/C/A | Gestao/F6 | candidate |
| MUC-004 | Setup | Import initial data | P0/P1-review | candidate-review | page/form | low | web-only | none | ImportJob |  | web | page/form | M/C/A | Gestao/F12 | candidate |
| MUC-005 | Setup | Resolve import duplicates | P0/P1-review | candidate-review | page/list | low | web-only | none | Contact | Student | web | review table | M/C | Atendimento/A7, Gestao/F12 | candidate |
| MUC-006 | Setup | Invite team members | P0/P1-review | candidate-review | page/form | low | web-only | none | Membership |  | web | page/form | M | CRM core | candidate |
| MUC-007 | Setup | Configure roles and permissions | P0/P1-review | candidate-review | config | high | web-only | none | Membership | Permission | web | config page | M/C | Gestao/F9, Historico/G11 | candidate |
| MUC-008 | Setup | Configure WhatsApp and channels | P0/P1-review | candidate-review | config | medium | web-only | none | ChannelConnection |  | web | config page | M/C/A | Atendimento + integrations | candidate |
| MUC-009 | Setup | Configure templates and answers | P0/P1-review | candidate-review | config | low | web-only | none | Template | FAQ | web | config page | M/C | Atendimento/A2 | candidate |
| MUC-010 | Setup | Configure agenda rules | P0/P1-review | candidate-review | config | high | web-only | none | AgendaPolicy |  | web | config page | M/C | Agenda | candidate |
| MUC-011 | Setup | Configure finance rules and plans | P0/P1-review | candidate-review | config | medium | web-only | none | StudioPlan |  | web | config page | M/C | Financeiro | candidate |
| MUC-012 | Setup | Configure privacy and opt-out | P0/P1-review | candidate-review | config | high | web-only | none | PrivacyPolicy |  | web | config page | M/C | Atendimento/A6/A8 | candidate |
| MUC-013 | Setup | Configure operational policies | P0/P1-review | candidate-review | page | high | web-only | none | PolicyVersion |  | web | policy page | M/C | Gestao/F15 | candidate |
| MUC-014 | Daily | Open daily priorities | P0/P1-review | candidate-review | page/report | low | mobile-action | none | TodayDashboard |  | web/mobile | dashboard/assistant | M/C/A | Gestao/F1 | candidate |
| MUC-015 | Daily | Review money on the table | P0/P1-review | candidate-review | page/report | low | mobile-review | none | OpportunityMetric |  | web | dashboard | M/C/A | Gestao/F2 | candidate |
| MUC-016 | Daily | Review human queue | P0/P1-review | candidate-review | page/list | low | mobile-partial | none | OperationCase |  | web/mobile | queue | M/C/A | Gestao/F3 | candidate |
| MUC-017 | Daily | Review tasks by owner/SLA | P0/P1-review | candidate-review | page/list | low | mobile-partial | none | Task |  | web/mobile | list | M/C/A | CRM operation | candidate |
| MUC-018 | Daily | Delegate task or case | P0/P1-review | candidate-review | drawer/button | low | mobile-action | none | Task | Case | web/mobile | action | M/C | CRM operation | candidate |
| MUC-019 | Daily | Close resolved cases | P0/P1-review | candidate-review | drawer/button | low | mobile-action | none | OperationCase |  | web/mobile | action/drawer | M/C | CRM operation | candidate |
| MUC-020 | Daily | Review notifications and alerts | P0/P1-review | candidate-review | review | low | mobile-partial | none | Notification |  | web/mobile | notification center | M/C/A | CRM operation | candidate |
| MUC-021 | Daily | Review bottlenecks | P0/P1-review | candidate-review | page/report | low | mobile-review | none | Bottleneck |  | web | report/assistant | M/C/A | Gestao/F4 | candidate |
| MUC-022 | Daily | Review weekly summary | P0/P1-review | candidate-review | page/report | low | mobile-partial | none | WeeklyReport |  | web/mobile | report | M/C/A | Gestao/F5 | candidate |
| MUC-023 | Daily | Check data/setup blockers | P0/P1-review | candidate-review | page/list | high | mobile-review | none | DataQualityIssue |  | web | data-quality list | M/C/A | Gestao/F6 | candidate |
| MUC-024 | Inbox | New WhatsApp conversation | P0/P1-review | candidate-review | background/action | medium | mobile-action | hybrid | Conversation |  | web/mobile/whatsapp | inbox + auto | M/C/A | Atendimento/A1 | candidate |
| MUC-025 | Inbox | Existing student request | P0/P1-review | candidate-review | drawer/button | low | mobile-action | hybrid | Conversation | Student | web/mobile/whatsapp | inbox action | M/C/A | Atendimento/A3 | candidate |
| MUC-026 | Inbox | FAQ or missing answer | P0/P1-review | candidate-review | drawer/button | low | mobile-action | hybrid | Conversation | FAQ | web/mobile/whatsapp | inbox action | M/C/A | Atendimento/A2 | candidate |
| MUC-027 | Inbox | Human takeover and response | P0/P1-review | candidate-review | drawer/button | low | mobile-action | hybrid | Conversation | Case | web/mobile/whatsapp | action/drawer | M/C | Atendimento/A5 | candidate |
| MUC-028 | Inbox | Register opt-out/preference | P0/P1-review | candidate-review | background/action | low | mobile-partial | hybrid | Contact |  | web/mobile/whatsapp | form/auto | M/C/A | Atendimento/A6 | candidate |
| MUC-029 | Inbox | Group/shared-phone/family | P0/P1-review | candidate-review | drawer/button | low | mobile-action | hybrid | Conversation | Responsible | web/mobile/whatsapp | inbox action | M/C/A | Atendimento/A9 | candidate |
| MUC-030 | Inbox | Update contact data safely | P0/P1-review | candidate-review | drawer/button | low | mobile-action | none | Contact |  | web/mobile | form/action | M/C | Atendimento/A8 | candidate |
| MUC-031 | Inbox | Validate responsible permission | P0/P1-review | candidate-review | drawer/button | high | mobile-action | none | ResponsibleParty |  | web/mobile | form/action | M/C | Atendimento/A9, Historico/G11 | candidate |
| MUC-032 | Inbox | Classify media/proof/document/audio | P0/P1-review | candidate-review | drawer/button | low | mobile-action | hybrid | Message | Document | web/mobile/whatsapp | inbox action | M/C/A | Atendimento/A7 | candidate |
| MUC-033 | Inbox | Resolve contact/student duplicate | P0/P1-review | candidate-review | page/list | low | mobile-review | none | Contact | Student | web | review table | M/C | Atendimento/A7 | candidate |
| MUC-034 | Inbox | Handle privacy/data request | P0/P1-review | candidate-review | case-workspace | high | mobile-review | none | PrivacyRequest |  | web | case | M/C | Atendimento/A8 | candidate |
| MUC-035 | Inbox | Reopen stale conversation/SLA | P0/P1-review | candidate-review | drawer/button | low | mobile-action | possible | Conversation | Task | web/mobile | alert/action | M/C/A | Atendimento/A10 | candidate |
| MUC-036 | Sales | Capture multichannel lead | P0/P1-review | candidate-review | page | low | mobile-review | none | InterestedPerson |  | web | capture page | M/C/A | Vendas/C15 | candidate |
| MUC-037 | Sales | Register walk-in/manual lead | P0/P1-review | candidate-review | page/form | low | mobile-partial | none | InterestedPerson |  | web/mobile | form | M/C | Vendas/C15 | candidate |
| MUC-038 | Sales | Review lead sources | P0/P1-review | candidate-review | page/report | low | mobile-review | none | SourceMetric |  | web | report | M/C/A | Vendas/C8/C15 | candidate |
| MUC-039 | Sales | Qualify interested person | P0/P1-review | candidate-review | drawer/button | low | mobile-action | none | InterestedPerson |  | web/mobile | detail action | M/C/A | Vendas/C8 | candidate |
| MUC-040 | Sales | Price/plan question | P0/P1-review | candidate-review | drawer/button | low | mobile-action | hybrid | Conversation | Plan | web/mobile/whatsapp | inbox action | M/C/A | Vendas/C1 | candidate |
| MUC-041 | Sales | Schedule trial class | P0/P1-review | candidate-review | review | low | mobile-partial | hybrid | Trial | ClassSession | web/mobile/whatsapp | scheduler | M/C/A | Vendas/C2, Agenda/B7 | candidate |
| MUC-042 | Sales | Send trial reminder | P0/P1-review | candidate-review | drawer/button | low | mobile-action | hybrid | Trial |  | web/mobile/whatsapp | auto/action | M/C/A | Vendas/C3 | candidate |
| MUC-043 | Sales | Trial no-show/reschedule | P0/P1-review | candidate-review | drawer/button | low | mobile-action | hybrid | Trial |  | web/mobile/whatsapp | action | M/C/A | Agenda/B12 | candidate |
| MUC-044 | Sales | Follow up after trial | P0/P1-review | candidate-review | drawer/button | low | mobile-action | hybrid | InterestedPerson |  | web/mobile/whatsapp | action | M/C/A | Vendas/C4 | candidate |
| MUC-045 | Sales | Commercial follow-up cadence | P0/P1-review | candidate-review | background/action | medium | mobile-review | hybrid | InterestedPerson |  | web/whatsapp | auto/bulk | M/C/A | Vendas/C5 | candidate |
| MUC-046 | Sales | Objection handling | P0/P1-review | candidate-review | drawer/button | low | mobile-action | hybrid | Conversation |  | web/mobile/whatsapp | approval/action | M/C/A | Vendas/C7 | candidate |
| MUC-047 | Sales | Create pre-enrollment | P0/P1-review | candidate-review | page/form | low | mobile-review | none | PreEnrollment |  | web | page/form | M/C | Vendas/C6 | candidate |
| MUC-048 | Sales | Checkout abandonment | P0/P1-review | candidate-review | drawer/button | low | mobile-review | hybrid | Checkout |  | web/whatsapp | auto/action | M/C/A | Vendas/C11 | candidate |
| MUC-049 | Sales | Referral and benefit review | P0/P1-review | candidate-review | page/form | low | mobile-review | none | Referral |  | web | page/form | M/C | Vendas/C10 | candidate |
| MUC-050 | Sales | Demand with no available slot | P0/P1-review | candidate-review | drawer/button | low | mobile-action | none | InterestedPerson | Waitlist | web/mobile | action | M/C/A | Vendas/C12 | candidate |
| MUC-051 | Sales | Convert lead to student | P0/P1-review | candidate-review | drawer/button | low | mobile-review | none | InterestedPerson | Student | web | conversion action | M/C | Vendas/C13 | candidate |
| MUC-052 | Agenda | Create/adjust weekly grade | P0/P1-review | candidate-review | page/form | low | mobile-review | none | ClassGroup |  | web | page/form | M/C | Agenda/B11 | candidate |
| MUC-053 | Agenda | Create class group | P0/P1-review | candidate-review | page/form | low | mobile-review | none | ClassGroup |  | web | page/form | M/C | Agenda/B11 | candidate |
| MUC-054 | Agenda | Review calendar/day schedule | P0/P1-review | candidate-review | page/list | low | mobile-action | none | ClassSession |  | web/mobile | calendar | M/C/A | Agenda | candidate |
| MUC-055 | Agenda | Open class session | P0/P1-review | candidate-review | page | low | mobile-action | none | ClassSession |  | web/mobile | detail page | M | Agenda | candidate |
| MUC-056 | Agenda | Take attendance | P0/P1-review | candidate-review | page/list | low | mobile-action | none | AttendanceRecord |  | web/mobile | checklist | M/C/A | Agenda/B3/B14 | candidate |
| MUC-057 | Agenda | Confirm presence | P0/P1-review | candidate-review | drawer/button | low | mobile-action | hybrid | ClassSession | Message | web/mobile/whatsapp | auto/action | M/C/A | Agenda/B1 | candidate |
| MUC-058 | Agenda | Absence with notice | P0/P1-review | candidate-review | drawer/button | low | mobile-action | hybrid | AttendanceRecord |  | web/mobile/whatsapp | action | M/C/A | Agenda/B2 | candidate |
| MUC-059 | Agenda | No-show | P0/P1-review | candidate-review | drawer/button | low | mobile-action | none | AttendanceRecord |  | web/mobile | auto/action | M/C/A | Agenda/B3 | candidate |
| MUC-060 | Agenda | Make-up request | P0/P1-review | candidate-review | drawer/button | low | mobile-action | hybrid | MakeUpCredit |  | web/mobile/whatsapp | action/drawer | M/C/A | Agenda/B5 | candidate |
| MUC-061 | Agenda | Make-up credit ledger | P0/P1-review | candidate-review | page/report | low | mobile-partial | none | MakeUpCredit |  | web/mobile | ledger | M/C/A | Agenda/B13 | candidate |
| MUC-062 | Agenda | Recover open slot | P0/P1-review | candidate-review | drawer/button | low | mobile-partial | hybrid | ClassSession | Waitlist | web/mobile/whatsapp | smart button | M/C/A | Agenda/B4 | candidate |
| MUC-063 | Agenda | Manage waitlist | P0/P1-review | candidate-review | page/list | low | mobile-action | none | WaitlistEntry |  | web/mobile | list/action | M/C/A | Agenda/B6 | candidate |
| MUC-064 | Agenda | Change fixed schedule | P0/P1-review | candidate-review | drawer/button | low | mobile-action | none | Student | ClassGroup | web/mobile | action/drawer | M/C | Agenda/B8 | candidate |
| MUC-065 | Agenda | Cancel/alter class by studio | P0/P1-review | candidate-review | drawer/button | medium | mobile-action | hybrid | ClassSession |  | web/mobile/whatsapp | approval/action | M/C | Agenda/B9 | candidate |
| MUC-066 | Agenda | Capacity/overbooking conflict | P0/P1-review | candidate-review | drawer/button | low | mobile-review | none | ClassGroup |  | web | alert/action | M/C/A | Agenda/B10 | candidate |
| MUC-067 | Agenda | First class checklist | P0/P1-review | candidate-review | page/list | low | mobile-action | none | Student | ClassSession | web/mobile | checklist | M/C/A | Agenda/B15 | candidate |
| MUC-068 | Agenda | Workshop/special class | P0/P1-review | candidate-review | review | medium | mobile-review | none | Event |  | web | page/bulk | M/C/A | Agenda/B16 | candidate |
| MUC-069 | Finance | Create/update student plan | P0/P1-review | candidate-review | page/form | medium | mobile-review | none | StudentPlan |  | web | page/form | M | Financeiro | candidate |
| MUC-070 | Finance | Review finance overview | P0/P1-review | candidate-review | page/report | medium | mobile-action | none | Payment |  | web/mobile | dashboard | M/C/A | Financeiro | candidate |
| MUC-071 | Finance | Send due reminder | P0/P1-review | candidate-review | drawer/button | medium | mobile-action | hybrid | Payment | Message | web/mobile/whatsapp | auto/action | M/C/A | Financeiro/D1 | candidate |
| MUC-072 | Finance | Overdue payment | P0/P1-review | candidate-review | drawer/button | medium | mobile-action | hybrid | Payment | Case | web/mobile/whatsapp | action | M/C/A | Financeiro/D2 | candidate |
| MUC-073 | Finance | Send Pix/payment link | P0/P1-review | candidate-review | drawer/button | medium | mobile-partial | hybrid | Payment | Charge | web/mobile/whatsapp | smart button | M/C/A | Financeiro/D3 | candidate |
| MUC-074 | Finance | Confirm payment | P0/P1-review | candidate-review | background/action | medium | mobile-review | none | Payment |  | web/webhook | form/auto | M/A | Financeiro/D4 | candidate |
| MUC-075 | Finance | Reconcile unmatched payment | P0/P1-review | candidate-review | page/list | medium | mobile-review | none | Payment |  | web | review table | M/C | Financeiro/D10 | candidate |
| MUC-076 | Finance | Failed payment | P0/P1-review | candidate-review | drawer/button | medium | mobile-review | hybrid | Payment |  | web/whatsapp | auto/action | M/C/A | Financeiro/D7 | candidate |
| MUC-077 | Finance | Receipt/invoice document | P0/P1-review | candidate-review | drawer/button | medium | mobile-action | hybrid | DocumentRecord |  | web/mobile/whatsapp | action | M/C/A | Financeiro/D8 | candidate |
| MUC-078 | Finance | Contract/terms | P0/P1-review | candidate-review | drawer/button | medium | mobile-review | hybrid | Contract |  | web/whatsapp | action | M/C/A | Financeiro/D11 | candidate |
| MUC-079 | Finance | Financial exception | P0/P1-review | candidate-review | case-workspace | high | mobile-action | none | OperationCase |  | web/mobile | case | M/C | Financeiro/D6 | candidate |
| MUC-080 | Finance | Pause/freeze plan | P0/P1-review | candidate-review | drawer/button | medium | mobile-action | none | StudentPlan |  | web/mobile | case/action | M/C | Financeiro/D9/D15 | candidate |
| MUC-081 | Finance | Block/release access | P0/P1-review | candidate-review | case-workspace | high | mobile-review | none | StudentPlan |  | web | case/approval | M/C | Financeiro/D12 | candidate |
| MUC-082 | Finance | Credit/courtesy | P0/P1-review | candidate-review | case-workspace | medium | mobile-review | none | Benefit |  | web | case/form | M | Financeiro/D13 | candidate |
| MUC-083 | Finance | Effective plan change/ending | P0/P1-review | candidate-review | drawer/button | medium | mobile-review | none | StudentPlan |  | web | case/action | M/C | Financeiro/D15 | candidate |
| MUC-084 | Finance | Monthly financial close | P0/P1-review | candidate-review | page/report | medium | mobile-review | none | FinanceReport |  | web | report | M/C/A | Financeiro/D14 | candidate |
| MUC-085 | Retention | Review retention dashboard | P0/P1-review | candidate-review | page/report | low | mobile-action | none | RetentionRisk |  | web/mobile | dashboard | M/C/A | Retencao | candidate |
| MUC-086 | Retention | Frequency drop | P0/P1-review | candidate-review | drawer/button | low | mobile-action | hybrid | Student |  | web/mobile/whatsapp | alert/action | M/C/A | Retencao/E1 | candidate |
| MUC-087 | Retention | Inactive student | P0/P1-review | candidate-review | drawer/button | low | mobile-action | hybrid | Student |  | web/mobile/whatsapp | alert/action | M/C/A | Retencao/E2 | candidate |
| MUC-088 | Retention | Student return | P0/P1-review | candidate-review | drawer/button | low | mobile-action | hybrid | Student |  | web/mobile/whatsapp | action | M/C/A | Retencao/E3 | candidate |
| MUC-089 | Retention | Cancellation risk | P0/P1-review | candidate-review | case-workspace | medium | mobile-action | none | OperationCase |  | web/mobile | case | M/C | Retencao/E4 | candidate |
| MUC-090 | Retention | Post-cancellation | P0/P1-review | candidate-review | drawer/button | medium | mobile-action | hybrid | Student |  | web/mobile/whatsapp | case/action | M/C/A | Retencao/E9 | candidate |
| MUC-091 | Retention | Ex-student reactivation | P0/P1-review | candidate-review | review | medium | mobile-review | hybrid | Segment |  | web/whatsapp | bulk/approval | M/C | Retencao/E5 | candidate |
| MUC-092 | Retention | Satisfaction check | P0/P1-review | candidate-review | drawer/button | low | mobile-action | hybrid | Feedback |  | web/mobile/whatsapp | auto/action | M/C/A | Retencao/E6 | candidate |
| MUC-093 | Retention | Open complaint case | P0/P1-review | candidate-review | case-workspace | high | mobile-action | hybrid | ComplaintCase |  | web/mobile/whatsapp | case | M/C/A | Retencao/E13 | candidate |
| MUC-094 | Retention | Resolve complaint/recover trust | P0/P1-review | candidate-review | drawer/button | high | mobile-action | hybrid | ComplaintCase |  | web/mobile/whatsapp | case/action | M/C | Retencao/E13 | candidate |
| MUC-095 | Retention | Return after pause | P0/P1-review | candidate-review | drawer/button | low | mobile-action | hybrid | Student |  | web/mobile/whatsapp | auto/action | M/C/A | Retencao/E7 | candidate |
| MUC-096 | Retention | Risk segmentation | P0/P1-review | candidate-review | page/report | low | mobile-review | none | Segment |  | web | report/action | M/C/A | Retencao/E8/E12 | candidate |
| MUC-097 | Retention | Sensitive health/personal event | P0/P1-review | candidate-review | case-workspace | high | mobile-action | none | OperationCase |  | web/mobile | case | M/C | Retencao/E11, Historico/G3 | candidate |
| MUC-098 | History | Teacher opens class context | P1-review | candidate-review | review | high | mobile-action | none | StudentHistory |  | web/mobile | assistant/detail | M/C/A | Historico/G1 | candidate |
| MUC-099 | History | Add post-class observation | P1-review | candidate-review | drawer/button | high | mobile-action | none | StudentHistoryEvent |  | web/mobile | form/action | M/C | Historico/G2 | candidate |
| MUC-100 | History | Register restriction/care | P1-review | candidate-review | case-workspace | high | mobile-action | none | StudentHistoryEvent |  | web/mobile | form/case | M/C | Historico/G3 | candidate |
| MUC-101 | History | Review objective/evolution | P1-review | candidate-review | page/report | high | mobile-action | none | StudentHistory |  | web/mobile | timeline | M/C/A | Historico/G4 | candidate |
| MUC-102 | History | Store document/anamnesis | P1-review | candidate-review | drawer/button | high | mobile-action | none | DocumentRecord |  | web/mobile | form/action | M/C/A | Historico/G6 | candidate |
| MUC-103 | History | Correct history event | P1-review | candidate-review | case-workspace | high | mobile-review | none | StudentHistoryEvent |  | web | form/case | M/C | Historico/G7 | candidate |
| MUC-104 | History | Handoff between teachers | P1-review | candidate-review | drawer/button | high | mobile-action | none | Task | StudentHistory | web/mobile | action | M/C/A | Historico/G8 | candidate |
| MUC-105 | History | Remind teacher note | P1-review | candidate-review | background/action | high | mobile-partial | none | Task |  | web/mobile | auto/task | M/C/A | Historico/G9 | candidate |
| MUC-106 | History | Share safe context with student | P1-review | candidate-review | drawer/button | high | mobile-action | hybrid | StudentHistory |  | web/mobile/whatsapp | approval/action | M/C | Historico/G10 | candidate |
| MUC-107 | History | History visibility permissions | P1-review | candidate-review | config | high | web-only | none | Permission |  | web | config page | M/C/A | Historico/G11 | candidate |
| MUC-108 | History | Unified student timeline | P1-review | candidate-review | page/report | high | mobile-action | none | StudentHistory |  | web/mobile | timeline/assistant | M/C/A | Historico/G12 | candidate |
| MUC-109 | Agents | Configure included agents | P0/P1-review | candidate-review | config | low | web-only | none | AgentConfiguration |  | web | config page | M/C | Agent runtime | candidate |
| MUC-110 | Agents | Configure an agent | P0/P1-review | candidate-review | config | low | web-only | none | AgentConfiguration |  | web | config page | M/C | Agent runtime | candidate |
| MUC-111 | Agents | Configure a flow | P0/P1-review | candidate-review | config | low | web-only | none | FlowConfiguration |  | web | config page | M/C | Agent runtime | candidate |
| MUC-112 | Agents | Simulate flow | P0/P1-review | candidate-review | simulation | low | web-only | none | FlowConfiguration |  | web | simulation | M/C | Gestao/F13 | candidate |
| MUC-113 | Agents | Activate/pause flow | P0/P1-review | candidate-review | drawer/button | low | web-only | none | FlowConfiguration |  | web | action | M/C | Agent runtime | candidate |
| MUC-114 | Agents | Review flow execution | P0/P1-review | candidate-review | review | low | web-only | none | FlowRun |  | web | run panel | M/C/A | Agent observability | candidate |
| MUC-115 | Agents | Approve/reject copilot action | P0/P1-review | candidate-review | drawer/button | low | mobile-action | none | Approval |  | web/mobile | approval drawer | M | Operation layer | candidate |
| MUC-116 | Agents | Review agent performance | P0/P1-review | candidate-review | page/report | low | web-only | none | AgentReport |  | web | report | M/C/A | Gestao/F8 | candidate |
| MUC-117 | Agents | Investigate automation incident | P0/P1-review | candidate-review | drawer/button | high | web-only | none | IncidentCase |  | web | case/action | M/C/A | Gestao/F14 | candidate |
| MUC-118 | Agents | Change operational rule/policy | P0/P1-review | candidate-review | drawer/button | high | web-only | none | PolicyVersion |  | web | policy/action | M/C | Gestao/F15 | candidate |
| MUC-119 | Agents | Resolve flow blocked by data | P0/P1-review | candidate-review | drawer/button | high | web-only | none | DataQualityIssue |  | web | action | M/C/A | Gestao/F6 | candidate |
| MUC-120 | Agents | Review quota/usage | P0/P1-review | candidate-review | page/report | medium | mobile-action | none | UsageLedger |  | web/mobile | dashboard | M/C/A | Gestao/F7 | candidate |
| MUC-121 | Agents | Configure economy rules | P0/P1-review | candidate-review | config | low | web-only | none | EconomyRule |  | web | config page | M/C/A | Gestao/F7 | candidate |
| MUC-122 | Agents | Buy/request quota pack | P0/P1-review | candidate-review | drawer/button | medium | web-only | none | QuotaPack |  | web | billing action | M | Billing/usage | candidate |
| MUC-123 | Admin | Manage Taliya subscription | P1/P2-review | candidate-review | page | low | web-only | none | Subscription |  | web | billing page | M/A | Billing | candidate |
| MUC-124 | Admin | View Taliya invoices | P1/P2-review | candidate-review | page | low | web-only | none | Invoice |  | web | billing page | M | Billing | candidate |
| MUC-125 | Admin | Review integrations | P1/P2-review | candidate-review | page | medium | web-only | none | Integration |  | web | integrations page | M/C/A | System | candidate |
| MUC-126 | Admin | Investigate integration logs | P1/P2-review | candidate-review | drawer/button | medium | web-only | none | IntegrationLog |  | web | logs/action | M/C/A | Gestao/F11 | candidate |
| MUC-127 | Admin | Review audit event | P1/P2-review | candidate-review | review | low | web-only | none | AuditEvent |  | web | audit detail | M/C | Security/governance | candidate |
| MUC-128 | Admin | Reports hub/export review | P1/P2-review | candidate-review | page/report | low | web-only | none | Report |  | web | reports hub | M/C/A | Reports | candidate |
| MUC-129 | Admin | Financial report | P1/P2-review | candidate-review | page/report | medium | web-only | none | Report |  | web | report | M/C/A | Financeiro | candidate |
| MUC-130 | Admin | Sales report | P1/P2-review | candidate-review | page/report | low | web-only | none | Report |  | web | report | M/C/A | Vendas | candidate |
| MUC-131 | Admin | Capacity/occupancy report | P1/P2-review | candidate-review | page/report | low | web-only | none | Report |  | web | report | M/C/A | Agenda/Gestao | candidate |
| MUC-132 | Admin | Source ROI/quality | P1/P2-review | candidate-review | page/report | low | web-only | none | Report |  | web | report | M/C/A | Vendas/C8/C15 | candidate |
| AUD-001 | AuditGap | Holidays/recess/closures | P0-candidate | candidate-review | config | high | web-only | none | ClosureCalendar |  | web | config/policy | M/C | CRM + Gestao/F15 | candidate |
| AUD-002 | AuditGap | Rooms/equipment/resources | P1-candidate | candidate-review | config | low | web-only | none | Resource |  | web | config page | M | CRM + Agenda | candidate |
| AUD-003 | AuditGap | Teacher availability rules | P2-candidate | candidate-review | config | low | web-only | none | TeacherAvailability |  | web | config page | M | CRM + Agenda | candidate |
| AUD-004 | AuditGap | Tags/segments/fields | P1-candidate | candidate-review | config | low | web-only | none | CustomField |  | web | config page | M/C | CRM core | candidate |
| AUD-005 | AuditGap | Role notification preferences | P1-candidate | candidate-review | config | low | web-only | none | NotificationPreference |  | web | config page | M/A | CRM core | candidate |
| AUD-006 | AuditGap | Daily opening/closing checklist | P1-candidate | candidate-review | page/list | low | mobile-action | none | ChecklistRun |  | web/mobile | checklist | M/C/A | Gestao | candidate |
| AUD-007 | AuditGap | Teacher availability issue | P2-candidate | candidate-review | drawer/button | low | mobile-review | none | OperationCase |  | web | case/action | M/C | Agenda/Gestao | candidate |
| AUD-008 | AuditGap | Room/equipment outage impact | P1-candidate | candidate-review | drawer/button | low | mobile-review | none | Resource | Case | web | case/action | M/C/A | Agenda/Gestao | candidate |
| AUD-009 | AuditGap | Holiday/recess class impact | P1-candidate | candidate-review | drawer/button | high | web-only | none | PolicyVersion | ClassSession | web | simulation/action | M/C | Agenda/Gestao | candidate |
| AUD-010 | AuditGap | Class/student broadcast | P1-candidate | candidate-review | review | medium | mobile-review | hybrid | Broadcast |  | web/whatsapp | bulk/approval | M/C | Atendimento/Gestao | candidate |
| AUD-011 | AuditGap | Partial payment/payment promise | P0-candidate | candidate-review | case-workspace | medium | mobile-action | none | PaymentAgreement |  | web/mobile | form/case | M/C/A | Financeiro | candidate |
| AUD-012 | AuditGap | Renegotiate overdue balance | P2-candidate | candidate-review | case-workspace | medium | mobile-review | none | PaymentAgreement |  | web | approval/case | M/C | Financeiro | candidate |
| AUD-013 | AuditGap | Refund/chargeback/dispute | P1-candidate | candidate-review | case-workspace | high | mobile-review | none | RefundDisputeCase |  | web | case | M/C | Financeiro | candidate |
| AUD-014 | AuditGap | Financial/accounting export | P2-candidate | candidate-review | review | medium | web-only | none | ExportJob |  | web | export | M/A | Financeiro | candidate |
| AUD-015 | AuditGap | Cashflow forecast | P2-candidate | candidate-review | page/report | medium | mobile-review | none | FinanceForecast |  | web | report | M/C/A | Financeiro/Gestao | candidate |
| AUD-016 | AuditGap | Milestone celebration | P2-candidate | candidate-review | drawer/button | low | mobile-action | hybrid | StudentMilestone |  | web/mobile/whatsapp | auto/action | M/C/A | Retencao/E10 | candidate |
| AUD-017 | AuditGap | First-week new student journey | P1-candidate | candidate-review | page/list | low | mobile-action | none | Student |  | web/mobile | checklist/auto | M/C/A | Retencao/E14 candidate | candidate |
| AUD-018 | AuditGap | Anamnesis/consent/emergency gate | P1-candidate | candidate-review | drawer/button | high | mobile-action | none | IntakeGate |  | web/mobile | data-quality/action | M/C/A | Historico/G13 candidate | candidate |
| AUD-019 | AuditGap | Periodic student review | P2-candidate | candidate-review | background/action | low | mobile-partial | none | StudentReview |  | web/mobile | task/auto | M/C/A | Historico | candidate |
| AUD-020 | AuditGap | Escalate sensitive complaint | P0-candidate | candidate-review | drawer/button | high | mobile-action | none | ComplaintCase |  | web/mobile | case/action | M/C/A | Retencao/E13 | candidate |
| AUD-021 | AuditGap | Full CRM export/backup | P2-candidate | candidate-review | review | low | web-only | none | ExportJob |  | web | export | M/A | Admin | candidate |
| AUD-022 | AuditGap | LGPD export/delete/anonymize | P1-candidate | candidate-review | case-workspace | high | mobile-review | none | PrivacyRequest |  | web | privacy case | M/C | Atendimento/A8 + Security | candidate |
| AUD-023 | AuditGap | Taliya support access approval | P1-candidate | candidate-review | review | high | mobile-review | none | SupportAccessGrant |  | web | approval | M/C/A | Security/Gestao | candidate |
| AUD-024 | AuditGap | Archive/reactivate record | P0-candidate | candidate-review | drawer/button | low | mobile-action | none | RecordArchiveState |  | web/mobile | action | M | CRM core | candidate |
| AUD-025 | AuditGap | Segment and bulk eligibility | P1-candidate | candidate-review | review | medium | mobile-review | none | SegmentDefinition |  | web | segment/bulk | M/C/A | Vendas/Retencao/Gestao | candidate |
