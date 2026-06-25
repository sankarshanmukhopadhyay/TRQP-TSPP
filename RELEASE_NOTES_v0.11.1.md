# TRQP-TSPP v0.11.1 Release Notes

## Summary

This patch adds lifecycle and revocation publication posture to TSPP. Operators can now declare where lifecycle/status information is published, which lifecycle states are supported, whether revocation is operationalized, and what publication SLA applies.

## Added

- `lifecycle_publication` metadata in the TSPP TRQP metadata schema.
- Harness checks `TSPP-LIFE-01` through `TSPP-LIFE-03`.
- Reference SUT endpoints for `/.well-known/trqp-lifecycle` and lifecycle evidence.
- Control registry entries for lifecycle publication metadata, revocation-capable state sets, and resolvable status feeds.

## Validation

- `python scripts/doc_tests.py`
- `python scripts/schema_check.py`

## Coordinated Release Tuple

- TRQP-TSPP: v0.11.1
- TRQP Conformance Suite: v1.3.1
- TRQP Assurance Hub: v1.6.1
