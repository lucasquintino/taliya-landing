# Contract: Product Knowledge Source

## Purpose

All commercial facts must come from this source or a controlled read path that returns this shape. The response generator must not rely on prompt-only memory for prices, plans, links, availability or promises.

## Shape

```ts
type ProductKnowledge = {
  version: string;
  updatedAt: string;
  brand: {
    name: "Taliya";
    category: "CRM SaaS para studios de Pilates";
  };
  plans: Array<{
    id: "base" | "essencial" | "avance" | "completo";
    name: string;
    priceMonthlyBrl: number;
    summary: string;
    includedRoutines: string[];
    limitations?: string[];
  }>;
  routines: Array<{
    id: string;
    name: string;
    painSignals: string[];
    practicalRole: string;
  }>;
  links: {
    landing: "https://www.taliya.com.br/pilates";
    plans: "https://www.taliya.com.br/pilates/planos";
    demonstration: "https://www.taliya.com.br/pilates/planos/demonstracao";
    privacy: "https://www.taliya.com.br/privacidade";
  };
  demo: {
    status: "available" | "guided_explanation_only" | "unavailable";
    message: string;
  };
  availability: {
    status: "limited_studios_waitlist";
    waitlistCopy: string;
  };
  commercialPolicies: {
    guaranteeCancellation?: string;
    unsupportedClaims: string[];
    noCheckoutWhileClosed: true;
  };
};
```

## Required Reads

Use product knowledge for:

- price
- plans
- plan comparison
- demo link/status
- landing/plans/demo/privacy links
- waitlist availability
- guarantee/cancelation if defined
- unsupported promises
- included routines/agents

## Failure Behavior

If source is unavailable:

- do not invent prices, plan contents, demo status or guarantees;
- answer only stable high-level context if safe;
- offer human follow-up for commercial specifics;
- log product-source failure in trace.

## Versioning

Every response that uses product facts must save `productSourceVersion` in the trace and eval transcript.
