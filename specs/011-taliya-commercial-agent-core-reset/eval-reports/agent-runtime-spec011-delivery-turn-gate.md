# agent-runtime-spec011-delivery-turn-gate

Generated at: 2026-05-31T16:09:45.321Z
Release gate: pass
Passed: 7/7

## PASS RC-011-010 duplicate inbound/provider messages are ignored before runtime execution

```json
{
  "hasProviderDuplicate": true,
  "hasDuplicateStatus": true,
  "hasSemanticDuplicateStatus": true
}
```

## PASS RC-011-010 outbound chunk delivery uses idempotency reservation

```json
{
  "hasOutboxConflictProtection": true,
  "hasBatchIdempotencyKey": true
}
```

## PASS RC-011-011 inbound during an active turn is queued/deferred instead of processed in parallel

```json
{
  "enqueueIndex": 13381,
  "lockIndex": 14109,
  "queuedReturnIndex": 14509,
  "deferredDrainIndex": 14222
}
```

## PASS RC-011-011 current outbound delivery is marked after send sequence finishes

```json
{
  "sendIndex": 21881,
  "markProcessedIndex": 23097
}
```

## PASS RC-011-011 deferred inbound must be processed as the next clean turn without delivery-interleaving semantic metadata

```json
{
  "routeDeliveryMetadataHits": []
}
```

## PASS RC-011-011 active Taliya commercial path is quarantined from legacy runner interleaving classifiers

```json
{
  "runtimeClientUsesSpec011Endpoint": true,
  "runtimeClientLegacyTurnHits": [],
  "runtimeApiLegacyQuarantineHits": [
    {
      "line": 231,
      "text": "\"legacy_commercial_runner_quarantined\","
    }
  ],
  "runtimeApiRunnerImportHits": []
}
```

## PASS RC-011-011 delivery layer must not use text-specific social acknowledgement shortcuts

```json
{
  "routeSemanticAckHits": []
}
```
