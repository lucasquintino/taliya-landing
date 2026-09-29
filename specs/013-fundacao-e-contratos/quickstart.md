# Retomada local
cd /Users/lucasquintino/Projects/taliya-copiloto-landing

```sh
specify version
bash .specify/scripts/bash/check-prerequisites.sh --json --require-spec --require-tasks --include-tasks
python3 docs/taliya-sdd/scripts/validate_plan.py
python3 docs/taliya-sdd/scripts/validate_progress.py
python3 -m unittest discover -s docs/taliya-sdd/tests -v
```
Leia verification.md e o checkpoint em docs/conversation-handoff-2026-05-14.md.
Próxima dependência: B013-01/T013-02, fonte do billing vigente. Não iniciar 014/015 ainda.
