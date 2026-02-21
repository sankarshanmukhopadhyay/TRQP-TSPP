# Traceability Matrix (Template)

This document provides a *living* mapping between:
- **Normative requirements** (TRQP / TSPP specs, profiles, and policy statements)
- **Test Cases** implemented in this repository
- **Evidence artifacts** produced by test runs (reports, logs, signed payloads)

## How to use this
- Treat this as an *assurance spine*: every new requirement SHOULD get at least one test case.
- Every test case SHOULD reference the requirement IDs it supports.
- Every requirement SHOULD have at least one negative-path test where applicable.

## Matrix

| Requirement ID | Requirement (short) | Profile(s) | Test Case ID(s) | Evidence artifacts |
|---|---|---|---|---|
| TRQP-REQ-XXX | *(fill in)* | baseline / enterprise / high_assurance | TC-XXX | report.json, verdicts.json, responses/ |
| TSPP-REQ-XXX | *(fill in)* | AL1 / AL2 / AL3 / AL4 | test_XX_* | tspp-conformance-report.json |

## Conventions
- Requirement IDs are stable identifiers defined in specs or repo docs.
- Test Case IDs match filenames or explicit identifiers in YAML/pytest.
- Evidence artifacts are paths relative to a run output directory.

