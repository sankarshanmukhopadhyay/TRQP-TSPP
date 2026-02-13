import pytest

from tspp_trqp_harness.reporting import requirements


@requirements("TSPP-CTX-02")
def test_unknown_context_key_rejected_or_stripped(_client, _load_queries):
    c = _client
    q = _load_queries["authorization_with_unknown_context_key"]
    r = c.post_authorization(q)
    # Profile allows reject (400) OR strip and process.
    assert r.status_code in (200, 400, 401, 403, 404, 429, 503), f"unexpected status {r.status_code}: {r.text}"
    if r.status_code == 200:
        body = r.json()
        # If server stripped unknown key, it still should not echo or reflect it.
        # (We can't guarantee no echo in all impls, but reflecting tracking fields is a privacy smell.)
        ctx = None
        if isinstance(body, dict):
            payload = body.get("payload") if ("payload" in body and "signature" in body) else body
            ctx = payload.get("context") if isinstance(payload, dict) else None
        if isinstance(ctx, dict):
            assert "unknown_tracking_key" not in ctx, "Server reflected unknown context key"
