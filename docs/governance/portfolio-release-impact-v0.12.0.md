---
layout: default
title: "Portfolio Release Impact: TRQP-TSPP v0.12.0"
nav_exclude: true
---

# Portfolio Release Impact: TRQP-TSPP v0.12.0

| Field | Value |
|---|---|
| Repository | `TRQP-TSPP` |
| Release version | v0.12.0 |
| Release date | 2026-06-29 |
| Primary change type | Posture evidence artifact contract alignment |
| Portfolio impact classification | Artifact / Assurance / Documentation |

## Changed surfaces

- [x] Schema or runtime artifact
- [x] Evidence bundle or decision receipt
- [x] Assurance level or control mapping
- [x] Registry publication or status/revocation semantics
- [x] README, onboarding, or adoption workflow

## Relationship review

| Source repo | Target repo | Relationship | Impact | Evidence |
|---|---|---|---|---|
| `TRQP-TSPP` | `trqp-assurance-hub` | `profiles` | TSPP posture evidence now exposes TIS projection metadata for Hub v1.7.0 | `schemas/evidence/tspp_posture_bundle_descriptor.schema.json` |
| `trust-infrastructure-schemas` | `TRQP-TSPP` | `informs` | TSPP documents how posture output maps to TIS assurance, control, decision, and status artifacts | `docs/tis-posture-evidence-contract.md` |
| `trust-systems-meta-model` | `TRQP-TSPP` | `informs` | TSPP clarifies authority, scope, enforcement, and revocation boundaries | `docs/tis-posture-evidence-contract.md` |

## Validation evidence

```text
python scripts/schema_check.py
python scripts/doc_tests.py
```

## Decision

- [ ] Release has no cross-repo impact.
- [ ] Release has documentation impact only.
- [x] Release requires downstream artifact/profile/test updates.
- [ ] Release should be held until downstream compatibility is updated.

