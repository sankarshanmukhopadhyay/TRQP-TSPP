import json, os
from pathlib import Path
import pytest

def _unwrap_payload(maybe_signed: dict) -> dict:
    if isinstance(maybe_signed, dict) and "payload" in maybe_signed and "signature" in maybe_signed:
        return maybe_signed["payload"]
    return maybe_signed

def test_bridge_semantic_equivalence_fixtures(_client):
    fixture_path = os.environ.get("TSPP_BRIDGE_FIXTURES")
    if not fixture_path:
        pytest.skip("Set TSPP_BRIDGE_FIXTURES to run bridge semantic equivalence tests.")
    cases = json.loads(Path(fixture_path).read_text())["cases"]
    c = _client()

    for case in cases:
        q = case["trqp_query"]
        expected = case["expected_trqp_outcome"]
        r = c.post_authorization(q)
        assert r.status_code == 200, f"{case['id']}: expected 200, got {r.status_code}: {r.text}"
        body = _unwrap_payload(r.json())
        got = body.get("authorized")
        assert got == expected, f"{case['id']}: expected {expected}, got {got}"
