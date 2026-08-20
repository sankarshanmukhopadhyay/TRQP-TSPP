# TRQP-TSPP v0.15.0

## Portfolio integration release

This release connects TRQP-TSPP to the current executable governance layer provided by Trust Systems Meta-Model v0.24.0 and Trust Infrastructure Schemas v0.14.1.

### Added

- Machine-readable cross-repository integration contract.
- Explicit upstream semantic and schema version pins.
- Declared relationships to the TRQP Conformance Suite and TRQP Assurance Hub.
- Automated validation of release pins, evidence availability, relationships, and invalidation conditions.
- CI-generated portfolio integration evidence artifact.

### Assurance impact

Cross-repository semantic drift and missing release evidence are now testable conditions. A release cannot satisfy the portfolio contract when required local evidence is missing or declared upstream compatibility is no longer valid.

### Compatibility

No protocol wire-format breaking change is introduced by this release. The feature is an integration and assurance control around the existing TSPP surface.
