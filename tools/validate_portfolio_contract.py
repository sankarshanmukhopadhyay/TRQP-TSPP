#!/usr/bin/env python3
"""Validate the repository's cross-repository portfolio integration contract."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "portfolio" / "integration-contract.json"
VERSION = ROOT / "VERSION"
EXPECTED_SEMANTIC = ("sankarshanmukhopadhyay/trust-systems-meta-model", "0.24.0")
EXPECTED_SCHEMA = ("sankarshanmukhopadhyay/trust-infrastructure-schemas", "0.15.0")
REQUIRED_KEYS = {
    "contractVersion", "repository", "release", "role", "authority",
    "provides", "consumes", "evidence", "relationships", "revocation",
}


def check(name: str, passed: bool, detail: str) -> dict:
    return {"check": name, "passed": passed, "detail": detail}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    data = json.loads(CONTRACT.read_text(encoding="utf-8"))
    release = VERSION.read_text(encoding="utf-8").strip()
    checks = []
    checks.append(check("required-keys", REQUIRED_KEYS <= data.keys(), "required contract fields are present"))
    checks.append(check("contract-version", data.get("contractVersion") == "1.0", "contractVersion must be 1.0"))
    checks.append(check("release-pin", data.get("release") == release, f"contract release must equal VERSION ({release})"))
    authority = data.get("authority", {})
    semantic = authority.get("semanticAuthority", {})
    schema = authority.get("schemaAuthority", {})
    checks.append(check("semantic-authority", (semantic.get("repository"), semantic.get("version")) == EXPECTED_SEMANTIC and bool(semantic.get("artifacts")), "TSMM authority must be pinned to 0.24.0 with declared artifacts"))
    checks.append(check("schema-authority", (schema.get("repository"), schema.get("version")) == EXPECTED_SCHEMA and bool(schema.get("artifacts")), "TIS authority must be pinned to 0.15.0 with declared artifacts"))
    missing_evidence = [e.get("path") for e in data.get("evidence", []) if not (ROOT / e.get("path", "")).is_file()]
    checks.append(check("evidence-exists", not missing_evidence, f"missing evidence: {missing_evidence}" if missing_evidence else "all declared evidence exists"))
    peers = {r.get("repository") for r in data.get("relationships", [])}
    checks.append(check("cross-repo-relations", {"sankarshanmukhopadhyay/trqp-conformance-suite", "sankarshanmukhopadhyay/trqp-assurance-hub"} <= peers, "required TRQP peer relationships are declared"))
    revocation = data.get("revocation", {})
    checks.append(check("revocation", bool(revocation.get("triggers")) and bool(revocation.get("effect")), "revocation triggers and effect must be explicit"))
    result = {"valid": all(item["passed"] for item in checks), "repository": data.get("repository"), "release": release, "contractVersion": data.get("contractVersion"), "authority": authority, "checks": checks}
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    print(rendered, end="")
    if args.output:
        output = args.output if args.output.is_absolute() else ROOT / args.output
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(rendered, encoding="utf-8")
    return 0 if result["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
