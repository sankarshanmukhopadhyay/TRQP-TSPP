import pytest

from tspp_trqp_harness.reporting import requirements
from tspp_trqp_harness.validate import assert_freshness


def _unwrap_payload(maybe_signed: dict) -> dict:
    # If signed envelope, return payload
    if isinstance(maybe_signed, dict) and "payload" in maybe_signed and "signature" in maybe_signed:
        return maybe_signed["payload"]
    return maybe_signed


@requirements("TSPP-FRESH-01", "TSPP-FRESH-02")
def test_authorization_freshness_fields(_client, _load_queries):
    c = _client
    q = _load_queries["authorization_valid"]
    r = c.post_authorization(q)
    assert r.status_code in (200, 401, 403, 404, 429, 503), f"unexpected status {r.status_code}: {r.text}"
    if r.status_code != 200:
        pytest.skip("authorization not successful")

    body = _unwrap_payload(r.json())
    meta = body.get("meta") if isinstance(body, dict) else None
    assert isinstance(meta, dict), "Expected meta object in response body"
    assert_freshness(meta)


@requirements("TSPP-FRESH-03")
def test_recognition_freshness_fields(_client, _load_queries):
    c = _client
    q = _load_queries.get("recognition_valid")
    if not q:
        pytest.skip("recognition_valid query fixture not provided")
    r = c.post_recognition(q)
    assert r.status_code in (200, 401, 403, 404, 429, 503), f"unexpected status {r.status_code}: {r.text}"
    if r.status_code != 200:
        pytest.skip("recognition not successful")

    body = _unwrap_payload(r.json())
    meta = body.get("meta") if isinstance(body, dict) else None
    assert isinstance(meta, dict), "Expected meta object in response body"
    assert_freshness(meta)
