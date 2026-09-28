# WhatsApp Coexistence Platform Audit - Taliya

Date: 2026-05-15

## Objective

Find Dualhook-like options for:

- Taliya's own WhatsApp Business App number.
- AI lead-capture agent running over official WhatsApp API.
- Same phone number kept active in WhatsApp Business App.
- Coexistence, webhooks, and API.
- Lowest possible recurring cost.
- No third-party inbox/CRM becoming the main product surface.

## Core Finding

The market splits into four categories:

1. **Thin coexistence layer**: best fit, but usually monthly.
2. **Inbox/marketing platform with coexistence**: works, but product surface competes with Taliya.
3. **Self-hosted/lifetime platform**: can avoid monthly vendor fees, but still costs infra, setup, and may require Meta approval or a BSP.
4. **Unofficial QR/Web automation**: cheap or free, but not official and creates ban/stability risk.

For the exact requirement "official coexistence + same number + no monthly fee", there is no clean public winner.

## Strongest Candidates

| Rank | Platform | Fit | Pricing signal | Main risk | Verdict |
| --- | --- | --- | --- | --- | --- |
| 1 | Dualhook | Thin layer, direct webhook, no inbox | $12/mo for 1 connection; $115/mo Platform for SaaS | Monthly fee | Best product fit, not best cost |
| 2 | WANotifier | Coexistence + 0% markup + free/trial-ish plan | Public pricing shows ₹0/mo tiers + Meta fees, but free plan stopped for new users after 2025-10-27 | Platform/inbox; India-oriented; unclear Brazil/payment | Best "maybe cheap" lead |
| 3 | WATI Pay-as-you-go | Coexistence + no monthly fee claim | ₹999 includes 500 messages; top-up model | Platform/inbox; campaign-oriented; unclear API/webhook direct fit | Worth testing if signup accepts Brazil |
| 4 | ZPRO by ZDG | Brazil, self-hosted, annual license, official API/coexistence claim | R$1.997/year own use; R$2.797/year reseller | Heavy inbox/SaaS platform; annual upfront; implementation burden | Best Brazilian no-monthly-ish path |
| 5 | Waplify | Lifetime plan + API/webhook + 0% markup | ₹24.999 lifetime | Coexistence not clearly proven; India-focused | Ask only if they confirm coexistence |
| 6 | Whats91 | Coexistence guide, Meta Partner, zero markup claims | "Start free"; pricing page focuses Meta rates | India-focused; platform fee unclear; Brazil support needs proof | Interesting, but needs validation |
| 7 | OpenBSP | Open-source/self-hosted, multi-tenant, AI-agent ready | No vendor monthly fee; infra only | Requires your own Meta app/approval; not shortcut for coexistence now | Strategic long-term path |
| 8 | Callbell | Documented coexistence | Paid support/inbox platform | CRM/inbox first; not thin layer | Good reference, not Taliya fit |
| 9 | Whautomate/WhautoChat | Coexistence docs, AI automation | Whautomate starts S$74.5/mo promo; WhautoChat has separate self-hosted claims | Platform/inbox; not cheap enough | Not priority |
| 10 | WhatChimp | Coexistence + AI + 0% markup | ~$40/mo basic; free/trial references | Platform/inbox; forum promotion signals | Backup only |

## Platform Notes

### Dualhook

Best fit for the Taliya architecture.

Public evidence:

- Official coexistence positioning: WhatsApp Business App and Cloud API on the same number.
- Direct webhook delivery via Webhook Override.
- No message storage and no inbox.
- Developer plan is $12/month with 30-day trial.
- Platform plan is $115/month, 25 connections included, +$4.50 per extra connection.
- Meta message fees are separate; Dualhook says it does not charge per message.

Why it matters:

- It is the closest to "infrastructure layer, not CRM".
- It solves the exact "agent in Taliya WhatsApp while keeping app on phone" use case.

Why it hurts:

- The user explicitly does not want monthly fees.

### WANotifier

Very interesting because it publicly says:

- Official WhatsApp Business API access.
- 0% markup.
- WhatsApp coexistence.
- Messaging API and webhooks on higher tier.
- It used to have a free plan, but says new users after 2025-10-27 only get a 7-day trial.

Risk:

- Looks like a marketing/CRM/inbox product, not a thin routing layer.
- Pricing is in INR/contact tiers and Brazil support is not obvious.
- API/webhook directness must be tested.

### WATI

The coexistence page is unusually interesting for cost:

- Same number in WhatsApp Business App + Wati Cloud API features.
- "Pay as you go" positioning for occasional campaigns.
- Public copy says pay ₹999 and get 500 messages, with "no monthly fees".

Risk:

- It is explicitly a Wati inbox/platform.
- The pay-as-you-go plan may be campaign/broadcast oriented, not general webhook/API for Taliya's agent.
- It may not allow invisible CRM usage.

### ZPRO / ZDG

Brazilian, annual/self-hosted route.

Public evidence:

- Claims WhatsApp Official API via embedded login with coexistence mode.
- Supports API and webhooks.
- Self-hosted and white-label.
- R$1.997/year own use, R$2.797/year reseller.

Why it matters:

- It avoids monthly vendor subscription psychology, but becomes annual license + VPS.
- It may be the cheapest Brazilian path if Taliya can tolerate owning an inbox platform.

Risk:

- It is a full multi-attendance product, not a thin layer.
- Need to confirm whether official API/coexistence works without paying a separate BSP.
- It may be too much product overlap with Taliya.

### Waplify

Interesting for no monthly:

- Lifetime plan.
- API and webhook access.
- 0% commission and direct Meta charges.
- ₹24.999 lifetime.

Risk:

- The public pricing page does not clearly prove WhatsApp Business App coexistence.
- Could be standard Cloud API only.
- India-oriented.

### Whats91

Interesting because it has a detailed coexistence guide:

- Mentions bidirectional sync and `smb_message_echoes`.
- Says Brazil is supported in regional availability.
- Claims zero markup and direct Meta rates on pricing page.

Risk:

- Pricing page is India-specific.
- Platform fee is unclear.
- Needs proof that signup/onboarding accepts Brazilian businesses/numbers.

### OpenBSP

Best long-term technical artifact, not an immediate provider replacement.

Public evidence:

- Open-source WhatsApp Business Platform.
- Self-hostable, multi-tenant, AI-agent ready.
- Mentions coexistence through Embedded Signup.
- Supports webhook fields including `smb_message_echoes`, `history`, and `smb_app_state_sync`.

Why it matters:

- Excellent reference implementation for Taliya's future direct-Meta architecture.
- Could become the base of our own WhatsApp module.

Why it does not solve "now":

- It still needs a Meta app, permissions, and coexistence approval.
- It is not a reviewed Tech Provider on our behalf.

## Forum Intelligence

### Repeated pain points

People repeatedly ask for:

- Same number in WhatsApp Business App and Cloud API.
- Manual replies on phone plus chatbot/API.
- No CRM/inbox, only coexistence and webhook.
- No monthly fee.
- No risk of losing the main number.

### Important Reddit signals

- A thread from 2026-04 says if a number is added to Cloud API first, then trying to do coexistence later can fail. The safer sequence is Business App first, coexistence onboarding second.
- Another 2026 thread says own-number coexistence under the same Business Portfolio can be blocked by Embedded Signup, even for Tech Providers.
- Multiple users say coexistence is real but not stable/simple, with bugs such as pairing errors, webhook gaps, and `PARTNER_REMOVED`.
- A Brazilian brdev thread strongly complains about official API bureaucracy, token breakage, template reclassification, and hidden business rules. It also notes coexistence was added recently.
- Several forum replies push QR/session automation as cheaper, but that is not official and should not be used for Taliya's core acquisition number unless we accept account-risk.

### Practical lessons from forums

- Do not experiment on the main WhatsApp number until the provider/path is known.
- Do not migrate the number into normal Cloud API if the goal is coexistence.
- The number should already be active in WhatsApp Business App before coexistence.
- Keep the Business App active/open periodically.
- Watch for missed `smb_message_echoes`; app-side messages may not always mirror cleanly.
- Avoid marketing-like broadcast behavior from the same number while testing coexistence.

## Rejected Or Low-Priority Categories

### QR / WhatsApp Web Automation

Examples: Evolution API Baileys mode, WPPConnect, WAHA, Z-API-like tools.

Pros:

- Cheap or self-hosted.
- No Meta fees/templates.
- Keeps app-like behavior.

Cons:

- Not official WhatsApp Business Platform.
- Ban/stability risk.
- Protocol can break.
- Bad foundation for Taliya's brand and future SaaS product.

Use only for internal experiments or disposable numbers, not the main acquisition number.

### Full inbox products

Examples: Callbell, WATI, WhatChimp, Whautomate, WaliChat, Zenvia, Huggy, Blip.

They may solve coexistence, but they pull usage into their product.

For Taliya, they are acceptable only if:

- API/webhook can be used without operating their inbox.
- Costs are low enough.
- We can keep Taliya as the primary experience.

## Cost Reality

Even with a "free" provider, official API costs still exist:

- Provider/platform fee, unless waived.
- Meta message/template fees.
- Infrastructure if self-hosted.
- App Review/approval time if going direct Meta.

There is no evidence of a reliable provider that gives all of this for free:

- Official coexistence.
- Same number.
- Webhook/API.
- No inbox.
- No monthly fee.
- Brazil supported.

## Recommended Next Tests

### Test 1: WANotifier

Why:

- Publicly says ₹0/mo tiers, coexistence, 0% markup, API/webhooks.

Test:

- Try signup.
- Check if Brazil number/business is accepted.
- Check whether API/webhooks are available without paid upgrade.
- Check if it can avoid their inbox.

### Test 2: WATI Pay-as-you-go

Why:

- Public coexistence page says no monthly fees for occasional usage.

Test:

- Confirm if Brazil can use the pay-as-you-go coexistence plan.
- Confirm if webhook/API is available.
- Confirm if agent can run from Taliya backend, not WATI bot.

### Test 3: ZPRO Demo

Why:

- Brazilian, no monthly per number/user/message, annual license, official API/coexistence claim.

Test:

- Ask for demo access.
- Confirm exact official coexistence flow.
- Confirm if it can route webhooks to Taliya.
- Confirm if any separate BSP/Meta provider fee is required.

### Test 4: Waplify Lifetime

Why:

- Lifetime cost and API/webhook access.

Test:

- Ask directly: "Do you support WhatsApp Business App + Cloud API coexistence for an existing Business App number in Brazil?"

### Test 5: OpenBSP Lab

Why:

- Long-term direct-Meta architecture.

Test:

- Run hosted/self-hosted demo with Meta test number.
- Inspect how they model accounts, conversations, agents, and `smb_message_echoes`.
- Use as reference for Taliya's future native provider.

## Current Recommendation

If the hard constraint is **no monthly subscription**, the best realistic paths are:

1. **Try WANotifier/WATI pay-as-you-go** and see if they actually allow Brazil + API/webhook.
2. **Evaluate ZPRO** as Brazilian annual/self-hosted option.
3. **Use Meta test number + OpenBSP/direct Cloud API** while preparing MEI/CNPJ and Meta App Review.

If the hard constraint softens to **lowest monthly for official thin layer**, Dualhook remains the cleanest architecture.

If the hard constraint is **zero recurring and immediate coexistence**, no audited option currently satisfies all requirements cleanly.

