from __future__ import annotations

import argparse
import os
from pathlib import Path

import pytest


def main() -> int:
    ap = argparse.ArgumentParser(
        prog="tspp-harness",
        description="Run the TRQP TSPP conformance harness and optionally emit a JSON report.",
    )
    ap.add_argument("--base-url", required=False, help="TRQP base URL (or set TRQP_BASE_URL)")
    ap.add_argument("--bearer-token", required=False, help="Bearer token (or set TRQP_BEARER_TOKEN)")
    ap.add_argument("--expected-al", required=False, help="Expected assurance level (AL1|AL2|AL3|AL4) (or set TSPP_EXPECT_AL)")
    ap.add_argument("--report-path", required=False, help="Write JSON report to this path (or set TSPP_REPORT_PATH)")
    ap.add_argument("--pytest-args", nargs=argparse.REMAINDER, default=[], help="Extra args passed to pytest after '--'")
    args = ap.parse_args()

    if args.base_url:
        os.environ["TRQP_BASE_URL"] = args.base_url
    if args.bearer_token:
        os.environ["TRQP_BEARER_TOKEN"] = args.bearer_token
    if args.expected_al:
        os.environ["TSPP_EXPECT_AL"] = args.expected_al
    if args.report_path:
        os.environ["TSPP_REPORT_PATH"] = args.report_path

    # Default: run harness tests directory
    here = Path(__file__).resolve().parent
    tests_dir = (here.parent / "tests").resolve()

    pytest_args = ["-q", str(tests_dir)] + list(args.pytest_args or [])
    return int(pytest.main(pytest_args))


if __name__ == "__main__":
    raise SystemExit(main())
