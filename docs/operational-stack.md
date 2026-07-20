---
owner: maintainers
last_reviewed: 2026-07-03
tier: 0
---

# Operational Trust Stack v1

This repository is the posture-computation layer in the Operational Trust Stack v1 release line.

## Role in the stack

TRQP-TSPP converts security, privacy, and control expectations into executable checks and a machine-readable Posture Report.

## Current maturity release

- TSPP v0.14.0 is part of the Hub v1.9.0 / CTS v1.6.0 / TSPP v0.14.0 maturity tuple.
- Release governance now distinguishes patch, minor, maturity, and no-release changes.
- Release validation is recorded in `docs/release-validation.md`.
- The posture evidence contract remains compatible with Hub ingestion while future releases are gated on executable posture or evidence value.

## Golden flow

System under test -> TSPP Posture Report -> Conformance Report -> Combined Assurance Manifest -> Trust Registry publication


## Required identity contract

For combined assurance workflows, the TSPP posture report MUST expose the same `run_id` and `target_id` as the paired CTS report. The Assurance Hub now treats drift in these fields as a hard validation failure rather than an advisory warning.
