import os
import pytest
from jwcrypto import jwk, jws

from tspp_trqp_harness.reporting import requirements
from tspp_trqp_harness.validate import validate_json


def _unwrap_if_signed(body: dict):
    if "payload" in body and "signature" in body:
        return body["payload"], body["signature"]
    return body, None


@requirements("TSPP-AL2-01")
def test_al2_signed_response_envelope_shape(_client, _load_queries, _load_schema):
    expected = os.environ.get("TSPP_EXPECT_AL")
    if expected != "AL2":
        pytest.skip("Not in AL2 mode")

    c = _client
    q = _load_queries["authorization_valid"]
    r = c.post_authorization(q, accept_signature="jws")
    assert r.status_code == 200, f"expected 200, got {r.status_code}: {r.text}"

    body = r.json()
    payload, sig = _unwrap_if_signed(body)
    assert sig is not None, "Expected signed response envelope with 'signature' field in AL2"
    assert isinstance(payload, dict), "payload must be an object"

    schema = _load_schema("tspp-trqp-signed-response.schema.json")
    validate_json(body, schema)


@requirements("TSPP-AL2-02")
def test_al2_signed_response_verifies_with_jwks(_client, _load_queries):
    expected = os.environ.get("TSPP_EXPECT_AL")
    if expected != "AL2":
        pytest.skip("Not in AL2 mode")

    c = _client
    q = _load_queries["authorization_valid"]
    r = c.post_authorization(q, accept_signature="jws")
    assert r.status_code == 200, f"expected 200, got {r.status_code}: {r.text}"

    body = r.json()
    payload, sig = _unwrap_if_signed(body)
    assert sig, "Expected signature in AL2 response"

    # Fetch JWKS and verify JWS
    m = c.get_metadata()
    if m.status_code != 200:
        pytest.skip("metadata not available for jwks discovery")
    md = m.json()
    jwks_uri = md.get("signing", {}).get("jwks_uri")
    if not jwks_uri:
        pytest.skip("jwks_uri not declared")

    import requests
    try:
        resp = requests.get(jwks_uri, timeout=10)
        resp.raise_for_status()
        jwks = resp.json()
    except Exception as e:
        pytest.fail(f"Failed to fetch/parse JWKS from {jwks_uri}: {e}")
    keys = jwks.get("keys", [])
    assert keys, "JWKS has no keys"

    verifier = jws.JWS()
    verifier.deserialize(sig)

    verified = False
    for k in keys:
        try:
            key = jwk.JWK.from_json(__import__("json").dumps(k))
            verifier.verify(key)
            verified = True
            break
        except Exception:
            continue
    assert verified, "Could not verify AL2 response signature with declared JWKS"
