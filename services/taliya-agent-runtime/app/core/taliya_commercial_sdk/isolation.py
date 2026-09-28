from __future__ import annotations

PAID_OPENAI_CALLS_APPROVED = False
PUBLIC_CUTOVER_ENABLED = False


class SdkSpikePaidCallBlocked(RuntimeError):
    """Raised when the isolated spike is asked to run a paid OpenAI call."""


class SdkSpikeCutoverBlocked(RuntimeError):
    """Raised if spike code is accidentally treated as a public cutover path."""


def require_paid_approval(*, approved: bool = PAID_OPENAI_CALLS_APPROVED) -> None:
    """Block real OpenAI SDK calls until the paid spike packet is approved."""

    if not approved:
        raise SdkSpikePaidCallBlocked(
            "Spec 012 paid SDK calls are blocked until mocked/no-cost tests pass "
            "and the user explicitly approves a paid spike budget."
        )


def assert_public_cutover_disabled() -> None:
    """Keep T012-020 isolated from the public Taliya commercial endpoint."""

    if PUBLIC_CUTOVER_ENABLED:
        raise SdkSpikeCutoverBlocked(
            "Spec 012 SDK spike cannot be used as a public cutover path in T012-020."
        )
