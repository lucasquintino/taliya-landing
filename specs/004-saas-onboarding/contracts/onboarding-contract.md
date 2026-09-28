# Onboarding Contract

## Start Onboarding

Route:

```text
GET /onboarding
```

Rules:

- Requires authenticated user.
- Requires active paid entitlement.
- Trial entitlement is not accepted in v1.
- Creates or resumes onboarding for the user's tenant.

## Save Studio Profile

Route:

```text
POST /api/onboarding/studio-profile
```

Input:

```json
{
  "studioName": "Studio Exemplo",
  "cityState": "Sao Paulo/SP",
  "contactWhatsApp": "+55 11 99999-9999",
  "activeStudentsRange": "51-100",
  "scheduleModel": "turmas e particulares",
  "currentSystem": "planilha",
  "biggestPains": ["reposicoes", "faltas"]
}
```

Rules:

- Authenticated membership required.
- Saves data only for verified tenant.

## Save Agent Configuration

Route:

```text
POST /api/onboarding/agent-config
```

Rules:

- Agent must be included in entitlement.
- Tenant ID must be verified through membership.
- Changes are audited for sensitive fields.

## Finish Onboarding

Route:

```text
POST /api/onboarding/finish
```

Rules:

- Required steps must be complete.
- Creates first-run checklist.
- Redirects to workspace.
