# Assurance Hub ↔ TSPP Crosswalk

This document maps **Assurance Hub** evidence expectations to the concrete artifacts emitted by **TRQP-TSPP**.

- Assurance Hub “front door”: https://github.com/sankarshanmukhopadhyay/trqp-assurance-hub
- Hub evidence artifacts matrix: https://github.com/sankarshanmukhopadhyay/trqp-assurance-hub/blob/main/docs/guides/evidence-artifacts.md

## What TSPP emits

TSPP produces two related outputs:

1) **Conformance report JSON** (from the harness test run)
2) **Posture evidence bundle** (a portable wrapper around the report with integrity metadata)

### Posture evidence bundle

Created via `scripts/create_evidence_bundle.py`, the bundle includes:

| Artifact | Path | artifact_kind |
|---|---|---|
| Posture report | `tspp_posture_report.json` | `tspp_posture_report` |
| Bundle descriptor | `bundle_descriptor.json` | `tspp_posture_evidence_bundle_descriptor` |
| Checksums | `checksums.json` | `evidence_bundle_checksums` |
| Bundle zip | `bundle.zip` | `tspp_posture_evidence_bundle_zip` |

## AL alignment notes

TSPP uses `TSPP_EXPECT_AL` (e.g., `AL1`, `AL2`, `AL3`, `AL4`) to parameterize test expectations for the reference SUT and harness.

For canonical AL definitions and AL3/AL4 artifact expectations, treat the Hub guides as the source of truth:

- `docs/guides/assurance-levels.md`
- `docs/guides/evidence-artifacts.md`

This repo focuses on emitting the **posture evidence bundle** and making its evidence surface deterministic and machine-checkable.

## Schema references

- `schemas/evidence/tspp_posture_bundle_descriptor.schema.json`
- `schemas/evidence/checksums.schema.json`
