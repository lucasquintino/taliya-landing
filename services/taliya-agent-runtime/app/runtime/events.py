from __future__ import annotations

from typing import Any, Literal
from uuid import uuid4

from pydantic import BaseModel, Field


class RuntimeEvent(BaseModel):
    id: str = Field(default_factory=lambda: uuid4().hex)
    run_id: str
    conversation_id: str
    agent_key: str
    type: Literal[
        "message",
        "tool_call",
        "tool_output",
        "handoff",
        "guardrail",
        "context_update",
        "usage",
        "error",
    ]
    agent: str
    content: str = ""
    metadata: dict[str, Any] = Field(default_factory=dict)
    timestamp_ms: int | None = None
