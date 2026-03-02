# SLSA (Supply-chain Levels for Software Artifacts)

> **Status:** informative (non-normative)

## Why this matters
SLSA is about reducing supply-chain surprises: you want to know what was built, from what source, by what process, and whether it was tampered with. For TRQP operators, this affects the service binary/container, deployment manifests, and the published TSPP artifacts.

## TSPP touchpoints
- **Related control IDs:** `TSPP-META-01`, `TSPP-META-02`, `TSPP-AL4-04`
- **Where to implement:** CI/CD build provenance, dependency pinning, and controlled promotion of releases and policy artifacts.

## Suggested evidence (operator-ready)
- Build provenance/attestation artifacts for releases (CI logs, signed attestations)
- Dependency manifests with pinned versions and review process
- Release promotion policy + rollback procedure linked from `metadata.governance.*`
- Reproducible build or deterministic packaging notes (where feasible)

## Practical implementation notes
- Treat these controls as “platform glue” that makes the TSPP controls easier to operate at scale.
- Where possible, automate evidence generation (CI/CD attestations, config snapshots, telemetry exports) to keep audit cost down.
