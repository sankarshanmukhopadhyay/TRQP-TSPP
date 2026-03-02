"""TSPP harness test for AL4 expectations.

What this test is proving:
- Highest-assurance control checks are enforced, targeting adversarial operation and high-impact ecosystems.

Why it matters:
- This is a ship-stopping check for deployments claiming AL4 posture.

Evidence:
- Conformance report sections: control outcomes, independent assessment references, and change transparency evidence.
"""

import os
import pytest

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

    import requests
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

    import requests
    rr = requests.get(mon["runbook_uri"], timeout=10)
    assert rr.status_code == 200, f"expected 200 from monitoring.runbook_uri, got {rr.status_code}"

@requirements("TSPP-AL4-01")
def test_al4_governance_policy_and_rollback_uris_resolve(_client):
    expected = os.environ.get("TSPP_EXPECT_AL")
    if expected != "AL4":
        pytest.skip("Not in AL4 mode")

    r = _client.get_metadata()
    assert r.status_code == 200, f"expected 200, got {r.status_code}: {r.text}"
    m = r.json()

    g = m.get("governance", {})
    assert "policy_uri" in g, "AL4 requires governance.policy_uri"
    assert "rollback_uri" in g, "AL4 requires governance.rollback_uri"

    import requests
    rr = requests.get(g["policy_uri"], timeout=10)
    assert rr.status_code == 200, f"expected 200 from governance.policy_uri, got {rr.status_code}"
    rr2 = requests.get(g["rollback_uri"], timeout=10)
    assert rr2.status_code == 200, f"expected 200 from governance.rollback_uri, got {rr2.status_code}"


@requirements("TSPP-AL4-04")
def test_al4_audit_log_posture_declared(_client):
    expected = os.environ.get("TSPP_EXPECT_AL")
    if expected != "AL4":
        pytest.skip("Not in AL4 mode")

    r = _client.get_metadata()
    assert r.status_code == 200, f"expected 200, got {r.status_code}: {r.text}"
    m = r.json()

    audit = m.get("audit", {})
    assert "audit_log_uri" in audit, "AL4 requires audit.audit_log_uri"
    assert audit.get("immutability") in ["append-only", "immutable"], "AL4 requires audit.immutability=append-only|immutable"
    assert isinstance(audit.get("retention_days"), int), "AL4 requires audit.retention_days (int)"

    import requests
    rr = requests.get(audit["audit_log_uri"], timeout=10)
    assert rr.status_code == 200, f"expected 200 from audit_log_uri, got {rr.status_code}"
