# Object Action Map - Taliya CRM

> Status: exploratory. This map shows which actions are available around each business object. It helps decide pages, buttons, drawers and mobile actions.

## Contact

| Actions | Related IDs | UI Pattern |
| --- | --- | --- |
| create/update contact | MUC-030 | form |
| opt-out/preference | MUC-028 | form/action |
| validate responsible/family context | MUC-029, MUC-031 | drawer |
| merge duplicate | MUC-033 | review table |
| archive/reactivate | AUD-024 | action |

## Conversation

| Actions | Related IDs | UI Pattern |
| --- | --- | --- |
| classify intent | MUC-024, MUC-025 | automatic/action |
| prepare reply | MUC-026, MUC-040, MUC-046 | smart button |
| summarize | MUC-027 | assistant |
| human takeover | MUC-027 | button |
| pause/resume AI | MUC-027, AUD-020 | button |
| route to case/flow | MUC-025, MUC-035 | action |

## InterestedPerson

| Actions | Related IDs | UI Pattern |
| --- | --- | --- |
| capture lead | MUC-036, MUC-037 | form/capture |
| dedupe/source attribution | MUC-036, MUC-038 | system/review |
| qualify | MUC-039 | smart action |
| schedule trial | MUC-041 | drawer |
| follow-up cadence | MUC-044, MUC-045 | action/auto |
| convert to student | MUC-051 | conversion action |
| mark lost | agent C9 | status action |

## Student

| Actions | Related IDs | UI Pattern |
| --- | --- | --- |
| view profile/timeline | MUC-108 | page/timeline |
| analyze retention risk | MUC-086, MUC-096 | smart button |
| change fixed schedule | MUC-064 | drawer |
| manage plan | MUC-069, MUC-083 | page/drawer |
| add note/restriction | MUC-099, MUC-100 | form |
| first-week follow-up | AUD-017 | checklist |
| archive/reactivate | AUD-024 | action |

## ClassSession

| Actions | Related IDs | UI Pattern |
| --- | --- | --- |
| open class | MUC-055 | detail page |
| take attendance | MUC-056 | checklist |
| confirm presence | MUC-057 | smart button/auto |
| register absence | MUC-058 | action |
| handle no-show | MUC-059 | auto/action |
| find fit for open slot | MUC-062 | smart button |
| cancel/alter class | MUC-065 | approval drawer |
| show teacher context | MUC-098 | assistant |

## MakeUpCredit

| Actions | Related IDs | UI Pattern |
| --- | --- | --- |
| create from absence | MUC-058 | automatic/action |
| use credit | MUC-060 | drawer |
| expire/alert | MUC-061 | automatic |
| suggest open slot | MUC-062 | smart button |
| audit correction | MUC-056, MUC-061 | audit link |

## WaitlistEntry

| Actions | Related IDs | UI Pattern |
| --- | --- | --- |
| add to waitlist | MUC-050, MUC-063 | form |
| rank candidates | MUC-062, MUC-063 | smart action |
| invite candidate | MUC-062 | copilot/auto |
| reserve accepted slot | MUC-062, MUC-063 | system action |

## Payment

| Actions | Related IDs | UI Pattern |
| --- | --- | --- |
| view status | MUC-070, MUC-072 | detail |
| send due reminder | MUC-071 | smart button/auto |
| send Pix/link | MUC-073 | smart button |
| confirm payment | MUC-074 | webhook/form |
| reconcile | MUC-075 | review table |
| failed payment retry | MUC-076 | action/auto |
| partial payment promise | AUD-011 | case/drawer |
| dispute/refund | AUD-013 | case |

## StudentPlan

| Actions | Related IDs | UI Pattern |
| --- | --- | --- |
| create/update | MUC-069 | form |
| pause/freeze | MUC-080 | case |
| block/release | MUC-081 | approval |
| credit/courtesy | MUC-082 | case |
| effective change/end | MUC-083 | case workflow |
| contract terms | MUC-078 | document/action |

## ComplaintCase

| Actions | Related IDs | UI Pattern |
| --- | --- | --- |
| open complaint | MUC-093 | case |
| classify severity | MUC-093, AUD-020 | AI/system |
| pause automation | AUD-020 | button/auto |
| resolve complaint | MUC-094 | workflow |
| recover trust | MUC-094 | follow-up |

## FlowConfiguration

| Actions | Related IDs | UI Pattern |
| --- | --- | --- |
| configure flow | MUC-111 | config page |
| simulate | MUC-112 | button |
| activate/pause | MUC-113 | button |
| view executions | MUC-114 | run list |
| explain blocked data | MUC-119 | assistant/action |

## FlowRun

| Actions | Related IDs | UI Pattern |
| --- | --- | --- |
| view execution | MUC-114 | detail |
| explain decision | MUC-114 | assistant |
| create incident | MUC-117 | button |
| inspect quota used | MUC-120 | usage link |
| audit | MUC-127 | audit link |

## PolicyVersion

| Actions | Related IDs | UI Pattern |
| --- | --- | --- |
| create/change policy | MUC-013, MUC-118 | page/form |
| simulate impact | MUC-118, AUD-009 | simulation |
| schedule effective date | MUC-013, AUD-001 | form |
| rollout communication | AUD-010 | approval |
| audit change | MUC-127 | audit link |

## DataQualityIssue

| Actions | Related IDs | UI Pattern |
| --- | --- | --- |
| list blockers | MUC-023, MUC-119 | page |
| fix missing data | MUC-119 | action |
| resolve duplicates | MUC-005, MUC-033 | review table |
| block automation | MUC-119 | system gate |

## Approval

| Actions | Related IDs | UI Pattern |
| --- | --- | --- |
| review proposal | MUC-016, MUC-115 | approval drawer |
| approve/edit/reject | MUC-115 | actions |
| inspect cost/risk | MUC-115, MUC-120 | drawer |
| audit decision | MUC-127 | audit link |
