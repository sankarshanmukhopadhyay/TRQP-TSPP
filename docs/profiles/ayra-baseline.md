---
owner: maintainers
last_reviewed: 2026-03-10
tier: 1
---

# TSPP Ayra Trust Network Baseline Profile

This document describes which TSPP controls are applicable to registries operating
within the [Ayra Trust Network](https://ayra.forum), and what evidence artifacts
satisfy each Ayra conformance tier.

Reference: [Ayra TRQP Profile v0.5.0-draft](https://ayraforum.github.io/ayra-trust-registry-resources/) |
[Ayra Implementers Guide](https://ayraforum.github.io/ayra-trust-registry-resources/guides/)

---

## Identifier requirements (normative — all tiers)

The Ayra Profile mandates `did:webvh` as the identifier method for all ecosystem,
trust registry, and cluster identifiers. This is a MUST, not a recommendation.

| Role | Format | Ayra service profile URL |
|---|---|---|
| Ecosystem DID | `did:webvh` | EGF: `https://ayra.forum/profiles/trqp/egfURI/v1`; TR: `https://ayra.forum/profiles/trqp/tr/v2` |
| Trust Registry DID | `did:webvh` | `https://ayra.forum/profiles/trqp/tr/v2` |
| Cluster DID | `did:webvh` | Trust metaregistry endpoint |

A lightweight format validator is available at `schemas/ayra/did_webvh_validator.py`.
Full DID document resolution and service endpoint verification are currently manual checks.

---

## JWS response signing (normative — all Ayra tiers)

Unlike standalone TSPP deployments where JWS signing is an AL2 upgrade, the Ayra
Profile requires JWS-signed responses for **all trust registries at all tiers**.
The JWS MUST be derived from the controller key of the Trust Registry's DID document.

This means `test_06_al2_signed_responses.py` is a **required** test even for Ayra
Basic tier registries operating at AL1 in the TSPP sense.

---

## Applicable TSPP controls per Ayra tier

| TSPP Control | Description | Ayra Basic | Ayra Cross-Ecosystem | Ayra Sovereign |
|---|---|---|---|---|
| TSPP-META-01 | Metadata endpoint present and valid | Required | Required | Required |
| TSPP-META-02 | Assurance level declared in metadata | Required | Required | Required |
| TSPP-FRESH-01 | Freshness: `time_evaluated` + `expires_at` on auth responses | Required | Required | Required |
| TSPP-FRESH-03 | Freshness: `time_evaluated` + `expires_at` on recognition responses | Required | Required | Required |
| TSPP-AUTH-01 | Bearer token authentication enforced | Recommended | Required | Required |
| TSPP-RATE-01 | Rate limiting headers present (auth + recognition) | Required | Required | Required |
| TSPP-CTX-01 | Context allowlist enforced on both endpoints | Required | Required | Required |
| TSPP-ENUM-01 | Anti-enumeration: uniform not-found on both endpoints | Required | Required | Required |
| TSPP-SIGN-01 | JWS-signed responses (Ayra MUST at all tiers) | **Required** | Required | Required |
| TSPP-SIGN-02 | DPoP sender-constrained tokens for bulk clients | Not required | Recommended | Required |
| TSPP-RECOG-01 | Recognition freshness fields | Required | Required | Required |
| TSPP-RECOG-02 | Recognition anti-enumeration | Required | Required | Required |
| TSPP-RECOG-03 | Recognition context allowlist | Required | Required | Required |
| TSPP-RECOG-04 | Recognition rate limit headers | Recommended | Required | Required |
| TSPP-RECOG-05 | Ayra ATN recognition query shape (flat response) | Required | Required | Required |

---

## Running the TSPP harness for Ayra

```bash
export TRQP_BASE_URL="https://your-registry.example"
export TSPP_EXPECT_AL="AL2"           # AL2 required for JWS; use AL1 for initial baseline run
export TSPP_REPORT_PATH="./tspp_conformance_report.json"
pytest harness/ -q
```

For Ayra Cross-Ecosystem and Sovereign tiers, also set:

```bash
export TSPP_EXPECT_AL="AL2"
pytest harness/ -q -k "not al3 and not al4"
```

For Sovereign tier:

```bash
export TSPP_EXPECT_AL="AL3"
pytest harness/ -q
```

---

## Evidence artifacts

The `tspp_conformance_report.json` artifact maps directly to Ayra conformance requirements:

| Ayra Conformance Requirement | TSPP Evidence |
|---|---|
| Registry security posture | Full TSPP report (all controls) |
| Freshness compliance (auth + recognition) | `test_02_freshness.py` + `test_10_recognition_security.py` |
| Recognition security controls | `test_10_recognition_security.py` (NEW) |
| Signed responses (MUST) | `test_06_al2_signed_responses.py` |
| Rate limiting (both endpoints) | `test_05_ratelimits.py` |
| Context enforcement (both endpoints) | `test_03_context_allowlist.py` + `test_10_recognition_security.py` |
| Metadata declaration | `test_01_metadata.py` |
| Ayra ATN recognition shape | `test_10_recognition_security.py::test_ayra_recognition_query_shape` |

---

## Required query fixtures

Add these to `harness/fixtures/queries.json` for full Ayra coverage:

| Fixture key | Required for |
|---|---|
| `recognition_valid` | TSPP-FRESH-03, TSPP-RECOG-01, TSPP-RECOG-03, TSPP-RECOG-04 |
| `recognition_unknown_ecosystem` | TSPP-RECOG-02 (anti-enumeration) |
| `recognition_ayra_atn` | TSPP-RECOG-05 (Ayra ATN query shape); set `authority_id` to `did:webvh:ayra.forum` |

---

## Combined assurance

For a complete Ayra submission, combine TSPP evidence with CTS evidence using the
Assurance Hub manifest generator:

```bash
python tools/generate-manifest.py \
  --cts-bundle reports/ayra-run/ \
  --tspp-report tspp_conformance_report.json \
  --out combined-assurance-manifest.json
```

See the Assurance Hub `tools/ayra-mapping.md` for the full submission checklist.

---

## Known gaps

The following Ayra requirements are not yet validated by automated controls:

- `did:webvh` format validation on `entity_id` and `authority_id` in request/response bodies
- EGF service endpoint presence in ecosystem DID document
- Recognition chain depth (transitive recognition across Ayra clusters)
- Ayra network registration (governance review, DID submission — out of scope)
