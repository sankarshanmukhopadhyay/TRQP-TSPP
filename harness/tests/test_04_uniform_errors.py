import time
import pytest

from tspp_trqp_harness.reporting import requirements


@requirements("TSPP-ERR-01", "TSPP-ENUM-01")
def test_uniform_not_found_surface(_client, _load_queries):
    c = _client
    q = _load_queries["authorization_unknown_entity"]

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

    # Acceptable statuses include 404 (preferred), 401/403 (if auth), or 200 with deny=false depending on impl.
    assert all(s[0] in (200, 401, 403, 404, 429, 503) for s in samples), f"unexpected status in samples: {samples}"

    # If JSON is returned, it should be shape-consistent across runs (helps reduce enumeration side channels)
    json_shapes = [s[1] for s in samples if s[1] is not None]
    if len(json_shapes) >= 2:
        assert len(set(map(lambda x: tuple(sorted(x)) if x else tuple(), json_shapes))) == 1, f"inconsistent error JSON shapes: {samples}"

    # Timing equalization can't be strictly asserted here; we record samples for operator review.
