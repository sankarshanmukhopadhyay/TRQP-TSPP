import os
import json
import uuid
from pathlib import Path
from typing import Any, Dict, List, Optional

import pytest

from tspp_trqp_harness.client import TRQPClient
from tspp_trqp_harness.reporting import TestResult, utc_now_iso

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
FIXTURES = ROOT / "fixtures"
SCHEMAS = ROOT.parent / "schemas" / "core"
VERSION = (ROOT.parent / "VERSION").read_text(encoding="utf-8").strip()


# -------------------------
# Fixtures
# -------------------------

_TSPP_PYTEST_CONFIG = None

@pytest.fixture
def _client() -> TRQPClient:
    base = os.environ.get("TRQP_BASE_URL") or os.environ.get("TSPP_BASE_URL")
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
    global _TSPP_PYTEST_CONFIG
    _TSPP_PYTEST_CONFIG = config
    config._tspp_results: List[TestResult] = []
    config._tspp_req_map: Dict[str, List[str]] = {}


def pytest_collection_modifyitems(config, items):
    for item in items:
        config._tspp_req_map[item.nodeid] = _get_req_ids(item)


def pytest_runtest_logreport(report):
    # Only capture the actual test call result (skip setup/teardown noise)
    if report.when != "call":
        return

    cfg = _TSPP_PYTEST_CONFIG
    if cfg is None:
        return
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


def _compute_summary_metrics(results: List[TestResult], exit_status: int) -> Dict[str, Any]:
    """Compute summary counts and derived posture/coverage metrics.

    These metrics are emitted in every TSPP report and must match the golden
    flow sample shape so the Assurance Hub generate-manifest.py can ingest them.
    """
    pass_count = sum(1 for r in results if r.outcome == "PASS")
    fail_count = sum(1 for r in results if r.outcome == "FAIL")
    skip_count = sum(1 for r in results if r.outcome == "SKIP")
    na_count = sum(1 for r in results if r.outcome == "NOT_APPLICABLE")
    error_count = sum(1 for r in results if r.outcome == "ERROR")
    xfail_count = sum(1 for r in results if r.outcome == "XFAIL")

    applicable = len(results) - na_count
    evaluated = pass_count + fail_count + error_count + xfail_count
    coverage_index = round((evaluated / applicable) * 100.0, 2) if applicable else 100.0
    posture_score = round((pass_count / applicable) * 100.0, 2) if applicable else 100.0

    return {
        "exit_status": exit_status,
        "PASS": pass_count,
        "FAIL": fail_count,
        "SKIP": skip_count,
        "NOT_APPLICABLE": na_count,
        "ERROR": error_count,
        "XFAIL": xfail_count,
        "posture_score": posture_score,
        "coverage_index": coverage_index,
        "control_satisfaction": {
            "applicable_checks": applicable,
            "evaluated_checks": evaluated,
            "passed_checks": pass_count,
            "failed_checks": fail_count,
            "skipped_checks": skip_count,
            "not_applicable_checks": na_count,
        },
    }


def pytest_sessionfinish(session, exitstatus):
    path = os.environ.get("TSPP_REPORT_PATH")
    if not path:
        return

    cfg = session.config
    summary = _compute_summary_metrics(cfg._tspp_results, int(exitstatus))

    report_obj: Dict[str, Any] = {
        "profile": "TSPP-TRQP-0.1",
        "generated_at": utc_now_iso(),
        "run_id": os.environ.get("TSPP_RUN_ID") or str(uuid.uuid4()),
        "target_id": os.environ.get("TSPP_TARGET_ID") or (os.environ.get("TRQP_BASE_URL") or os.environ.get("TSPP_BASE_URL")),
        "assurance_level": os.environ.get("TSPP_EXPECT_AL"),
        "tool_version": VERSION,
        "tool": {"name": "trqp-tspp", "version": VERSION},
        "target": {
            "base_url": os.environ.get("TRQP_BASE_URL") or os.environ.get("TSPP_BASE_URL"),
            "expected_assurance_level": os.environ.get("TSPP_EXPECT_AL"),
        },
        "summary": summary,
        "results": [r.to_dict() for r in cfg._tspp_results],
    }

    out_path = Path(path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(report_obj, indent=2, sort_keys=True), encoding="utf-8")


# -------------------------
# Bridge fixture schema validation
# -------------------------

def pytest_sessionstart(session):
    """Validate the bundled bridge fixture file against its schema at session start.

    This catches fixture drift early, before any tests run. Failures are
    reported as warnings rather than errors to avoid blocking the whole suite
    when a fixture file is intentionally under construction.
    """
    import warnings
    try:
        from jsonschema import Draft202012Validator
        schema_path = ROOT.parent / "harness" / "schemas" / "tspp-bridge-fixtures.schema.json"
        fixture_path_str = os.environ.get("TSPP_BRIDGE_FIXTURES")
        fixture_path = Path(fixture_path_str) if fixture_path_str else FIXTURES / "bridge_golden_fixtures.json"

        if not schema_path.exists() or not fixture_path.exists():
            return

        schema = json.loads(schema_path.read_text(encoding="utf-8"))
        instance = json.loads(fixture_path.read_text(encoding="utf-8"))
        errors = list(Draft202012Validator(schema).iter_errors(instance))
        if errors:
            msgs = "; ".join(e.message for e in errors[:3])
            warnings.warn(f"Bridge fixture schema validation failed: {msgs}", stacklevel=1)
    except Exception as exc:
        warnings.warn(f"Bridge fixture schema validation skipped: {exc}", stacklevel=1)
