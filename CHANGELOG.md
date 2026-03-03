# Changelog


## v0.4.0 (2026-03-03)

- Add **DeDi experimental** posture profile for decentralized directory operators.
- Documentation updates linking Hub profile mapping and CTS schema validation.
- Repo hygiene: remove stray OS and bytecode artifacts.


## v0.4.0 (2026-03-03)

- Add SAD-1 security and privacy expectations for authoritative directory publication and governance.
- Add GRID security and privacy expectations aligned to SAD-1 and the Assurance Hub workflow.
- Update public documentation to position TSPP as a reusable security layer for evaluating authoritative directories.

## Unreleased

- Add Software Supply Chain Integrity controls (TSPP-SCI-01..05) aligned with OpenSSF guidance.
- Support bundling optional SBOM/provenance/Scorecard artifacts in posture evidence bundles.

- (nothing yet)
- Add SAD-1 identity anchoring extension requirements aligned to UNTP Digital Identity Anchor (DIA) and Identity Resolver (IDR); vendor DIA JSON-LD context.
## v0.2.4
### Added
- GRID interop guidance for TSPP consumers
- Version-pinned cross-repo reference updates

## v0.2.1
### Added
- Machine-readable `al-contract.json` to pin Assurance Level semantics to the canonical TRQP Assurance Hub definitions.
- `controls/control-registry.json` exporting TSPP control/requirement IDs for automation and mapping.
- `docs/standards-alignment.md` (informative) mapping TSPP controls to OWASP, NIST, and ISO references.

### Changed
- Clarified that AL1–AL4 definitions are canonical in the TRQP Assurance Hub and are not redefined in this repo.
- Moved traceability fill-in content into an explicit template under `docs/templates/`.

### Fixed
- Reduced audit noise by removing template language from primary docs and templates.
