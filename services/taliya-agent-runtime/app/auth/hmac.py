from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
import hashlib
import hmac

HMAC_HEADER_TIMESTAMP = "X-Taliya-Agent-Timestamp"
HMAC_HEADER_SIGNATURE = "X-Taliya-Agent-Signature"
HMAC_HEADER_REQUEST_ID = "X-Taliya-Agent-Request-Id"


class HmacAuthError(Exception):
    def __init__(self, code: str, message: str) -> None:
        self.code = code
        self.message = message
        super().__init__(message)


@dataclass(frozen=True)
class VerifiedHmacRequest:
    request_id: str
    timestamp: datetime
    signature: str


def compute_signature(secret: str, timestamp: str, body: bytes) -> str:
    payload = timestamp.encode("utf-8") + b"." + body
    return hmac.new(secret.encode("utf-8"), payload, hashlib.sha256).hexdigest()


def _header(headers: dict[str, str], name: str) -> str | None:
    if name in headers:
        return headers[name]
    lowered = {key.lower(): value for key, value in headers.items()}
    return lowered.get(name.lower())


def _parse_timestamp(value: str) -> datetime:
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise HmacAuthError("stale_timestamp", "Request timestamp is malformed.") from exc
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=UTC)
    return parsed.astimezone(UTC)


def verify_hmac_headers(
    *,
    body: bytes,
    headers: dict[str, str],
    secret: str,
    now: datetime | None = None,
    max_skew: timedelta = timedelta(seconds=300),
) -> VerifiedHmacRequest:
    timestamp = _header(headers, HMAC_HEADER_TIMESTAMP)
    signature = _header(headers, HMAC_HEADER_SIGNATURE)
    request_id = _header(headers, HMAC_HEADER_REQUEST_ID)

    if not timestamp or not signature or not request_id:
        raise HmacAuthError("invalid_signature", "Required HMAC headers are missing.")

    parsed_timestamp = _parse_timestamp(timestamp)
    current = (now or datetime.now(UTC)).astimezone(UTC)
    if abs(current - parsed_timestamp) > max_skew:
        raise HmacAuthError("stale_timestamp", "Request timestamp is outside the allowed window.")

    expected = compute_signature(secret, timestamp, body)
    if not hmac.compare_digest(expected, signature):
        raise HmacAuthError("invalid_signature", "Request signature is invalid.")

    return VerifiedHmacRequest(
        request_id=request_id,
        timestamp=parsed_timestamp,
        signature=signature,
    )


class ReplayWindow:
    def __init__(self, ttl_seconds: int) -> None:
        self.ttl = timedelta(seconds=ttl_seconds)
        self._seen: dict[str, datetime] = {}

    def check_and_store(self, request_id: str, *, now: datetime | None = None) -> bool:
        current = (now or datetime.now(UTC)).astimezone(UTC)
        expired = [key for key, seen_at in self._seen.items() if current - seen_at > self.ttl]
        for key in expired:
            self._seen.pop(key, None)

        seen_at = self._seen.get(request_id)
        if seen_at is not None and current - seen_at <= self.ttl:
            return False

        self._seen[request_id] = current
        return True
