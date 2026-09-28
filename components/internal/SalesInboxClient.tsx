"use client";

import { useCallback, useEffect, useMemo, useState } from "react";

type LeadSummary = {
  leadId: string;
  status: string;
  priority: "hot" | "warm" | "cold" | "manual";
  urgency: string;
  readiness: string;
  channel: string;
  sourceSection?: string;
  sourcePage: string;
  conversionPath: string;
  commercialStage?: string;
  waitlistStatus?: string;
  waitlistOfferedAt?: string;
  waitlistJoinedAt?: string;
  waitlistDeclinedAt?: string;
  diagnosticStatus?: string;
  diagnosticCompletedAt?: string;
  demoStatus?: string;
  demoOfferedAt?: string;
  demoSeenAt?: string;
  leadSourceChannel?: string;
  leadSourceDetail?: string;
  primaryPainOrIntent?: string;
  missingWaitlistFields?: string;
  closureState?: string;
  humanActive?: boolean;
  lastMessageAt?: string;
  selectedPlanId?: string;
  recommendedPlanId: string;
  selectedPainIds: string[];
  recommendedAgentIds: string[];
  contact: {
    name?: string;
    whatsapp?: string;
    email?: string;
    normalizedWhatsapp?: string;
  };
  summary: string;
  nextAction: string;
  diagnosticClassification?: string;
  diagnosticContextVariant?: string;
  diagnosticReportId?: string;
  selectedDiagnosticCtaId?: string;
  crmAgentDiagnostic?: Record<string, string | undefined>;
  agentV2?: {
    macroState?: string;
    traceId?: string;
    productSourceVersion?: string;
    estimatedCostUsd?: number;
    priority?: string;
  };
  agentRuntime?: {
    currentAgent?: string;
    previousState?: string;
    currentState?: string;
    nextState?: string;
    route?: string;
    detectedIntents?: string;
    templateIds?: string;
    diagnosticLedgerStatus?: string;
    demoStatus?: string;
    demoNextStep?: string;
    finalPlanLine?: string;
    finalDemoLine?: string;
    crmBaseRecommendation?: string;
    agentRecommendations?: string;
    guardrailFlags?: string;
    waitlistIntentEvidence?: string;
    productSourceKeys?: string;
    latestProductFollowupIntent?: string;
    postDiagnosticContextUsed?: boolean;
    unsupportedFactRequested?: string;
    humanConfirmationOffered?: boolean;
    diagnosticRefusalRespected?: boolean;
    traceId?: string;
    runId?: string;
    productSourceVersion?: string;
    estimatedCostUsd?: number;
    productSourceWarning?: string;
  };
  aiPaused: boolean;
  externalSyncStatus: string;
  updatedAt: string;
};

type LeadDetail = LeadSummary & {
  qualification?: Record<string, string>;
  recentMessages?: Array<{ id: string; role: string; content: string; createdAt: string }>;
};

type AuditAction = {
  actionId: string;
  action: string;
  beforeStatus: string;
  afterStatus: string;
  createdAt: string;
};

const statuses = ["ai_active", "handoff_requested", "human_active", "waiting_customer", "follow_up_scheduled", "checkout_sent", "won", "lost", "do_not_contact"];
const channels = ["web", "whatsapp"];
const conversionPaths = [
  "cold_lead",
  "guided_demo",
  "view_plans",
  "plan_recommendation",
  "checkout_intent",
  "waitlist_intent",
  "analysis_request",
  "human_whatsapp_assist",
  "crm_agent_diagnostic",
  "custom_agent_follow_up",
  "custom_agent_diagnostic_mapped",
  "mixed_subscription_plus_custom",
  "custom_agent_diagnostic_unclear",
  "high_intent",
];
const actions = ["take_over", "send_plan_page", "send_checkout_link", "schedule_follow_up", "resume_ai", "mark_waiting_customer", "mark_won", "mark_lost", "mark_do_not_contact"];
const actionLabels: Record<string, string> = {
  send_whatsapp_message: "Enviar WhatsApp",
  take_over: "Assumir conversa",
  send_plan_page: "Enviar planos",
  send_checkout_link: "Enviar checkout",
  schedule_follow_up: "Agendar follow-up",
  resume_ai: "Retomar atendimento",
  mark_waiting_customer: "Aguardando cliente",
  mark_won: "Marcar ganho",
  mark_lost: "Marcar perdido",
  mark_do_not_contact: "Nao contatar",
};

export function SalesInboxClient({ token }: { token: string }) {
  const [leads, setLeads] = useState<LeadSummary[]>([]);
  const [selectedLeadId, setSelectedLeadId] = useState<string>();
  const [detail, setDetail] = useState<{ lead: LeadDetail; audit: AuditAction[] } | null>(null);
  const [statusFilter, setStatusFilter] = useState("");
  const [priorityFilter, setPriorityFilter] = useState("");
  const [channelFilter, setChannelFilter] = useState("");
  const [conversionPathFilter, setConversionPathFilter] = useState("");
  const [nextActionFilter, setNextActionFilter] = useState("");
  const [operatorMessage, setOperatorMessage] = useState("");
  const [loading, setLoading] = useState(true);
  const [notice, setNotice] = useState("");

  const selectedLead = useMemo(() => leads.find((lead) => lead.leadId === selectedLeadId) ?? leads[0], [leads, selectedLeadId]);

  const loadLeads = useCallback(async () => {
    setLoading(true);
    const params = new URLSearchParams();
    if (statusFilter) params.set("status", statusFilter);
    if (priorityFilter) params.set("priority", priorityFilter);
    if (channelFilter) params.set("channel", channelFilter);
    if (conversionPathFilter) params.set("conversionPath", conversionPathFilter);
    if (nextActionFilter) params.set("nextAction", nextActionFilter);
    const response = await fetch(`/api/internal/sales-inbox/leads?${params.toString()}`, {
      headers: { "x-internal-sales-token": token },
    });
    if (response.ok) {
      const payload = (await response.json()) as { leads: LeadSummary[] };
      setLeads(payload.leads);
      setSelectedLeadId((current) => current ?? payload.leads[0]?.leadId);
    } else {
      setNotice("Nao foi possivel carregar os leads.");
    }
    setLoading(false);
  }, [channelFilter, conversionPathFilter, nextActionFilter, priorityFilter, statusFilter, token]);

  const loadDetail = useCallback(async (leadId: string) => {
    const response = await fetch(`/api/internal/sales-inbox/leads/${leadId}`, {
      headers: { "x-internal-sales-token": token },
    });
    if (response.ok) setDetail((await response.json()) as { lead: LeadDetail; audit: AuditAction[] });
  }, [token]);

  useEffect(() => {
    const timeout = window.setTimeout(() => {
      void loadLeads();
    }, 0);
    return () => window.clearTimeout(timeout);
  }, [loadLeads]);

  useEffect(() => {
    if (!selectedLead?.leadId) return;
    const timeout = window.setTimeout(() => {
      void loadDetail(selectedLead.leadId);
    }, 0);
    return () => window.clearTimeout(timeout);
  }, [loadDetail, selectedLead?.leadId]);

  async function runAction(action: string) {
    if (!selectedLead?.leadId) return;
    const payload =
      action === "send_checkout_link"
        ? { planId: selectedLead.selectedPlanId ?? selectedLead.recommendedPlanId }
        : action === "send_whatsapp_message"
          ? { message: operatorMessage }
          : {};
    const response = await fetch(`/api/internal/sales-inbox/leads/${selectedLead.leadId}/actions`, {
      method: "POST",
      headers: {
        "x-internal-sales-token": token,
        "content-type": "application/json",
      },
      body: JSON.stringify({ action, payload }),
    });
    const result = (await response.json()) as { error?: string };
    setNotice(response.ok ? `Acao registrada: ${action}` : result.error ?? "Acao bloqueada.");
    if (response.ok && action === "send_whatsapp_message") setOperatorMessage("");
    await loadLeads();
    await loadDetail(selectedLead.leadId);
  }

  return (
    <main className="min-h-screen bg-[#F7F8FA] text-[#101828]">
      <header className="border-b border-[#E4E7EC] bg-white px-5 py-4">
        <div className="mx-auto flex max-w-7xl flex-col gap-3 md:flex-row md:items-center md:justify-between">
          <div>
            <p className="text-xs font-bold uppercase tracking-[0.18em] text-[#667085]">Taliya interno</p>
            <h1 className="text-2xl font-black tracking-[-0.03em]">Sales Inbox</h1>
          </div>
          <div className="flex flex-wrap gap-2">
            <select className="h-10 rounded-lg border border-[#D0D5DD] bg-white px-3 text-sm font-semibold" onChange={(event) => setStatusFilter(event.target.value)} value={statusFilter}>
              <option value="">Todos os status</option>
              {statuses.map((status) => (
                <option key={status} value={status}>{status}</option>
              ))}
            </select>
            <select className="h-10 rounded-lg border border-[#D0D5DD] bg-white px-3 text-sm font-semibold" onChange={(event) => setPriorityFilter(event.target.value)} value={priorityFilter}>
              <option value="">Todas prioridades</option>
              <option value="hot">hot</option>
              <option value="warm">warm</option>
              <option value="cold">cold</option>
              <option value="manual">manual</option>
            </select>
            <select className="h-10 rounded-lg border border-[#D0D5DD] bg-white px-3 text-sm font-semibold" onChange={(event) => setChannelFilter(event.target.value)} value={channelFilter}>
              <option value="">Todos canais</option>
              {channels.map((channel) => (
                <option key={channel} value={channel}>{channel}</option>
              ))}
            </select>
            <select className="h-10 rounded-lg border border-[#D0D5DD] bg-white px-3 text-sm font-semibold" onChange={(event) => setConversionPathFilter(event.target.value)} value={conversionPathFilter}>
              <option value="">Todos caminhos</option>
              {conversionPaths.map((path) => (
                <option key={path} value={path}>{path}</option>
              ))}
            </select>
            <input
              aria-label="Filtrar proxima acao"
              className="h-10 w-44 rounded-lg border border-[#D0D5DD] bg-white px-3 text-sm font-semibold"
              onChange={(event) => setNextActionFilter(event.target.value)}
              placeholder="Proxima acao"
              value={nextActionFilter}
            />
            <button className="h-10 rounded-lg bg-[#101828] px-4 text-sm font-black text-white" onClick={() => loadLeads()} type="button">Atualizar</button>
          </div>
        </div>
      </header>

      <div className="mx-auto grid max-w-7xl gap-4 px-5 py-5 lg:grid-cols-[420px_1fr]">
        <section className="rounded-xl border border-[#E4E7EC] bg-white">
          <div className="border-b border-[#E4E7EC] px-4 py-3">
            <p className="text-sm font-black">Leads</p>
            <p className="text-xs font-semibold text-[#667085]">{loading ? "Carregando..." : `${leads.length} registros`}</p>
          </div>
          <div className="max-h-[calc(100vh-190px)] overflow-auto">
            {leads.length ? leads.map((lead) => (
              <button
                className={`block w-full border-b border-[#F2F4F7] px-4 py-3 text-left transition hover:bg-[#F9FAFB] ${lead.leadId === selectedLead?.leadId ? "bg-[#EEF4FF]" : ""}`}
                key={lead.leadId}
                onClick={() => setSelectedLeadId(lead.leadId)}
                type="button"
              >
                <div className="flex items-center justify-between gap-2">
                  <p className="truncate text-sm font-black">{lead.contact.name ?? lead.contact.whatsapp ?? lead.leadId}</p>
                  <span className={`rounded-full px-2 py-1 text-[11px] font-black ${lead.priority === "manual" ? "bg-[#F4E8FF] text-[#6941C6]" : lead.priority === "hot" ? "bg-[#FEE4E2] text-[#B42318]" : lead.priority === "warm" ? "bg-[#FEF0C7] text-[#B54708]" : "bg-[#EAECF0] text-[#344054]"}`}>
                    {lead.priority}
                  </span>
                </div>
                <p className="mt-1 truncate text-xs font-semibold text-[#667085]">{lead.conversionPath} / {lead.readiness}</p>
                <p className="mt-1 truncate text-xs font-semibold text-[#667085]">
                  {lead.channel} / {lead.agentRuntime?.currentAgent ?? lead.agentV2?.macroState ?? lead.commercialStage ?? "sem runtime"}
                </p>
                <p className="mt-2 line-clamp-2 text-xs leading-5 text-[#475467]">{lead.summary}</p>
              </button>
            )) : (
              <div className="px-4 py-10 text-sm font-semibold text-[#667085]">Nenhum lead ainda.</div>
            )}
          </div>
        </section>

        <section className="rounded-xl border border-[#E4E7EC] bg-white">
          {detail?.lead ? (
            <div className="grid gap-5 p-5">
              <div className="flex flex-col gap-4 border-b border-[#E4E7EC] pb-5 lg:flex-row lg:items-start lg:justify-between">
                <div>
                  <p className="text-xs font-bold uppercase tracking-[0.16em] text-[#667085]">{detail.lead.channel} / {detail.lead.sourcePage}</p>
                  <h2 className="mt-1 text-2xl font-black">{detail.lead.contact.name ?? detail.lead.contact.whatsapp ?? detail.lead.leadId}</h2>
                  <p className="mt-1 text-xs font-bold uppercase tracking-[0.14em] text-[#667085]">Sync externo: {detail.lead.externalSyncStatus}</p>
                  <p className="mt-2 text-sm font-semibold text-[#667085]">{detail.lead.status} / {detail.lead.priority} / {detail.lead.readiness}</p>
                </div>
                <div className="flex flex-wrap gap-2">
                  {["send_whatsapp_message", ...actions].map((action) => (
                    <button className="h-9 rounded-lg border border-[#D0D5DD] bg-white px-3 text-xs font-black hover:bg-[#F9FAFB]" key={action} onClick={() => runAction(action)} type="button">
                      {actionLabels[action] ?? action}
                    </button>
                  ))}
                </div>
              </div>

              {notice ? <div className="rounded-lg border border-[#D0D5DD] bg-[#F9FAFB] px-4 py-3 text-sm font-bold text-[#344054]">{notice}</div> : null}

              <div className="rounded-lg border border-[#E4E7EC] bg-[#FCFCFD] p-4">
                <label className="text-xs font-black uppercase tracking-[0.14em] text-[#667085]" htmlFor="operator-whatsapp-message">Mensagem WhatsApp</label>
                <textarea
                  className="mt-2 min-h-24 w-full resize-none rounded-lg border border-[#D0D5DD] bg-white px-3 py-2 text-sm font-semibold text-[#344054]"
                  id="operator-whatsapp-message"
                  onChange={(event) => setOperatorMessage(event.target.value)}
                  placeholder="Escreva uma resposta curta para o lead..."
                  value={operatorMessage}
                />
              </div>

              <div className="grid gap-4 xl:grid-cols-3">
                <InfoBlock title="Resumo" value={detail.lead.summary} />
                <InfoBlock title="Proxima acao" value={detail.lead.nextAction} />
                <InfoBlock title="Contato" value={[detail.lead.contact.whatsapp, detail.lead.contact.email].filter(Boolean).join(" / ") || "Sem contato"} />
                <InfoBlock title="Etapa comercial" value={[detail.lead.commercialStage, detail.lead.primaryPainOrIntent].filter(Boolean).join(" / ") || "Nao informado"} />
                <InfoBlock title="Lista de espera" value={[detail.lead.waitlistStatus, detail.lead.waitlistOfferedAt, detail.lead.waitlistJoinedAt, detail.lead.missingWaitlistFields ? `faltando: ${detail.lead.missingWaitlistFields}` : undefined].filter(Boolean).join(" / ") || "Nao informado"} />
                <InfoBlock title="Controle humano" value={[detail.lead.aiPaused ? "IA pausada" : "IA ativa", detail.lead.humanActive ? "humano ativo" : undefined, detail.lead.closureState].filter(Boolean).join(" / ") || "Nao informado"} />
                <InfoBlock
                  title="Runtime oficial"
                  value={
                    detail.lead.agentRuntime
                      ? [
                          detail.lead.agentRuntime.currentAgent,
                          detail.lead.agentRuntime.route,
                          [detail.lead.agentRuntime.previousState, detail.lead.agentRuntime.currentState, detail.lead.agentRuntime.nextState].filter(Boolean).join(" > "),
                          detail.lead.agentRuntime.templateIds ? `templates: ${detail.lead.agentRuntime.templateIds}` : undefined,
                          detail.lead.agentRuntime.diagnosticLedgerStatus ? `ledger: ${detail.lead.agentRuntime.diagnosticLedgerStatus}` : undefined,
                          detail.lead.agentRuntime.demoStatus ? `demo runtime: ${detail.lead.agentRuntime.demoStatus}` : undefined,
                          detail.lead.agentRuntime.finalPlanLine ? `plano final: ${detail.lead.agentRuntime.finalPlanLine}` : undefined,
                          detail.lead.agentRuntime.finalDemoLine ? `demo final: ${detail.lead.agentRuntime.finalDemoLine}` : undefined,
                          detail.lead.agentRuntime.crmBaseRecommendation ? `base CRM: ${detail.lead.agentRuntime.crmBaseRecommendation}` : undefined,
                          detail.lead.agentRuntime.agentRecommendations ? `agentes: ${detail.lead.agentRuntime.agentRecommendations}` : undefined,
                          detail.lead.agentRuntime.detectedIntents ? `intencoes: ${detail.lead.agentRuntime.detectedIntents}` : undefined,
                          detail.lead.agentRuntime.latestProductFollowupIntent ? `follow-up produto: ${detail.lead.agentRuntime.latestProductFollowupIntent}` : undefined,
                          detail.lead.agentRuntime.productSourceKeys ? `fontes: ${detail.lead.agentRuntime.productSourceKeys}` : undefined,
                          typeof detail.lead.agentRuntime.postDiagnosticContextUsed === "boolean" ? `contexto pos-diagnostico: ${detail.lead.agentRuntime.postDiagnosticContextUsed ? "sim" : "nao"}` : undefined,
                          detail.lead.agentRuntime.unsupportedFactRequested ? `fato a confirmar: ${detail.lead.agentRuntime.unsupportedFactRequested}` : undefined,
                          typeof detail.lead.agentRuntime.humanConfirmationOffered === "boolean" ? `confirmacao humana: ${detail.lead.agentRuntime.humanConfirmationOffered ? "sim" : "nao"}` : undefined,
                          typeof detail.lead.agentRuntime.diagnosticRefusalRespected === "boolean" ? `recusa diagnostico respeitada: ${detail.lead.agentRuntime.diagnosticRefusalRespected ? "sim" : "nao"}` : undefined,
                          detail.lead.agentRuntime.waitlistIntentEvidence ? `waitlist: ${detail.lead.agentRuntime.waitlistIntentEvidence}` : undefined,
                          detail.lead.agentRuntime.guardrailFlags ? `flags: ${detail.lead.agentRuntime.guardrailFlags}` : undefined,
                          detail.lead.agentRuntime.productSourceVersion,
                          detail.lead.agentRuntime.productSourceWarning,
                          typeof detail.lead.agentRuntime.estimatedCostUsd === "number" ? `US$ ${detail.lead.agentRuntime.estimatedCostUsd.toFixed(4)}` : undefined,
                          detail.lead.agentRuntime.traceId,
                          detail.lead.agentRuntime.runId,
                        ].filter(Boolean).join(" / ")
                      : "Nao informado"
                  }
                />
                <InfoBlock
                  title="Agente v2"
                  value={
                    detail.lead.agentV2
                      ? [
                          detail.lead.agentV2.macroState,
                          detail.lead.agentV2.priority,
                          detail.lead.agentV2.productSourceVersion,
                          typeof detail.lead.agentV2.estimatedCostUsd === "number" ? `US$ ${detail.lead.agentV2.estimatedCostUsd.toFixed(4)}` : undefined,
                          detail.lead.agentV2.traceId,
                        ].filter(Boolean).join(" / ")
                      : "Nao informado"
                  }
                />
                <InfoBlock title="Demo" value={[detail.lead.demoStatus, detail.lead.demoOfferedAt, detail.lead.demoSeenAt].filter(Boolean).join(" / ") || "Nao informado"} />
                <InfoBlock title="Plano" value={detail.lead.selectedPlanId ?? detail.lead.recommendedPlanId} />
                <InfoBlock title="Origem" value={[detail.lead.sourceSection, detail.lead.sourcePage].filter(Boolean).join(" / ") || "Nao informado"} />
                <InfoBlock
                  title="Diagnostico sob medida"
                  value={
                    [
                      detail.lead.diagnosticReportId,
                      detail.lead.diagnosticClassification,
                      detail.lead.diagnosticContextVariant,
                      detail.lead.selectedDiagnosticCtaId,
                    ]
                      .filter(Boolean)
                      .join(" / ") || "Nao informado"
                  }
                />
                <InfoBlock
                  title="Diagnostico gratuito"
                  value={
                    detail.lead.crmAgentDiagnostic
                      ? [
                          detail.lead.crmAgentDiagnostic.studioSizeRange,
                          detail.lead.crmAgentDiagnostic.operationalPains,
                          detail.lead.crmAgentDiagnostic.recommendedCrmModules,
                          detail.lead.crmAgentDiagnostic.recommendedAgents,
                          detail.lead.crmAgentDiagnostic.recommendedPlan,
                          detail.lead.crmAgentDiagnostic.leadTemperature,
                        ]
                          .filter(Boolean)
                          .join(" / ")
                      : "Nao informado"
                  }
                />
                <InfoBlock title="Dores" value={detail.lead.selectedPainIds.join(", ") || detail.lead.primaryPainOrIntent || "Nao informado"} />
                <InfoBlock title="Agentes" value={detail.lead.recommendedAgentIds.join(", ") || "Nao informado"} />
              </div>

              <div>
                <h3 className="text-sm font-black">Auditoria</h3>
                <div className="mt-2 overflow-hidden rounded-lg border border-[#E4E7EC]">
                  {detail.audit.length ? detail.audit.map((item) => (
                    <div className="grid gap-1 border-b border-[#F2F4F7] px-4 py-3 text-sm md:grid-cols-[1fr_auto]" key={item.actionId}>
                      <span className="font-bold">{item.action}: {item.beforeStatus} -&gt; {item.afterStatus}</span>
                      <span className="text-xs font-semibold text-[#667085]">{new Date(item.createdAt).toLocaleString("pt-BR")}</span>
                    </div>
                  )) : <div className="px-4 py-4 text-sm font-semibold text-[#667085]">Sem acoes de operador.</div>}
                </div>
              </div>
            </div>
          ) : (
            <div className="p-10 text-sm font-semibold text-[#667085]">Selecione um lead para ver detalhes.</div>
          )}
        </section>
      </div>
    </main>
  );
}

function InfoBlock({ title, value }: { title: string; value: string }) {
  return (
    <div className="rounded-lg border border-[#E4E7EC] bg-[#FCFCFD] p-4">
      <p className="text-xs font-black uppercase tracking-[0.14em] text-[#667085]">{title}</p>
      <p className="mt-2 text-sm font-semibold leading-6 text-[#344054]">{value}</p>
    </div>
  );
}
