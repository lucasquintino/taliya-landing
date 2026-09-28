from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class RuntimeSettingsError(ValueError):
    def __init__(self, errors: list[str]) -> None:
        super().__init__("; ".join(errors))
        self.errors = errors


class RuntimeSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    environment: str = Field("local", alias="TALIYA_AGENT_RUNTIME_ENV")
    hmac_secret: str = Field("dev-secret", alias="TALIYA_AGENT_RUNTIME_HMAC_SECRET")
    hmac_max_skew_seconds: int = Field(300, alias="TALIYA_AGENT_RUNTIME_HMAC_MAX_SKEW_SECONDS")
    provider: str = Field("mock", alias="TALIYA_AGENT_PROVIDER")
    openai_api_key: str | None = Field(None, alias="OPENAI_API_KEY")
    model: str = Field("gpt-5.6-luna", alias="TALIYA_AGENT_MODEL")
    guardrail_model: str = Field("gpt-4.1-mini", alias="TALIYA_AGENT_GUARDRAIL_MODEL")
    strong_model: str | None = Field(None, alias="TALIYA_AGENT_STRONG_MODEL")
    hard_cost_cap_usd: float = Field(0.15, alias="TALIYA_AGENT_HARD_COST_CAP_USD")
    review_cost_usd: float = Field(0.05, alias="TALIYA_AGENT_REVIEW_COST_USD")
    high_cost_usd: float = Field(0.10, alias="TALIYA_AGENT_HIGH_COST_USD")
    simple_opening_triage_enabled: bool = Field(True, alias="TALIYA_SIMPLE_OPENING_TRIAGE_ENABLED")
    database_url: str | None = Field(None, alias="DATABASE_URL")


def validate_production_settings(settings: RuntimeSettings) -> None:
    if settings.environment.lower() not in {"production", "prod"}:
        return

    errors: list[str] = []
    if settings.provider != "openai":
        errors.append("TALIYA_AGENT_PROVIDER must be openai in production")
    if not settings.openai_api_key:
        errors.append("OPENAI_API_KEY is required in production")
    if not settings.database_url:
        errors.append("DATABASE_URL is required in production")
    if (
        not settings.hmac_secret
        or settings.hmac_secret == "dev-secret"
        or len(settings.hmac_secret) < 24
    ):
        errors.append("TALIYA_AGENT_RUNTIME_HMAC_SECRET must be a non-default production secret")
    if not settings.model:
        errors.append("TALIYA_AGENT_MODEL is required in production")

    if errors:
        raise RuntimeSettingsError(errors)


@lru_cache
def get_settings() -> RuntimeSettings:
    return RuntimeSettings()
