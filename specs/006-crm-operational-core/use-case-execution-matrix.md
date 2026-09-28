# Draft Matrix - Use Case Execution Paths

> Status: exploratory draft. This matrix maps every currently known manager-followable use case by execution path: programmatic core, AI role, manual path, copilot path, autonomous path, gates and outputs.

## Scope

This matrix covers:

- 132 cataloged manager use cases from `manager-use-case-catalog.md`;
- 25 candidate gaps from `complete-manager-use-case-audit.md`;
- 157 total candidate manager use cases.

It is intentionally compact. Detailed implementation specs should be created only for accepted P0/P1 slices.

## Legend

### Trigger

| Code | Meaning |
| --- | --- |
| U | User starts from UI click/form/button. |
| I | Inbound message or contact action. |
| S | Scheduled job/time window. |
| E | System event/data state. |
| W | Webhook/integration event. |
| B | Bulk/list action. |

### Invocation

| Code | Meaning |
| --- | --- |
| Form | Normal CRM form/action. |
| Btn | Contextual smart button. |
| Auto | Automatic configured trigger. |
| Approval | Copilot approval item. |
| Assistant | Taliya side panel/command bar. |
| Bulk | Selected-list action. |

### AI Role

| Code | Meaning |
| --- | --- |
| None | No AI needed. |
| Draft | Draft message/action text. |
| Summ | Summarize context. |
| Classify | Classify intent/source/risk/status. |
| Explain | Explain recommendation, failure, usage or impact. |
| Recommend | Suggest next action/ranking/priority. |
| Interpret | Interpret ambiguous natural-language reply or media. |

### Gates

| Code | Meaning |
| --- | --- |
| Auth | Auth, tenant, role, entitlement. |
| Data | Required data present/quality. |
| Perm | Object-level permission. |
| Consent | Consent/opt-out/channel eligibility. |
| Quota | AI/WhatsApp/usage quota and economy mode. |
| Risk | Health, finance, privacy, reputation, legal or low confidence. |
| Window | Send window/timing. |
| Idem | Idempotency/retry safety. |
| Capacity | Schedule/resource capacity/conflicts. |
| Provider | External provider state/availability. |

### Outputs

| Code | Meaning |
| --- | --- |
| Rec | CRM record/state update. |
| Case | Operation case. |
| Task | Task. |
| Appr | Approval. |
| Msg | Message/send attempt. |
| Audit | Audit event. |
| Run | Flow run. |
| Usage | Quota/usage ledger. |
| Report | Report/metric. |
| Log | Integration/system log. |

## A. Setup, Access And Governance

| ID | Use Case | Trig | Invoke | Programmatic Core | AI Role | Manual Path | Copilot Path | Autonomous Path | Gates | Outputs |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| MUC-001 | Claim paid workspace | U/W | Form | validate activation, create tenant/user/membership | None | owner claims via OTP/magic link | n/a | n/a | Auth, Provider, Idem | Rec, Audit |
| MUC-002 | Complete studio profile | U | Form | save profile/hours/contact data | None | owner fills form | suggest missing fields | n/a | Auth, Data | Rec, Audit |
| MUC-003 | Finish setup checklist | U/E | Assistant | compute required setup status | Recommend | owner checks off items | suggest next setup order | auto-surface blockers | Auth, Data | Task, Report |
| MUC-004 | Import initial data | U/W | Form | upload/import/map/validate rows | Classify | owner maps and confirms import | suggest mappings/merges | detect import blockers | Auth, Data, Idem | Rec, Task, Log |
| MUC-005 | Resolve import duplicates | U/E | Btn | compare records, propose merge candidates | Recommend | user merges/skips | suggest safe merge | auto-flag only | Auth, Data, Risk | Rec, Task, Audit |
| MUC-006 | Invite team members | U | Form | create invitation/membership | None | owner invites user | n/a | n/a | Auth, Perm | Rec, Audit |
| MUC-007 | Configure roles/permissions | U | Form | update role/permission matrix | Explain | owner edits permissions | explain impact | n/a | Auth, Perm, Risk | Rec, Audit |
| MUC-008 | Configure WhatsApp/channels | U/W | Form | connect provider, store channel status | Explain | owner connects manually | guide setup/errors | monitor connection | Auth, Provider, Idem | Rec, Log, Audit |
| MUC-009 | Configure templates/answers | U | Form | store templates/FAQ/version | Draft | owner writes templates | draft answer/template | n/a | Auth, Perm, Risk | Rec, Audit |
| MUC-010 | Configure agenda rules | U | Form | store absence/makeup/capacity rules | Explain | owner edits rules | simulate impact | n/a | Auth, Data, Risk | Rec, Audit |
| MUC-011 | Configure finance rules/plans | U | Form | store student plans/finance policies | Explain | owner edits plans/rules | warn impact | n/a | Auth, Perm, Risk | Rec, Audit |
| MUC-012 | Configure privacy/opt-out behavior | U | Form | store consent/privacy rules | Explain | owner configures rules | explain compliance impact | n/a | Auth, Perm, Risk | Rec, Audit |
| MUC-013 | Configure operational policies | U | Btn | version policy/effective date | Explain | owner changes policy | simulate rollout | n/a | Auth, Perm, Risk | Rec, Appr, Audit |

## B. Daily Command Center

| ID | Use Case | Trig | Invoke | Programmatic Core | AI Role | Manual Path | Copilot Path | Autonomous Path | Gates | Outputs |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| MUC-014 | Open daily priorities | U/S | Assistant | aggregate tasks/cases/agenda/finance/risk | Recommend | manager reviews list | suggest order/actions | auto-generate daily summary | Auth, Data | Report, Task |
| MUC-015 | Review money on the table | U/S | Assistant | compute opportunities/losses | Explain | manager reviews metrics | suggest actions | auto-refresh metrics | Auth, Data | Report |
| MUC-016 | Review human queue | U/E | Form | list approvals/handoffs/exceptions | Summ | manager triages | suggest priority | auto-prioritize | Auth, Perm | Case, Appr, Task |
| MUC-017 | Review tasks by owner/SLA | U/E | Form | filter/sort task queue | Recommend | manager filters/delegates | suggest reassignment | auto-alert SLA risk | Auth, Perm | Task, Report |
| MUC-018 | Delegate task/case | U | Form | update assignment/due date | None | manager assigns | suggest owner | n/a | Auth, Perm | Task, Audit |
| MUC-019 | Close resolved cases | U | Btn | validate required resolution fields | Summ | user closes case | draft close summary | n/a | Auth, Perm, Data | Case, Audit |
| MUC-020 | Review notifications/alerts | U/E | Form | list alerts by severity | Summ | user opens/dismisses | suggest action | auto-generate alerts | Auth, Data | Task, Report |
| MUC-021 | Review bottlenecks | U/S | Assistant | detect repeated patterns | Explain | manager reviews | suggest fixes | auto-detect only | Auth, Data | Report, Task |
| MUC-022 | Review weekly summary | U/S | Assistant | aggregate week metrics | Summ | manager reads | suggest follow-ups | auto-create summary | Auth, Data | Report |
| MUC-023 | Check data/setup blockers | U/E | Form | detect missing/conflicting data | Recommend | user fixes data | suggest fix order | auto-create blocker tasks | Auth, Data | Task, Report |

## C. Inbox, Contacts And Privacy

| ID | Use Case | Trig | Invoke | Programmatic Core | AI Role | Manual Path | Copilot Path | Autonomous Path | Gates | Outputs |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| MUC-024 | New WhatsApp conversation | I | Auto/Btn | create/find contact/conversation | Classify | staff replies manually | draft reply/route | auto-classify/respond if safe | Auth, Consent, Quota, Risk, Idem | Rec, Msg, Run, Usage |
| MUC-025 | Existing student request | I/U | Auto/Btn | link student/context | Classify | staff handles | suggest route/action | execute allowed routine | Auth, Consent, Data, Risk | Case, Msg, Run |
| MUC-026 | FAQ or missing answer | I/U | Auto/Btn | lookup approved answer | Draft | staff answers | draft from base | answer approved FAQ | Auth, Consent, Quota, Risk | Msg, Task, Run |
| MUC-027 | Human takeover/response | I/U | Btn | pause AI, assign owner | Summ | human takes over | summarize + draft | n/a | Auth, Perm, Risk | Case, Task, Audit |
| MUC-028 | Opt-out/preference | I/U | Auto/Form | update consent/preference | Interpret | staff records | suggest category | detect opt-out phrases | Auth, Consent, Risk | Rec, Audit |
| MUC-029 | Group/shared-phone/family | I/U | Auto/Btn | check responsible permissions | Classify | staff validates | draft safe response | safe generic response only | Auth, Consent, Perm, Risk | Case, Msg, Audit |
| MUC-030 | Update contact data | U/I | Form/Btn | validate/update contact | Interpret | user edits | parse requested changes | n/a | Auth, Perm, Risk | Rec, Audit |
| MUC-031 | Validate responsible permission | U/I | Form/Btn | check ResponsibleParty permissions | Explain | staff validates manually | suggest allowed info | block unsafe exposure | Auth, Perm, Risk | Rec, Audit |
| MUC-032 | Classify media/proof/document/audio | I/W | Auto/Btn | store media, route by type | Interpret | staff reviews media | classify + suggest route | auto-classify low risk | Auth, Data, Risk, Provider | Rec, Case, Log |
| MUC-033 | Resolve duplicate | U/E | Btn | compare identifiers | Recommend | user merges/skips | suggest merge | auto-flag only | Auth, Data, Risk | Rec, Audit |
| MUC-034 | Privacy/data request | I/U | Case | create privacy case | Summ | staff handles securely | prepare response/checklist | n/a | Auth, Perm, Risk | Case, Task, Audit |
| MUC-035 | Reopen stale conversation/SLA | E/S | Auto/Btn | detect stale status/SLA | Recommend | staff reopens | suggest next message | auto-create SLA task | Auth, Data, Consent | Task, Case |

## D. Sales And Interested People

| ID | Use Case | Trig | Invoke | Programmatic Core | AI Role | Manual Path | Copilot Path | Autonomous Path | Gates | Outputs |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| MUC-036 | Capture multichannel lead | I/W/U | Auto/Form | create/dedupe lead/source | Classify | staff registers | classify + route | auto-create from source | Auth, Data, Idem | Rec, Task |
| MUC-037 | Register walk-in/manual lead | U | Form | create InterestedPerson/contact | None | staff enters | suggest next action | n/a | Auth, Data | Rec |
| MUC-038 | Review lead sources | U/S | Report | aggregate source attribution | Explain | manager reviews | explain quality | auto-update metrics | Auth, Data | Report |
| MUC-039 | Qualify interested person | U/I | Btn | update stage/fields | Classify | staff qualifies | suggest score/stage | auto-qualify simple leads | Auth, Data, Consent | Rec, Task |
| MUC-040 | Price/plan question | I/U | Auto/Btn | fetch policy/plans | Draft | staff replies | draft response | answer within policy | Auth, Consent, Quota, Risk | Msg, Run |
| MUC-041 | Schedule trial class | U/I | Btn | find slots/create reservation | Recommend | staff schedules | suggest slots/message | book if rules allow | Auth, Data, Capacity, Consent | Rec, Msg, Run |
| MUC-042 | Send trial reminder | S/U | Auto/Btn | find upcoming trials | Draft | staff sends | approve reminder | auto-send configured reminder | Consent, Quota, Window, Idem | Msg, Usage, Run |
| MUC-043 | Trial no-show/reschedule | E/I | Auto/Btn | detect no-show/update stage | Draft | staff handles | suggest reschedule/follow-up | auto-follow-up limited | Consent, Quota, Risk | Rec, Msg, Task |
| MUC-044 | Follow up after trial | S/E/U | Auto/Btn | detect completed trial/status | Draft | staff follows | draft CTA | auto-cadence if safe | Consent, Quota, Window | Msg, Task, Run |
| MUC-045 | Commercial follow-up cadence | S/E | Auto/Bulk | compute cadence/limits | Draft | staff creates tasks | approve sequence | auto-send within cadence | Consent, Quota, Window, Risk | Msg, Task, Usage |
| MUC-046 | Objection handling | I/U | Btn | classify objection/policy | Draft | staff replies | draft safe response | low-risk response only | Consent, Risk, Quota | Msg, Appr, Run |
| MUC-047 | Create pre-enrollment | U | Form/Btn | create pre-enrollment checklist | Recommend | staff creates | suggest missing steps | n/a | Auth, Data, Risk | Rec, Task |
| MUC-048 | Checkout abandonment | E/W/S | Auto/Btn | detect abandoned checkout | Draft | staff follows | prepare follow-up | auto-limited reminder | Consent, Quota, Window, Idem | Msg, Task |
| MUC-049 | Referral/benefit review | U/I | Form/Btn | link referrer/referred | Explain | staff registers | suggest benefit task | n/a | Auth, Data, Risk | Rec, Task, Audit |
| MUC-050 | Demand with no slot | U/I/E | Btn | detect unavailable preference | Recommend | staff adds waitlist | suggest alternatives | auto-notify if configured | Capacity, Consent, Quota | Rec, Task, Msg |
| MUC-051 | Convert lead to student | U/W | Btn | create student/link plan/schedule | Recommend | staff converts | checklist/approval | n/a | Auth, Data, Risk | Rec, Task, Audit |

## E. Agenda And Attendance

| ID | Use Case | Trig | Invoke | Programmatic Core | AI Role | Manual Path | Copilot Path | Autonomous Path | Gates | Outputs |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| MUC-052 | Create/adjust weekly grade | U | Form | create recurrence/capacity/teacher | Explain | manager edits | simulate impact | n/a | Auth, Data, Capacity | Rec, Audit |
| MUC-053 | Create class group | U | Form | create ClassGroup | None | manager creates | suggest fields | n/a | Auth, Data | Rec |
| MUC-054 | Review calendar/day schedule | U | Form/Assistant | query sessions/status | Summ | user reviews | summarize day | auto-highlight issues | Auth, Data | Report |
| MUC-055 | Open class session | U | Form | fetch session/students/status | None | user opens | context summary | n/a | Auth, Perm | Rec |
| MUC-056 | Take attendance | U | Form/Btn | update AttendanceRecord | None | teacher marks | detect anomalies | auto-remind missing call | Auth, Perm, Data | Rec, Audit |
| MUC-057 | Confirm presence | S/U | Auto/Btn | select eligible classes/students | Draft | staff sends | approve batch | auto-send within rules | Consent, Quota, Window, Capacity | Msg, Run, Usage |
| MUC-058 | Absence with notice | I/U | Auto/Btn | identify class/apply policy | Interpret | staff records | suggest credit/message | auto-create credit if clear | Data, Consent, Risk, Capacity | Rec, Msg, Run |
| MUC-059 | No-show | E/U | Auto/Btn | detect absent after class | Recommend | staff records | suggest retention action | auto-log/low-risk msg | Data, Consent, Quota, Risk | Rec, Task, Run |
| MUC-060 | Make-up request | I/U | Btn | validate credit/find slots | Recommend | staff chooses slot | suggest options/message | offer options if safe | Data, Capacity, Consent, Quota | Rec, Msg, Run |
| MUC-061 | Make-up credit ledger | U/E | Form | list/create/use/expire credits | Explain | staff manages | suggest expiring credits | auto-alert expiry | Auth, Data | Rec, Task |
| MUC-062 | Recover open slot | E/U | Btn | rank candidates by rules | Recommend | user invites/reserves | suggest candidates/msg | invite by rules | Data, Capacity, Consent, Quota, Window | Rec, Msg, Run, Usage |
| MUC-063 | Manage waitlist | U/E | Form/Btn | add/order/update waitlist | Recommend | staff manages | suggest priority | auto-invite if configured | Data, Capacity, Consent | Rec, Msg |
| MUC-064 | Change fixed schedule | I/U | Btn | find compatible slots/update default | Recommend | staff changes | suggest options/impact | n/a or limited | Data, Capacity, Risk | Rec, Audit |
| MUC-065 | Cancel/alter class by studio | U/E | Approval | compute affected students/credits | Draft | staff handles | prepare comms/tasks | n/a for batch | Consent, Risk, Capacity, Quota | Appr, Msg, Task, Audit |
| MUC-066 | Capacity/overbooking conflict | E/U | Auto/Btn | detect conflict/block booking | Explain | manager resolves | suggest fixes | auto-block unsafe booking | Data, Capacity, Risk | Task, Case, Audit |
| MUC-067 | First class checklist | E/U | Btn | verify plan/payment/contract/history | Recommend | staff checks | suggest missing actions | auto-create reminders | Data, Risk, Consent | Task, Rec |
| MUC-068 | Workshop/special class | U/B | Form/Bulk | create event/capacity/payment rules | Draft | manager creates | prepare campaign | auto-reminders only | Auth, Capacity, Consent, Quota | Rec, Msg, Appr |

## F. Finance And Student Plans

| ID | Use Case | Trig | Invoke | Programmatic Core | AI Role | Manual Path | Copilot Path | Autonomous Path | Gates | Outputs |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| MUC-069 | Create/update student plan | U | Form | create/update StudentPlan | None | staff edits | explain impact | n/a | Auth, Perm, Data | Rec, Audit |
| MUC-070 | Review finance overview | U/S | Assistant | aggregate receivables/status | Explain | manager reviews | suggest priorities | auto-refresh alerts | Auth, Perm, Data | Report |
| MUC-071 | Send due reminder | S/U | Auto/Btn | select due payments/policy | Draft | staff sends | approve message | auto-send within policy | Consent, Quota, Window, Idem | Msg, Run, Usage |
| MUC-072 | Overdue payment | E/S/U | Auto/Btn | classify overdue range/history | Draft | staff handles | prepare collection | auto low-risk reminder | Consent, Quota, Risk, Window | Msg, Task, Run |
| MUC-073 | Send Pix/payment link | U/I | Btn | fetch/generate link safely | Draft | staff sends link | approve send | auto-send if requested/safe | Provider, Consent, Idem, Risk | Msg, Log, Audit |
| MUC-074 | Confirm payment | W/U | Auto/Form | update payment idempotently | None | staff confirms | suggest match if unclear | auto-confirm webhook | Provider, Idem, Data | Rec, Log, Audit |
| MUC-075 | Reconcile unmatched payment | W/U | Btn | match payment candidates | Recommend | staff matches | suggest match | n/a | Auth, Data, Risk | Rec, Audit |
| MUC-076 | Failed payment | W/E | Auto/Btn | mark failed/retry policy | Draft | staff contacts | prepare retry/link | auto-retry if safe | Provider, Idem, Consent, Quota | Msg, Log, Task |
| MUC-077 | Receipt/invoice document | I/U | Btn | find/generate document ref | Draft | staff sends | prepare response | auto-send existing doc | Auth, Perm, Consent, Risk | Msg, Rec, Audit |
| MUC-078 | Contract/terms | U/S | Btn | track send/sign/status | Draft | staff manages | prepare reminder | auto-reminder if safe | Consent, Risk, Window | Msg, Task, Audit |
| MUC-079 | Financial exception | U/I | Case | create exception case | Summ | human decides | summarize/propose | n/a | Auth, Perm, Risk | Case, Task, Audit |
| MUC-080 | Pause/freeze plan | U/I | Case | compute agenda/finance impact | Explain | human handles | prepare impact/approval | n/a | Auth, Perm, Risk | Case, Appr, Audit |
| MUC-081 | Block/release access | U/E | Case | evaluate criteria/status | Explain | human decides | prepare approval | n/a | Auth, Perm, Risk | Case, Appr, Audit |
| MUC-082 | Credit/courtesy | U | Case | create benefit with reason | None | human records | n/a or explain | n/a | Auth, Perm, Risk | Rec, Audit |
| MUC-083 | Effective plan change/ending | U/I | Case/Btn | stop/update charges/schedule/credits | Explain | staff executes | simulate/approval | n/a | Auth, Perm, Data, Risk | Rec, Case, Audit |
| MUC-084 | Monthly financial close | S/U | Report | aggregate period/payments | Summ | manager reviews | explain anomalies | auto-create report | Auth, Data | Report |

## G. Retention And Complaints

| ID | Use Case | Trig | Invoke | Programmatic Core | AI Role | Manual Path | Copilot Path | Autonomous Path | Gates | Outputs |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| MUC-085 | Review retention dashboard | U/S | Assistant | compute risks/segments | Explain | manager reviews | suggest priorities | auto-update dashboard | Auth, Data | Report |
| MUC-086 | Frequency drop | E/S/U | Auto/Btn | detect attendance decline | Recommend | staff acts | suggest message/task | auto-create low-risk task/msg | Data, Consent, Quota, Risk | Task, Msg, Run |
| MUC-087 | Inactive student | E/S | Auto/Btn | detect inactivity window | Draft | staff contacts | prepare check-in | auto limited check-in | Consent, Quota, Risk, Window | Msg, Task, Run |
| MUC-088 | Student return | I/U | Btn | find status/slots/context | Recommend | staff schedules | suggest plan/slot | auto-handle simple return | Data, Capacity, Consent | Rec, Msg |
| MUC-089 | Cancellation risk | I/E/U | Case | open risk/cancel case | Summ | human handles | draft save plan | n/a | Risk, Perm, Data | Case, Task, Audit |
| MUC-090 | Post-cancellation | U/E | Case | cancel schedules/charges/status | Draft | staff finalizes | prepare final msg | limited internal updates | Auth, Risk, Consent | Rec, Msg, Audit |
| MUC-091 | Ex-student reactivation | B/S | Bulk/Approval | build eligible segment | Draft | staff creates campaign | approve batch | n/a for batch in MVP | Consent, Quota, Risk, Window | Appr, Msg, Usage |
| MUC-092 | Satisfaction check | S/U | Auto/Btn | select event/window | Draft | staff sends | approve/check | auto-send low-risk survey | Consent, Quota, Window | Msg, Run |
| MUC-093 | Open complaint case | I/U | Case | create complaint/SLA/owner | Classify | staff opens | classify severity | auto-open from message | Auth, Data, Risk | Case, Task |
| MUC-094 | Resolve complaint/recover trust | U | Case/Btn | update status/follow-up | Draft | owner resolves | draft response/plan | n/a | Risk, Perm, Consent | Case, Msg, Audit |
| MUC-095 | Return after pause | S/I/U | Auto/Btn | detect pause end/status | Draft | staff contacts | prepare return options | auto-reminder if safe | Consent, Quota, Data | Msg, Task |
| MUC-096 | Risk segmentation | U/S | Assistant | compute segment/risk factors | Explain | manager reviews | suggest actions | auto-update segments | Auth, Data | Report, Task |
| MUC-097 | Sensitive health/personal event | I/U | Case | pause unsafe automation/log restricted note | Summ | human handles | summarize for owner | n/a | Risk, Perm, Consent | Case, Task, Audit |

## H. Student History And Teacher Work

| ID | Use Case | Trig | Invoke | Programmatic Core | AI Role | Manual Path | Copilot Path | Autonomous Path | Gates | Outputs |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| MUC-098 | Teacher opens class context | U/S | Assistant | fetch relevant student context | Summ | teacher reads | highlight key points | auto-prepare context | Auth, Perm, Data | Report |
| MUC-099 | Add post-class observation | U | Form/Btn | save note/event | Summ | teacher writes | summarize/transcribe | n/a | Auth, Perm, Risk | Rec, Audit |
| MUC-100 | Register restriction/care | U/I | Form/Case | save restricted history event | Classify | staff records | suggest visibility | n/a | Auth, Perm, Risk | Rec, Audit |
| MUC-101 | Review objective/evolution | U/S | Assistant | fetch goals/history | Summ | staff reviews | suggest review task | auto-remind stale goals | Auth, Perm, Data | Task, Report |
| MUC-102 | Store document/anamnesis | U/I | Form/Btn | upload/store/classify doc | Classify | staff uploads | classify/extract safe fields | auto-flag missing docs | Auth, Perm, Risk | Rec, Task |
| MUC-103 | Correct history event | U | Form/Case | update event with audit | Explain | user corrects | explain impact | n/a | Auth, Perm, Risk | Rec, Audit |
| MUC-104 | Handoff between teachers | U/E | Btn | collect context/assign task | Summ | teacher writes handoff | draft summary | auto-create when teacher/class changes | Auth, Perm, Data | Task, Rec |
| MUC-105 | Remind teacher note | S/E | Auto | detect missing note/priority | Draft | manager asks teacher | prepare reminder | auto-create reminder | Auth, Data, Quota | Task, Msg |
| MUC-106 | Share safe context with student | U/I | Approval | filter shareable data | Draft | human shares | prepare approval | n/a | Auth, Perm, Risk, Consent | Appr, Msg, Audit |
| MUC-107 | History visibility permissions | U | Form | update/view RBAC rules | Explain | owner edits | explain exposure | auto-block access | Auth, Perm, Risk | Rec, Audit |
| MUC-108 | Unified student timeline | U | Assistant | aggregate timeline events | Summ | staff reviews | summarize/filter | auto-detect conflicts | Auth, Perm, Data | Report, Task |

## I. Agents, Runtime And Quotas

| ID | Use Case | Trig | Invoke | Programmatic Core | AI Role | Manual Path | Copilot Path | Autonomous Path | Gates | Outputs |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| MUC-109 | Configure included agents | U | Form | enforce entitlements | Explain | owner configures | setup suggestions | n/a | Auth, Perm, Entitlement | Rec, Audit |
| MUC-110 | Configure an agent | U | Form/Assistant | save agent config | Explain | owner edits | suggest defaults | n/a | Auth, Perm, Entitlement | Rec, Audit |
| MUC-111 | Configure a flow | U | Form/Assistant | save flow config/rules | Explain | owner edits | suggest rules | n/a | Auth, Perm, Risk | Rec, Audit |
| MUC-112 | Simulate flow | U | Btn | run dry-run scenario | Explain | user tests | agent explains result | n/a | Auth, Data, Quota | Run, Report |
| MUC-113 | Activate/pause flow | U | Btn | update enabled state | Explain | owner toggles | warn impact | n/a | Auth, Perm, Risk | Rec, Audit |
| MUC-114 | Review flow execution | U/E | FlowPanel | fetch run/tool/logs | Explain | user reviews | explain failure/result | auto-log run | Auth, Perm | Run, Log, Usage |
| MUC-115 | Approve/reject copilot action | U | Approval | decide approval state | Explain | user approves/edits | n/a | n/a | Auth, Perm, Risk | Appr, Audit |
| MUC-116 | Review agent performance | U/S | Report | aggregate run metrics | Explain | manager reviews | suggest improvements | auto-refresh metrics | Auth, Data | Report |
| MUC-117 | Investigate automation incident | U/E | Case/Btn | link run/impact/correction | Explain | human investigates | suggest fix | auto-open incident on anomaly | Auth, Risk, Data | Case, Task, Audit |
| MUC-118 | Change operational rule/policy | U | Form/Btn | version/simulate policy | Explain | owner changes | impact simulation | n/a | Auth, Perm, Risk | Rec, Appr, Audit |
| MUC-119 | Resolve flow blocked by data | E/U | Btn | list blockers/object links | Recommend | user fixes | suggest fix sequence | auto-create tasks | Auth, Data | Task, Report |
| MUC-120 | Review quota/usage | U/S | Assistant | aggregate usage ledger | Explain | owner reviews | recommend economy | auto-alert thresholds | Auth, Data, Quota | Report, Usage |
| MUC-121 | Configure economy rules | U | Form | update economy priorities | Explain | owner edits | suggest settings | auto-apply thresholds | Auth, Perm, Quota | Rec, Audit |
| MUC-122 | Buy/request quota pack | U/W | Form | start trusted add-on flow | None | owner buys | n/a | n/a | Auth, Provider, Quota | Rec, Audit |

## J. Reports, Integrations And Administration

| ID | Use Case | Trig | Invoke | Programmatic Core | AI Role | Manual Path | Copilot Path | Autonomous Path | Gates | Outputs |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| MUC-123 | Manage Taliya subscription | U/W | Form | provider portal/session | None | owner manages | n/a | webhook updates state | Auth, Provider, Idem | Rec, Audit |
| MUC-124 | View Taliya invoices | U | Form | fetch invoices | None | owner views/downloads | n/a | n/a | Auth, Provider | Report |
| MUC-125 | Review integrations | U/E | Form | list provider statuses | Explain | admin reviews | explain setup/failure | auto-monitor status | Auth, Provider | Report, Log |
| MUC-126 | Investigate integration logs | U/E | Btn | fetch log/event/idempotency | Explain | admin inspects | suggest retry/fix | auto-create alert | Auth, Provider, Idem | Log, Task |
| MUC-127 | Review audit event | U | Form | fetch audit metadata | Explain | authorized user reviews | explain before/after | n/a | Auth, Perm | Audit |
| MUC-128 | Reports hub/export review | U/S | Report | aggregate report list | Summ | manager reviews | explain metrics | auto-generate scheduled reports | Auth, Data | Report |
| MUC-129 | Financial report | U/S | Report | aggregate payments/charges | Explain | manager reviews | explain anomalies | auto-refresh | Auth, Perm, Data | Report |
| MUC-130 | Sales report | U/S | Report | aggregate pipeline/source | Explain | manager reviews | suggest improvements | auto-refresh | Auth, Data | Report |
| MUC-131 | Capacity/occupancy report | U/S | Report | aggregate sessions/capacity | Explain | manager reviews | suggest capacity actions | auto-refresh | Auth, Data, Capacity | Report |
| MUC-132 | Source ROI/quality | U/S | Report | aggregate source/conversion | Explain | manager reviews | suggest source actions | auto-refresh | Auth, Data | Report |

## K. Candidate Gaps From Complete Audit

| ID | Use Case | Trig | Invoke | Programmatic Core | AI Role | Manual Path | Copilot Path | Autonomous Path | Gates | Outputs |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| AUD-001 | Configure holidays/recess/closures | U | Form/Btn | store closure calendar/apply dates | Explain | owner configures | simulate impact | n/a | Auth, Perm, Capacity | Rec, Audit |
| AUD-002 | Configure rooms/equipment/resources | U | Form | create Resource/capacity | None | owner configures | suggest setup gaps | n/a | Auth, Data | Rec |
| AUD-003 | Configure teacher availability rules | U | Form | store availability/substitution prefs | None | owner configures | suggest gaps | n/a | Auth, Data | Rec |
| AUD-004 | Configure tags/segments/fields | U | Form | create custom metadata schema | None | admin configures | suggest fields | n/a | Auth, Perm | Rec, Audit |
| AUD-005 | Role notification preferences | U | Form | store notification routing | None | user configures | suggest defaults | auto-route alerts | Auth, Perm | Rec |
| AUD-006 | Daily opening/closing checklist | U/S | Form/Assistant | instantiate checklist run | Recommend | staff completes | suggest missing items | auto-create checklist | Auth, Data | Task, Rec |
| AUD-007 | Teacher availability/substitution issue | E/U | Case/Btn | detect affected classes/options | Recommend | manager resolves | suggest options | auto-alert only | Auth, Data, Capacity, Risk | Case, Task |
| AUD-008 | Room/equipment outage impact | E/U | Case/Btn | find affected classes/capacity | Explain | manager resolves | suggest mitigation | auto-block unsafe booking | Auth, Data, Capacity, Risk | Case, Task, Audit |
| AUD-009 | Holiday/recess class impact | U/E | Btn | apply closure calendar/find impacted sessions | Explain | manager adjusts | simulate rollout/comms | n/a | Auth, Capacity, Risk | Case, Appr, Audit |
| AUD-010 | Class/student broadcast | U/B | Bulk/Approval | select audience/template/category | Draft | staff sends manually | approve broadcast | n/a for batch MVP | Auth, Consent, Quota, Window, Risk | Appr, Msg, Usage |
| AUD-011 | Partial payment/payment promise | U/I | Form/Case | create PaymentAgreement/status | Summ | staff records | draft terms/reminder | auto-reminder only | Auth, Perm, Risk, Consent | Rec, Task, Audit |
| AUD-012 | Renegotiate overdue balance | U/I | Case/Approval | compute balance/proposed terms | Explain | human negotiates | prepare proposal | n/a | Auth, Perm, Risk | Appr, Rec, Audit |
| AUD-013 | Refund/chargeback/dispute | U/W | Case | create dispute/refund case | Summ | human handles | summarize facts | n/a | Auth, Perm, Risk, Provider | Case, Audit |
| AUD-014 | Financial/accounting export | U/S | Form | generate export file/report | None | user exports | explain report | scheduled export optional | Auth, Perm, Data | Report, Audit |
| AUD-015 | Cashflow forecast | U/S | Report/Assistant | forecast receivables from payments | Explain | manager reviews | explain risks | auto-refresh forecast | Auth, Data | Report |
| AUD-016 | Milestone/engagement celebration | E/S | Auto/Btn | detect milestone | Draft | staff recognizes | draft message | auto-low priority if allowed | Consent, Quota, Risk, Window | Msg, Task, Run |
| AUD-017 | First-week new student journey | E/S | Auto/Btn | detect new student/week status | Recommend | staff follows checklist | suggest follow-up | auto-create reminders/check-ins | Data, Consent, Quota, Risk | Task, Msg, Run |
| AUD-018 | Anamnese/consent/emergency gate | E/U | Form/Btn | check required intake fields | Explain | staff completes | suggest missing docs | auto-block/alert only | Auth, Perm, Data, Risk | Task, Audit |
| AUD-019 | Periodic student evaluation/review | S/U | Auto/Btn | find due review periods | Recommend | teacher schedules | suggest agenda/task | auto-create review tasks | Auth, Data, Perm | Task, Rec |
| AUD-020 | Escalate sensitive complaint/pause automations | E/U | Case/Btn | set severity/pause flags | Summ | owner handles | draft escalation summary | auto-pause on severe flags | Auth, Perm, Risk | Case, Audit |
| AUD-021 | Full CRM export/backup | U/S | Form | generate tenant export | None | owner exports | n/a | scheduled backup optional | Auth, Perm, Risk | Report, Audit |
| AUD-022 | LGPD export/delete/anonymize | U/I | Case | create privacy request workflow | Summ | human executes | prepare checklist/response | n/a | Auth, Perm, Risk | Case, Audit |
| AUD-023 | Approve Taliya support access | U | Approval | create scoped access grant | Explain | owner approves | explain scope | auto-expire grant | Auth, Perm, Risk | Appr, Audit |
| AUD-024 | Archive/reactivate record | U | Form | update archive state | None | user archives/reactivates | warn dependencies | n/a | Auth, Perm, Data | Rec, Audit |
| AUD-025 | Segment and bulk eligibility | U/B | Bulk/Approval | build segment/check eligibility | Recommend | manager selects | suggest segment/action | auto-refresh segment only | Auth, Consent, Quota, Risk | Rec, Appr |

## Completeness Result

This matrix maps all 157 currently known candidate manager use cases:

```text
132 cataloged MUC rows
+ 25 audit candidate rows
= 157 execution-mapped rows
```

This is now enough to evaluate:

- whether each use case can be done manually;
- where copiloto is useful;
- where autonomy is safe;
- where AI is unnecessary;
- which gates must block execution;
- what each action should produce in the CRM.

## Remaining Product Decisions

Before implementation, each row still needs:

- final priority: P0/P1/P2/out;
- accepted vs merged vs deferred;
- exact UI copy for buttons/actions;
- exact data contracts;
- tests/evals for AI-assisted rows;
- permissions per role;
- quota policy per autonomous/costly action.
