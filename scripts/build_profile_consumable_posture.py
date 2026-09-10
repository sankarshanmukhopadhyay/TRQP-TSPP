#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

STATUS_MAP = {
    "PASS": "PASS",
    "FAIL": "FAIL",
    "NOT_TESTED": "INDETERMINATE",
    "NOT_APPLICABLE": "NOT_APPLICABLE",
}


def revision(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def effective_reassessment(base_state: str, profile_context: dict | None) -> tuple[str, str | None]:
    if base_state in {"REASSESS_REQUIRED", "INVALID"}:
        return base_state, None
    if not profile_context or not profile_context.get("source_changed"):
        return base_state, None
    if profile_context.get("posture_relevant") is True:
        return "REASSESS_REQUIRED", "profile-posture-obligation-changed"
    if profile_context.get("posture_relevant") is False:
        return "CURRENT", "profile-change-posture-non-material"
    return "REASSESS_REQUIRED", "profile-change-posture-impact-unknown"


def build(report: dict, *, tspp_version: str, control_set_id: str,
          control_set_revision: str, reassessment_state: str = "CURRENT",
          profile_context: dict | None = None) -> dict:
    controls = []
    for item in report.get("results", []):
        raw = item.get("status")
        if raw not in STATUS_MAP:
            raise ValueError(f"unsupported TSPP status: {raw}")
        out = {
            "control_id": item["control_id"],
            "result": STATUS_MAP[raw],
            "evidence_ref": f"tspp-report.json#control_id={item['control_id']}",
        }
        if item.get("evidence"):
            out["reason"] = item["evidence"]
        controls.append(out)

    summary = report.get("summary", {})
    if summary.get("FAIL", 0) > 0:
        posture_result = "FAIL"
    elif summary.get("NOT_TESTED", 0) > 0:
        posture_result = "INDETERMINATE"
    else:
        posture_result = "PASS"

    state, rationale = effective_reassessment(reassessment_state, profile_context)
    reassessment = {"state": state}
    if rationale:
        reassessment["rationale_code"] = rationale

    evidence = {
        "schema_version": "1.0",
        "producer": "TRQP-TSPP",
        "tspp_version": tspp_version,
        "target": {"id": report["target_id"]},
        "run": {"id": report["run_id"], "generated_at": report["generated_at"]},
        "assurance_level": report["assurance_level"],
        "control_set": {"id": control_set_id, "revision": control_set_revision},
        "posture": {"result": posture_result, "controls": controls},
        "reassessment": reassessment,
    }
    if profile_context:
        evidence["profile_context"] = dict(profile_context)
    return evidence


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--report", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--control-set", type=Path, default=Path("controls/control-registry.json"))
    parser.add_argument("--control-set-id", default="tspp-control-registry")
    parser.add_argument("--reassessment-state", choices=["CURRENT", "REASSESS_REQUIRED", "INVALID"], default="CURRENT")
    args = parser.parse_args()

    report = json.loads(args.report.read_text(encoding="utf-8"))
    version = Path("VERSION").read_text(encoding="utf-8").strip()
    evidence = build(
        report,
        tspp_version=version,
        control_set_id=args.control_set_id,
        control_set_revision=revision(args.control_set),
        reassessment_state=args.reassessment_state,
    )
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(evidence, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"wrote {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
