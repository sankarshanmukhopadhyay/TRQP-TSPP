---
owner: maintainers
last_reviewed: 2026-08-25
tier: 0
---

# TRQP Security & Privacy Baseline (TSPP)

TRQP-TSPP is the **security and privacy posture computation layer** in the TRQP Operational Trust Stack. It turns assurance-level requirements into executable controls, validates implementation evidence, and produces machine-readable posture and traceability artifacts for downstream conformance and assurance workflows.

> **Current component release:** v0.15.0  
> **Current coordinated stack:** TRQP Stack 2026.1 — Coconut  
> **Lifecycle:** Active  
> **Maturity:** Implementation draft  
> **Operational status:** Active validation

| Attribute | Value |
|---|---|
| Primary role | Security/privacy control profile and posture computation |
| Portfolio contract role | `normative-protocol-profile` |
| Primary output | Posture Report and control-coverage evidence |
| Validation | `make validate` |
| Assurance evidence | `make assurance-check` |
| Producer contract | [`portfolio/stack-producer-contract.json`](portfolio/stack-producer-contract.json) |
| Portfolio integration | [`docs/portfolio-integration.md`](docs/portfolio-integration.md) |
| Documentation site | https://sankarshanmukhopadhyay.github.io/TRQP-TSPP/ |

## Start here

If you want the **validated multi-repository adoption path**, start with **TRQP Stack 2026.1 — Coconut** in the TRQP Assurance Hub. The coordinated release fixes the component versions for you and proves that the declared tuple works together end to end.

If you are implementing or evaluating TSPP itself, start with:

- [`QUICKSTART.md`](QUICKSTART.md) — run the reference harness;
- [`docs/profile.md`](docs/profile.md) — profile and requirements overview;
- [`docs/requirements.md`](docs/requirements.md) — stable TSPP Control IDs;
- [`controls/control-registry.json`](controls/control-registry.json) — machine-readable control registry;
- [`docs/OUTPUT_CONTRACT.md`](docs/OUTPUT_CONTRACT.md) — posture output contract; and
- [`docs/portfolio-integration.md`](docs/portfolio-integration.md) — coordinated Stack relationship.

## Coordinated Stack 2026.1 — Coconut

The current validated tuple is:

| Layer | Release | Authority / output |
|---|---:|---|
| TRQP-TSPP | v0.15.0 | Security/privacy controls and posture evidence |
| TRQP Conformance Suite | v1.8.0 | Protocol conformance and deterministic replay evidence |
| TRQP Assurance Hub | v1.11.0 | Combined assurance and coordinated release publication |
| TSMM | v0.24.0 | Semantic authority |
| TIS | v0.14.1 | Schema and portfolio authority |

For adopters, the value of the coordinated release is simple: **you do not have to determine cross-repository compatibility yourself**. The Hub publishes the validated tuple and evidence provenance; TSPP contributes the posture/control evidence for that declared stack.

The coordinated release is a compatibility and assurance contract, not a fourth implementation product and not a transfer of authority between repositories.

## What v0.15.0 establishes

v0.15.0 connects TSPP to the executable governance layer and makes cross-repository drift testable. It pins TSMM v0.24.0 and TIS v0.14.1, validates repository relationships and release pins, aligns AL3/AL4 supply-chain evidence, binds freshness-relevant context, and prevents canonical metadata-schema drift.

See [`RELEASE_NOTES_v0.15.0.md`](RELEASE_NOTES_v0.15.0.md).

## Authority and scope

TSPP is authoritative for:

- TRQP security and privacy control profiles;
- posture computation rules;
- assurance-level control evidence; and
- the machine-readable artifacts produced from those rules.

TSPP is **not** authoritative for the upstream TRQP protocol specification, general protocol-conformance verdicts, CTS replay-comparison semantics, cross-stack assurance publication, or external certification. The coordinated Stack release preserves those boundaries.

## Assurance levels

TSPP supports four assurance levels without changing the underlying TRQP protocol semantics:

- **AL1** — baseline internet-safe posture and core metadata/freshness controls;
- **AL2** — authenticated and signed-response controls;
- **AL3** — stronger operational and software supply-chain evidence; and
- **AL4** — strongest bundled profile, including explicit SBOM/provenance evidence.

The executable AL contract is validated by `scripts/verify_al_contract.py` and the harness integration tests.

## Evidence and auditability

TSPP evidence is intended to make authority, required controls, producer/version provenance, evidence satisfaction, and invalidation conditions machine-reviewable. The current producer boundary is declared in [`portfolio/stack-producer-contract.json`](portfolio/stack-producer-contract.json).

Primary outputs include:

- `artifacts/validation/tspp-report.json`; and
- `artifacts/traceability/tspp-control-coverage.json`.

Example or self-generated evidence is not independent certification.

## Quick validation

```bash
make validate
make assurance-check
```

For live/reference-SUT testing, see [`QUICKSTART.md`](QUICKSTART.md) and [`docs/deployment-guidance.md`](docs/deployment-guidance.md).

## Governance and release policy

- [`GOVERNANCE.md`](GOVERNANCE.md) — repository-local authority and decision rights.
- [`docs/governance/release-policy.md`](docs/governance/release-policy.md) — component release policy.
- [`docs/portfolio-integration.md`](docs/portfolio-integration.md) — relationship to coordinated Stack releases.

Component releases remain independently versioned. A new TSPP release does not automatically cause a new Stack release; the Hub cuts a new coordinated release only after the complete tuple passes the Stack eligibility gate.

## License

Apache 2.0. See [`LICENSE`](LICENSE).
