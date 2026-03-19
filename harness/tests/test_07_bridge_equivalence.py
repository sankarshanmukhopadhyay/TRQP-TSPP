"""TSPP harness test for bridge semantic equivalence.

What this test proves:
- The TRQP response for a given query matches the expected outcome from the
  system-of-record ground truth declared in the bridge fixture set.
- Semantic equivalence is validated per-fixture-case, not just structurally.

Why it matters:
- A TRQP adapter that passes protocol tests but returns wrong decisions is
  not bridge-equivalent. This test catches that class of failure.

Evidence:
- Conformance report section: bridge_equivalence, requirement TSPP-BRIDGE-01.
"""
import json
import os
from pathlib import Path
import pytest

from tspp_trqp_harness.reporting import requirements

HERE = Path(__file__).resolve().parent
FIXTURES_DIR = HERE.parent / "fixtures"
_DEFAULT_FIXTURE_PATH = FIXTURES_DIR / "bridge_golden_fixtures.json"


def _unwrap_payload(maybe_signed: dict) -> dict:
    if isinstance(maybe_signed, dict) and "payload" in maybe_signed and "signature" in maybe_signed:
        return maybe_signed["payload"]
    return maybe_signed


@requirements("TSPP-BRIDGE-01")
def test_bridge_semantic_equivalence_fixtures(_client):
    # Allow override via env; fall back to the canonical fixture file bundled with the harness.
    fixture_path_str = os.environ.get("TSPP_BRIDGE_FIXTURES")
    if fixture_path_str:
        fixture_path = Path(fixture_path_str)
    else:
        fixture_path = _DEFAULT_FIXTURE_PATH

    if not fixture_path.exists():
        pytest.skip(f"Bridge fixture file not found: {fixture_path}")

    cases = json.loads(fixture_path.read_text(encoding="utf-8")).get("cases", [])
    c = _client

    for case in cases:
        # Support both canonical 'query' and legacy 'trqp_query' keys
        q = case.get("query") or case.get("trqp_query")
        if q is None:
            pytest.fail(f"Bridge fixture case '{case.get('id')}' has no 'query' field")

        # Support both canonical 'expected' dict and legacy 'expected_trqp_outcome' string
        expected = case.get("expected")
        legacy_outcome = case.get("expected_trqp_outcome")

        r = c.post_authorization(q)
        assert r.status_code == 200, f"[{case.get('id')}] expected 200, got {r.status_code}: {r.text}"
        got = _unwrap_payload(r.json())

        if expected is not None:
            # Recursive shallow check: expected keys and values must match in got
            for k, v in expected.items():
                if isinstance(v, dict):
                    for sub_k, sub_v in v.items():
                        actual_sub = got.get(k, {}).get(sub_k) if isinstance(got.get(k), dict) else None
                        assert actual_sub == sub_v, (
                            f"[{case.get('id')}] bridge mismatch on {k}.{sub_k}: "
                            f"expected {sub_v!r}, got {actual_sub!r}"
                        )
                else:
                    assert got.get(k) == v, (
                        f"[{case.get('id')}] bridge mismatch on {k}: expected {v!r}, got {got.get(k)!r}"
                    )
        elif legacy_outcome is not None:
            # Legacy flat check: decision.authorized == expected_trqp_outcome
            decision = got.get("decision", got)
            actual = decision.get("authorized") if isinstance(decision, dict) else got.get("authorized")
            assert str(actual).lower() == str(legacy_outcome).lower(), (
                f"[{case.get('id')}] bridge mismatch: expected authorized={legacy_outcome!r}, got {actual!r}"
            )
