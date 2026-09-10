---
owner: maintainers
last_reviewed: 2026-09-10
tier: 1
---

# TSPP Ayra Trust Network Baseline Profile

This document describes how TSPP security/privacy posture evidence can support assessment of registries operating under the **Ayra TRQP Profile v0.6.0-draft**. Ayra remains authoritative for Ayra profile requirements; TSPP remains authoritative for its own control definitions and posture semantics. A TSPP control MUST NOT silently strengthen, weaken, or replace an Ayra normative requirement.

Reference: [Ayra TRQP Profile v0.6.0-draft](https://ayraforum.github.io/ayra-trust-registry-resources/) and the [Ayra Implementers Guide](https://ayraforum.github.io/ayra-trust-registry-resources/guides/).

## Identifier requirements

The current Ayra profile requires Ayra `_id` values to be DIDs represented as DID URI strings. It does **not** require `did:webvh` universally. Supported DID methods are defined by the relevant registry or authority and may be exposed through the optional `/lookups/didMethods` endpoint. `did:webvh` is preferred and may be required by higher-assurance or authority-specific policy.

TSPP therefore treats DID-method restrictions as profile/authority applicability information, not as a universal TSPP control. Full DID resolution, controller evidence, service discovery and governance legitimacy remain separate assurance concerns.

A lightweight `did:webvh` format validator exists at `schemas/ayra/did_webvh_validator.py`; its presence does not make `did:webvh` mandatory for every Ayra deployment.

## Response signing

Ayra v0.6.0-draft says registries **SHOULD** sign TRQP responses with JWS where supported. The signing mechanism remains under active discussion, and unsigned `application/json` responses remain conformant to the current Ayra profile API.

TSPP independently defines stronger signing posture at applicable assurance levels. In the current control registry:

| TSPP control | TSPP meaning | Relationship to Ayra v0.6.0-draft |
|---|---|---|
| `TSPP-AL2-01` | Signed envelope in AL2 | Producer-owned evidence that can support the Ayra signing SHOULD; does not turn the SHOULD into a MUST |
| `TSPP-AL2-02` | Verifiable signature via declared JWKS | Additional TSPP posture evidence where applicable |
| `TSPP-AL3-01` | Default signing at AL3 | Stronger TSPP posture expectation at AL3/AL4, independent of Ayra normative strength |

The Assurance Hub may compose these TSPP observations into an Ayra assurance result while preserving both authorities: Ayra owns the requirement strength; TSPP owns the posture evidence.

## Current TSPP evidence relevant to Ayra

The following current controls can provide supporting posture evidence where their applicability has been established. They are not a restatement of Ayra's normative requirements.

| TSPP control | Evidence concern | Ayra relationship |
|---|---|---|
| `TSPP-AL2-01`, `TSPP-AL2-02` | Response signing and verification | Supports Ayra signing SHOULD when applicable |
| `TSPP-RL-01` | Rate-limit signals on HTTP 429 | Supports Ayra's conditional 429 behaviour when rate limiting is exercised |
| `TSPP-CTX-01`, `TSPP-CTX-02` | Context handling | Supports posture around declared/unknown context handling |
| `TSPP-ENUM-01`, `TSPP-ERR-01` | Enumeration/error surface | Security/privacy posture evidence; does not replace TRQP/Ayra HTTP semantics |
| `TSPP-FRESH-01`, `TSPP-FRESH-02`, `TSPP-FRESH-03` | Response freshness | Supporting operational/posture evidence where applicable |
| `TSPP-META-01`, `TSPP-META-02` | Metadata publication/schema | Relevant only when the optional Ayra metadata extension is implemented/applicable |
| `TSPP-LIFE-01`, `TSPP-LIFE-02`, `TSPP-LIFE-03` | Lifecycle publication | TSPP lifecycle/posture evidence; not an Ayra profile requirement unless separately established |

Ayra's optional extension endpoints remain optional. TSPP MUST NOT convert an unimplemented optional Ayra extension into a failure merely because a related TSPP control exists outside the selected posture profile.

## Profile-consumable posture evidence

TSPP exposes a profile-consumable producer artifact using `schemas/evidence/profile-consumable-posture.schema.json`. The artifact binds posture observations to exact target, run, assurance level, control-set revision and reassessment state.

Profile context is applicability/correlation metadata only. It cannot override TSPP control conclusions. Conversely, TSPP evidence cannot rewrite Ayra normative strength.

Lifecycle consequences remain fail-safe:

```text
posture-relevant profile change
    -> REASSESS_REQUIRED

profile-change impact unknown
    -> REASSESS_REQUIRED

explicitly posture-irrelevant change
    -> CURRENT only with machine-verifiable rationale
```

Missing applicable evidence remains `INDETERMINATE`; it does not become PASS.

## Running TSPP for an Ayra deployment

Choose the TSPP assurance level required by the deployment's own security/privacy posture policy rather than inferring one from Ayra alone. For example:

```bash
export TRQP_BASE_URL="https://your-registry.example"
export TSPP_EXPECT_AL="AL2"
export TSPP_REPORT_PATH="./tspp_conformance_report.json"
pytest harness/ -q
```

Selecting AL2 means the TSPP AL2 controls apply. It does not mean Ayra itself requires AL2 or makes JWS mandatory.

## Evidence and combined assurance

TSPP posture evidence should be composed with CTS protocol-conformance evidence and profile-owned/authority evidence by the Assurance Hub:

```text
CTS core conformance evidence
        +
TSPP posture evidence
        +
Ayra profile-owned constraints
        +
external authority evidence
        -> Assurance Hub composition
```

A complete result preserves the producer and normative source for each material proposition. A TSPP PASS does not establish governance legitimacy, and a profile-local PASS cannot override a TSPP FAIL or non-current lifecycle state.

## Known boundaries

TSPP does not by itself establish:

- which DID methods an Ayra authority permits for a particular deployment;
- DID resolution or controller legitimacy;
- ecosystem governance-framework authority;
- Ayra network registration or governance approval;
- transitive recognition semantics;
- that the current Ayra signing SHOULD has become a MUST.

Those claims require the applicable profile, protocol, governance or external evidence authority. This document should be reassessed when the referenced Ayra profile revision changes.
