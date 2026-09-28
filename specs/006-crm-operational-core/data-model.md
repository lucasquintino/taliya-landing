# Data Model: Taliya CRM Operational Core

## Tenant

Fields:

- `id`
- `name`
- `status`: active, past_due_limited, canceled, suspended
- `planId`
- `createdAt`
- `updatedAt`

Rules:

- All operational records are tenant-scoped.
- Tenant access must be checked through membership and entitlement.

## UserAccount

Fields:

- `id`
- `name`
- `email`
- `phone`
- `createdAt`
- `updatedAt`

## Membership

Fields:

- `tenantId`
- `userId`
- `role`: owner, admin, operations, finance, teacher, member
- `permissions`
- `createdAt`

Rules:

- Object-level permissions are required for finance, history, sensitive notes and configuration.

## StudioProfile

Fields:

- `tenantId`
- `studioName`
- `cityState`
- `contactWhatsApp`
- `activeStudentsRange`
- `scheduleModel`
- `currentSystem`
- `biggestPains`
- `openingHours`
- `attendanceWindows`

## Contact

Fields:

- `id`
- `tenantId`
- `name`
- `phone`
- `email`
- `type`: interested, student, ex_student, responsible, supplier, team, unknown
- `whatsappOptOut`
- `consentStatus`
- `createdAt`
- `updatedAt`

## ResponsibleParty

Fields:

- `id`
- `tenantId`
- `contactId`
- `studentId`
- `relationship`
- `permissions`: schedule, financial, history_limited, emergency

## Student

Fields:

- `id`
- `tenantId`
- `contactId`
- `status`: active, inactive, paused, canceled, trial, pending_start
- `currentPlanId`
- `defaultClassSlots`
- `teacherIds`
- `riskStatus`
- `createdAt`
- `updatedAt`

## InterestedPerson

Fields:

- `id`
- `tenantId`
- `contactId`
- `stage`: new, qualified, trial_scheduled, trial_completed, pre_enrollment, won, lost
- `source`
- `preferredTimes`
- `interestedPlan`
- `lastContactAt`
- `nextActionAt`
- `lostReason`

## StudioPlan

Represents plans sold by the studio to its own students.

Fields:

- `id`
- `tenantId`
- `name`
- `price`
- `frequency`
- `billingCycle`
- `makeUpPolicy`
- `renewalWindowDays`
- `active`

## ClassGroup

Fields:

- `id`
- `tenantId`
- `name`
- `teacherId`
- `capacity`
- `recurrence`
- `room`
- `status`

## ClassSession

Fields:

- `id`
- `tenantId`
- `classGroupId`
- `startsAt`
- `endsAt`
- `teacherId`
- `capacity`
- `status`: scheduled, canceled, completed
- `attendanceClosedAt`

## AttendanceRecord

Fields:

- `id`
- `tenantId`
- `classSessionId`
- `studentId`
- `status`: expected, confirmed, absent_with_notice, no_show, attended, corrected
- `source`: team, agent, student_message, import
- `correctedBy`
- `correctedAt`

## MakeUpCredit

Fields:

- `id`
- `tenantId`
- `studentId`
- `sourceClassSessionId`
- `status`: available, reserved, used, expired, canceled
- `expiresAt`
- `policySnapshot`

## WaitlistEntry

Fields:

- `id`
- `tenantId`
- `studentId`
- `preferredClassGroupId`
- `preferredTimes`
- `priority`
- `status`

## Payment

Fields:

- `id`
- `tenantId`
- `studentId`
- `studioPlanId`
- `amount`
- `dueDate`
- `paidAt`
- `status`: pending, paid, overdue, failed, disputed, refunded, canceled
- `providerRef`

## Charge

Fields:

- `id`
- `tenantId`
- `paymentId`
- `channel`
- `status`: draft, pending_approval, sent, failed, paid, closed
- `lastSendId`

## Contract

Fields:

- `id`
- `tenantId`
- `studentId`
- `studioPlanId`
- `status`: draft, sent, signed, expired, canceled
- `documentRef`

## StudentHistoryEvent

Fields:

- `id`
- `tenantId`
- `studentId`
- `type`: note, goal, restriction, document, attendance, payment, retention, correction
- `visibility`: owner_admin, teacher_allowed, finance_allowed, restricted
- `content`
- `createdBy`
- `createdAt`

## DocumentRecord

Fields:

- `id`
- `tenantId`
- `studentId`
- `type`: anamnesis, receipt, contract, medical_note, image, audio, other
- `storageRef`
- `visibility`
- `reviewStatus`

## Conversation

Fields:

- `id`
- `tenantId`
- `channel`: whatsapp, internal_note, email, other
- `contactId`
- `studentId`
- `interestedPersonId`
- `status`: open, waiting_contact, waiting_team, human_active, closed, opted_out
- `lastMessageAt`

## Message

Fields:

- `id`
- `tenantId`
- `conversationId`
- `direction`: inbound, outbound
- `senderType`: contact, user, agent, system
- `content`
- `providerMessageId`
- `createdAt`

## OperationCase

Fields:

- `id`
- `tenantId`
- `caseType`
- `sourceFlowId`
- `sourceConversationId`
- `primaryObjectType`
- `primaryObjectId`
- `status`: open, waiting_contact, waiting_team, pending_approval, running, blocked, resolved, paused, canceled
- `priority`
- `summary`
- `nextAction`
- `createdAt`
- `updatedAt`

## Task

Fields:

- `id`
- `tenantId`
- `caseId`
- `assignedToUserId`
- `assignedQueue`
- `title`
- `status`: open, in_progress, done, canceled
- `dueAt`

## Approval

Fields:

- `id`
- `tenantId`
- `caseId`
- `flowRunId`
- `type`: message_send, financial_exception, campaign, schedule_change, history_share, config_change
- `proposedAction`
- `status`: pending, approved, edited, rejected, expired
- `approvedBy`
- `decidedAt`

## SendAttempt

Fields:

- `id`
- `tenantId`
- `caseId`
- `conversationId`
- `channel`: whatsapp, email, internal
- `templateName`
- `costClass`: service, utility, marketing, internal
- `status`: queued, sent, delivered, failed, skipped
- `providerRef`
- `idempotencyKey`

## AgentConfiguration

Fields:

- `tenantId`
- `agentId`
- `enabled`
- `includedByEntitlement`
- `defaultMode`: manual, copilot, autonomous
- `rules`

## FlowConfiguration

Fields:

- `tenantId`
- `flowId`
- `agentId`
- `enabled`
- `mode`: manual, copilot, autonomous
- `autonomousScope`
- `afterLimitAction`
- `tone`
- `templates`
- `sendWindow`
- `attemptLimit`
- `creditLimit`
- `responsibleQueue`
- `approvalRules`
- `handoffRules`
- `pauseRules`

## FlowRun

Fields:

- `id`
- `tenantId`
- `flowId`
- `agentId`
- `mode`
- `caseId`
- `status`: started, waiting_data, pending_approval, sent, transitioned, resolved, blocked, failed, paused
- `inputSummary`
- `outputSummary`
- `nextFlowId`
- `quotaConsumed`
- `createdAt`
- `updatedAt`

## QuotaLedgerEntry

Fields:

- `id`
- `tenantId`
- `flowRunId`
- `agentId`
- `origin`: ai, whatsapp_service, whatsapp_utility, whatsapp_marketing, batch_job, media, history
- `quantity`
- `estimatedCost`
- `createdAt`

## AuditEvent

Fields:

- `id`
- `tenantId`
- `actorType`: user, agent, system, integration
- `actorId`
- `action`
- `objectType`
- `objectId`
- `before`
- `after`
- `safeMetadata`
- `createdAt`

## IntegrationLog

Fields:

- `id`
- `tenantId`
- `integration`: whatsapp, billing, calendar, import, ai, payment
- `eventType`
- `status`
- `idempotencyKey`
- `safeError`
- `createdAt`

## Round 1 Candidate Object Addendum

Round 1 audit found that the use-case and screen maps now reference business objects that are not yet in the core model above.

Do not add all of these blindly as separate database tables. Before implementation, classify each one as:

- first-class entity;
- operation-case type;
- job/log type;
- derived report/view;
- configuration object;
- not needed.

### Likely First-Class Entities

| Object | Needed for |
| --- | --- |
| `PolicyVersion` | Operational rule changes, effective dates, rollout, rollback and simulation. |
| `PrivacyRequest` | LGPD export, correction, deletion and anonymization requests. |
| `SupportAccessGrant` | Tenant-approved temporary Taliya support access. |
| `SegmentDefinition` | Saved audience rules and bulk-action eligibility. |
| `PaymentAgreement` | Partial payment, payment promise and renegotiation. |
| `StudentPlan` | The sold plan attached to one student, with frequency, price, status and effective dates. |
| `DataQualityIssue` | Missing, conflicting or unsafe data that blocks setup, automations or decisions. |
| `Resource` | Rooms, equipment, capacity and outage impact. |
| `ClosureCalendar` | Holidays, recesses and studio closure impact. |
| `NotificationPreference` | Role/user routing for alerts and work queues. |
| `ChecklistRun` | Daily opening/closing and setup checklist execution. |
| `TeacherAvailability` | Teacher availability, restrictions and substitution preferences if teacher scheduling becomes first-class. |

### Likely OperationCase Types

| Object name in maps | Recommended modeling |
| --- | --- |
| `ComplaintCase` | `OperationCase` with complaint type, severity, owner and recovery status. |
| `IncidentCase` | `OperationCase` linked to `FlowRun`, impact and correction. |
| `RefundDisputeCase` | `OperationCase` linked to `Payment`, provider state and evidence. |
| `Broadcast` | `OperationCase` or send batch with audience, approval and send attempts. |
| `RecordArchiveState` | Archive/reactivation state on `Contact`, `InterestedPerson`, `Student` or related record. |
| `IntakeGate` | Data-quality/history gate linked to `Student`, `DocumentRecord` and `Approval`. |
| `StudentReview` | Periodic review case or task linked to `StudentHistoryEvent`, teacher notes and goals. |

### Likely Jobs, Logs Or Reports

| Object name in maps | Recommended modeling |
| --- | --- |
| `ExportJob` | Job/log with requester, scope, status, file availability and audit. |
| `ImportJob` | Job/log with mapping, validation, duplicate review and audit. |
| `AgentReport`, `FinanceReport`, `WeeklyReport`, `Report` | Derived reports backed by persisted CRM records. |
| `OpportunityMetric`, `SourceMetric`, `Bottleneck`, `FinanceForecast`, `RetentionRisk` | Derived metrics or materialized reporting views, not necessarily user-edited entities. |
| `Feedback` | Satisfaction signal, complaint precursor or survey response; may be stored as its own record or as a typed history/case event. |
| `StudentMilestone` | Derived engagement milestone used by retention; avoid a separate table unless milestone rules become configurable. |
| `UsageLedger` | Alias or product view over `QuotaLedgerEntry`. |

### Configuration Objects To Validate

| Object | Notes |
| --- | --- |
| `AgendaPolicy` | Could be part of `PolicyVersion` or configuration. |
| `PrivacyPolicy` | Could be settings plus versioned policy history. |
| `EconomyRule` | Could belong to tenant settings and flow limits. |
| `Template` | Required for approved answers and sends; decide whether it belongs in CRM settings or messaging module. |
| `ChannelConnection` | Provider/channel configuration and status. |
| `CustomField` | Metadata definition for contacts, students, leads and segments. |
| `Referral` | Referral source and benefit tracking; may be a sales object or fields on `InterestedPerson`/`Student`. |
| `Invoice` | Taliya billing invoice or studio financial document; clarify ownership before schema design. |

### Product Naming Alignment

Some map labels are product views, not entities:

- `TodayDashboard`;
- `SetupChecklist`;
- `StudentHistory`;
- `Trial`;
- `PreEnrollment`;
- `Checkout`;
- `Benefit`;
- `QuotaPack`;
- `Subscription`.

These may still need routes and UI, but the final data model should decide whether they are real persisted objects, aliases for existing objects, or product-facing names for grouped behavior.
