from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from app.shared.memory.postgres import InMemoryMemoryStore


@dataclass
class TaliyaCommercialContext:
    conversation_id: str
    lead_id: str | None = None
    memory_store: InMemoryMemoryStore | None = None
    state: dict[str, Any] = field(default_factory=dict)

    @property
    def store(self) -> InMemoryMemoryStore:
        if self.memory_store is None:
            self.memory_store = InMemoryMemoryStore()
        return self.memory_store
