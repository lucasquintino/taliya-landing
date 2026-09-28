import crypto from "node:crypto";
import fs from "node:fs";
import path from "node:path";

const sourceTargets = [
  "services/taliya-agent-runtime/app/core/taliya_commercial",
  "services/taliya-agent-runtime/app/main.py",
  "services/taliya-agent-runtime/app/settings.py",
  "services/taliya-agent-runtime/app/runtime/schemas.py",
  "services/taliya-agent-runtime/app/shared/memory",
  "scripts/eval-agent-runtime-spec011.py",
  "scripts/spec011-t011-105-source-fingerprint.mjs",
  "scripts/eval-agent-runtime-spec011-fixture-inventory.mjs",
  "scripts/eval-agent-runtime-spec011-golden-do-not-do.mjs",
  "scripts/eval-agent-runtime-spec011-known-validator-recovery.mjs",
  "scripts/eval-agent-runtime-spec011-mocked-conductor.mjs",
  "scripts/eval-agent-runtime-spec011-public-fallback-quarantine.mjs",
  "scripts/eval-agent-runtime-spec011-rollback.mjs",
  "scripts/eval-agent-runtime-spec011-runner-quarantine.mjs",
  "scripts/eval-agent-runtime-spec011-static-audit.mjs",
  "scripts/eval-agent-runtime-spec011-t011-105-paid-batch.mjs",
  "scripts/eval-agent-runtime-spec011-t011-105-readiness.mjs",
  "scripts/eval-agent-runtime-spec011-t011-105-safety-audit.mjs",
  "scripts/eval-agent-runtime-spec011-unit-contract.mjs",
  "scripts/eval-agent-runtime-spec011-widget-adapter.mjs",
  "scripts/eval-agent-runtime-spec011-t011-105-closure.mjs",
  "scripts/fixtures/agent-runtime/spec-011-golden-transcripts.json",
  "scripts/fixtures/agent-runtime/spec-011-do-not-do-runtime.json",
];

const ignoredNames = new Set(["__pycache__"]);
const ignoredExtensions = new Set([".pyc", ".pyo"]);

export function buildSpec011T011105SourceFingerprint(root) {
  const files = collectSourceFiles(root);
  const hash = crypto.createHash("sha256");
  for (const relativePath of files) {
    const absolutePath = path.join(root, relativePath);
    hash.update(relativePath.replaceAll(path.sep, "/"));
    hash.update("\0");
    hash.update(fs.readFileSync(absolutePath));
    hash.update("\0");
  }
  return {
    algorithm: "sha256",
    digest: hash.digest("hex"),
    fileCount: files.length,
    targets: sourceTargets,
  };
}

function collectSourceFiles(root) {
  const files = [];
  for (const target of sourceTargets) {
    const absoluteTarget = path.join(root, target);
    if (!fs.existsSync(absoluteTarget)) {
      continue;
    }
    const stat = fs.statSync(absoluteTarget);
    if (stat.isDirectory()) {
      collectDirectory(root, absoluteTarget, files);
    } else if (stat.isFile() && !isIgnoredFile(absoluteTarget)) {
      files.push(path.relative(root, absoluteTarget));
    }
  }
  return [...new Set(files)].sort();
}

function collectDirectory(root, directory, files) {
  for (const entry of fs.readdirSync(directory, { withFileTypes: true })) {
    const absolutePath = path.join(directory, entry.name);
    if (entry.isDirectory()) {
      if (!ignoredNames.has(entry.name)) {
        collectDirectory(root, absolutePath, files);
      }
      continue;
    }
    if (entry.isFile() && !isIgnoredFile(absolutePath)) {
      files.push(path.relative(root, absolutePath));
    }
  }
}

function isIgnoredFile(absolutePath) {
  return ignoredExtensions.has(path.extname(absolutePath));
}
