# Output Contract: TSPP Harness Runs

This document defines the **stable output artifact** produced by the TSPP harness when `TSPP_REPORT_PATH` is set.

It exists so operators can reliably archive evidence and automation pipelines can validate runs without parsing CI logs.

## JSON report

When you run the harness with `TSPP_REPORT_PATH=...`, a JSON report is written at that path.

Example directory layout:

```
reports/
  tspp_conformance_AL1.json
  tspp_conformance_AL2.json
```

### Report schema (shape)

The report is a single JSON object with these keys:

- `profile` — fixed identifier for the harness profile (currently `TSPP-TRQP-0.1`)
- `generated_at` — timestamp for the report (UTC ISO 8601)
- `target`
  - `base_url`
  - `expected_assurance_level`
- `summary`
  - `exit_status`
  - counts by outcome: `PASS`, `FAIL`, `SKIP`, `NOT_APPLICABLE`, `ERROR`, `XFAIL`
- `results[]`
  - `nodeid`
  - `name`
  - `outcome`
  - `duration_seconds`
  - `requirement_ids[]`
  - `notes` (optional)

## CLI runner (Increment 2)

The harness can be run either via `pytest` directly (as CI does today) or via the wrapper CLI:

```
python -m pip install -r harness/requirements.txt
python -m pip install -e harness

tspp-harness \
  --base-url http://127.0.0.1:8001 \
  --bearer-token dev-token \
  --expected-al AL1 \
  --report-path reports/tspp_conformance_AL1.json
```

This CLI simply sets the standard environment variables and invokes pytest against `harness/tests`.
