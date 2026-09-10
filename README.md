---
owner: maintainers
last_reviewed: 2026-09-10
tier: 0
---

# TRQP Security & Privacy Baseline (TSPP)

TRQP-TSPP is the **security and privacy posture computation layer** in the TRQP Operational Trust Stack. It turns assurance-level requirements into executable controls, validates implementation evidence, and produces machine-readable posture and traceability artifacts for downstream conformance and assurance workflows.

> **Current component release:** v0.17.0  
> **Current coordinated stack:** TRQP Stack 2026.2 — Ashoka  
> **Coordinated release candidate:** TRQP Stack 2026.3 — Banyan  
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
| Profile-consumable posture schema | [`schemas/evidence/profile-consumable-posture.schema.json`](schemas/evidence/profile-consumable-posture.schema.json) |
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

## v0.17.0 profile-aware posture producer

v0.17.0 makes profile-consumable security/privacy posture evidence an explicit TSPP producer contract. The exported artifact binds posture observations to exact TSPP version, target/run identity, assurance level, control-set identity/revision, individual control evidence, and lifecycle/reassessment state.

Profile context is applicability/correlation metadata only. It cannot change TSPP control conclusions. Posture-relevant profile change or unknown profile impact requires reassessment; demonstrably posture-irrelevant change may preserve current evidence only with explicit rationale. Missing applicable evidence remains `INDETERMINATE`.

This release also corrects the Ayra integration guide to the current Ayra v0.6.0-draft authority: DID methods are not universally restricted to `did:webvh`, and response signing remains an Ayra `SHOULD`. TSPP AL2+ signing controls provide posture evidence without strengthening the Ayra normative requirement.

The candidate coordinated compatibility tuple is **TSPP v0.17.0 / CTS v1.10.0 / Assurance Hub v1.13.0**. Until Stack 2026.3 passes its coordinated release gate, **TRQP Stack 2026.2 — Ashoka remains the current coordinated Stack release**.

## Profile-aware posture producer boundary

TSPP may expose posture evidence for use by a named profile-aware consumer such as the TRQP Assurance Hub. This does **not** make TSPP an ecosystem-profile policy engine.

The profile-consumable posture contract preserves:

- exact TSPP version;
- target and run identity;
- assurance level;
- control-set identity and revision;
- control-level posture results and evidence references; and
- current/reassessment/invalid lifecycle state.

Optional `profile_context` is applicability/correlation metadata only. It cannot override a TSPP posture result or change a control conclusion. The same current posture evidence may be correlated to multiple profiles when the underlying control applicability is unchanged.

The responsibility boundary is:

| Observation | Authority |
|---|---|
| Security/privacy controls and posture semantics | TSPP |
| TRQP core/binding conformance and deterministic replay | CTS |
| Ecosystem-profile narrowing and extensions | Profile authority + Assurance Hub projection |
| Governance legitimacy and external authority facts | Applicable external authority/evidence source |
| Composition of independent evidence into profile assurance | TRQP Assurance Hub |

Profile changes are evaluated through the existing TSPP lifecycle model. A profile revision that changes posture-relevant obligations produces `REASSESS_REQUIRED`. If the posture impact of a changed profile is unknown, it also fails safe to `REASSESS_REQUIRED`. A demonstrably posture-irrelevant profile metadata change may preserve `CURRENT`, but only with an explicit machine-readable rationale.

Missing or untested signing, TLS, or other applicable control evidence remains `INDETERMINATE`; profile metadata cannot promote it to `PASS`.

The export helper is `scripts/build_profile_consumable_posture.py`; the machine-readable contract is `schemas/evidence/profile-consumable-posture.schema.json`.

## Authority and scope

TSPP is authoritative for TRQP security and privacy control profiles, posture computation rules, assurance-level control evidence, and its machine-readable outputs. It is **not** authoritative for the upstream TRQP protocol specification, general protocol-conformance verdicts, CTS replay-comparison semantics, ecosystem-profile policy, cross-stack assurance publication, governance legitimacy, or external certification.

## Assurance levels

TSPP supports four assurance levels without changing underlying protocol semantics: AL1 baseline controls, AL2 authenticated/signed-response controls, AL3 stronger operational and software supply-chain evidence, and AL4 the strongest bundled profile including explicit SBOM/provenance evidence.

## Evidence and auditability

The producer boundary is declared in [`portfolio/stack-producer-contract.json`](portfolio/stack-producer-contract.json). Primary evidence outputs are `artifacts/validation/tspp-report.json` and `artifacts/traceability/tspp-control-coverage.json`; profile-aware consumers may additionally consume the version-bound posture projection. Example or self-generated evidence is not independent certification.

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
