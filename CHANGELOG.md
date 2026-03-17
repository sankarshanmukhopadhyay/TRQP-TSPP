## v0.8.0

- Added Posture Report scoring, coverage, and control satisfaction metrics.
- Added Operational Trust Stack public documentation and Golden Flow examples.
- Refreshed public-facing docs and synchronized versions across the stack.

## v0.7.0

- Add Operational Stack metadata to TSPP JSON reports: `run_id`, `target_id`, `assurance_level`, and `tool_version`.
- Extend the harness CLI with `--run-id` and `--target-id` support.
- Add `docs/profiles/interop-demo.md` and update the output contract for integrated stack workflows.

# Changelog

## v0.6.0 (2026-03-10)

### Fixed
- Align `docs/hub-crosswalk.md` version pins with `al-contract.json`: Hub v0.8.1 → v0.9.0;
  CTS v0.7.1 → v0.8.0; TSPP v0.5.1 → v0.6.0. Previously the crosswalk claimed v0.8.1 while
  `al-contract.json` in the same repo already pinned v0.9.0.

### Added
- `schemas/README.md`: documents the canonical (`schemas/core/`) vs alias (`schemas/`,
  `harness/schemas/`) schema layout, preventing future drift and explaining the `$ref`
  wrapper pattern to contributors.
- `docs/profiles/ayra-baseline.md`: TSPP control applicability table and evidence artifact
  mapping for registries operating within the Ayra Trust Network.
- Frontmatter (`owner`, `last_reviewed`, `tier`) to `docs/hub-crosswalk.md` to bring it
  under freshness SLA enforcement.

### Changed
- Update `README.md` to reflect v0.6.0 and the current downstream release train
  (CTS v0.8.0 · Hub v0.9.0).

## Cross-repo versions

| Repository | Version |
|---|---|
| TRQP-TSPP | v0.6.0 |
| Conformance Suite | v0.8.0 |
| Assurance Hub | v0.9.0 |

## v0.5.1 (2026-03-06)

- Synchronize public-facing documentation and release metadata with Conformance Suite v0.7.1 and Assurance Hub v0.8.1.
- Update cross-repo version pins and compatibility references after Commit 3 and 4 completion.
- Refresh roadmap and release artifacts for the patch alignment release.

## v0.5.0 (2026-03-06)

### Added
- Add `harness/README.md` consolidating harness documentation (supersedes `README.txt`), covering all AL1–AL4 test files, environment variables, and evidence packaging steps.
- Add `QUICKSTART.md` at the repository root for fast onboarding of new implementers and operators.
- Add documentation cross-links from `harness/tests/test_08_al3_controls.py` and `test_09_al4_controls.py` to the canonical Assurance Hub AL definitions.

### Changed
- Update `SECURITY.md` to expand threat model references and reporting scope clarification.
- Synchronize roadmap, release notes, and version pins for the coordinated v0.5.0 release.

---

*Prior entries below reflect earlier releases in this series.*

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
