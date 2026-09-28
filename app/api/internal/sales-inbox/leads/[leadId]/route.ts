import { deleteSalesLeadThread, getSalesLead, listOperatorActions } from "@/lib/landing/ai-attendant/sales-inbox-store";
import { requireSalesInboxAuth } from "../../auth";

export async function GET(
  request: Request,
  {
    params,
  }: {
    params: Promise<{ leadId: string }>;
  },
) {
  const auth = requireSalesInboxAuth(request);
  if (!auth.ok) return auth.response;

  const { leadId } = await params;
  const lead = await getSalesLead(leadId);
  if (!lead) return Response.json({ error: "Lead not found." }, { status: 404 });

  return Response.json({
    lead,
    audit: await listOperatorActions(leadId),
  });
}

export async function DELETE(
  request: Request,
  {
    params,
  }: {
    params: Promise<{ leadId: string }>;
  },
) {
  const auth = requireSalesInboxAuth(request);
  if (!auth.ok) return auth.response;

  const { leadId } = await params;
  const deleted = await deleteSalesLeadThread(leadId);
  if (!deleted) return Response.json({ error: "Lead not found." }, { status: 404 });

  return Response.json({
    deleted,
  });
}
