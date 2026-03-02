

## v0.2.2

### Added
- Program playbook (`docs/PLAYBOOK.md`) mirrored from Assurance Hub for cross-repo adoption consistency.

### Changed
- README and deployment guidance updated to reference the playbook and Hub operator runbook.
- Version bump for documentation alignment release.

# Changelog

All notable changes to this repository will be documented here.

## Unreleased
- (nothing yet)

## v0.2.3 (2026-03-02)

### Changed
- Pinned harness dependencies for deterministic CI runs (`harness/requirements.txt` and `harness/pyproject.toml`).
- CI now installs pinned FastAPI/Uvicorn deps for the reference SUT (`harness/ci-requirements.txt`).
- CI uses `tspp-harness` wrapper to ensure report emission is stable and explicit.

### Fixed
- CI reliability: wait-for-port loop for reference SUT startup; integration matrix no longer fail-fast.


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
