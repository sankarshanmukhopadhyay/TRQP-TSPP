---
owner: maintainers
last_reviewed: 2026-08-30
tier: 0
---

# TRQP Security & Privacy Baseline (TSPP)

TRQP-TSPP is the **security and privacy posture computation layer** in the TRQP Operational Trust Stack. It turns assurance-level requirements into executable controls, validates implementation evidence, and produces machine-readable posture and traceability artifacts for downstream conformance and assurance workflows.

> **Current component release:** v0.16.1  
> **Current coordinated stack:** TRQP Stack 2026.1 — Coconut  
> **Lifecycle:** Active  
> **Maturity:** Implementation draft  
> **Operational status:** Active validation

| Attribute | Value |
|---|---|
| Portfolio tier | Flagship |
| Primary role | Security/privacy control profile and posture computation |
| Portfolio contract role | `normative-protocol-profile` |
| Primary output | Posture Report and control-coverage evidence |
| Validation | `make validate` |
| Assurance evidence | `make assurance-check` |
| Evidence output | `artifacts/validation/tspp-report.json`, `artifacts/traceability/tspp-control-coverage.json` |
| Governance authority | [`GOVERNANCE.md`](GOVERNANCE.md) and [`PROJECT-STATUS.yaml`](PROJECT-STATUS.yaml) |
| Producer contract | [`portfolio/stack-producer-contract.json`](portfolio/stack-producer-contract.json) |
| Portfolio integration | [`docs/portfolio-integration.md`](docs/portfolio-integration.md) |
| Documentation site | https://sankarshanmukhopadhyay.github.io/TRQP-TSPP/ |

## Start here

For the validated multi-repository adoption path, start with the coordinated TRQP Stack release in the TRQP Assurance Hub. If you are implementing or evaluating TSPP directly, use:

- [`QUICKSTART.md`](QUICKSTART.md) — run the reference harness;
- [`docs/profile.md`](docs/profile.md) — profile and requirements overview;
- [`docs/requirements.md`](docs/requirements.md) — stable TSPP Control IDs;
- [`controls/control-registry.json`](controls/control-registry.json) — machine-readable control registry;
- [`docs/OUTPUT_CONTRACT.md`](docs/OUTPUT_CONTRACT.md) — posture output contract; and
- [`docs/portfolio-integration.md`](docs/portfolio-integration.md) — coordinated Stack relationship.

## v0.16.x lifecycle capability

The v0.16 line adds portable lifecycle materiality evidence for material, unknown, and demonstrably non-material change. Negative tests prevent material or unknown change from silently preserving current assurance. v0.16.1 is a patch release that repairs the repository-status contract exposed by clean-room Stack execution; it does not change lifecycle semantics.

TSPP remains authoritative for security/privacy posture materiality and affected controls. TIS owns portable lifecycle serialization, CTS owns conformance/replay reassessment consequence, and the Assurance Hub owns combined current-assurance recomposition.

## Authority and scope

TSPP is authoritative for TRQP security and privacy control profiles, posture computation rules, assurance-level control evidence, and its machine-readable outputs. It is **not** authoritative for the upstream TRQP protocol specification, general protocol-conformance verdicts, CTS replay-comparison semantics, cross-stack assurance publication, or external certification.

## Assurance levels

TSPP supports four assurance levels without changing underlying protocol semantics: AL1 baseline controls, AL2 authenticated/signed-response controls, AL3 stronger operational and software supply-chain evidence, and AL4 the strongest bundled profile including explicit SBOM/provenance evidence.

## Evidence and auditability

The producer boundary is declared in [`portfolio/stack-producer-contract.json`](portfolio/stack-producer-contract.json). Primary evidence outputs are `artifacts/validation/tspp-report.json` and `artifacts/traceability/tspp-control-coverage.json`. Example or self-generated evidence is not independent certification.

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

Component releases remain independently versioned. A new TSPP release does not automatically cause a Stack release; the Hub publishes a coordinated release only after the complete tuple passes the Stack eligibility gate.

## License

Apache 2.0. See [`LICENSE`](LICENSE).
