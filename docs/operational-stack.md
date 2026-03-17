---
owner: maintainers
last_reviewed: 2026-03-17
tier: 0
---

# Operational Trust Stack v1

This repository is the posture-computation layer in the Operational Trust Stack v1 release line.

## Role in the stack

TRQP-TSPP converts security, privacy, and control expectations into executable checks and a machine-readable Posture Report.

## What is new in v0.8.0

- Posture Report now includes `posture_score` and `coverage_index`
- Control satisfaction summary is emitted in the stable JSON output
- Golden flow example assets are included for stack integration
- Public documentation is synchronized with the cross-repo release narrative

## Golden flow

System under test -> TSPP Posture Report -> Conformance Report -> Combined Assurance Manifest -> Trust Registry publication
