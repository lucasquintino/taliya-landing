#!/usr/bin/env python3
"""Offline consistency gate; evidence references never imply runtime success."""
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]

def read(root, name):
    return json.loads((root / name).read_text())

def validate(root=ROOT):
    repo = root.parents[1]
    stages = read(root, "planning/program.json")["stages"]
    tasks = read(root, "planning/tasks.json")
    reqs = read(root, "planning/requirements.json")
    cases = read(root, "evals/acceptance-cases.json")
    status = read(root, "STATUS.json")
    errors = []
    def check(ok, message):
        if not ok:
            errors.append(message)
    def evidence(item):
        refs = item.get("evidence")
        if not isinstance(refs, list) or not refs:
            return False
        return all(isinstance(x, str) and not Path(x).is_absolute()
                   and ".." not in Path(x).parts and (repo / x).is_file() for x in refs)
    def index(items):
        result = {x["id"]: x for x in items}
        check(len(result) == len(items), "duplicate IDs")
        return result
    ss, tt, rr, cc = map(index, (status["specs"], tasks, reqs, cases))
    st = index(stages)
    check(set(ss) == set(st), "stage/status mismatch")
    check(sum(s["weight"] for s in stages) == 100, "planning weights mismatch")
    completed = all(s["status"] == "completed" for s in ss.values())
    check(sum(s["status"] in {"in_progress", "blocked"} for s in ss.values()) == (0 if completed else 1),
          "exactly one active or blocked spec required until completion")
    check(status.get("active_spec") is None if completed else status.get("active_spec") in ss,
          "invalid active spec")
    active = status.get("active_spec")
    if active in st:
        expected = "specs/" + st[active]["directory"]
        check(read(repo, ".specify/feature.json").get("feature_directory") == expected,
              "active pointer mismatch")
        check(ss[active]["status"] in {"in_progress", "blocked"}, "active status mismatch")
    visited, visiting = set(), set()
    def visit(sid):
        if sid in visiting:
            errors.append("cyclic dependency")
            return
        if sid in visited:
            return
        visiting.add(sid)
        for dep in st[sid]["deps"]:
            check(dep in st, "unknown dependency")
            if dep in st:
                visit(dep)
        visiting.remove(sid)
        visited.add(sid)
    for sid in st:
        visit(sid)
    for s in stages:
        sid = s["id"]
        state = ss.get(sid, {}).get("status")
        check(state in {"proposed", "in_progress", "blocked", "completed"}, "invalid spec state")
        for fn in ("spec.md", "plan.md", "tasks.md", "verification.md"):
            check((repo / "specs" / s["directory"] / fn).is_file(), "missing artifact " + sid + "/" + fn)
        if state != "proposed":
            check(all(ss.get(d, {}).get("status") == "completed" for d in s["deps"]),
                  "unfinished dependency for " + sid)
        if state == "completed":
            check(all(t["status"] == "completed" for t in tasks if t["spec"] == sid), "unfinished tasks " + sid)
            check(all(c["execution_status"] == "passed" for c in cases if c["spec"] == sid), "unpassed cases " + sid)
            check(all(r["status"] == "verified" for r in reqs if r["spec"] == sid), "unverified requirements " + sid)
    for t in tasks:
        check(t["spec"] in st, "unknown task spec")
        check(t["status"] in {"not_started", "in_progress", "blocked", "completed"}, "invalid task state")
        check(bool(t["requirement_ids"]) and set(t["requirement_ids"]) <= rr.keys(), "orphan task")
        if t["status"] != "not_started":
            check(evidence(t), "missing task evidence " + t["id"])
        if t["spec"] in st:
            content = (repo / "specs" / st[t["spec"]]["directory"] / "tasks.md").read_text()
            lines = [line for line in content.splitlines() if re.search(r"\b" + re.escape(t["id"]) + r"\b", line) and line.startswith("- [")]
            check(len(lines) == 1, "task checkbox missing or duplicate " + t["id"])
            if len(lines) == 1:
                check((lines[0].lower().startswith("- [x]")) == (t["status"] == "completed"), "task checkbox disagrees " + t["id"])
    for c in cases:
        check(c["execution_status"] in {"not_run", "partial", "blocked", "failed", "passed"}, "invalid case state")
        check(bool(c["requirement_ids"]) and set(c["requirement_ids"]) <= rr.keys(), "orphan case")
        if c["execution_status"] != "not_run":
            check(evidence(c), "missing case evidence " + c["id"])
    labels = {"not_verified": "NÃO VERIFICADO", "partial": "PARCIAL", "blocked": "BLOQUEADO", "verified": "VERIFICADO"}
    matrix = (root / "05_MATRIZ_DE_COBERTURA.md").read_text()
    for r in reqs:
        check(r["status"] in labels, "invalid requirement state")
        check(bool(r["test_ids"]) and set(r["test_ids"]) <= cc.keys(), "orphan requirement")
        check(any(r["id"] in t["requirement_ids"] for t in tasks), "requirement without work")
        if r["status"] == "verified":
            check(all(cc[c]["execution_status"] == "passed" for c in r["test_ids"] if c in cc), "verified without passed case " + r["id"])
        check(any(line.startswith("| " + r["id"] + " |") and line.endswith("| " + labels.get(r["status"], "INVALID") + " |") for line in matrix.splitlines()), "matrix disagreement " + r["id"])
    config = read(root, "agent/config.intent.json")
    check(config["model"] == "gpt-6-luna" and config["reasoning_effort"] == "max", "model or effort changed")
    check(config["environment_type"] == "none" and config["multi_agent_enabled"] is False and config["shell_enabled"] is False and config["web_search_enabled"] is False, "agent capabilities expanded")
    tools = read(root, "contracts/tools.json")
    allowed = {"consultar_taliya", "buscar_material", "atualizar_contato", "preparar_proximo_passo", "solicitar_atendimento_humano"}
    check(len(tools) == 5 and {t["name"] for t in tools} == allowed and set(config["tool_names"]) == allowed, "five tools changed")
    return errors

if __name__ == "__main__":
    try:
        errors = validate()
    except (ValueError, KeyError, OSError, TypeError) as exc:
        errors = [str(exc)]
    print(json.dumps({"scope": "execution_artifact_consistency_only", "passed": not errors, "errors": errors}, ensure_ascii=False, indent=2))
    sys.exit(bool(errors))
