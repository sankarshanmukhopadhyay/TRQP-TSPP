import os
import json
from pathlib import Path
from typing import Any, Dict, List, Optional

import pytest

from tspp_trqp_harness.client import TRQPClient
from tspp_trqp_harness.reporting import TestResult, utc_now_iso

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
FIXTURES = ROOT / "fixtures"
SCHEMAS = ROOT.parent / "schemas" / "core"


# -------------------------
# Fixtures
# -------------------------

@pytest.fixture
def _client() -> TRQPClient:
    base = os.environ.get("TRQP_BASE_URL")
    if not base:
        pytest.skip("TRQP_BASE_URL not set")
    token = os.environ.get("TRQP_BEARER_TOKEN")
    dpop = os.environ.get("TRQP_DPOP")
    return TRQPClient(base_url=base, token=token, dpop=dpop)


@pytest.fixture
def _load_queries() -> Dict[str, Any]:
    return json.loads((FIXTURES / "queries.json").read_text(encoding="utf-8"))


@pytest.fixture
def _load_schema():
    def _inner(name: str) -> Dict[str, Any]:
        return json.loads((SCHEMAS / name).read_text(encoding="utf-8"))
    return _inner


# -------------------------
# Reporting (optional)
# -------------------------
# Enable by setting:
#   TSPP_REPORT_PATH=./tspp_conformance_report.json
#
# The report is intentionally lightweight and CI-friendly.

def _get_req_ids(item) -> List[str]:
    try:
        fn = item.obj
        return list(getattr(fn, "TSPP_REQUIREMENTS", []))
    except Exception:
        return []


def pytest_configure(config):
    config._tspp_results: List[TestResult] = []
    config._tspp_req_map: Dict[str, List[str]] = {}


def pytest_collection_modifyitems(config, items):
    for item in items:
        config._tspp_req_map[item.nodeid] = _get_req_ids(item)


def pytest_runtest_logreport(report):
    # Only capture the actual test call result (skip setup/teardown noise)
    if report.when != "call":
        return

    cfg = report.config
    nodeid = report.nodeid
    reqs = cfg._tspp_req_map.get(nodeid, [])

    outcome_raw = report.outcome  # passed|failed|skipped
    if report.outcome == "failed" and getattr(report, "wasxfail", False):
        outcome_raw = "xfailed"

    # Normalize outcomes to a shared TRQP taxonomy
    if outcome_raw == "passed":
        outcome = "PASS"
    elif outcome_raw == "failed":
        outcome = "FAIL"
    elif outcome_raw == "xfailed":
        outcome = "XFAIL"
    elif outcome_raw == "skipped":
        # Treat explicit 'not applicable' skips as NOT_APPLICABLE
        lr = str(report.longrepr) if report.longrepr else ""
        outcome = "NOT_APPLICABLE" if "not applicable" in lr.lower() else "SKIP"
    else:
        outcome = "ERROR"


    notes: Optional[str] = None
    if report.longrepr:
        # Keep this short; details belong in CI logs
        try:
            notes = str(report.longrepr)[:1000]
        except Exception:
            notes = "see test output"

    cfg._tspp_results.append(
        TestResult(
            nodeid=nodeid,
            name=report.head_line or nodeid,
            outcome=outcome,
            duration_seconds=float(getattr(report, "duration", 0.0) or 0.0),
            requirement_ids=reqs,
            notes=notes,
        )
    )


def pytest_sessionfinish(session, exitstatus):
    path = os.environ.get("TSPP_REPORT_PATH")
    if not path:
        return

    cfg = session.config
    report_obj: Dict[str, Any] = {
        "profile": "TSPP-TRQP-0.1",
        "generated_at": utc_now_iso(),
        "target": {
            "base_url": os.environ.get("TRQP_BASE_URL"),
            "expected_assurance_level": os.environ.get("TSPP_EXPECT_AL"),
        },
        "summary": {
            "exit_status": exitstatus,
            "PASS": sum(1 for r in cfg._tspp_results if r.outcome == "PASS"),
            "FAIL": sum(1 for r in cfg._tspp_results if r.outcome == "FAIL"),
            "SKIP": sum(1 for r in cfg._tspp_results if r.outcome == "SKIP"),
            "NOT_APPLICABLE": sum(1 for r in cfg._tspp_results if r.outcome == "NOT_APPLICABLE"),
            "ERROR": sum(1 for r in cfg._tspp_results if r.outcome == "ERROR"),
            "XFAIL": sum(1 for r in cfg._tspp_results if r.outcome == "XFAIL"),
        },
        "results": [r.to_dict() for r in cfg._tspp_results],
    }

    out_path = Path(path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(report_obj, indent=2, sort_keys=True), encoding="utf-8")