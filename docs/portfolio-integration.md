---
layout: default
title: "Portfolio Integration"
nav_exclude: true
permalink: /docs/portfolio-integration/
---

# Portfolio Integration

TRQP-TSPP participates in the coordinated TRQP Operational Trust Stack through `portfolio/integration-contract.json` and the machine-readable producer contract in `portfolio/stack-producer-contract.json`.

## Current coordinated release

**TRQP Stack 2026.3 — Banyan** validates the following adopter-facing tuple:

| Layer | Release |
|---|---:|
| TRQP-TSPP | v0.17.0 |
| TRQP Conformance Suite | v1.10.0 |
| TRQP Assurance Hub | v1.13.0 |
| TSMM | 0.24.0 |
| TIS | 0.15.0 |

The Assurance Hub is the coordinated-release authority and adopter front door. A Stack release declares that the specific tuple passed immutable component resolution, clean bootstrap, component evidence generation, deterministic CTS replay, profile-aware producer/consumer validation, combined-assurance composition, fail-closed negative cases, whole-stack semantic replay equivalence, provenance/integrity checks, and the executable adopter walkthrough.

The coordinated release does **not** replace TSPP's independent versioning or authority. TSPP remains authoritative for its security/privacy controls, assurance-level profiles, posture computation, and producer-issued profile-consumable posture evidence.

## Consumer value

An adopter who selects a coordinated Stack release does not need to determine compatible TSPP, CTS, Hub, TSMM, and TIS versions independently. The release manifest provides the validated tuple and evidence provenance; TSPP v0.17.0 supplies posture/control evidence with explicit profile-correlation context and lifecycle/reassessment state for consumption by the rest of the declared stack.

## Repository responsibilities

TRQP-TSPP owns its security/privacy control profiles, posture rules, and validation artifacts. Shared semantic definitions are referenced from QBF Consulting's `trust-systems-meta-model` 0.24.0, while shared portable contract/schema authority is referenced from QBF Consulting's `trust-infrastructure-schemas` 0.15.0.

The Conformance Suite produces independent executable conformance and replay evidence, and the Assurance Hub aggregates TSPP and CTS evidence with applicable profile/external-authority evidence into a combined assurance decision. Profile metadata cannot strengthen or overwrite a TSPP posture conclusion; material or unknown profile impact requires reassessment.

## Automated validation

`tools/validate_portfolio_contract.py` checks release pins, upstream authority versions, required local evidence, repository relationships, and invalidation conditions. `.github/workflows/portfolio-contract.yml` runs these checks on pull requests and pushes to `main` and uploads a JSON validation result.

A missing required artifact, incompatible authority version, producer-contract violation, or incompatible release relationship makes cross-repository integration invalid and detectable in CI.

## Release record

The canonical coordinated release record is maintained by the TRQP Assurance Hub under `stack/releases/2026.3/` and as the GitHub release tag `trqp-stack-2026.3`. Component releases continue to be published independently using repository-local semantic versioning.

Historical Stack 2026.1 and 2026.2 records remain immutable evidence of their tested tuples and are not rewritten when a newer coordinated release becomes current.
