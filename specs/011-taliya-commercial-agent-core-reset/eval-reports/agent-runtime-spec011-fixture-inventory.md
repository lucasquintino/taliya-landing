# agent-runtime-spec011-fixture-inventory

Release gate: pass
Paid OpenAI spend: US$0
Passed: 8/8

## PASS fixtures have unique scenario ids

```json
{
  "goldenDuplicates": [],
  "doNotDoDuplicates": []
}
```

## PASS golden fixtures use the expected versioned schema

```json
{
  "schemaVersions": [
    "011.golden_transcript.v1"
  ]
}
```

## PASS do-not-do fixtures use the expected versioned schema

```json
{
  "schemaVersions": [
    "011.do_not_do_runtime.v1"
  ]
}
```

## PASS regression-case IDs are unique

```json
{
  "duplicateRegressionCaseIds": [],
  "count": 79
}
```

## PASS fixture case references exist in regression-cases.md

```json
{
  "referencedCaseIds": [
    "RC-011-048",
    "RC-011-052",
    "RC-011-053",
    "RC-011-053A",
    "RC-011-054",
    "RC-011-055",
    "RC-011-056",
    "RC-011-057",
    "RC-011-058",
    "RC-011-059",
    "RC-011-060",
    "RC-011-061",
    "RC-011-062",
    "RC-011-063",
    "RC-011-064",
    "RC-011-065",
    "RC-011-066",
    "RC-011-067"
  ],
  "missing": []
}
```

## PASS golden fixture covers all required T011-019 flow categories

```json
{
  "requiredGolden": [
    [
      "price",
      "final-price-first"
    ],
    [
      "price_plus_pain",
      "final-price-plus-pain"
    ],
    [
      "pain_first",
      "final-pain-first"
    ],
    [
      "instagram_source",
      "final-instagram-interest"
    ],
    [
      "whatsapp_product",
      "final-whatsapp-question"
    ],
    [
      "diagnostic_and_long_conversation",
      "step3g-long-conversation"
    ],
    [
      "waitlist",
      "final-waitlist-joined"
    ],
    [
      "human_handoff",
      "final-human-request-silent-after"
    ],
    [
      "product_demo",
      "final-demo-request"
    ]
  ],
  "missing": [],
  "count": 9
}
```

## PASS do-not-do fixture covers all required T011-019A forbidden-behavior categories

```json
{
  "requiredDoNotDo": [
    [
      "early_phone_capture",
      "do-not-do-early-phone-capture"
    ],
    [
      "invented_checkout",
      "final-checkout-buy-intent"
    ],
    [
      "invented_date_vip_discount",
      "do-not-do-date-vip-discount"
    ],
    [
      "invented_integrations",
      "product-delta-integration-scope"
    ],
    [
      "invented_certifications_security",
      "product-delta-security-data"
    ],
    [
      "client_studio_whatsapp_capture",
      "do-not-do-client-studio-whatsapp-capture"
    ],
    [
      "wrong_student_language",
      "do-not-do-wrong-student-language"
    ],
    [
      "price_497_not_student_count",
      "spec011-rc003-price-497-not-student-count"
    ]
  ],
  "missing": [],
  "count": 8
}
```

## PASS pain-first golden explicitly blocks translated English feedback leaks

```json
{
  "painFirstMustNot": [
    "lead loses",
    "interested leads",
    "team takes too long",
    "clientes",
    "consumidores"
  ]
}
```
