# Roadmap

This roadmap tracks high-level increments for TSPP.

## Completed

- ✅ Formalize AL dependency contract (`al-contract.json`) and clarify canonical AL source.
- ✅ Add standards alignment annex (`docs/standards-alignment.md`).
- ✅ Expand executable requirements coverage for AL3/AL4 governance + audit expectations (independent assessment, change control, rollback, policy, monitoring, and audit-log checks).
- ✅ Consolidate harness documentation into `harness/README.md` with full AL coverage table.
- ✅ Add `QUICKSTART.md` for fast onboarding.
- ✅ Update AL3/AL4 harness test cross-links to canonical Assurance Hub AL definitions.
- ✅ Ayra Trust Network baseline profile: control applicability table and evidence artifact mapping (`docs/profiles/ayra-baseline.md`).
- ✅ `schemas/README.md`: canonical vs alias schema layout documented, `$ref` wrapper pattern explained.
- ✅ Operational Stack metadata in TSPP JSON reports: `run_id`, `target_id`, `assurance_level`, `tool_version`.
- ✅ Harness CLI extended with `--run-id` and `--target-id` for integrated stack workflows.
- ✅ Interop demo profile added (`docs/profiles/interop-demo.md`) for coordinated stack demonstrations.

## Release readiness (v0.7.1)

- CI executes AL1 through AL4 against the reference SUT.
- TSPP reports carry shared `run_id`, `target_id`, `assurance_level`, and `tool_version` for Operational Stack integration.
- Ayra Trust Network baseline profile published with control mapping and evidence guidance.
- AL contract pinning verified against the canonical Assurance Hub snapshot (Hub v1.1.0).
- Harness documentation consolidated; quickstart available for new implementers.

_Last updated: 2026-03-17_

## UNTP DIA / IDR alignment

Add explicit guidance and examples for evaluating authoritative directories that use UNTP Digital Identity Anchor (DIA) and Identity Resolver (IDR) patterns (identity anchoring extension for SAD-1).

- Add TSPP evidence expectations for DIA `identityAnchor` and IDR `identityResolver` endpoints.
- Provide example harness test stubs for DIA/IDR endpoint validation.
- Cross-link to `docs/reference/untp-digital-identity-anchor.md` in the Assurance Hub.

### Supply chain integrity

- Expand TSPP-SCI evidence patterns (SBOM, provenance, signed releases) and align validation hooks with CTS and Assurance Hub.
- Add a supply chain integrity harness test module (`harness/tests/test_10_sci_controls.py`) covering SBOM presence, release provenance, and signing key freshness.

### Schema contract guidance

- Publish a schema contract note (analogous to `schemas/README.md`) clarifying which fields are stable across minor versions and what migration path adopters should follow when upgrading AL contract pins.
