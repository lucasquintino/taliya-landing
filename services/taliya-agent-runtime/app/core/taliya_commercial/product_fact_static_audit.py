from __future__ import annotations

from dataclasses import dataclass

_OFFICIAL_SOURCE_MARKERS = (
    "product_knowledge",
    "specs/006-crm-operational-core",
    "spec_006_product_contract",
    "spec006",
)

_PATTERNS_BY_CODE = {
    "product_fact_price_literal": (
        "r$ 197",
        "r$ 497",
        "r$ 897",
        "r$ 1.497",
    ),
    "product_fact_payment_promise": (
        "checkout",
        "link de pagamento",
        "pagamento",
        "desconto",
        "vip",
    ),
    "product_fact_availability_promise": (
        "data de abertura",
        "pre-venda",
        "pre venda",
    ),
    "product_fact_unsupported_claim": (
        "integracao garantida",
        "integração garantida",
        "certificacao",
        "certificação",
    ),
    "product_fact_technical_demo": (
        "openai_demo",
        "demo_video",
        "video production",
        "video_production",
    ),
}


@dataclass(frozen=True)
class ProductFactFinding:
    code: str
    path: str
    line: int
    snippet: str
    matched: str


@dataclass(frozen=True)
class ProductFactAuditResult:
    passed: bool
    findings: list[ProductFactFinding]


def audit_product_fact_locations(
    files: dict[str, str],
    *,
    allowlisted_paths: set[str] | None = None,
) -> ProductFactAuditResult:
    allowlisted = allowlisted_paths or set()
    findings: list[ProductFactFinding] = []
    for path, text in sorted(files.items()):
        if _is_allowed_path(path, allowlisted):
            continue
        findings.extend(_find_product_fact_literals(path, text))
    return ProductFactAuditResult(passed=not findings, findings=findings)


def _find_product_fact_literals(path: str, text: str) -> list[ProductFactFinding]:
    findings: list[ProductFactFinding] = []
    for line_number, line in enumerate(text.splitlines(), start=1):
        normalized = line.casefold()
        for code, patterns in _PATTERNS_BY_CODE.items():
            for pattern in patterns:
                if pattern.casefold() not in normalized:
                    continue
                findings.append(
                    ProductFactFinding(
                        code=code,
                        path=path,
                        line=line_number,
                        snippet=line.strip()[:240],
                        matched=pattern,
                    )
                )
                break
    return findings


def _is_allowed_path(path: str, allowlisted_paths: set[str]) -> bool:
    normalized = path.replace("\\", "/").casefold()
    if path in allowlisted_paths or normalized in {
        item.replace("\\", "/").casefold() for item in allowlisted_paths
    }:
        return True
    return any(marker in normalized for marker in _OFFICIAL_SOURCE_MARKERS)
