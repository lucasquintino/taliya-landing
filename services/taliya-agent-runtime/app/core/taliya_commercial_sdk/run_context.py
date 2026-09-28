from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class TranscriptItem:
    role: str
    text: str


@dataclass(frozen=True)
class TaliyaSpikeContext:
    """Local SDK run context for the Spec 012 spike.

    The state snapshot travels in the runner's local context so read-only tools
    can consult it directly. The model never has to echo state JSON into tool
    arguments, which keeps tokens low and prevents hallucinated state.
    """

    conversation_id: str
    turn_id: str
    channel: str
    state_snapshot: Mapping[str, Any] = field(default_factory=dict)
    prior_transcript: Sequence[TranscriptItem] = field(default_factory=tuple)

    def snapshot_value(self, key: str) -> Any:
        return dict(self.state_snapshot).get(key)
