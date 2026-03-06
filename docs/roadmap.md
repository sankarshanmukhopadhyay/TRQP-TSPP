# Roadmap

This roadmap tracks high-level increments for TSPP.

## Completed

- ✅ Formalize AL dependency contract (`al-contract.json`) and clarify canonical AL source.
- ✅ Add standards alignment annex (`docs/standards-alignment.md`).
- ✅ Expand executable requirements coverage for AL3/AL4 governance + audit expectations (independent assessment, change control, rollback, policy, monitoring, and audit-log checks).
- ✅ Consolidate harness documentation into `harness/README.md` with full AL coverage table.
- ✅ Add `QUICKSTART.md` for fast onboarding.
- ✅ Update AL3/AL4 harness test cross-links to canonical Assurance Hub AL definitions.

## Release readiness (v0.5.1)

- CI executes AL1 through AL4 against the reference SUT.
- AL3 and AL4 controls now have executable harness coverage for the highest-assurance governance and audit expectations.
- AL contract pinning is verified against the canonical Assurance Hub snapshot.
- Harness documentation consolidated and quickstart added for new implementers.

_Last updated: 2026-03-06_

## UNTP DIA / IDR alignment

Add explicit guidance and examples for evaluating authoritative directories that use UNTP Digital Identity Anchor (DIA) and Identity Resolver (IDR) patterns (identity anchoring extension for SAD-1).

### Supply chain integrity

- Expand TSPP-SCI evidence patterns (SBOM, provenance, signed releases) and align validation hooks with CTS and Assurance Hub.
