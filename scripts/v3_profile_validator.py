#!/usr/bin/env python3
"""Validate TRQP v3 candidate realizability at the TSPP protocol/profile layer.

The validator reuses the existing independent WP8 lifecycle/evidence evaluator for
material-bound observations, then checks additional profile-boundary invariants.
It intentionally does not import the candidate reference evaluator or CTS oracle.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from wp8_evidence_validator import evaluate as evaluate_wp8

ROOT = Path(__file__).resolve().parents[1]
PIN_PATH = ROOT / "experimental" / "trqp-v3" / "source-pin.json"
CONTRACT_PATH = ROOT / "experimental" / "trqp-v3" / "profile-contract.json"

CANDIDATE_SHA = "532a570ed8b7b468b7a317030077577b9859c14f"
AUTHORITY_STATUS = "DOWNSTREAM_EXPERIMENTAL_NOT_ADOPTED"

REQUIRED_REQUIREMENTS = {
    "TRQP3-PROP-001", "TRQP3-PROP-002",
    "TRQP3-MAT-001", "TRQP3-MAT-002", "TRQP3-MAT-003",
    "TRQP3-CTX-001",
    "TRQP3-LIFE-001", "TRQP3-LIFE-002", "TRQP3-LIFE-003",
    "TRQP3-EVID-001", "TRQP3-EVID-002", "TRQP3-EVID-003",
    "TRQP3-DEC-001", "TRQP3-DEC-002",
    "TRQP3-REQ-001", "TRQP3-EVAL-001", "TRQP3-RESP-001",
    "TRQP3-NEG-001", "TRQP3-NEG-002", "TRQP3-BIND-001",
    "TRQP3-DISC-001", "TRQP3-DISC-002",
    "TRQP3-PROF-001", "TRQP3-PROF-002",
    "TRQP3-REC-001", "TRQP3-REC-002",
    "TRQP3-ERR-001", "TRQP3-SEC-001", "TRQP3-SEC-002",
    "TRQP3-PRIV-001", "TRQP3-AUD-001", "TRQP3-COMP-001",
}

PRINCIPALS = [{
    "id": "did:example:issuer-a",
    "materials": [
        {
            "id": "C1",
            "purpose": "issue",
            "resource": "credential-x",
            "valid_from": "2026-01-01T00:00:00Z",
            "valid_until": "2026-07-01T00:00:00Z",
        },
        {
            "id": "C2",
            "purpose": "issue",
            "resource": "credential-x",
            "valid_from": "2026-07-01T00:00:00Z",
            "revoked_at": "2026-09-01T00:00:00Z",
        },
    ],
}]


def load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def source(**overrides: Any) -> dict[str, Any]:
    value = {
        "authoritative": True,
        "complete_for_scope": True,
        "history_complete": True,
        "observed_at": "2026-09-10T00:00:00Z",
        "fresh_for_seconds": 7 * 24 * 60 * 60,
        "supported_context": ["verification_material", "time"],
    }
    value.update(overrides)
    return value


def query(**overrides: Any) -> dict[str, Any]:
    value = {
        "entity_id": "did:example:issuer-a",
        "action": "issue",
        "resource": "credential-x",
        "verification_material": "C2",
        "time": "2026-08-15T00:00:00Z",
        "critical_context": ["verification_material"],
    }
    value.update(overrides)
    return value


def semantic_class(observation: tuple[str, str]) -> str:
    state, _reason = observation
    if state == "positive":
        return "positive"
    if state == "negative":
        return "negative"
    if state in {"unknown", "stale"}:
        return "indeterminate"
    raise ValueError(f"unsupported TSPP evidence state: {state}")


def evaluate_profile_boundary(case: dict[str, Any]) -> dict[str, str]:
    if case.get("applicable") is False:
        return {"semantic_decision": "not_applicable", "processing": "accept"}
    if case.get("requested_version", "v3") != "v3":
        return {"semantic_decision": "indeterminate", "processing": "reject"}
    if case.get("legacy_fallback", False):
        return {"semantic_decision": "indeterminate", "processing": "reject"}
    if not case.get("processing_contract_established", True):
        return {"semantic_decision": "indeterminate", "processing": "reject"}
    if not case.get("critical_supported", True):
        return {"semantic_decision": "indeterminate", "processing": "reject"}
    if case.get("profile_conflict", False) or case.get("profile_weakens_core", False):
        return {"semantic_decision": "indeterminate", "processing": "reject"}
    if case.get("binding_changes_semantics", False):
        return {"semantic_decision": "indeterminate", "processing": "reject"}
    if case.get("discovery_used_as_authority", False):
        return {"semantic_decision": "indeterminate", "processing": "reject"}
    if case.get("recognition_used_as_authorization", False):
        return {"semantic_decision": "indeterminate", "processing": "reject"}
    if case.get("privacy_dropped_critical", False):
        return {"semantic_decision": "indeterminate", "processing": "reject"}
    if not case.get("transport_ok", True):
        return {"semantic_decision": "indeterminate", "processing": "reject"}
    if not case.get("audit_reconstructable", True):
        return {"semantic_decision": "indeterminate", "processing": "reject"}
    if case.get("recognition_transitive_without_authority", False):
        return {"semantic_decision": "negative", "processing": "accept"}
    return {"semantic_decision": "positive", "processing": "accept"}


def validate() -> dict[str, Any]:
    pin = load_json(PIN_PATH)
    profile = load_json(CONTRACT_PATH)

    if pin.get("commit") != CANDIDATE_SHA:
        raise AssertionError("candidate source pin moved without TSPP reassessment")
    if pin.get("authority_status") != AUTHORITY_STATUS:
        raise AssertionError("candidate authority boundary changed")
    if profile.get("candidate_commit") != CANDIDATE_SHA:
        raise AssertionError("TSPP profile contract is not bound to the candidate pin")
    if profile.get("authority_status") != AUTHORITY_STATUS:
        raise AssertionError("TSPP profile contract authority status is invalid")

    mappings = profile.get("requirement_mappings")
    if not isinstance(mappings, list):
        raise AssertionError("requirement_mappings must be a list")
    mapped_ids = {row.get("id") for row in mappings}
    if mapped_ids != REQUIRED_REQUIREMENTS:
        missing = sorted(REQUIRED_REQUIREMENTS - mapped_ids)
        extra = sorted(mapped_ids - REQUIRED_REQUIREMENTS)
        raise AssertionError(f"requirement mapping drift: missing={missing}, extra={extra}")
    if any(row.get("status") != "PASS" for row in mappings):
        raise AssertionError("profile mapping contains unresolved requirement evidence")

    contract = profile.get("contract") or {}
    expected_contract = {
        "semantic_version": "v3",
        "silent_legacy_fallback": False,
        "decision_classes": ["positive", "negative", "indeterminate", "not_applicable"],
        "unknown_evidence_maps_to": "indeterminate",
        "stale_evidence_maps_to": "indeterminate",
        "transport_failure_maps_to": "indeterminate",
        "critical_unknown_processing": "fail_closed",
        "critical_drop_allowed": False,
        "principal_material_independent": True,
        "historical_uses_as_of_state": True,
        "current_state_projected_backwards": False,
        "authoritative_absence_requires_complete_scope": True,
        "discovery_is_authority": False,
        "recognition_is_authorization": False,
        "recognition_transitive_by_default": False,
        "profile_may_weaken_core": False,
        "conflicting_mandatory_profiles": "fail_closed",
        "audit_reconstruction_required": True,
    }
    if contract != expected_contract:
        raise AssertionError("TSPP candidate profile contract no longer matches required invariants")

    wp8_cases = {
        "material-current": (source(), query(), "positive"),
        "material-revoked": (source(), query(time="2026-09-05T00:00:00Z"), "negative"),
        "historical-prior-material": (
            source(),
            query(verification_material="C1", time="2026-06-01T00:00:00Z", historical=True),
            "positive",
        ),
        "history-incomplete": (
            source(history_complete=False),
            query(verification_material="C1", time="2026-06-01T00:00:00Z", historical=True),
            "indeterminate",
        ),
        "source-stale": (source(), query(time="2026-09-20T00:00:00Z"), "indeterminate"),
        "unsupported-critical": (
            source(supported_context=["time"]),
            query(),
            "indeterminate",
        ),
        "incomplete-absence": (
            source(complete_for_scope=False),
            query(entity_id="did:example:absent"),
            "indeterminate",
        ),
    }
    for name, (src, qry, expected) in wp8_cases.items():
        actual = semantic_class(evaluate_wp8(src, PRINCIPALS, qry))
        if actual != expected:
            raise AssertionError(f"{name}: expected {expected}, got {actual}")

    boundary_cases = {
        "safe": ({}, {"semantic_decision": "positive", "processing": "accept"}),
        "no-silent-downgrade": (
            {"requested_version": "v2", "legacy_fallback": True},
            {"semantic_decision": "indeterminate", "processing": "reject"},
        ),
        "unknown-critical": (
            {"critical_supported": False},
            {"semantic_decision": "indeterminate", "processing": "reject"},
        ),
        "profile-conflict": (
            {"profile_conflict": True},
            {"semantic_decision": "indeterminate", "processing": "reject"},
        ),
        "transport-failure": (
            {"transport_ok": False},
            {"semantic_decision": "indeterminate", "processing": "reject"},
        ),
        "discovery-not-authority": (
            {"discovery_used_as_authority": True},
            {"semantic_decision": "indeterminate", "processing": "reject"},
        ),
        "recognition-nontransitive": (
            {"recognition_transitive_without_authority": True},
            {"semantic_decision": "negative", "processing": "accept"},
        ),
        "privacy-no-drop": (
            {"privacy_dropped_critical": True},
            {"semantic_decision": "indeterminate", "processing": "reject"},
        ),
    }
    for name, (case, expected) in boundary_cases.items():
        actual = evaluate_profile_boundary(case)
        if actual != expected:
            raise AssertionError(f"{name}: expected {expected}, got {actual}")

    return {
        "candidate_commit": CANDIDATE_SHA,
        "authority_status": AUTHORITY_STATUS,
        "mapped_requirements": len(mapped_ids),
        "wp8_cases": len(wp8_cases),
        "profile_boundary_cases": len(boundary_cases),
        "status": "PASS",
    }


def main() -> int:
    print(json.dumps(validate(), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
