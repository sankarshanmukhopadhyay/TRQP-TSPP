# Changelog

All notable changes to this repository will be documented here.

## Unreleased
- (nothing yet)

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
