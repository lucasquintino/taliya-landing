from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Literal

from pydantic import Field, model_validator

from app.core.taliya_commercial.schemas import Channel, StrictModel, TurnContext

CONTEXT_SNAPSHOT_SCHEMA_VERSION = "011.context_snapshot.v1"


class ContextSnapshotRecord(StrictModel):
    snapshot_schema_version: Literal["011.context_snapshot.v1"] = (
        CONTEXT_SNAPSHOT_SCHEMA_VERSION
    )
    snapshot_id: str
    purpose: Literal["eval_debug"] = "eval_debug"
    customer_visible: Literal[False] = False
    created_at: str | None = None
    context_schema_version: str
    turn_id: str
    conversation_id: str
    agent_key: str
    channel: Channel
    context: TurnContext
    metadata: dict[str, str] = Field(default_factory=dict)

    @model_validator(mode="after")
    def top_level_fields_mirror_context(self) -> ContextSnapshotRecord:
        if self.context_schema_version != self.context.schema_version:
            raise ValueError("context snapshot schema version mismatch")
        if self.turn_id != self.context.turn_id:
            raise ValueError("context snapshot turn id mismatch")
        if self.conversation_id != self.context.conversation_id:
            raise ValueError("context snapshot conversation id mismatch")
        if self.agent_key != self.context.agent_key:
            raise ValueError("context snapshot agent key mismatch")
        if self.channel != self.context.channel:
            raise ValueError("context snapshot channel mismatch")
        return self


def build_context_snapshot(
    context: TurnContext,
    *,
    snapshot_id: str | None = None,
    created_at: str | None = None,
    metadata: dict[str, str] | None = None,
) -> ContextSnapshotRecord:
    stable_snapshot_id = snapshot_id or _stable_snapshot_id(context)
    return ContextSnapshotRecord(
        snapshot_id=stable_snapshot_id,
        created_at=created_at,
        context_schema_version=context.schema_version,
        turn_id=context.turn_id,
        conversation_id=context.conversation_id,
        agent_key=context.agent_key,
        channel=context.channel,
        context=context,
        metadata=metadata or {},
    )


def context_snapshot_to_json(snapshot: ContextSnapshotRecord) -> str:
    return json.dumps(
        snapshot.model_dump(mode="json"),
        ensure_ascii=True,
        separators=(",", ":"),
        sort_keys=True,
    )


def context_snapshot_from_json(payload: str) -> ContextSnapshotRecord:
    return ContextSnapshotRecord.model_validate_json(payload)


def replay_turn_context(snapshot: ContextSnapshotRecord | str) -> TurnContext:
    if isinstance(snapshot, str):
        snapshot = context_snapshot_from_json(snapshot)
    return snapshot.context


class ContextSnapshotFileStore:
    def __init__(self, directory: str | Path) -> None:
        self.directory = Path(directory)

    def save(self, snapshot: ContextSnapshotRecord) -> Path:
        self.directory.mkdir(parents=True, exist_ok=True)
        path = self._path_for(snapshot.snapshot_id)
        path.write_text(context_snapshot_to_json(snapshot), encoding="utf-8")
        return path

    def load(self, snapshot_id: str) -> ContextSnapshotRecord:
        return context_snapshot_from_json(
            self._path_for(snapshot_id).read_text(encoding="utf-8")
        )

    def list_for_conversation(self, conversation_id: str) -> list[ContextSnapshotRecord]:
        snapshots: list[ContextSnapshotRecord] = []
        if not self.directory.exists():
            return snapshots
        for path in sorted(self.directory.glob("*.json")):
            snapshot = context_snapshot_from_json(path.read_text(encoding="utf-8"))
            if snapshot.conversation_id == conversation_id:
                snapshots.append(snapshot)
        return snapshots

    def _path_for(self, snapshot_id: str) -> Path:
        safe_id = _safe_snapshot_id(snapshot_id)
        return self.directory / f"{safe_id}.json"


def _stable_snapshot_id(context: TurnContext) -> str:
    digest = hashlib.sha256(_stable_context_json(context).encode("utf-8")).hexdigest()
    return f"context_snapshot_{context.turn_id}_{digest[:16]}"


def _stable_context_json(context: TurnContext) -> str:
    return json.dumps(
        context.model_dump(mode="json"),
        ensure_ascii=True,
        separators=(",", ":"),
        sort_keys=True,
    )


def _safe_snapshot_id(snapshot_id: str) -> str:
    safe_id = "".join(
        character
        if character.isalnum() or character in {"-", "_", "."}
        else "_"
        for character in snapshot_id.strip()
    )
    if not safe_id:
        raise ValueError("snapshot_id cannot be empty")
    return safe_id
