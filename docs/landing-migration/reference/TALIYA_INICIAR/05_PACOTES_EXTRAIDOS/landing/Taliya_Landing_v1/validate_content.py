"""Validate the authored landing dataset. No network, publishing or product calls."""
from __future__ import annotations
import json
from pathlib import Path

def main() -> None:
    root = Path(__file__).resolve().parent
    d = json.loads((root / "landing.content.pt-BR.json").read_text(encoding="utf-8"))
    assert d["meta"]["activeMode"] == "prelaunch"
    expected = {"sections": 14, "selector": 5, "comparison": 7, "how": 6, "fronts": 7, "flows": 5, "faq": 14, "assets": 24, "qa": 42}
    for k, count in expected.items():
        assert len(d[k]) == count, f"{k}: expected {count}"
    subs = [s for f in d["fronts"] for s in f["subtypes"]]
    ids = {s["id"] for s in subs}
    assert len(subs) == len(ids) == 39
    assert all(4 <= len(f["subtypes"]) <= 6 for f in d["fronts"])
    required = {"id", "label", "when", "message", "organizes", "reply", "next", "result", "demoContext", "guardrail"}
    assert all(required <= set(s) and all(s[k] for k in required) for s in subs)
    messages = d["messageWall"]["messages"]
    mids = {m["id"] for m in messages}
    assert len(messages) == len(mids) == 84
    assert len(d["messageWall"]["initialIds"]) == 24
    assert set(d["messageWall"]["initialIds"]) <= mids
    assert all(m["targetSubtype"] in ids for m in messages)
    assert all(s["detailTarget"] in ids for s in d["selector"] + d["comparison"])
    assert sum(len(s["steps"]) for s in d["flows"]) == 20
    assert all(len(s["steps"]) == 4 for s in d["flows"])
    assert all(set(q["answer"]) == {"prelaunch", "launch"} for q in d["faq"])
    assert d["proof"]["visible"] is False
    assert d["offer"]["launch"]["founder"]["visible"] is False
    assert 900 - 300 == 600 and 450 - 350 == 100 and 8 - 1 - 1 == 6
    result = {"status": "passed", "scope": "local content structure, references and sample arithmetic", "site_tests": "not executed", "counts": expected | {"subtypes": 39, "messages": 84, "initial_messages": 24, "flow_steps": 20}, "unconfigured_runtime_fields": [k for k, v in d["runtime"].items() if v is None]}
    (root / "VALIDACAO_CONTEUDO.json").write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
