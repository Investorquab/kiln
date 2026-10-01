"""Run a lightweight submission hygiene audit.

This checks repository structure and obvious secret-like material. It does not
claim that BAND evidence exists or that runtime behavior has been verified.
"""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

REQUIRED = [
    "README.md",
    "docker-compose.yml",
    "factory/control_plane.py",
    "factory/work_orders/tablekeeper.json",
    "factory/work_orders/tablekeeper-cancellation.json",
    "factory/mandates/architect.md",
    "factory/mandates/modeler.md",
    "factory/mandates/builder.md",
    "factory/mandates/adversary.md",
    "factory/mandates/repairer.md",
    "factory/mandates/verifier.md",
    "docs/BAND_RUNBOOK.md",
    "docs/SUBMISSION_CHECKLIST.md",
    "docs/DEMO_SCRIPT.md",
]

SECRET_PATTERNS = [
    re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    re.compile(r"(?i)\b(?:ghp|github_pat)_[A-Za-z0-9_]{20,}\b"),
    re.compile(r"(?i)\bsk-[A-Za-z0-9_-]{20,}\b"),
]

TEXT_SUFFIXES = {".md", ".py", ".json", ".yml", ".yaml", ".toml", ".txt", ".sh", ".ps1"}


def main() -> int:
    failures: list[str] = []

    for relative in REQUIRED:
        if not (ROOT / relative).is_file():
            failures.append(f"missing required file: {relative}")

    for path in ROOT.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        if any(part in {".git", "node_modules", ".venv", "venv"} for part in path.parts):
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for pattern in SECRET_PATTERNS:
            if pattern.search(text):
                failures.append(f"secret-like material found: {path.relative_to(ROOT)}")

    compose = ROOT / "docker-compose.yml"
    if compose.is_file():
        compose_text = compose.read_text(encoding="utf-8")
        if "internal: true" not in compose_text:
            failures.append("docker-compose.yml: internal network declaration missing")
        if "mem_limit: 512m" not in compose_text:
            failures.append("docker-compose.yml: expected 512m service memory cap missing")
        if 'cpus: "1.0"' not in compose_text:
            failures.append("docker-compose.yml: expected 1.0 CPU cap missing")

    if failures:
        print("SUBMISSION HYGIENE FAILED")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("SUBMISSION HYGIENE PASSED")
    print(f"required_files={len(REQUIRED)}")
    print("secret_scan=passed")
    print("runtime_contract_scan=passed")
    print("band_evidence_claims=not_checked")
    print("note=This audit does not prove a live BAND run.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
