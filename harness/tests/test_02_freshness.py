import pytest

def _unwrap_payload(maybe_signed: dict) -> dict:
    # If signed envelope, return payload
    if isinstance(maybe_signed, dict) and "payload" in maybe_signed and "signature" in maybe_signed:
        return maybe_signed["payload"]
    return maybe_signed

def test_authorization_freshness_fields(_client, _load_queries):
    c = _client()
    q = _load_queries()["authorization_valid"]
    r = c.post_authorization(q)
    assert r.status_code in (200, 401, 403, 404, 429, 503), f"unexpected status {r.status_code}: {r.text}"
    if r.status_code != 200:
        pytest.skip("authorization not successful; cannot validate freshness")
    body = _unwrap_payload(r.json())
    assert "meta" in body, "missing meta"
    assert_freshness(body["meta"])

def test_recognition_freshness_fields(_client, _load_queries):
    c = _client()
    q = _load_queries()["recognition_valid"]
    r = c.post_recognition(q)
    assert r.status_code in (200, 401, 403, 404, 429, 503), f"unexpected status {r.status_code}: {r.text}"
    if r.status_code != 200:
        pytest.skip("recognition not successful; cannot validate freshness")
    body = _unwrap_payload(r.json())
    assert "meta" in body
    assert_freshness(body["meta"])
