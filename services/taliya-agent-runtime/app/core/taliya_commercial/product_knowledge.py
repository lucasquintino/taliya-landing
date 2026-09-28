from __future__ import annotations

import hashlib
import json
from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from app.core.taliya_commercial.schemas import ProductKnowledgeRef
from app.shared.product_knowledge.source import (
    ProductKnowledgeSource,
    get_product_knowledge_source,
)

DEFAULT_OFFICIAL_PRODUCT_KNOWLEDGE_KEYS: tuple[str, ...] = (
    "plans",
    "prices",
    "plan_comparison",
    "links",
    "demo_status",
    "waitlist_status",
    "checkout_status",
    "availability",
    "cancellation_or_guarantee_policy",
    "privacy_or_data_notes",
    "how_it_works",
    "routine_areas",
    "whatsapp_scope",
    "integration_scope",
    "comparison_spreadsheet",
    "comparison_management_system",
    "security_and_data",
    "availability_and_onboarding",
    "out_of_profile",
    "unsupported_claims",
)

DEFAULT_SPEC006_CONTRACT_KEYS: tuple[str, ...] = (
    "product_positioning",
    "plan_entitlements",
    "operating_modes",
    "setup_scope",
    "access_subscription",
    "navigation_routes",
)


@dataclass(frozen=True)
class Spec006ContractDefinition:
    key: str
    sources: tuple[tuple[str, str | None], ...]


SPEC006_CONTRACT_DEFINITIONS: dict[str, Spec006ContractDefinition] = {
    "product_positioning": Spec006ContractDefinition(
        key="product_positioning",
        sources=(("specs/006-crm-operational-core/spec.md", "Product Positioning"),),
    ),
    "plan_entitlements": Spec006ContractDefinition(
        key="plan_entitlements",
        sources=(
            (
                "specs/006-crm-operational-core/agent-plan-entitlements.pt-BR.md",
                "Regra central",
            ),
        ),
    ),
    "operating_modes": Spec006ContractDefinition(
        key="operating_modes",
        sources=(("specs/006-crm-operational-core/operating-modes.md", None),),
    ),
    "setup_scope": Spec006ContractDefinition(
        key="setup_scope",
        sources=(
            (
                "specs/006-crm-operational-core/setup-initial-configuration-scope.pt-BR.md",
                "O Que O Setup Inicial Deve Configurar",
            ),
        ),
    ),
    "access_subscription": Spec006ContractDefinition(
        key="access_subscription",
        sources=(
            (
                "specs/006-crm-operational-core/access-subscription-pending-confirmation-approved.pt-BR.md",
                "Papel Da Tela",
            ),
            (
                "specs/006-crm-operational-core/access-subscription-confirmed-setup-approved.pt-BR.md",
                "Papel Da Tela",
            ),
        ),
    ),
    "navigation_routes": Spec006ContractDefinition(
        key="navigation_routes",
        sources=(
            (
                "specs/006-crm-operational-core/final-navigation-web-app.pt-BR.md",
                "Pre-CRM",
            ),
        ),
    ),
}


def build_official_product_knowledge_refs(
    requested_keys: Sequence[str] | None = None,
    *,
    source: ProductKnowledgeSource | None = None,
) -> list[ProductKnowledgeRef]:
    official_source = source or get_product_knowledge_source()
    keys = _normalize_requested_keys(requested_keys)
    payload = official_source.query(keys)
    version = str(payload["source_version"])
    refs: list[ProductKnowledgeRef] = []

    for key, value in payload["facts"].items():
        refs.append(
            ProductKnowledgeRef(
                key=key,
                source="official_product_knowledge",
                version=version,
                value=value,
                excerpt=_compact_product_excerpt(key, value),
                evidence=[f"product_knowledge.{key}"],
            )
        )

    for key in payload["missing_facts"]:
        refs.append(
            ProductKnowledgeRef(
                key=key,
                source="official_product_knowledge",
                version=version,
                missing=True,
                evidence=[f"product_knowledge.{key}"],
            )
        )

    return refs


def build_spec006_product_contract_refs(
    requested_keys: Sequence[str] | None = None,
) -> list[ProductKnowledgeRef]:
    repo_root = _repo_root()
    refs: list[ProductKnowledgeRef] = []

    for key in _normalize_spec006_keys(requested_keys):
        definition = SPEC006_CONTRACT_DEFINITIONS.get(key)
        if definition is None:
            refs.append(
                ProductKnowledgeRef(
                    key=f"spec006.{key}",
                    source="spec_006_product_contract",
                    version=_spec006_version_for_all_sources(repo_root),
                    missing=True,
                    evidence=[f"specs/006-crm-operational-core#{key}"],
                )
            )
            continue

        value = _build_spec006_value(repo_root, definition)
        refs.append(
            ProductKnowledgeRef(
                key=f"spec006.{key}",
                source="spec_006_product_contract",
                version=value["version"],
                value=value["payload"],
                excerpt=_compact_excerpt(value["payload"]),
                evidence=value["evidence"],
            )
        )

    return refs


def _normalize_requested_keys(requested_keys: Sequence[str] | None) -> list[str]:
    raw_keys = requested_keys or DEFAULT_OFFICIAL_PRODUCT_KNOWLEDGE_KEYS
    keys: list[str] = []
    seen: set[str] = set()
    for key in raw_keys:
        normalized = str(key).strip()
        if not normalized or normalized in seen:
            continue
        keys.append(normalized)
        seen.add(normalized)
    return keys or list(DEFAULT_OFFICIAL_PRODUCT_KNOWLEDGE_KEYS)


def _normalize_spec006_keys(requested_keys: Sequence[str] | None) -> list[str]:
    raw_keys = requested_keys or DEFAULT_SPEC006_CONTRACT_KEYS
    keys: list[str] = []
    seen: set[str] = set()
    for key in raw_keys:
        normalized = str(key).strip().removeprefix("spec006.")
        if not normalized or normalized in seen:
            continue
        keys.append(normalized)
        seen.add(normalized)
    return keys or list(DEFAULT_SPEC006_CONTRACT_KEYS)


def _repo_root() -> Path:
    current = Path(__file__).resolve()
    for parent in current.parents:
        if (parent / "specs" / "006-crm-operational-core").exists():
            return parent
    raise RuntimeError("Could not locate repository root for Spec 006 contracts")


def _build_spec006_value(
    repo_root: Path,
    definition: Spec006ContractDefinition,
) -> dict[str, Any]:
    sources: list[dict[str, str | None]] = []
    version_parts: list[str] = []
    evidence: list[str] = []

    for source_path, heading in definition.sources:
        text = _read_spec006_source(repo_root, source_path)
        excerpt = _extract_markdown_section(text, heading) if heading else text.strip()
        source = {
            "source_path": source_path,
            "heading": heading,
            "excerpt": _trim_whitespace(excerpt),
        }
        sources.append(source)
        version_parts.extend([source_path, text])
        evidence.append(f"{source_path}#{heading}" if heading else source_path)

    payload: dict[str, Any]
    if len(sources) == 1:
        payload = dict(sources[0])
    else:
        payload = {"sources": sources}

    return {
        "version": _spec006_version(version_parts),
        "payload": payload,
        "evidence": evidence,
    }


def _read_spec006_source(repo_root: Path, source_path: str) -> str:
    path = repo_root / Path(source_path)
    return path.read_text(encoding="utf-8")


def _extract_markdown_section(text: str, heading: str | None) -> str:
    if not heading:
        return text.strip()

    lines = text.splitlines()
    start_index: int | None = None
    heading_level: int | None = None
    for index, line in enumerate(lines):
        stripped = line.strip()
        if not stripped.startswith("#"):
            continue
        level = len(stripped) - len(stripped.lstrip("#"))
        title = stripped.lstrip("#").strip()
        if title == heading:
            start_index = index + 1
            heading_level = level
            break

    if start_index is None or heading_level is None:
        return text.strip()

    end_index = len(lines)
    for index in range(start_index, len(lines)):
        stripped = lines[index].strip()
        if not stripped.startswith("#"):
            continue
        level = len(stripped) - len(stripped.lstrip("#"))
        if level <= heading_level:
            end_index = index
            break

    return "\n".join(lines[start_index:end_index]).strip()


def _trim_whitespace(text: str) -> str:
    return "\n".join(line.rstrip() for line in text.strip().splitlines()).strip()


def _spec006_version(parts: Sequence[str]) -> str:
    digest = hashlib.sha256()
    for part in parts:
        digest.update(part.encode("utf-8"))
    return f"spec006-{digest.hexdigest()[:12]}"


def _spec006_version_for_all_sources(repo_root: Path) -> str:
    parts: list[str] = []
    for definition in SPEC006_CONTRACT_DEFINITIONS.values():
        for source_path, _heading in definition.sources:
            parts.extend([source_path, _read_spec006_source(repo_root, source_path)])
    return _spec006_version(parts)


def _compact_excerpt(value: Any, *, max_length: int = 900) -> str:
    if isinstance(value, str):
        text = value
    else:
        text = json.dumps(value, ensure_ascii=True, sort_keys=True, separators=(",", ":"))
    if len(text) <= max_length:
        return text
    return f"{text[: max_length - 3]}..."


def _compact_product_excerpt(key: str, value: Any) -> str:
    if key == "plans":
        return _compact_plans_excerpt(value)
    return _compact_excerpt(value)


def _compact_plans_excerpt(value: Any, *, max_length: int = 1400) -> str:
    if not isinstance(value, list):
        return _compact_excerpt(value, max_length=max_length)

    plan_summaries: list[str] = []
    for raw_plan in value:
        if not isinstance(raw_plan, dict):
            continue
        included_agents = raw_plan.get("included_agents") or ["no active AI agents"]
        included = ", ".join(str(agent) for agent in included_agents)
        plan_summaries.append(
            " ".join(
                part
                for part in [
                    f"{raw_plan.get('name')} ({raw_plan.get('id')})",
                    str(raw_plan.get("price_label") or "").strip(),
                    f"best_for={raw_plan.get('best_for')}",
                    f"included={included}",
                    f"whatsapp={raw_plan.get('whatsapp_availability')}",
                    f"usage={raw_plan.get('usage_boundary')}",
                ]
                if part.strip()
            )
        )

    if not plan_summaries:
        return _compact_excerpt(value, max_length=max_length)
    return _compact_excerpt(" | ".join(plan_summaries), max_length=max_length)
