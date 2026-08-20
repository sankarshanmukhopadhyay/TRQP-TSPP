---
owner: maintainers
last_reviewed: 2026-08-20
tier: 0
---

# TRQP Security & Privacy Baseline (TSPP)

TRQP-TSPP is the **security and privacy posture computation layer** in the TRQP Operational Trust Stack. It turns assurance-level requirements into executable controls, validates implementation evidence, and produces machine-readable posture and traceability artifacts for downstream conformance and assurance workflows.

> **Current release:** v0.15.0  
> **Lifecycle:** Active  
> **Maturity:** Implementation draft  
> **Operational status:** Active validation  
> **Specification status:** Working draft

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
| Portfolio integration | [`portfolio/integration-contract.json`](portfolio/integration-contract.json) |
| Documentation site | https://sankarshanmukhopadhyay.github.io/TRQP-TSPP/ |

![License](https://img.shields.io/github/license/sankarshanmukhopadhyay/TRQP-TSPP)
![Last Commit](https://img.shields.io/github/last-commit/sankarshanmukhopadhyay/TRQP-TSPP)
![Issues](https://img.shields.io/github/issues/sankarshanmukhopadhyay/TRQP-TSPP)
![Conformance](https://img.shields.io/badge/Conformance-Harness-brightgreen)
![Assurance Levels](https://img.shields.io/badge/Assurance-AL1%20%7C%20AL2%20%7C%20AL3%20%7C%20AL4-purple)

## What v0.15.0 establishes

v0.15.0 connects TSPP to the current executable governance layer and makes cross-repository drift a testable condition.

- Pins **Trust Systems Meta-Model (TSMM) v0.24.0** as semantic authority for the TRQP binding.
- Pins **Trust Infrastructure Schemas (TIS) v0.14.1** as schema and portfolio-authority baseline.
- Declares the Conformance Suite relationship as `tested-by` and the Assurance Hub relationship as `assured-by`.
- Validates release pins, required local evidence, repository relationships, and integration invalidation conditions in CI.
- Aligns the reference SUT and canonical metadata schema with AL3/AL4 supply-chain evidence requirements.
- Includes freshness-relevant `time_requested` context in the reference SUT contract and signed-query binding.
- Prevents the canonical `schemas/core/` metadata schema from silently drifting from its harness-side mirror.

See [`RELEASE_NOTES_v0.15.0.md`](RELEASE_NOTES_v0.15.0.md) for the release record.

## Authority and scope

TSPP has repository-local authority over:

- TRQP security and privacy control profiles;
- posture computation rules;
- assurance-level control evidence; and
- the machine-readable artifacts it publishes from those rules.

TSPP **does not** own the TRQP protocol specification, general protocol-conformance verdicts, cross-stack assurance publication, or external certification. Those boundaries are machine-declared in [`PROJECT-STATUS.yaml`](PROJECT-STATUS.yaml) and [`portfolio/integration-contract.json`](portfolio/integration-contract.json).

## Where this fits

| Layer | Repository role | Primary output |
|---|---|---|
| TRQP-TSPP v0.15.0 | Security/privacy posture computation | Posture Report and control evidence |
| TRQP Conformance Suite v1.7.0 | Executable protocol conformance | Conformance Report and evidence bundle |
| TRQP Assurance Hub v1.10.0 | Evidence aggregation and assurance publication | Combined Assurance Manifest and assurance decision |

Shared authorities:

| Authority | Version | Purpose |
|---|---:|---|
| Trust Systems Meta-Model | 0.24.0 | TRQP semantic binding and semantic concepts |
| Trust Infrastructure Schemas | 0.14.1 | Portfolio relationships, repository authority and validation-result contracts |

A portfolio integration becomes invalid when required evidence is missing or the declared semantic/schema authority versions are incompatible.

## Assurance levels

TSPP supports four assurance levels. Profiles increase evidence and control expectations without changing the underlying TRQP protocol semantics.

- **AL1** — baseline internet-safe posture and core metadata/freshness controls.
- **AL2** — authenticated and signed-response controls for higher-assurance deployments.
- **AL3** — stronger operational and software supply-chain evidence requirements.
- **AL4** — highest bundled profile, including explicit SBOM/provenance evidence and the strongest reference-SUT control expectations.

The executable AL contract is validated by `scripts/verify_al_contract.py` and exercised through the harness integration tests.

## Start here

- [`QUICKSTART.md`](QUICKSTART.md) — run the reference harness.
- [`docs/profile.md`](docs/profile.md) — profile and requirements overview.
- [`docs/requirements.md`](docs/requirements.md) — stable TSPP Control IDs.
- [`controls/control-registry.json`](controls/control-registry.json) — machine-readable control registry.
- [`docs/threat-model.md`](docs/threat-model.md) — adversarial model and harms.
- [`docs/deployment-guidance.md`](docs/deployment-guidance.md) — operator rollout guidance.
- [`docs/OUTPUT_CONTRACT.md`](docs/OUTPUT_CONTRACT.md) — posture output contract.
- [`docs/portfolio-integration.md`](docs/portfolio-integration.md) — synchronized TRQP portfolio integration.
- [`docs/governance/release-policy.md`](docs/governance/release-policy.md) — release governance.
- [`docs/governance/change-intake.md`](docs/governance/change-intake.md) — change intake criteria.

## Quick validation

Run the repository-level governance and schema gate:

```bash
make validate
```

Generate the repository assurance artifacts:

```bash
make assurance-check
```

For live/reference-SUT conformance testing:

```bash
cd harness
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export TRQP_BASE_URL="https://your-registry.example"
export TSPP_EXPECT_AL="AL1"   # AL1, AL2, AL3 or AL4 as supported by the SUT
pytest -q
```

The harness can emit a machine-readable conformance report by setting `TSPP_REPORT_PATH`.

## Repository map

| Path | Purpose |
|---|---|
| `schemas/core/` | Canonical TSPP metadata and signed-response schemas |
| `controls/` | Stable machine-readable control registry |
| `harness/` | Executable conformance harness and fixtures |
| `examples/` | Reference SUT and sample inputs |
| `artifacts/validation/` | Validation evidence, including the TSPP report |
| `artifacts/traceability/` | Control-coverage evidence |
| `portfolio/` | Cross-repository integration contract |
| `docs/` | Profiles, governance, threat model, deployment and integration guidance |

## Evidence and auditability

TSPP evidence is designed to answer four questions directly:

1. **What authority and profile were evaluated?**
2. **Which controls were required and satisfied?**
3. **Which evidence was produced, and by which version?**
4. **What condition would invalidate or supersede the result?**

Artifacts retain producer/version context and are intended for machine consumption by CTS, the Assurance Hub, and other compatible assurance tooling. Example or self-generated evidence is not independent certification.

## Related mappings

- [`docs/ctr-acb-alignment.md`](docs/ctr-acb-alignment.md) — Candidate Trust Registry Assurance & Certification Baseline alignment.
- [`docs/standards-alignment.md`](docs/standards-alignment.md) — informative OWASP, NIST and ISO/IEC mappings.
- [`docs/profiles/ayra-baseline.md`](docs/profiles/ayra-baseline.md) — Ayra deployment profile.
- [`docs/profiles/dedi-experimental.md`](docs/profiles/dedi-experimental.md) — experimental DeDi posture mapping.
- [`docs/tis-posture-evidence-contract.md`](docs/tis-posture-evidence-contract.md) — TIS projection/evidence mapping.

## Documentation site

GitHub Pages uses Just the Docs and is deployed from `main` through GitHub Actions. Repository administrators should configure **Settings → Pages → Source: GitHub Actions**.

Documentation governance: [`docs/governance/README.md`](docs/governance/README.md).

## License

Apache 2.0. See [`LICENSE`](LICENSE).
