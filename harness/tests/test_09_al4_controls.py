"""TSPP harness tests for AL4 expectations.

Canonical AL semantics: see the TRQP Assurance Hub guide:
https://github.com/sankarshanmukhopadhyay/trqp-assurance-hub/blob/main/docs/guides/assurance-levels.md

What this test is proving:
- AL4 claims are backed by key protection evidence, monitoring/runbook evidence,
  rollback/policy evidence, and audit-log retention declarations.
"""

import os
import pytest
import requests

from tspp_trqp_harness.reporting import requirements


@requirements("TSPP-AL4-02")
def test_al4_key_protection_declared(_client):
    expected = os.environ.get("TSPP_EXPECT_AL")
    if expected != "AL4":
        pytest.skip("Not in AL4 mode")

    r = _client.get_metadata()
    assert r.status_code == 200, f"expected 200, got {r.status_code}: {r.text}"
    m = r.json()
    assert m.get("assurance_level") == "AL4", f"metadata assurance_level mismatch: {m.get('assurance_level')}"

    kp = m.get("key_protection", {})
    assert kp.get("protection") in ["software", "KMS", "HSM"], "AL4 requires key_protection.protection"
    assert "evidence_uri" in kp, "AL4 requires key_protection.evidence_uri"

    rr = requests.get(kp["evidence_uri"], timeout=10)
    assert rr.status_code == 200, f"expected 200 from key_protection.evidence_uri, got {rr.status_code}"


@requirements("TSPP-AL4-03")
def test_al4_monitoring_declared(_client):
    expected = os.environ.get("TSPP_EXPECT_AL")
    if expected != "AL4":
        pytest.skip("Not in AL4 mode")

    r = _client.get_metadata()
    assert r.status_code == 200, f"expected 200, got {r.status_code}: {r.text}"
    m = r.json()

    mon = m.get("monitoring", {})
    assert isinstance(mon.get("evidence_retention_days"), int), "AL4 requires monitoring.evidence_retention_days"
    assert "incident_contact" in mon, "AL4 requires monitoring.incident_contact"
    assert "runbook_uri" in mon, "AL4 requires monitoring.runbook_uri"

    rr = requests.get(mon["runbook_uri"], timeout=10)
    assert rr.status_code == 200, f"expected 200 from monitoring.runbook_uri, got {rr.status_code}"


@requirements("TSPP-AL4-04")
def test_al4_policy_and_rollback_uris_resolve(_client):
    expected = os.environ.get("TSPP_EXPECT_AL")
    if expected != "AL4":
        pytest.skip("Not in AL4 mode")

    r = _client.get_metadata()
    assert r.status_code == 200, f"expected 200, got {r.status_code}: {r.text}"
    m = r.json()

    governance = m.get("governance", {})
    for field in ("policy_uri", "rollback_uri"):
        uri = governance.get(field)
        assert uri, f"AL4 requires governance.{field}"
        rr = requests.get(uri, timeout=10)
        assert rr.status_code == 200, f"expected 200 from governance.{field}, got {rr.status_code}"


@requirements("TSPP-AL4-05")
def test_al4_audit_log_declared(_client):
    expected = os.environ.get("TSPP_EXPECT_AL")
    if expected != "AL4":
        pytest.skip("Not in AL4 mode")

    r = _client.get_metadata()
    assert r.status_code == 200, f"expected 200, got {r.status_code}: {r.text}"
    m = r.json()

    audit = m.get("audit", {})
    assert audit.get("audit_log_uri"), "AL4 requires audit.audit_log_uri"
    assert isinstance(audit.get("immutability"), bool), "AL4 requires audit.immutability"
    assert isinstance(audit.get("retention_days"), int), "AL4 requires audit.retention_days"

    rr = requests.get(audit["audit_log_uri"], timeout=10)
    assert rr.status_code == 200, f"expected 200 from audit_log_uri, got {rr.status_code}"
