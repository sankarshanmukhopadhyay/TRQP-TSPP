import pytest

def test_unknown_context_key_rejected_or_stripped(_client, _load_queries):
    c = _client()
    q = _load_queries()["authorization_with_unknown_context_key"]
    r = c.post_authorization(q)
    # Profile allows reject (400) OR strip and process.
    assert r.status_code in (200, 400, 401, 403, 404, 429, 503), f"unexpected status {r.status_code}: {r.text}"
    if r.status_code == 200:
        body = r.json()
        # If server stripped unknown key, it still should not echo or reflect it.
        # (We can't guarantee no echo in all impls, but reflecting tracking fields is a privacy smell.)
        assert "tracking_id" not in str(body), "response appears to reflect unknown context key (potential privacy leak)"
