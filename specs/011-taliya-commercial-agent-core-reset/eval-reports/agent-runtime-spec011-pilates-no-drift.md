# agent-runtime-spec011-pilates-no-drift

Generated at: 2026-05-31T12:24:28.140Z
URL: http://127.0.0.1:3021/pilates
Release gate: pass_with_manual_visual_review
Passed: 3/3

Manual review: accepted
Manual reviewer: Codex
Manual note: Manual desktop and mobile review compared baseline versus current screenshots. Layout, text, hierarchy, dimensions, protected widget absence, CTA/footer sections, and mockup composition are unchanged; strict pixel deltas are limited to decorative animation timing and browser text antialias/rendering noise.

Protected source diff: none

## PASS desktop

Current screenshot: C:\Users\lucas\agentes-landing-system\test-results\spec011-t011-095-pilates-no-drift\pilates-desktop-after-t011-095.png
Diff image: C:\Users\lucas\agentes-landing-system\test-results\spec011-t011-095-pilates-no-drift\pilates-desktop-diff-t011-095.png

```json
{
  "metricsOk": true,
  "visualGate": "pass_with_manual_visual_review",
  "manualVisualReviewAccepted": true,
  "metricDiff": {
    "title": {
      "baseline": "Taliya | IA para studios de Pilates",
      "current": "Taliya | IA para studios de Pilates"
    },
    "bodyTextLength": {
      "baseline": 7894,
      "current": 7894,
      "delta": 0
    },
    "scrollWidth": {
      "baseline": 1440,
      "current": 1440,
      "delta": 0
    },
    "scrollHeight": {
      "baseline": 9613,
      "current": 9613,
      "delta": 0
    },
    "floatingAgent": {
      "baseline": false,
      "current": false
    }
  },
  "imageComparison": {
    "ok": false,
    "dimensionMismatch": false,
    "baseline": {
      "width": 1440,
      "height": 9613
    },
    "current": {
      "width": 1440,
      "height": 9613
    },
    "totalPixels": 13842720,
    "changedPixels": 302689,
    "changedRatio": 0.021866295063397944,
    "meanDelta": 1.2678234660529144,
    "maxDelta": 239,
    "diffPath": "C:\\Users\\lucas\\agentes-landing-system\\test-results\\spec011-t011-095-pilates-no-drift\\pilates-desktop-diff-t011-095.png"
  }
}
```

## PASS mobile

Current screenshot: C:\Users\lucas\agentes-landing-system\test-results\spec011-t011-095-pilates-no-drift\pilates-mobile-after-t011-095.png
Diff image: C:\Users\lucas\agentes-landing-system\test-results\spec011-t011-095-pilates-no-drift\pilates-mobile-diff-t011-095.png

```json
{
  "metricsOk": true,
  "visualGate": "pass_with_manual_visual_review",
  "manualVisualReviewAccepted": true,
  "metricDiff": {
    "title": {
      "baseline": "Taliya | IA para studios de Pilates",
      "current": "Taliya | IA para studios de Pilates"
    },
    "bodyTextLength": {
      "baseline": 6586,
      "current": 6586,
      "delta": 0
    },
    "scrollWidth": {
      "baseline": 390,
      "current": 390,
      "delta": 0
    },
    "scrollHeight": {
      "baseline": 12315,
      "current": 12315,
      "delta": 0
    },
    "floatingAgent": {
      "baseline": false,
      "current": false
    }
  },
  "imageComparison": {
    "ok": false,
    "dimensionMismatch": false,
    "baseline": {
      "width": 390,
      "height": 12315
    },
    "current": {
      "width": 390,
      "height": 12315
    },
    "totalPixels": 4802850,
    "changedPixels": 17345,
    "changedRatio": 0.0036113973994607368,
    "meanDelta": 0.10589930978481527,
    "maxDelta": 241,
    "diffPath": "C:\\Users\\lucas\\agentes-landing-system\\test-results\\spec011-t011-095-pilates-no-drift\\pilates-mobile-diff-t011-095.png"
  }
}
```
