import os, json
import pytest
from jwcrypto import jwk, jws

def _unwrap_if_signed(body: dict):
    if "payload" in body and "signature" in body:
        return body["payload"], body["signature"]
    return body, None

def test_al2_signed_response_envelope_shape(_client, _load_queries):
    expected = os.environ.get("TSPP_EXPECT_AL")
    if expected != "AL2":
        pytest.skip("Not in AL2 mode")
    c = _client()
    q = _load_queries()["authorization_valid"]
    r = c.post_authorization(q, accept_signature="jws")
    assert r.status_code == 200, f"expected 200, got {r.status_code}: {r.text}"
    body = r.json()
    assert "payload" in body and "signature" in body, "AL2 expected signed envelope, got unsigned response"

def test_al2_verify_jws_if_jwks_available(_client, _load_queries):
    expected = os.environ.get("TSPP_EXPECT_AL")
    if expected != "AL2":
        pytest.skip("Not in AL2 mode")
    c = _client()
    md = c.get_metadata()
    if md.status_code != 200:
        pytest.skip("metadata unavailable")
    meta = md.json()
    jwks_uri = meta.get("signing", {}).get("jwks_uri")
    if not jwks_uri:
        pytest.skip("jwks_uri not advertised; cannot verify JWS")

    # Fetch JWKS
    import requests
    jwks = requests.get(jwks_uri, timeout=10).json()
    keyset = jwk.JWKSet.from_json(json.dumps(jwks))

    q = _load_queries()["authorization_valid"]
    r = c.post_authorization(q, accept_signature="jws")
    assert r.status_code == 200, f"expected 200, got {r.status_code}: {r.text}"
    body = r.json()
    assert "signature" in body and "payload" in body
    sig = body["signature"]
    jws_compact = sig["jws"]

    # Verify JWS signature only (semantic binding to query_hash requires operator-defined signing input).
    # This test provides evidence that signing is enabled and keys are valid.
    token = jws.JWS()
    token.deserialize(jws_compact)
    token.verify(keyset)
