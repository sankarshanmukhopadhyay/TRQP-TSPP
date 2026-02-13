import os
import pytest

from tspp_trqp_harness.reporting import requirements
from tspp_trqp_harness.validate import validate_json


@requirements("TSPP-META-01", "TSPP-META-02")
def test_metadata_published_and_valid(_client, _load_schema):
    c = _client
    r = c.get_metadata()
    assert r.status_code == 200, f"metadata status {r.status_code}: {r.text}"
    data = r.json()

    schema = _load_schema("tspp-trqp-metadata.schema.json")
    validate_json(data, schema)

    expected = os.environ.get("TSPP_EXPECT_AL")
    if expected:
        assert data.get("assurance_level") == expected, f"Expected assurance_level={expected}, got {data.get('assurance_level')}"


@requirements("TSPP-CTX-01")
def test_metadata_declares_context_allowlist(_client):
    c = _client
    r = c.get_metadata()
    if r.status_code != 200:
        pytest.skip("metadata not available")
    data = r.json()
    assert "context_allowlist" in data
    assert isinstance(data["context_allowlist"], list)
