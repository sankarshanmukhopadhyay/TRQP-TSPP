import pytest

def test_ratelimit_headers_present_on_429(_client, _load_queries):
    c = _client()
    q = _load_queries()["authorization_valid"]

    # Try a small burst. Not all environments will trigger 429; treat as informational.
    last = None
    for _ in range(20):
        last = c.post_authorization(q)
        if last.status_code == 429:
            hdrs = parse_ratelimit_headers(last)
            # At least one informative header should exist
            assert hdrs, "429 without any rate limit headers"
            return

    pytest.skip("Did not hit 429; cannot assert rate limit headers in this environment.")
