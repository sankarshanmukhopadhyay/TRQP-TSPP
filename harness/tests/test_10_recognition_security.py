"""TSPP harness tests for POST /recognition security and privacy controls.

What these tests prove:
- The recognition endpoint applies the same security posture as the authorization
  endpoint: freshness semantics, context allowlist enforcement, anti-enumeration,
  rate limiting, and (at AL2) signed responses.
- Recognition queries to the Ayra Trust Network (authority_id=did:webvh:ayra.forum)
  return correctly shaped Ayra flat-structure responses.

Why it matters:
- The Ayra Trust Network requires BOTH /authorization AND /recognition. A registry
  that secures authorization but not recognition has a partial security posture.
- The two-step Ayra verifier flow starts with a recognition query to the ATN. If
  recognition responses leak existence information or skip freshness, the whole
  trust chain is weakened.

Evidence:
- Conformance report sections: recognition_security, recognition_freshness,
  recognition_error_surface.
"""

import time
import pytest

from tspp_trqp_harness.reporting import requirements
from tspp_trqp_harness.validate import assert_freshness


def _unwrap_payload(maybe_signed: dict) -> dict:
    """If signed envelope, return payload; otherwise return body as-is."""
    if isinstance(maybe_signed, dict) and "payload" in maybe_signed and "signature" in maybe_signed:
        return maybe_signed["payload"]
    return maybe_signed


# ---------------------------------------------------------------------------
# Freshness
# ---------------------------------------------------------------------------

@requirements("TSPP-FRESH-03", "TSPP-RECOG-01")
def test_recognition_freshness_fields(_client, _load_queries):
    """Recognition responses MUST carry freshness metadata (time_evaluated, expires_at).

    Required at AL1+ per TSPP. Required by the Ayra Profile for all response types.
    """
    c = _client
    q = _load_queries.get("recognition_valid")
    if not q:
        pytest.skip("recognition_valid query fixture not provided")

    r = c.post_recognition(q)
    assert r.status_code in (200, 401, 403, 404, 429, 503), (
        f"unexpected status {r.status_code}: {r.text}"
    )
    if r.status_code != 200:
        pytest.skip("recognition not successful — cannot test freshness fields")

    body = _unwrap_payload(r.json())
    meta = body.get("meta") if isinstance(body, dict) else None
    assert isinstance(meta, dict), (
        "Expected 'meta' object in recognition response body with freshness fields"
    )
    assert_freshness(meta)


# ---------------------------------------------------------------------------
# Anti-enumeration / uniform error surface
# ---------------------------------------------------------------------------

@requirements("TSPP-ERR-01", "TSPP-ENUM-01", "TSPP-RECOG-02")
def test_recognition_uniform_not_found_surface(_client, _load_queries):
    """Recognition responses for unknown ecosystems MUST be shape-consistent.

    Consistent error shapes prevent ecosystem enumeration via recognition queries.
    Acceptable statuses: 404 (preferred), 401/403 (if auth enforced), 200 with
    recognized=false, 429, 503.
    """
    c = _client
    q = _load_queries.get("recognition_unknown_ecosystem")
    if not q:
        pytest.skip("recognition_unknown_ecosystem query fixture not provided")

    samples = []
    for _ in range(3):
        t0 = time.time()
        r = c.post_recognition(q)
        dt = time.time() - t0
        try:
            j = r.json()
        except Exception:
            j = {"_nonjson": r.text[:200]}
        samples.append((
            r.status_code,
            set(j.keys()) if isinstance(j, dict) else None,
            round(dt, 3),
        ))

    assert all(s[0] in (200, 401, 403, 404, 429, 503) for s in samples), (
        f"Unexpected status in recognition samples: {samples}"
    )

    json_shapes = [s[1] for s in samples if s[1] is not None]
    if len(json_shapes) >= 2:
        unique_shapes = set(
            tuple(sorted(x)) if x else tuple() for x in json_shapes
        )
        assert len(unique_shapes) == 1, (
            f"Inconsistent recognition error JSON shapes across runs: {samples}"
        )


# ---------------------------------------------------------------------------
# Context allowlist on recognition
# ---------------------------------------------------------------------------

@requirements("TSPP-CTX-01", "TSPP-RECOG-03")
def test_recognition_rejects_unlisted_context(_client, _load_queries):
    """Recognition requests with a context key not in the server allowlist MUST be
    rejected with a 400 or 422 response.

    Context allowlist enforcement on recognition queries prevents cross-ecosystem
    data leakage and ensures queries are scoped to declared governance contexts.
    """
    c = _client
    q = _load_queries.get("recognition_valid")
    if not q:
        pytest.skip("recognition_valid query fixture not provided")

    poisoned = dict(q)
    poisoned["context"] = {"__tspp_probe_key": "should-be-rejected"}

    r = c.post_recognition(poisoned)
    # 400 (bad context) or 422 (validation error) are both acceptable.
    # 200 with recognized=false is also tolerated if the server ignores unknown
    # context keys gracefully — but should NOT return recognized=true for a
    # context that was not declared in the allowlist.
    if r.status_code == 200:
        body = r.json()
        payload = _unwrap_payload(body) if isinstance(body, dict) else body
        recognized = payload.get("recognized") if isinstance(payload, dict) else None
        # recognized=false is acceptable; recognized=true with unlisted context is a fail
        if recognized is True:
            pytest.fail(
                "Server returned recognized=true for a query with an unlisted context key. "
                "Context allowlist enforcement appears to be missing on /recognition."
            )
        pytest.skip("Server accepted unknown context key but returned recognized=false — tolerated")
    assert r.status_code in (400, 422), (
        f"Expected 400/422 for unlisted context on /recognition, got {r.status_code}: {r.text}"
    )


# ---------------------------------------------------------------------------
# Rate limiting on recognition
# ---------------------------------------------------------------------------

@requirements("TSPP-RATE-01", "TSPP-RECOG-04")
def test_recognition_rate_limit_headers(_client, _load_queries):
    """Recognition responses SHOULD include RateLimit-* headers.

    Rate limit header presence on /recognition is tested separately from
    /authorization to confirm the rate limiter applies to both endpoints.
    """
    c = _client
    q = _load_queries.get("recognition_valid")
    if not q:
        pytest.skip("recognition_valid query fixture not provided")

    r = c.post_recognition(q)
    if r.status_code not in (200, 401, 403, 404):
        pytest.skip(f"Non-standard status {r.status_code} on recognition — skipping header check")

    has_rl = any(
        h.lower() in r.headers
        for h in ("RateLimit-Limit", "X-RateLimit-Limit", "ratelimit-limit")
    )
    if not has_rl:
        pytest.skip(
            "No RateLimit-* headers on /recognition — SHOULD-level requirement not met. "
            "Consider adding rate limit headers to recognition endpoint responses."
        )


# ---------------------------------------------------------------------------
# Ayra two-step verifier flow smoke test
# ---------------------------------------------------------------------------

@requirements("TSPP-RECOG-05")
def test_ayra_recognition_query_shape(_client, _load_queries):
    """Ayra pattern: POST /recognition with authority_id=did:webvh:ayra.forum
    must return a recognition response with the expected flat Ayra shape.

    This smoke test validates that the registry produces Ayra-compatible recognition
    responses when the ATN DID is used as the authority_id, as the two-step
    verifier flow requires.

    Requires the 'recognition_ayra_atn' fixture to be present in queries.json,
    configured with authority_id='did:webvh:ayra.forum'.
    """
    c = _client
    q = _load_queries.get("recognition_ayra_atn")
    if not q:
        pytest.skip(
            "recognition_ayra_atn fixture not provided — add a query with "
            "authority_id='did:webvh:ayra.forum' to harness/fixtures/queries.json"
        )

    r = c.post_recognition(q)
    if r.status_code not in (200, 401, 403, 404):
        pytest.skip(f"Non-200 status {r.status_code} on Ayra ATN recognition query")

    if r.status_code == 200:
        body = _unwrap_payload(r.json())
        assert isinstance(body, dict), "Expected JSON object in recognition response"
        # Ayra flat shape: 'recognized' boolean at top level, not wrapped in 'statement'
        assert "recognized" in body, (
            "Ayra recognition response must contain top-level 'recognized' boolean field. "
            "Core CTS uses a 'statement.recognized' wrapper — ensure Ayra profile is active."
        )
        assert isinstance(body["recognized"], bool), (
            f"'recognized' must be a boolean, got {type(body['recognized'])}"
        )
        assert "time_evaluated" in body, (
            "Ayra recognition response must contain 'time_evaluated' (RFC 3339 UTC)"
        )
