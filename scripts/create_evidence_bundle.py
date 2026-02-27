#!/usr/bin/env python3
"""
Create a Hub-aligned posture evidence bundle for TSPP runs.

Inputs:
  - a TSPP conformance report JSON (produced via TSPP_REPORT_PATH)
Outputs (under --out):
  - tspp_posture_report.json
  - bundle_descriptor.json
  - checksums.json
  - bundle.zip
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
from typing import Any, Dict, List

def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def guess_media_type(p: Path) -> str | None:
    if p.suffix == ".json":
        return "application/json"
    if p.suffix == ".zip":
        return "application/zip"
    if p.suffix in (".md", ".txt"):
        return "text/plain"
    return None

ARTIFACT_KIND_MAP = {
    "tspp_posture_report": "tspp_posture_report",
    "tspp_posture_bundle_descriptor": "tspp_posture_evidence_bundle_descriptor",
    "tspp_checksums": "evidence_bundle_checksums",
    "tspp_bundle_zip": "tspp_posture_evidence_bundle_zip",
}

def add_idx(out: Path, artifact_index: List[Dict[str, Any]], kind: str, rel_path: str, notes: str | None = None):
    p = out / rel_path
    entry: Dict[str, Any] = {
        "kind": kind,
        "artifact_kind": ARTIFACT_KIND_MAP.get(kind),
        "path": rel_path,
        "produced_by": "trqp-tspp",
    }
    if p.exists() and p.is_file():
        entry["sha256"] = sha256_file(p)
        mt = guess_media_type(p)
        if mt:
            entry["media_type"] = mt
    if notes:
        entry["notes"] = notes
    artifact_index.append(entry)

def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--report", required=True, help="Path to the TSPP conformance report JSON")
    ap.add_argument("--out", required=True, help="Output directory for evidence bundle")
    args = ap.parse_args()

    report_p = Path(args.report)
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)

    report_obj = json.loads(report_p.read_text(encoding="utf-8"))

    # Normalize the report filename inside the bundle (stable path)
    stable_report = out / "tspp_posture_report.json"
    stable_report.write_text(json.dumps(report_obj, indent=2, sort_keys=True), encoding="utf-8")

    profile = report_obj.get("profile") or "TSPP-TRQP"
    generated_at = report_obj.get("generated_at")
    target = report_obj.get("target") or {}

    descriptor: Dict[str, Any] = {
        "bundle_version": "0.1.0",
        "profile": profile,
        "generated_at": generated_at,
        "target": target,
        "artifacts": {
            "tspp_posture_report": "tspp_posture_report.json",
        },
    }

    artifact_index: List[Dict[str, Any]] = []
    add_idx(out, artifact_index, "tspp_posture_report", "tspp_posture_report.json")

    # Write descriptor first (zip comes later)
    descriptor["artifact_index"] = artifact_index
    desc_p = out / "bundle_descriptor.json"
    desc_p.write_text(json.dumps(descriptor, indent=2), encoding="utf-8")
    add_idx(out, artifact_index, "tspp_posture_bundle_descriptor", "bundle_descriptor.json")

    # Checksums
    checksums = [{"path": a["path"], "sha256": a["sha256"]} for a in artifact_index if a.get("sha256") and a.get("path")]
    checksums_obj = {
        "checksums_version": "0.1.0",
        "algorithm": "sha256",
        "generated_by": "trqp-tspp",
        "generated_at": generated_at,
        "entries": sorted(checksums, key=lambda e: e["path"]),
    }
    checks_p = out / "checksums.json"
    checks_p.write_text(json.dumps(checksums_obj, indent=2), encoding="utf-8")
    add_idx(out, artifact_index, "tspp_checksums", "checksums.json")

    # Bundle zip
    import zipfile
    zip_p = out / "bundle.zip"
    with zipfile.ZipFile(zip_p, "w", zipfile.ZIP_DEFLATED) as z:
        for p in sorted(out.rglob("*")):
            if p.is_file() and p.name != "bundle.zip":
                z.write(p, arcname=str(p.relative_to(out)))
    # Update descriptor and checksums to include bundle.zip
    descriptor["artifacts"]["bundle_zip"] = "bundle.zip"
    add_idx(out, artifact_index, "tspp_bundle_zip", "bundle.zip", notes="Convenience packaging of the evidence bundle directory.")

    # Rewrite descriptor with updated artifact_index
    descriptor["artifact_index"] = artifact_index
    desc_p.write_text(json.dumps(descriptor, indent=2), encoding="utf-8")

    # Update checksums entries with bundle.zip
    entries = {e["path"]: e["sha256"] for e in checksums_obj["entries"]}
    entries["bundle.zip"] = sha256_file(zip_p)
    checksums_obj["entries"] = [{"path": p, "sha256": h} for p, h in sorted(entries.items())]
    checks_p.write_text(json.dumps(checksums_obj, indent=2), encoding="utf-8")

    print(f"OK: posture evidence bundle written to {out}")

if __name__ == "__main__":
    main()
