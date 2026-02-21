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
