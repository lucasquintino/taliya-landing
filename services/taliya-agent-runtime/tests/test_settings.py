from app.settings import RuntimeSettings, RuntimeSettingsError, validate_production_settings


def test_local_settings_allow_mock_and_dev_secret():
    settings = RuntimeSettings(
        TALIYA_AGENT_RUNTIME_ENV="local",
        TALIYA_AGENT_PROVIDER="mock",
        TALIYA_AGENT_RUNTIME_HMAC_SECRET="dev-secret",
    )

    validate_production_settings(settings)
    assert settings.simple_opening_triage_enabled is True


def test_production_settings_reject_mock_provider_and_missing_secrets():
    settings = RuntimeSettings(
        TALIYA_AGENT_RUNTIME_ENV="production",
        TALIYA_AGENT_PROVIDER="mock",
        TALIYA_AGENT_RUNTIME_HMAC_SECRET="dev-secret",
        TALIYA_AGENT_MODEL="gpt-5.4-mini",
    )

    try:
        validate_production_settings(settings)
    except RuntimeSettingsError as exc:
        errors = "\n".join(exc.errors)
    else:  # pragma: no cover - defensive assertion
        raise AssertionError("production settings should fail")

    assert "TALIYA_AGENT_PROVIDER must be openai" in errors
    assert "OPENAI_API_KEY is required" in errors
    assert "DATABASE_URL is required" in errors
    assert "HMAC_SECRET must be a non-default production secret" in errors


def test_production_settings_accept_complete_openai_config():
    settings = RuntimeSettings(
        TALIYA_AGENT_RUNTIME_ENV="production",
        TALIYA_AGENT_PROVIDER="openai",
        OPENAI_API_KEY="sk-test",
        DATABASE_URL="postgres://user:pass@example.com:5432/db",
        TALIYA_AGENT_RUNTIME_HMAC_SECRET="production-secret-with-enough-length",
        TALIYA_AGENT_MODEL="gpt-5.4-mini",
    )

    validate_production_settings(settings)
