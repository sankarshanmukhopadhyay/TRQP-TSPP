---
owner: maintainers
last_reviewed: 2026-03-10
tier: 0
---

## Documentation

- Documentation governance: [`docs/governance/README.md`](docs/governance/README.md)

# TRQP Security & Privacy Baseline (TSPP)

📘 **Documentation site (GitHub Pages):** https://sankarshanmukhopadhyay.github.io/TRQP-TSPP/

**Current version:** v0.7.0

![License](https://img.shields.io/github/license/sankarshanmukhopadhyay/TRQP-TSPP)
![Last Commit](https://img.shields.io/github/last-commit/sankarshanmukhopadhyay/TRQP-TSPP)
![Issues](https://img.shields.io/github/issues/sankarshanmukhopadhyay/TRQP-TSPP)
![TRQP](https://img.shields.io/badge/TRQP-Protocol-blue)
![Trust over IP](https://img.shields.io/badge/Trust%20over%20IP-Alignment-0A66C2)
![Security Profile](https://img.shields.io/badge/Security-Profile-critical)
![Conformance](https://img.shields.io/badge/Conformance-Harness-brightgreen)
![Assurance Levels](https://img.shields.io/badge/Assurance-AL1%20%7C%20AL2%20%7C%20AL3%20%7C%20AL4-purple)

## Start here: TRQP Assurance Hub

Looking for the *single front door* across TRQP conformance + security/privacy assurance?

- Hub repo (onboarding, operating model, combined workflows): https://github.com/sankarshanmukhopadhyay/trqp-assurance-hub
- Hub crosswalk for this repo: `docs/hub-crosswalk.md`
- Evidence bundles: `docs/evidence_bundles.md`


This repository packages a practical, implementer-ready **security and privacy profile** for the Trust Over IP
**Trust Registry Query Protocol (TRQP)** and supports evaluating **authoritative digital trust directories** (SAD-1), including sovereign registry patterns.
**Trust Registry Query Protocol (TRQP)**, along with machine-readable artifacts and a conformance harness.

If TRQP becomes the *query plane* for institutional trust, this repo is the seatbelt kit: it converts high-level
security considerations into enforceable requirements, and ships tooling to test deployments against them.

## Assurance Level Dependency

This repository **does not define** Assurance Level (AL1–AL4) semantics.

- Canonical definitions live in **TRQP Assurance Hub**: `docs/guides/assurance-levels.md`
- Machine-readable contract: `al-contract.json`

**Pinning for audit stability:** this repo ships an `al-contract.json` that includes the SHA-256 of the canonical AL definition document (`61c599c5fa06e0c9110f40ff71c0174db5502105b97f1391dbd9ae8548115f71`).

TSPP implements **requirements, tests, and evidence expectations** parameterized by AL. It MUST NOT redefine AL meanings locally.

## Ayra Trust Network

For registries targeting the [Ayra Trust Network](https://ayra.forum), see the Ayra baseline profile:

- Profile guidance: [`docs/profiles/ayra-baseline.md`](docs/profiles/ayra-baseline.md)
- `did:webvh` format validator: `schemas/ayra/did_webvh_validator.py`
- Assurance Hub crosswalk: https://github.com/sankarshanmukhopadhyay/trqp-assurance-hub/blob/main/tools/ayra-mapping.md

Key Ayra requirements handled by TSPP:

- **JWS response signing is MUST at all Ayra tiers** — not an AL2-only upgrade. Run `test_06_al2_signed_responses.py` even for Basic tier.
- **Recognition security parity** — `test_10_recognition_security.py` covers POST /recognition with the same freshness, anti-enumeration, context allowlist, and rate limiting controls as POST /authorization.
- **`did:webvh` format validation** — `schemas/ayra/did_webvh_validator.py` provides syntax checking. Full DID resolution remains a manual step.

Required query fixtures for full Ayra coverage (add to `harness/fixtures/queries.json`):

| Fixture key | Used by |
|---|---|
| `recognition_valid` | `test_10_recognition_security.py` freshness, context, rate limit tests |
| `recognition_unknown_ecosystem` | `test_10_recognition_security.py` anti-enumeration test |
| `recognition_ayra_atn` | `test_10_recognition_security.py` ATN query shape test (set `authority_id` to `did:webvh:ayra.forum`) |

## What's in here

- **OpenAPI contract** (`openapi/tspp-trqp-openapi.yaml`)
  An HTTP-level contract capturing profile-required headers/fields, freshness semantics, and optional AL2 signed envelopes.

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
