import os, json, time
from pathlib import Path

import pytest

from tspp_trqp_harness.client import TRQPClient, parse_ratelimit_headers
from tspp_trqp_harness.validate import validate_json, assert_freshness

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
FIXTURES = ROOT / "fixtures"
SCHEMAS = ROOT / "schemas"

def _client():
    base = os.environ.get("TRQP_BASE_URL")
    if not base:
        pytest.skip("TRQP_BASE_URL not set")
    token = os.environ.get("TRQP_BEARER_TOKEN")
    dpop = os.environ.get("TRQP_DPOP")
    return TRQPClient(base_url=base, token=token, dpop=dpop)

def _load_queries():
    return json.loads((FIXTURES / "queries.json").read_text())

def _load_schema(name):
    return json.loads((SCHEMAS / name).read_text())
