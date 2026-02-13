# Harness configuration

Use environment variables for secrets:

- `TRQP_BASE_URL` (e.g., https://trqp.example.org)
- `TRQP_BEARER_TOKEN` (optional)
- `TRQP_DPOP` (optional)

Optional:
- `TSPP_EXPECT_AL` = AL1 or AL2 (if you want to enforce expected level)
- `TSPP_REQUIRE_SIGNED` = "true"/"false"

## Conformance report artifact

Set `TSPP_REPORT_PATH` to emit a JSON conformance report after the run.

Example:

```bash
export TSPP_REPORT_PATH=./tspp_conformance_report.json
pytest -q
```
