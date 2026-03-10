---
owner: maintainers
last_reviewed: 2026-03-10
tier: 1
---

# TSPP Ayra Trust Network Baseline Profile

This document describes which TSPP controls are applicable to registries operating
within the [Ayra Trust Network](https://ayra.forum), and what evidence artifacts
satisfy each Ayra conformance tier.

Reference: [Ayra TRQP Profile API](https://ayraforum.github.io/ayra-trust-registry-resources/api.html)

## Applicable TSPP controls per Ayra tier

| TSPP Control | Description | Ayra Basic | Ayra Cross-Ecosystem | Ayra Sovereign |
|---|---|---|---|---|
| TSPP-META-01 | Metadata endpoint (`/.well-known/trqp-metadata`) present and valid | Required | Required | Required |
| TSPP-META-02 | Assurance level declared in metadata | Required | Required | Required |
| TSPP-FRESH-01 | Freshness semantics: `time_evaluated` + `expires_at` on responses | Required | Required | Required |
| TSPP-AUTH-01 | Bearer token authentication enforced | Recommended | Required | Required |
| TSPP-RATE-01 | Rate limiting headers present | Required | Required | Required |
| TSPP-CTX-01 | Context allowlist enforced | Required | Required | Required |
| TSPP-ENUM-01 | Anti-enumeration: uniform not-found responses | Required | Required | Required |
| TSPP-SIGN-01 | JWS-signed response envelopes (AL2) | Not required | Required | Required |
| TSPP-SIGN-02 | DPoP sender-constrained tokens for bulk clients | Not required | Recommended | Required |
| TSPP-RECOG-01 | Recognition policy: scoped + expiry | Recommended | Required | Required |

## Evidence artifacts

Run the TSPP harness against your registry and collect:

```bash
export TRQP_BASE_URL="https://your-registry.example"
export TSPP_EXPECT_AL="AL1"          # AL1 for Basic; AL2 for Cross-Ecosystem/Sovereign
export TSPP_REPORT_PATH="./tspp_conformance_report.json"
pytest harness/ -q
```

The `tspp_conformance_report.json` artifact maps directly to:

| Ayra Conformance Requirement | TSPP Evidence |
|---|---|
| Registry security posture | Full TSPP report (all controls) |
| Freshness compliance | `test_02_freshness.py` results |
| Signed responses | `test_06_al2_signed_responses.py` results |
| Rate limiting | `test_05_ratelimits.py` results |
| Context enforcement | `test_03_context_allowlist.py` results |
| Metadata declaration | `test_01_metadata.py` results |

## Combined assurance

For a complete Ayra submission, combine TSPP evidence with Conformance Suite evidence
using the Assurance Hub manifest generator. See `docs/ctr-acb-alignment.md`.

## Known gaps

Ayra-specific governance fields (`governance_framework_id` populated with Ayra ecosystem ID,
`network_credential_type` vocabulary) are not yet validated by automated controls.
These should be verified manually against the Ayra TRQP Implementation Profile.
