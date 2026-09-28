from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from app.runtime.schemas import Usage


@dataclass(frozen=True)
class ModelRate:
    input_per_million: float
    cached_input_per_million: float
    cache_write_input_per_million: float
    output_per_million: float


CapStatus = Literal["ok", "review", "hard_cap_blocked"]


@dataclass(frozen=True)
class ModelUsageRecord:
    run_id: str
    conversation_id: str
    agent_key: str
    operation: str
    model: str | None
    input_tokens: int
    output_tokens: int
    cost_usd: float
    budget_before: float
    budget_after: float
    cap_status: CapStatus


DEFAULT_RATES = {
    # Standard text token rates per 1M tokens. Luna verified on 2026-08-04.
    "gpt-5.2": ModelRate(
        input_per_million=1.75,
        cached_input_per_million=0.175,
        cache_write_input_per_million=1.75,
        output_per_million=14.0,
    ),
    "gpt-5.4-mini": ModelRate(
        input_per_million=0.75,
        cached_input_per_million=0.075,
        cache_write_input_per_million=0.75,
        output_per_million=4.5,
    ),
    "gpt-5.6-luna": ModelRate(
        input_per_million=1.00,
        cached_input_per_million=0.10,
        cache_write_input_per_million=1.25,
        output_per_million=6.00,
    ),
    "gpt-4.1-mini": ModelRate(
        input_per_million=0.4,
        cached_input_per_million=0.1,
        cache_write_input_per_million=0.4,
        output_per_million=1.6,
    ),
}


def estimate_cost_usd(
    model: str | None,
    input_tokens: int,
    output_tokens: int,
    *,
    cached_input_tokens: int = 0,
    cache_write_input_tokens: int = 0,
) -> float:
    if model is None:
        return 0
    rate = DEFAULT_RATES.get(model)
    if rate is None:
        raise ValueError(
            f"No recorded pricing for model '{model}'. Refusing to guess cost."
        )
    cached = min(max(cached_input_tokens, 0), max(input_tokens, 0))
    cache_write = min(
        max(cache_write_input_tokens, 0),
        max(input_tokens - cached, 0),
    )
    uncached = max(input_tokens - cached - cache_write, 0)
    return round(
        (uncached / 1_000_000 * rate.input_per_million)
        + (cached / 1_000_000 * rate.cached_input_per_million)
        + (
            cache_write
            / 1_000_000
            * rate.cache_write_input_per_million
        )
        + (output_tokens / 1_000_000 * rate.output_per_million),
        6,
    )


def usage_from_tokens(model: str | None, input_tokens: int, output_tokens: int) -> Usage:
    return Usage(
        model=model,
        input_tokens=input_tokens,
        output_tokens=output_tokens,
        cost_usd=estimate_cost_usd(model, input_tokens, output_tokens),
    )


def cap_status_for_cost(
    cost_usd: float,
    *,
    review_cost_usd: float,
    hard_cost_cap_usd: float,
) -> CapStatus:
    if cost_usd >= hard_cost_cap_usd:
        return "hard_cap_blocked"
    if cost_usd >= review_cost_usd:
        return "review"
    return "ok"


def build_usage_record(
    *,
    run_id: str,
    conversation_id: str,
    agent_key: str,
    operation: str,
    usage: Usage,
    budget_before: float,
    review_cost_usd: float,
    hard_cost_cap_usd: float,
) -> ModelUsageRecord:
    budget_after = round(budget_before + usage.cost_usd, 6)
    return ModelUsageRecord(
        run_id=run_id,
        conversation_id=conversation_id,
        agent_key=agent_key,
        operation=operation,
        model=usage.model,
        input_tokens=usage.input_tokens,
        output_tokens=usage.output_tokens,
        cost_usd=usage.cost_usd,
        budget_before=budget_before,
        budget_after=budget_after,
        cap_status=cap_status_for_cost(
            budget_after,
            review_cost_usd=review_cost_usd,
            hard_cost_cap_usd=hard_cost_cap_usd,
        ),
    )
