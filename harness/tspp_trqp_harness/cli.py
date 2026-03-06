"""TSPP harness CLI wrapper.

This provides a stable operator interface around the pytest-based harness so CI and
humans run the same command shape.

The CLI:
- configures the SUT base URL and expected AL via env vars
- sets an optional report output path
- invokes pytest for the harness test suite
"""
from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path

DEFAULT_TEST_PATH = str(Path(__file__).resolve().parent.parent / "tests")

def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="tspp-harness")
    p.add_argument("--base-url", required=True, help="Base URL for the TRQP SUT (e.g., http://127.0.0.1:8000)")
    p.add_argument("--expect-al", choices=["AL1","AL2","AL3","AL4"], required=True, help="Assurance level expectation")
    p.add_argument("--report-path", default="", help="Path for JSON report output (optional)")
    p.add_argument("--tests", default=DEFAULT_TEST_PATH, help="Path to harness tests")
    p.add_argument("--pytest-args", nargs=argparse.REMAINDER, default=[], help="Additional args passed to pytest")
    args = p.parse_args(argv)

    os.environ["TRQP_BASE_URL"] = args.base_url
    os.environ["TSPP_BASE_URL"] = args.base_url
    os.environ["TSPP_EXPECT_AL"] = args.expect_al
    if args.report_path:
        os.environ["TSPP_REPORT_PATH"] = args.report_path

    cmd = [sys.executable, "-m", "pytest", args.tests] + args.pytest_args
    return subprocess.call(cmd)

if __name__ == "__main__":
    raise SystemExit(main())
