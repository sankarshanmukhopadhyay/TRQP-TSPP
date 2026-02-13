import json
import os
from pathlib import Path
import pytest

from tspp_trqp_harness.reporting import requirements


def _unwrap_payload(maybe_signed: dict) -> dict:
    if isinstance(maybe_signed, dict) and "payload" in maybe_signed and "signature" in maybe_signed:
        return maybe_signed["payload"]
    return maybe_signed


@requirements("TSPP-BRIDGE-01")
def test_bridge_semantic_equivalence_fixtures(_client):
    fixture_path = os.environ.get("TSPP_BRIDGE_FIXTURES")
    if not fixture_path:
        pytest.skip("Set TSPP_BRIDGE_FIXTURES to run bridge semantic equivalence tests.")
    cases = json.loads(Path(fixture_path).read_text(encoding="utf-8")).get("cases", [])
    c = _client

    for case in cases:
        q = case["query"]
        expected = case["expected"]
        r = c.post_authorization(q)
        assert r.status_code == 200, f"expected 200, got {r.status_code}: {r.text}"
        got = _unwrap_payload(r.json())

        # Shallow semantic check: expected keys and values must match.
        # Implementers can extend this with domain-specific equivalence logic.
        for k, v in expected.items():
            assert got.get(k) == v, f"bridge mismatch on {k}: expected {v}, got {got.get(k)}"
