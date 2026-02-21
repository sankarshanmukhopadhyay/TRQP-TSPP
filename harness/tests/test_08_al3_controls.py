import os
import pytest

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

    # Request *no signature* to confirm AL3 default-signing behavior.
    r = _client.post_authorization(q, accept_signature="none")
    assert r.status_code == 200, f"expected 200, got {r.status_code}: {r.text}"

    body = r.json()
    payload, sig, meta = _unwrap_if_signed(body)

    assert sig is not None, "AL3 requires default signing for successful machine-consumed responses"
    assert meta is not None, "AL3 requires meta fields in signed envelopes"
    for k in ["query_hash", "iat", "exp"]:
        assert k in meta, f"AL3 meta missing {k}"

    schema = _load_schema("tspp-trqp-signed-response.schema.json")
    validate_json(body, schema)


@requirements("TSPP-AL3-04")
def test_al3_transparency_uris_resolve(_client):
    expected = os.environ.get("TSPP_EXPECT_AL")
    if expected != "AL3":
        pytest.skip("Not in AL3 mode")

    r = _client.get_metadata()
    assert r.status_code == 200, f"expected 200, got {r.status_code}: {r.text}"
    m = r.json()

    t = m.get("transparency", {})
    assert "change_log_uri" in t, "AL3 requires transparency.change_log_uri"
    assert "published_at" in t, "AL3 requires transparency.published_at"

    # Best-effort fetch (200 expected for conformant deployments)
    import requests
    rr = requests.get(t["change_log_uri"], timeout=10)
    assert rr.status_code == 200, f"expected 200 from change_log_uri, got {rr.status_code}"
