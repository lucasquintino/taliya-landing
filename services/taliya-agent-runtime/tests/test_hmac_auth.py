from datetime import UTC, datetime, timedelta
import hmac

import pytest

from app.auth.hmac import (
    HMAC_HEADER_REQUEST_ID,
    HMAC_HEADER_SIGNATURE,
    HMAC_HEADER_TIMESTAMP,
    HmacAuthError,
    ReplayWindow,
    compute_signature,
    verify_hmac_headers,
)


def test_accepts_valid_hmac_signature():
    body = b'{"agent_key":"taliya_commercial"}'
    timestamp = "2026-05-22T12:00:00Z"
    secret = "test-secret"
    headers = {
        HMAC_HEADER_TIMESTAMP: timestamp,
        HMAC_HEADER_SIGNATURE: compute_signature(secret, timestamp, body),
        HMAC_HEADER_REQUEST_ID: "req_123",
    }

    result = verify_hmac_headers(
        body=body,
        headers=headers,
        secret=secret,
        now=datetime(2026, 5, 22, 12, 0, 10, tzinfo=UTC),
    )

    assert result.request_id == "req_123"
    assert hmac.compare_digest(result.signature, headers[HMAC_HEADER_SIGNATURE])


def test_rejects_stale_timestamp():
    body = b"{}"
    timestamp = "2026-05-22T12:00:00Z"
    secret = "test-secret"
    headers = {
        HMAC_HEADER_TIMESTAMP: timestamp,
        HMAC_HEADER_SIGNATURE: compute_signature(secret, timestamp, body),
        HMAC_HEADER_REQUEST_ID: "req_stale",
    }

    with pytest.raises(HmacAuthError) as exc:
        verify_hmac_headers(
            body=body,
            headers=headers,
            secret=secret,
            now=datetime(2026, 5, 22, 12, 10, 1, tzinfo=UTC),
            max_skew=timedelta(seconds=300),
        )

    assert exc.value.code == "stale_timestamp"


def test_rejects_invalid_signature():
    body = b'{"agent_key":"taliya_commercial"}'
    headers = {
        HMAC_HEADER_TIMESTAMP: "2026-05-22T12:00:00Z",
        HMAC_HEADER_SIGNATURE: "00" * 32,
        HMAC_HEADER_REQUEST_ID: "req_bad",
    }

    with pytest.raises(HmacAuthError) as exc:
        verify_hmac_headers(
            body=body,
            headers=headers,
            secret="test-secret",
            now=datetime(2026, 5, 22, 12, 0, 0, tzinfo=UTC),
        )

    assert exc.value.code == "invalid_signature"


def test_replay_window_tracks_duplicate_request_ids():
    window = ReplayWindow(ttl_seconds=300)
    now = datetime(2026, 5, 22, 12, 0, 0, tzinfo=UTC)

    assert window.check_and_store("req_1", now=now) is True
    assert window.check_and_store("req_1", now=now + timedelta(seconds=30)) is False
    assert window.check_and_store("req_1", now=now + timedelta(seconds=301)) is True
