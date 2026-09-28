# Privacy, LGPD And Consent Requirements: Landing

## Purpose

Define privacy and consent requirements for the public landing, plan CTAs, assisted-conversion forms and WhatsApp assistance links.

This is a product/engineering checklist, not legal advice. Final public policy text should be reviewed before launch.

## Requirements

- The landing must link to a privacy notice/policy before collecting contact details.
- Assisted-conversion forms must state why data is collected: analysis, plan guidance, human assistance or custom-agent follow-up.
- Forms must collect only necessary fields for the selected conversion path.
- Marketing forms must not collect card data, payment credentials, billing documents or sensitive student health details.
- WhatsApp assistance CTAs must make clear that the visitor is choosing to continue by WhatsApp.
- Tracking should avoid storing full raw message/form text when structured metadata is enough.
- Any cookie/analytics banner added later must not be blocked by the floating agent or sticky CTAs.
- The system must support deletion or suppression of assisted-conversion records when required by policy/process.
- Public copy must not imply hidden monitoring of the visitor.

## Minimum Public UI Copy Requirements

Forms should include short consent/help text near submission:

```text
Ao enviar, voce concorda que a gente use esses dados para responder sua solicitacao sobre o sistema e orientar o melhor proximo passo.
```

When WhatsApp is used:

```text
Ao continuar pelo WhatsApp, voce autoriza nosso contato sobre sua solicitacao.
```

## Data Minimization

Required fields should stay limited to:

- name
- WhatsApp or email when follow-up is requested
- studio name
- city/state
- active student range
- biggest pain
- current system usage
- preferred next step

Avoid:

- exact student records
- clinical/health details
- payment credentials
- full billing documents
- unnecessary personal details about students

## Acceptance Criteria

- Public form shows privacy/consent helper text.
- Privacy link is reachable from landing footer or form area.
- Form payload includes conversion purpose/context.
- No visible form asks for sensitive student data or payment data.
- WhatsApp CTA includes intentional-contact framing.
