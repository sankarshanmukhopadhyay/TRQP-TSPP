---
owner: maintainers
last_reviewed: 2026-04-16
tier: 0
---

# Operational Trust Stack v1

This repository is the posture-computation layer in the Operational Trust Stack v1 release line.

## Role in the stack

TRQP-TSPP converts security, privacy, and control expectations into executable checks and a machine-readable Posture Report.

## What is new in v0.10.1

- Posture Report now includes `posture_score` and `coverage_index`
- Control satisfaction summary is emitted in the stable JSON output
- Golden flow example assets are included for stack integration
- Public documentation is synchronized with the cross-repo release narrative

## Golden flow

System under test -> TSPP Posture Report -> Conformance Report -> Combined Assurance Manifest -> Trust Registry publication


## Required identity contract

For combined assurance workflows, the TSPP posture report MUST expose the same `run_id` and `target_id` as the paired CTS report. The Assurance Hub now treats drift in these fields as a hard validation failure rather than an advisory warning.
