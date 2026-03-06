# Changelog

## v0.4.1 (2026-03-06)

### Fixed
- Align the harness CLI and pytest fixtures so `--base-url` populates `TRQP_BASE_URL` reliably.
- Harden the reference SUT rate limiter with async locking and correct the 429 boundary condition.
- Synchronize public documentation, roadmap entries, and version pins for the patch release.

### Changed
- Replace the placeholder GitHub Pages URL in the README with the production repository URL.
- Expand `SECURITY.md` to cover reference implementation, workflow, and evidence-surface scope.

### Added
- Add a repository `.gitignore` to prevent bytecode, virtualenv, report, and OS cruft from shipping.

## v0.4.0 (2026-03-03)

### Added
- DeDi experimental posture profile for decentralized directory operators.
- SAD-1 security and privacy expectations for authoritative directory publication and governance.
- GRID security and privacy expectations aligned to SAD-1 and the Assurance Hub workflow.

### Changed
- Documentation updates linking Hub profile mapping and CTS schema validation.
- Update public documentation to position TSPP as a reusable security layer for evaluating authoritative directories.

### Fixed
- Repo hygiene improvements removing stray OS and bytecode artifacts.

## v0.3.0

### Added
- GRID interop guidance for TSPP consumers.
- Version-pinned cross-repo reference updates.

## v0.2.1

### Added
- Machine-readable `al-contract.json` to pin Assurance Level semantics to the canonical TRQP Assurance Hub definitions.
- `controls/control-registry.json` exporting TSPP control and requirement IDs for automation and mapping.
- `docs/standards-alignment.md` mapping TSPP controls to OWASP, NIST, and ISO references.

### Changed
- Clarified that AL1 to AL4 definitions are canonical in the TRQP Assurance Hub and are not redefined in this repo.
- Moved traceability fill-in content into an explicit template under `docs/templates/`.

### Fixed
- Reduced audit noise by removing template language from primary docs and templates.
