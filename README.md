---
owner: maintainers
last_reviewed: 2026-04-16
tier: 0
---

## Documentation

- Documentation governance: [`docs/governance/README.md`](docs/governance/README.md)

# TRQP Security & Privacy Baseline (TSPP)

📘 **Documentation site (GitHub Pages):** https://sankarshanmukhopadhyay.github.io/TRQP-TSPP/

**Current version:** v0.10.1

**Release line:** Operational Trust Stack v1

![License](https://img.shields.io/github/license/sankarshanmukhopadhyay/TRQP-TSPP)
![Last Commit](https://img.shields.io/github/last-commit/sankarshanmukhopadhyay/TRQP-TSPP)
![Issues](https://img.shields.io/github/issues/sankarshanmukhopadhyay/TRQP-TSPP)
![TRQP](https://img.shields.io/badge/TRQP-Protocol-blue)
![Trust over IP](https://img.shields.io/badge/Trust%20over%20IP-Alignment-0A66C2)
![Security Profile](https://img.shields.io/badge/Security-Profile-critical)
![Conformance](https://img.shields.io/badge/Conformance-Harness-brightgreen)
![Assurance Levels](https://img.shields.io/badge/Assurance-AL1%20%7C%20AL2%20%7C%20AL3%20%7C%20AL4-purple)

TSPP is the **posture computation layer** in the three-repository Operational Trust Stack v1 release line.
It converts TRQP security and privacy expectations into executable checks, control satisfaction evidence,
and a machine-readable **Posture Report** that downstream layers can consume without reinterpretation.

## Where this fits

| Layer | Repository role | Primary output |
|---|---|---|
| TSPP | Posture computation | Posture Report |
| Conformance Suite | Protocol verification | Conformance Report |
| Assurance Hub | Assurance orchestration and publication | Combined Assurance Manifest |

## What is new in v0.10.1

- Stable Posture Report metrics: `posture_score`, `coverage_index`, and `control_satisfaction`
- Golden flow example assets for cross-repo integration
- Public-facing docs synchronized with the Operational Trust Stack v1 narrative
- Cross-repo output contract refreshed for Assurance Hub v1.5.0 and Conformance Suite v1.2.1
- Operational Stack guidance now treats shared `run_id` and `target_id` as a required contract for combined assurance workflows

## Start here

- Operational stack overview: [`docs/operational-stack.md`](docs/operational-stack.md)
- Output contract: [`docs/OUTPUT_CONTRACT.md`](docs/OUTPUT_CONTRACT.md)
- Quickstart: [`QUICKSTART.md`](QUICKSTART.md)
- Hub repo: https://github.com/sankarshanmukhopadhyay/trqp-assurance-hub
- Hub crosswalk for this repo: [`docs/hub-crosswalk.md`](docs/hub-crosswalk.md)

## Why this exists

If TRQP becomes the query plane for institutional trust, TSPP is the layer that keeps security and privacy from
turning into hand-wavy prose. It makes requirements testable, produces portable evidence, and gives operators a way
to show what was checked, what passed, and what remains outside scope.

- **JSON Schemas** (`schemas/`)
  - `schemas/core/tspp-trqp-metadata.schema.json` — machine-readable declaration of a registry's posture and constraints
  - `schemas/core/tspp-trqp-signed-response.schema.json` — AL2 signed response envelope schema
  - `schemas/ayra/did_webvh_validator.py` — did:webvh format validator for Ayra deployments

- **Conformance harness** (`harness/`)
  A pytest-based harness validating metadata, freshness, context allowlisting, rate limiting, anti-enumeration,
  AL2 signed envelopes, bridge equivalence, and recognition endpoint security.

- **Docs** (`docs/`)
  - `profile.md` — the profile summary and requirements map
  - `threat-model.md` — adversarial model of likely harms
  - `deployment-guidance.md` — operator-focused rollout sequence
  - `profiles/ayra-baseline.md` — Ayra Trust Network control mapping and evidence guide

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
Edit `harness/fixtures/queries.json` to replace example identifiers (`did:example:*`) and vocab URIs with
values valid in your environment. For Ayra deployments, also add the three recognition fixtures listed above.

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


## Certification Baseline Compatibility (CTR-ACB)

TSPP provides **security and privacy posture expectations** that can be used as evidence inputs to the *Candidate Trust Registry Assurance & Certification Baseline (CTR-ACB)* (defined in the TRQP Assurance Hub).

- TSPP describes **what security posture looks like** (profiles, expectations, artifacts).
- CTR-ACB describes **how that posture becomes certifiable** (controls, evaluation procedure, certification attestation).

See: `docs/ctr-acb-alignment.md`.


## Standards Alignment

To reduce adoption friction in mature security programs, TSPP includes an **informative mapping** from TSPP Requirement IDs to common security frameworks:

- OWASP API Security Top 10
- NIST SP 800-53 / 800-63 / 800-218 (SSDF)
- ISO/IEC 27001 / 27002 (and 27701 where relevant)

See `docs/standards-alignment.md` and the at-scale notes in `docs/standards/README.md`.


## Control IDs

TSPP requirements are expressed as stable **Control IDs** (e.g., `TSPP-META-01`).

- Normative list: `docs/requirements.md`
- Machine-readable export: `controls/control-registry.json`

## UNTP Digital Identity Anchor (DIA)

SAD-1 includes an identity anchoring extension for directories that use UNTP DIA / Identity Resolver patterns.

- DIA spec: https://untp.unece.org/docs/specification/DigitalIdentityAnchor/
- DIA context (0.6.1): https://test.uncefact.org/vocabulary/untp/dia/0.6.1/context/

## Experimental: DeDi posture mapping

TRQP-TSPP includes an **experimental** DeDi operator posture profile to align decentralized directory deployments with Hub controls and evidence bundle patterns.

- Profile: `docs/profiles/dedi-experimental.md`
- Upstream: https://github.com/LF-Decentralized-Trust-labs/decentralized-directory-protocol

- DeDi mapping matrix: `docs/reference/dedi-mapping-matrix.md`
- Machine-readable matrix: `docs/reference/dedi-mapping-matrix.yaml`


## Operational Stack integration

TSPP reports now include shared `run_id`, `target_id`, `assurance_level`, and `tool_version` metadata so the Assurance Hub can assemble a combined manifest with less hand-waving and fewer brittle assumptions.
