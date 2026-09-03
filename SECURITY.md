---
layout: default
title: "Security Policy"
nav_exclude: true
---

# Security Policy

## Supported versions

Security fixes are supported for the current released `v0.16.x` line. Older component releases and historical Stack tuples remain available for reproducibility and audit, but should not be assumed to receive security fixes unless a release note explicitly states otherwise.

If a vulnerability affects the current coordinated TRQP Stack release, remediation may require a component release and a subsequent Stack recomposition in the TRQP Assurance Hub. A component-level fix does not silently make previously published assurance current.

## Reporting a vulnerability

If you discover a security issue in this repository or its reference implementation artifacts, do not open a public issue with exploit details. Use GitHub's private vulnerability reporting for this repository when available, or contact the repository maintainer privately through the contact route listed on the maintainer's GitHub profile.

Include:

- affected files, versions, or components;
- potential impact;
- safe reproduction steps; and
- suggested remediation, if available.

Maintainers will acknowledge receipt, triage impact, coordinate remediation, and determine disclosure timing. Security reports are treated as evidence inputs; they do not by themselves establish a PASS/FAIL assurance conclusion until the affected authority and evidence are evaluated.

## Scope

This repository is in scope for reports that affect:

- the TSPP harness and its ability to produce trustworthy posture verdicts;
- the reference SUT under `examples/reference_sut/`;
- schemas, examples, and evidence-bundle tooling that could mislead adopters or auditors; and
- CI workflows and software-supply-chain integrity controls.

## Assurance and revocation

TSPP is authoritative for its security/privacy posture computation and affected-control evidence. The TRQP Assurance Hub is authoritative for coordinated Stack assurance state. If a material security change invalidates prior TSPP evidence, the previous evidence must be treated as stale until reassessment and supersession are recorded.

## Related guidance

Security reports should be interpreted alongside [`docs/threat-model.md`](docs/threat-model.md), [`docs/deployment-guidance.md`](docs/deployment-guidance.md), and [`GOVERNANCE.md`](GOVERNANCE.md).
