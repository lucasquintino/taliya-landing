export function requireSalesInboxAuth(request: Request) {
  const expectedToken = process.env.INTERNAL_SALES_INBOX_TOKEN;
  if (!expectedToken) {
    return {
      ok: false as const,
      response: Response.json({ error: "Sales Inbox token is not configured." }, { status: 503 }),
    };
  }

  const authorization = request.headers.get("authorization");
  const bearer = authorization?.startsWith("Bearer ") ? authorization.slice("Bearer ".length).trim() : undefined;
  const headerToken = request.headers.get("x-internal-sales-token") ?? undefined;
  const token = bearer ?? headerToken;

  if (token !== expectedToken) {
    return {
      ok: false as const,
      response: Response.json({ error: "Unauthorized." }, { status: 401 }),
    };
  }

  return { ok: true as const, actorUserId: request.headers.get("x-operator-id") ?? "internal_operator" };
}
