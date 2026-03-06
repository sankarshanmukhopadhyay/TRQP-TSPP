# TSPP TRQP Conformance Harness

This harness runs HTTP-level and semantic conformance checks for a TRQP deployment against the TRQP Security & Privacy Profile (TSPP).

It is intentionally profile-first:

- validates required freshness semantics (`time_evaluated`, `expires_at`)
- checks metadata publication and declared constraints
- exercises rate limiting
- probes anti-enumeration behavior (uniform `not_found` surface)
- validates context allowlisting behavior
- validates tri-state client outcomes
- (AL2) validates signed response envelope shape and verifies JWS with JWKS
- (AL3) validates independent assessment URI, change control URI, and default signing declarations
- (AL4) validates key protection, monitoring runbook, policy and rollback URIs, and audit log declarations

## Quick start

### 1. Install dependencies

```bash
cd harness
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Set environment variables

```bash
export TRQP_BASE_URL="https://your-registry.example"
export TRQP_BEARER_TOKEN="..."   # optional depending on your deployment
export TRQP_DPOP="..."           # optional (if using DPoP)
export TSPP_EXPECT_AL="AL1"      # AL1 | AL2 | AL3 | AL4
```

### 3. Update fixtures

Edit `fixtures/queries.json` to replace `did:example:*` identifiers with values valid in your environment.

### 4. Run tests

```bash
pytest -q
```

## Configuration reference

| Variable | Purpose | Required |
|---|---|---|
| `TRQP_BASE_URL` | Base URL of the SUT (e.g., `https://trqp.example.org`) | Yes |
| `TRQP_BEARER_TOKEN` | Bearer token for authenticated endpoints | No |
| `TRQP_DPOP` | DPoP proof (if using DPoP) | No |
| `TSPP_EXPECT_AL` | Expected assurance level (`AL1`–`AL4`) | No |
| `TSPP_REQUIRE_SIGNED` | `true` / `false` — enforce signed responses | No |
| `TSPP_REPORT_PATH` | Path to write JSON conformance report | No |

See `CONFIG.md` for extended configuration notes.

## Assurance level test coverage

| Test file | Assurance level | Controls covered |
|---|---|---|
| `test_01_metadata.py` | AL1+ | Metadata publication, field presence |
| `test_02_freshness.py` | AL1+ | `time_evaluated`, `expires_at` semantics |
| `test_03_context_allowlist.py` | AL1+ | Context allowlisting |
| `test_04_uniform_errors.py` | AL1+ | Uniform `not_found` surface |
| `test_05_ratelimits.py` | AL1+ | Rate limit enforcement |
| `test_06_al2_signed_responses.py` | AL2+ | JWS envelope shape, JWKS verification |
| `test_07_bridge_equivalence.py` | AL2+ | Bridge equivalence fixtures |
| `test_08_al3_controls.py` | AL3 | Independent assessment URI, change control URI, default signing |
| `test_09_al4_controls.py` | AL4 | Key protection, monitoring runbook, policy/rollback URIs, audit log |
| `test_validate_unit.py` | Unit | Validation helper functions (`iso8601_like`, `assert_freshness`, etc.) |

Canonical AL semantics are defined in the TRQP Assurance Hub:
https://github.com/sankarshanmukhopadhyay/trqp-assurance-hub/blob/main/docs/guides/assurance-levels.md

## Reporting

Set `TSPP_REPORT_PATH` to write a JSON conformance report after the run:

```bash
export TSPP_REPORT_PATH=./tspp_conformance_report.json
pytest -q
```

The report includes per-test outcomes and mapped TSPP requirement IDs. Schema: `schemas/tspp-conformance-report.schema.json`.

To package a posture evidence bundle from the report:

```bash
python ../scripts/create_evidence_bundle.py --report tspp_conformance_report.json --out reports/posture-bundle
```

## Notes

Some controls (mTLS, true timing equalization) cannot be fully validated from client-side tests. The harness treats them as "evidence required" controls, with optional operator-provided attestations.
