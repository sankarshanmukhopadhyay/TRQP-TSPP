# TRQP Security & Privacy Baseline (TSPP)

![License](https://img.shields.io/github/license/sankarshanmukhopadhyay/TRQP-TSPP)
![Last Commit](https://img.shields.io/github/last-commit/sankarshanmukhopadhyay/TRQP-TSPP)
![Issues](https://img.shields.io/github/issues/sankarshanmukhopadhyay/TRQP-TSPP)
![TRQP](https://img.shields.io/badge/TRQP-Protocol-blue)
![Trust over IP](https://img.shields.io/badge/Trust%20over%20IP-Alignment-0A66C2)
![Security Profile](https://img.shields.io/badge/Security-Profile-critical)
![Conformance](https://img.shields.io/badge/Conformance-Harness-brightgreen)
![Assurance Levels](https://img.shields.io/badge/Assurance-AL1%20%7C%20AL2-purple)

This repository packages a practical, implementer-ready **security and privacy profile** for the Trust Over IP
**Trust Registry Query Protocol (TRQP)**, along with machine-readable artifacts and a conformance harness.

If TRQP becomes the *query plane* for institutional trust, this repo is the seatbelt kit: it converts high-level
security considerations into enforceable requirements, and ships tooling to test deployments against them.

## What’s in here

- **OpenAPI contract** (`openapi/tspp-trqp-openapi.yaml`)  
  An HTTP-level contract capturing profile-required headers/fields, freshness semantics, and optional AL2 signed envelopes.

- **JSON Schemas** (`schemas/`)  
  - `tspp-trqp-metadata.schema.json` — machine-readable declaration of a registry’s posture and constraints  
  - `tspp-trqp-signed-response.schema.json` — AL2 signed response envelope schema

- **Conformance harness** (`harness/`)  
  A pytest-based harness that validates metadata, freshness, context allowlisting, rate limiting evidence,
  anti-enumeration heuristics, optional AL2 signed envelopes, and optional bridge equivalence fixtures.

- **Docs** (`docs/`)  
  - `profile.md` — the profile summary and requirements map  
  - `threat-model.md` — adversarial model of likely harms  
  - `deployment-guidance.md` — operator-focused rollout sequence

- **Examples** (`examples/`)  
  Sample queries and bridge golden fixtures.

## Quick start (run the harness)

### 1) Install dependencies
```bash
cd harness
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2) Configure environment
```bash
export TRQP_BASE_URL="https://your-registry.example"
export TRQP_BEARER_TOKEN="..."   # if required by your deployment
export TRQP_DPOP="..."           # optional (if using DPoP)
export TSPP_EXPECT_AL="AL1"      # or AL2
```

### 3) Update fixtures
Edit `harness/fixtures/queries.json` to replace placeholder identifiers (`did:example:*`) and vocab URIs with
values valid in your environment.

### 4) Run tests
```bash
pytest -q
```

## Conformance levels

- **AL1 (Baseline / Internet-safe)**  
  Minimum posture for internet exposure: freshness semantics, context allowlisting, rate limiting evidence,
  and safe client semantics.

- **AL2 (High Assurance / Critical infrastructure)**  
  Tightened posture: authenticated access required, sender-constrained tokens for bulk clients, stronger
  anti-enumeration expectations, and signed response envelopes.

## What this repo does *not* do

- It does not define governance frameworks.
- It does not decide relying-party policy (fail-open vs fail-closed).
- It does not magically eliminate network-layer correlation (architecture still matters).

## License

Apache 2.0 (see `LICENSE`).

## Conformance report output

The harness can emit a machine-readable conformance report artifact (JSON) suitable for CI pipelines.

```bash
cd harness
export TRQP_BASE_URL="https://example.org"
export TSPP_EXPECT_AL="AL1"   # or AL2
export TSPP_REPORT_PATH="./tspp_conformance_report.json"
pytest -q
```

Report schema: `harness/schemas/tspp-conformance-report.schema.json`.



## Repo hygiene and assurance artifacts

- Schema checks: `python scripts/schema_check.py`
- Preflight (optional): `python scripts/preflight.py --base-url https://your-sut/ --endpoint /.well-known/jwks.json`
- Traceability template: `docs/traceability.md`
- Evidence bundle guidance: `docs/evidence_bundles.md`
