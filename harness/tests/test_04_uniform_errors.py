import pytest
import time

def test_uniform_not_found_surface(_client, _load_queries):
    c = _client()
    q = _load_queries()["authorization_unknown_entity"]

    # Run a few times to observe status/body shape
    samples = []
    for _ in range(3):
        t0 = time.time()
        r = c.post_authorization(q)
        dt = time.time() - t0
        try:
            j = r.json()
        except Exception:
            j = {"_nonjson": r.text[:200]}
        samples.append((r.status_code, set(j.keys()) if isinstance(j, dict) else None, round(dt, 3)))

    # Acceptable statuses include 404 (preferred), 200 (if registry returns explicit false/indeterminate),
    # or 400 (if request invalid). Any of these can be policy choices; the goal is to avoid detailed leakage.
    for code, keys, dt in samples:
        assert code in (200, 400, 404, 401, 403, 429, 503), f"unexpected status {code}"

    # Heuristic check: if 404 used, body should be uniform ErrorResponse-like (error/message/meta)
    for code, keys, _ in samples:
        if code == 404 and keys:
            assert {"error", "message", "meta"}.issubset(keys), f"404 body missing expected keys: {keys}"
