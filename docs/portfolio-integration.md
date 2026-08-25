---
layout: default
title: "Portfolio Integration"
nav_exclude: true
permalink: /docs/portfolio-integration/
---

# Portfolio Integration

TRQP-TSPP participates in the coordinated TRQP Operational Trust Stack through `portfolio/integration-contract.json` and the machine-readable producer contract in `portfolio/stack-producer-contract.json`.

## Current coordinated release

**TRQP Stack 2026.1 — Coconut** validates the following adopter-facing tuple:

| Layer | Release |
|---|---:|
| TRQP-TSPP | v0.15.0 |
| TRQP Conformance Suite | v1.8.0 |
| TRQP Assurance Hub | v1.11.0 |
| TSMM | v0.24.0 |
| TIS | v0.14.1 |

The Assurance Hub is the coordinated-release authority and adopter front door. A Stack release declares that the specific tuple has passed clean bootstrap, component evidence generation, deterministic CTS replay, combined-assurance validation, fail-closed negative cases, whole-stack semantic replay equivalence, provenance/integrity checks, and the executable adopter walkthrough.

The coordinated release does **not** replace TSPP's independent versioning or authority. TSPP remains authoritative for its security/privacy controls, assurance-level profiles, posture computation, and producer-issued evidence.

## Consumer value

An adopter who selects a coordinated Stack release does not need to determine compatible TSPP, CTS, Hub, TSMM, and TIS versions independently. The release manifest provides the validated tuple and evidence provenance; TSPP then supplies the posture/control evidence consumed by the rest of that declared stack.

## Repository responsibilities

TRQP-TSPP owns its security/privacy control profiles, posture rules, and validation artifacts. Shared semantic definitions are referenced from `trust-systems-meta-model` v0.24.0, while shared portfolio and repository schemas are referenced from `trust-infrastructure-schemas` v0.14.1.

The Conformance Suite produces independent executable conformance and replay evidence, and the Assurance Hub aggregates TSPP and CTS evidence into a combined assurance decision.

## Automated validation

`tools/validate_portfolio_contract.py` checks release pins, upstream authority versions, required local evidence, repository relationships, and invalidation conditions. `.github/workflows/portfolio-contract.yml` runs these checks on pull requests and pushes to `main` and uploads a JSON validation result.

A missing required artifact, incompatible authority version, producer-contract violation, or incompatible release relationship makes cross-repository integration invalid and detectable in CI.

## Release record

The canonical coordinated release record is maintained by the TRQP Assurance Hub under `stack/releases/2026.1/`. Component releases continue to be published independently using repository-local semantic versioning.
