#!/usr/bin/env python3
"""Lightweight schema hygiene checks with zero external deps.

Checks:
  - All *.json files under schemas/ parse as JSON
  - Any "$ref": "<path>" that is a relative file path points to an existing file
    (supports file fragments like "foo.json#/defs/bar" by stripping fragment)
  - The canonical TRQP metadata schema and harness mirror are semantically identical
"""

import json
from pathlib import Path


def iter_json_files(root: Path):
    for p in root.rglob("*.json"):
        if p.is_file():
            yield p


def walk_refs(obj):
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k == "$ref" and isinstance(v, str):
                yield v
            else:
                yield from walk_refs(v)
    elif isinstance(obj, list):
        for it in obj:
            yield from walk_refs(it)


def main():
    repo_root = Path(__file__).resolve().parents[1]
    schemas_dir = repo_root / "schemas"
    if not schemas_dir.exists():
        print("schemas/ directory not found; nothing to check.")
        return 0

    failed = False
    for jf in iter_json_files(schemas_dir):
        try:
            data = json.loads(jf.read_text(encoding="utf-8"))
        except Exception as e:
            print(f"[FAIL] JSON parse: {jf}: {e}")
            failed = True
            continue

        for ref in walk_refs(data):
            if ref.startswith("#") or "://" in ref:
                continue
            ref_path = ref.split("#", 1)[0]
            if not ref_path:
                continue
            target = (jf.parent / ref_path).resolve()
            if not target.exists():
                print(f"[FAIL] Missing $ref target: {jf} -> {ref}")
                failed = True

    canonical = repo_root / "schemas" / "core" / "tspp-trqp-metadata.schema.json"
    harness_mirror = repo_root / "harness" / "schemas" / "tspp-trqp-metadata.schema.json"
    if canonical.exists() and harness_mirror.exists():
        try:
            canonical_json = json.loads(canonical.read_text(encoding="utf-8"))
            harness_json = json.loads(harness_mirror.read_text(encoding="utf-8"))
            if canonical_json != harness_json:
                print(
                    "[FAIL] Metadata schema drift: schemas/core/tspp-trqp-metadata.schema.json "
                    "and harness/schemas/tspp-trqp-metadata.schema.json differ"
                )
                failed = True
        except Exception as e:
            print(f"[FAIL] Metadata schema mirror comparison: {e}")
            failed = True

    if failed:
        print("Schema checks FAILED.")
        return 1
    print("Schema checks PASSED.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
