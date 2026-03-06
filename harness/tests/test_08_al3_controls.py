"""TSPP harness tests for AL3 expectations.

Canonical AL semantics: see the TRQP Assurance Hub guide:
https://trustoverip.github.io/tswg-trqp-specification/ (or the repo canonical doc docs/guides/assurance-levels.md)

What this test is proving:
- AL3 claims are backed by independent review evidence, change-control evidence,
  and default signing behavior suitable for audit-style reliance.
"""

import os
import pytest
import requests

from tspp_trqp_harness.reporting import requirements
from tspp_trqp_harness.validate import validate_json


def _unwrap_if_signed(body: dict):
    if "payload" in body and "signature" in body:
        return body["payload"], body.get("signature"), body.get("meta")
    return body, None, None


@requirements("TSPP-AL3-01")
def test_al3_metadata_declares_default_signing(_client):
    expected = os.environ.get("TSPP_EXPECT_AL")
    if expected != "AL3":
        pytest.skip("Not in AL3 mode")

    r = _client.get_metadata()
    assert r.status_code == 200, f"expected 200, got {r.status_code}: {r.text}"
    m = r.json()
    assert m.get("assurance_level") == "AL3", f"metadata assurance_level mismatch: {m.get('assurance_level')}"
    signing = m.get("signing", {})
    assert signing.get("default_signed_responses") is True, "AL3 requires signing.default_signed_responses=true"


@requirements("TSPP-AL3-02")
def test_al3_signed_envelope_includes_meta(_client, _load_queries, _load_schema):
    expected = os.environ.get("TSPP_EXPECT_AL")
    if expected != "AL3":
        pytest.skip("Not in AL3 mode")

    q = _load_queries["authorization_valid"]
    r = _client.post_authorization(q, accept_signature="none")
    assert r.status_code == 200, f"expected 200, got {r.status_code}: {r.text}"

    body = r.json()
    payload, sig, meta = _unwrap_if_signed(body)
    assert isinstance(payload, dict), "AL3 signed responses must carry payload"
    assert sig is not None, "AL3 requires default signing for successful machine-consumed responses"
    assert meta is not None, "AL3 requires top-level meta fields in signed envelopes"
    for k in ["query_hash", "iat", "exp"]:
        assert k in meta, f"AL3 meta missing {k}"

    schema = _load_schema("tspp-trqp-signed-response.schema.json")
    validate_json(body, schema)


@requirements("TSPP-AL3-03")
def test_al3_independent_assessment_uri_resolves(_client):
    expected = os.environ.get("TSPP_EXPECT_AL")
    if expected != "AL3":
        pytest.skip("Not in AL3 mode")

    r = _client.get_metadata()
    assert r.status_code == 200, f"expected 200, got {r.status_code}: {r.text}"
    m = r.json()
    audit = m.get("audit", {})
    uri = audit.get("independent_assessment_uri")
    assert uri, "AL3 requires audit.independent_assessment_uri"

    rr = requests.get(uri, timeout=10)
    assert rr.status_code == 200, f"expected 200 from independent_assessment_uri, got {rr.status_code}"


@requirements("TSPP-AL3-04")
def test_al3_change_control_uri_resolves(_client):
    expected = os.environ.get("TSPP_EXPECT_AL")
    if expected != "AL3":
        pytest.skip("Not in AL3 mode")

    r = _client.get_metadata()
    assert r.status_code == 200, f"expected 200, got {r.status_code}: {r.text}"
    m = r.json()
    governance = m.get("governance", {})
    uri = governance.get("change_control_uri")
    assert uri, "AL3 requires governance.change_control_uri"

    rr = requests.get(uri, timeout=10)
    assert rr.status_code == 200, f"expected 200 from change_control_uri, got {rr.status_code}"
