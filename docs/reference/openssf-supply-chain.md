# OpenSSF-aligned Supply Chain Integrity (Reference)

This repo aligns parts of its **Software Supply Chain Integrity** requirements with guidance from the **OpenSSF** ecosystem.

Scope:
- These references support **implementation guidance** and **evidence expectations**.
- TSPP remains profile-driven and standards-agnostic: implementers may meet the requirements using equivalent mechanisms.

## Referenced OpenSSF work (non-exhaustive)

- **SLSA** (Supply-chain Levels for Software Artifacts): provenance and build integrity expectations.
- **OpenSSF Scorecard**: automated checks for repository and project security practices.

## How TSPP uses this

TSPP introduces a control family **TSPP-SCI-xx** that:
- requires verifiable build provenance and signed releases for higher assurance,
- expects SBOM availability for deployed artifacts,
- expects continuous dependency/vulnerability monitoring,
- supports “audit-ready” evidence packaging.

See:
- `docs/requirements.md` (normative requirements)
- `docs/standards-alignment.md` (mapping guidance)
- `docs/evidence_bundles.md` (evidence bundling expectations)
