# Tasks: SaaS Onboarding And Studio Setup

**Input**: Design documents from `/specs/004-saas-onboarding/`
**Prerequisites**: `spec.md`, `plan.md`, `data-model.md`, `contracts/onboarding-contract.md`

## Phase 1: Tenant And Account Foundation

- [ ] T001 Define user, tenant and membership models
- [ ] T002 Add tenant authorization helper
- [ ] T003 Connect onboarding access to active entitlement from billing
- [ ] T004 Create or link tenant after trusted billing activation
- [ ] T005 Add cross-tenant denial tests
- [ ] T028 Implement activation claim flow from Spec 3 pending tenant activation
- [ ] T029 Require magic link/OTP or equivalent authenticated owner session before workspace claim
- [ ] T030 Verify checkout return URL, external CRM/spreadsheet status, chat intent and unpaid subscription cannot start onboarding
- [ ] T035 Define safe commercial context payload accepted from billing activation for onboarding prefill
- [ ] T036 Verify commercial context does not grant access, override entitlement or enable unavailable agents

## Phase 2: Studio Profile

- [ ] T006 Build onboarding route/page shell
- [ ] T007 Add studio profile form
- [ ] T008 Persist studio profile tenant-scoped
- [ ] T009 Track onboarding progress
- [ ] T010 Add validation for required studio profile fields
- [ ] T037 Prefill/suggest studio pains and setup priorities from safe commercial context when present

## Phase 3: Agent Setup

- [ ] T011 Load plan entitlements and included agents
- [ ] T012 Render setup cards for Atendimento, Agenda, Vendas, Financeiro, Retencao, Gestao and Historico/Evolucao
- [ ] T013 Lock or upsell-gate unavailable agents
- [ ] T014 Save tenant-scoped agent configuration
- [ ] T015 Audit sensitive agent setup changes
- [ ] T031 Verify Base configures CRM only and 0 active AI agents by default
- [ ] T032 Verify 1 Agente configures exactly one selected primary agent
- [ ] T033 Verify 3 Agentes configures exactly three selected primary agents
- [ ] T034 Verify 7 Agentes configures all seven primary agents and does not include Agente sob medida by default
- [ ] T038 Suggest recommended agents from consultor/demo context only when included by active entitlement

## Phase 4: Channel/Tool Setup Status

- [ ] T016 Add WhatsApp setup status step
- [ ] T017 Mark pending/manual setup without blocking required onboarding when allowed
- [ ] T018 Ensure provider secrets are never exposed to frontend

## Phase 5: First Workspace

- [ ] T019 Implement onboarding finish action
- [ ] T020 Create first-run checklist
- [ ] T021 Redirect to workspace after required steps
- [ ] T022 Show incomplete optional setup inside workspace

## Final Verification

- [ ] T023 Verify paid tenant reaches onboarding
- [ ] T024 Verify unpaid visitor is denied
- [ ] T025 Verify tenant A cannot read tenant B setup data
- [ ] T026 Verify agent availability follows plan entitlement
- [ ] T027 Verify onboarding progress and first-run checklist survive refresh
- [ ] T039 Verify consultor/demo context improves onboarding checklist without bypassing billing or tenant authorization
- [ ] T040 Verify onboarding starts only from trusted pending tenant activation created after paid webhook confirmation, not from Sales Inbox, external CRM/spreadsheet, chat intent, checkout return or query string
- [ ] T041 Verify commercial context prefill preserves `leadId`, selected pains, recommended agents, recommended plan and guided-demo context while billing entitlement remains the only access source
