#!/usr/bin/env python3
"""Validate the immutable planning snapshot, never current execution states."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import zipfile

ROOT = Path(__file__).resolve().parents[1]

def main():
    archive = ROOT / "source/Taliya_Inicio_Implementacao_SDD.zip"
    expected = json.loads((ROOT / "evidence/input-import.json").read_text())["zip_sha256"]
    if hashlib.sha256(archive.read_bytes()).hexdigest() != expected:
        raise ValueError("source archive hash mismatch")
    with zipfile.ZipFile(archive) as z, tempfile.TemporaryDirectory() as tmp:
        for item in z.infolist():
            path = Path(item.filename)
            if path.is_absolute() or ".." in path.parts:
                raise ValueError("unsafe archive path")
        z.extractall(tmp)
        snapshot = Path(tmp) / "Taliya_Plano_Integral_SDD_v3"
        manifest = json.loads((snapshot / "MANIFESTO_SHA256.json").read_text())
        for entry in manifest["files"]:
            if hashlib.sha256((snapshot / entry["path"]).read_bytes()).hexdigest() != entry["sha256"]:
                raise ValueError("manifest mismatch: " + entry["path"])
        subprocess.run([sys.executable, str(snapshot / "scripts/validate_plan.py")], check=True)
    print("Current progress was not reset or assessed. Runtime acceptance was not tested.")

if __name__ == "__main__":
    main()
