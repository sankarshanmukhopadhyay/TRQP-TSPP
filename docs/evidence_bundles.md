# Evidence Bundles

TSPP produces **posture evidence bundles**: portable artifacts that make TSPP results *auditable*, *replayable*, and easy to ingest into the **TRQP Assurance Hub** combined-assurance workflow.

## What the bundle contains

When you run the harness with `TSPP_REPORT_PATH=...`, the conformance report is generated as JSON.

To package a Hub-aligned evidence bundle:

```bash
python scripts/create_evidence_bundle.py \
  --report reports/tspp_conformance_AL2.json \
  --out reports/evidence_AL2
```

This produces:

| Artifact | Path | artifact_kind | Notes |
|---|---|---|---|
| Posture report | `tspp_posture_report.json` | `tspp_posture_report` | Normalized TSPP results (stable filename). |
| Bundle descriptor | `bundle_descriptor.json` | `tspp_posture_evidence_bundle_descriptor` | Machine-readable index (paths + hashes). |
| Checksums | `checksums.json` | `evidence_bundle_checksums` | SHA-256 checksums for key artifacts. |
| Bundle zip | `bundle.zip` | `tspp_posture_evidence_bundle_zip` | Convenience packaging of the directory. |

## Assurance Hub alignment

- Hub combined workflow guide: https://github.com/sankarshanmukhopadhyay/trqp-assurance-hub/blob/main/docs/guides/combined-assurance.md
- Hub evidence artifacts matrix: https://github.com/sankarshanmukhopadhyay/trqp-assurance-hub/blob/main/docs/guides/evidence-artifacts.md

TSPP bundles are the primary producer for the Hub row “**TSPP posture evidence bundle**”.

## Schema references

- `schemas/evidence/tspp_posture_bundle_descriptor.schema.json`
- `schemas/evidence/checksums.schema.json`
