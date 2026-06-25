"""Lifecycle/status publication checks for TSPP metadata.

These checks make revocation and renewal operationally visible. A registry can
claim strong assurance only if relying parties can discover where lifecycle
state changes are published and how quickly they are expected to appear.
"""

from urllib.parse import urlparse

import pytest
import requests

from tspp_trqp_harness.reporting import requirements


@requirements("TSPP-LIFE-01", "TSPP-LIFE-02")
def test_lifecycle_publication_metadata(_client):
    r = _client.get_metadata()
    if r.status_code != 200:
        pytest.skip("metadata not available")

    data = r.json()
    lifecycle = data.get("lifecycle_publication")
    assert isinstance(lifecycle, dict), "metadata.lifecycle_publication is required for lifecycle-aware deployments"
    assert lifecycle.get("supported") is True
    assert lifecycle.get("revocation_supported") is True
    assert isinstance(lifecycle.get("sla_seconds"), int)
    assert lifecycle["sla_seconds"] >= 0

    states = set(lifecycle.get("states") or [])
    assert "active" in states
    assert "revoked" in states

    status_uri = lifecycle.get("status_feed_uri")
    parsed = urlparse(status_uri)
    assert parsed.scheme in {"http", "https"} and parsed.netloc
    assert parsed.path, "status_feed_uri must include a path"


@requirements("TSPP-LIFE-03")
def test_lifecycle_status_feed_resolves(_client):
    r = _client.get_metadata()
    if r.status_code != 200:
        pytest.skip("metadata not available")

    lifecycle = r.json().get("lifecycle_publication") or {}
    status_uri = lifecycle.get("status_feed_uri")
    if not status_uri:
        pytest.skip("lifecycle status_feed_uri not declared")

    rr = requests.get(status_uri, timeout=10)
    assert rr.status_code == 200, f"expected 200 from lifecycle status feed, got {rr.status_code}"
    body = rr.json()
    assert isinstance(body.get("entries"), list), "lifecycle status feed must contain entries array"
    assert body.get("generated_at"), "lifecycle status feed must contain generated_at"
