#!/usr/bin/env python3
"""Validate TSPP lifecycle fixtures against the portable TIS contract boundary."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "examples" / "lifecycle"


def load(name):
    with (FIXTURES / name).open(encoding="utf-8") as f:
        return json.load(f)


def validate(event):
    required = {"event_id", "event_type", "observed_at", "target", "previous_state_refs", "changed_dimensions", "impact", "disposition", "authority", "rationale"}
    missing = required - event.keys()
    assert not missing, f"missing required fields: {sorted(missing)}"
    assert event["previous_state_refs"], "prior assurance must be attributable"
    assert event.get("provenance", {}).get("producer") == "TRQP-TSPP", "producer authority must remain attributable"
    assert event.get("provenance", {}).get("run_id"), "run correlation must remain intact"
    assert len(event["rationale"]) >= 10, "materiality rationale must be machine-visible"

    impact = event["impact"]
    disposition = event["disposition"]
    if impact in {"material", "unknown"}:
        assert disposition != "current", f"{impact} impact must never preserve current assurance"
    if impact == "material":
        assert disposition in {"stale", "reassessment_required", "invalid", "superseded", "indeterminate"}
    if impact == "unknown":
        assert disposition in {"indeterminate", "reassessment_required", "stale"}
    if disposition == "reassessment_required":
        assert event.get("reassessment_scope"), "bounded reassessment requires explicit scope"
    if impact == "non_material" and disposition == "current":
        assert event["changed_dimensions"] == ["documentation"], "current counter-case is intentionally narrow"


def main():
    names = [
        "material-change.lifecycle-event.json",
        "unknown-impact.lifecycle-event.json",
        "non-material-documentation.lifecycle-event.json",
    ]
    for name in names:
        validate(load(name))

    # Explicit falsification probes: these MUST be rejected.
    material = load(names[0]); material["disposition"] = "current"
    unknown = load(names[1]); unknown["disposition"] = "current"
    no_scope = load(names[0]); no_scope.pop("reassessment_scope", None)
    for label, candidate in [("material+current", material), ("unknown+current", unknown), ("reassessment-without-scope", no_scope)]:
        try:
            validate(candidate)
        except AssertionError:
            continue
        raise AssertionError(f"negative pressure test unexpectedly accepted: {label}")

    print("TSPP lifecycle fixtures satisfy fail-safe boundaries")


if __name__ == "__main__":
    main()
