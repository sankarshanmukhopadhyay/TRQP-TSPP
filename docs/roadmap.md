---
layout: default
title: "Roadmap"
nav_exclude: true
---

# TRQP-TSPP Roadmap

**Last reviewed:** 2026-08-28

This roadmap records TSPP-owned delivery priorities and its contribution to coordinated TRQP Stack releases. TSPP retains authority over security/privacy controls and posture semantics; coordinated Stack planning does not transfer that authority to the Assurance Hub.

## Current coordinated baseline

TRQP Stack 2026.1 — Coconut validates TSPP `v0.15.0` with CTS `v1.8.0` and Assurance Hub `v1.11.0`.

## September 2026 priority: assurance validity under change

**Coordinating issue:** https://github.com/sankarshanmukhopadhyay/trqp-assurance-hub/issues/39  
**TSPP issue:** https://github.com/sankarshanmukhopadhyay/TRQP-TSPP/issues/69  
**Target coordinated release:** TRQP Stack 2026.2 by 30 September 2026, subject to evidence readiness.

### TSPP proposition

> TSPP posture evidence MUST NOT remain reusable when a material change invalidates the target, control applicability, security/privacy posture, evidence freshness, producer identity, or another declared validity condition.

### Required capability

TSPP should produce machine-verifiable evidence sufficient to distinguish at least:

- unchanged/reusable posture evidence;
- reassessment required;
- invalid/non-reusable posture evidence.

Unknown impact must not be interpreted as reusable evidence.

### Required pressure tests

Material cases include weakened/removed controls, target-identity change, evidence expiry/unavailability, assurance/deployment-profile change, producer/provenance discontinuity, and material supply-chain evidence change.

A legitimate counter-case must also be executable: documentation-only or equivalent non-material metadata change should not force reassessment when non-impact is supported by evidence.

### Acceptance evidence

- material and non-material change fixtures;
- fail-safe unknown-impact behavior;
- machine-readable evidence-reuse decision;
- preserved run/target/provenance correlation;
- AL1–AL4 regression coverage;
- negative tests rejecting stale/invalid posture evidence;
- synchronized producer contract and adopter documentation.

## Candidate release decision

`v0.16.0` is a candidate only if the material invalidation capability lands. Routine documentation/dependency changes do not justify a Stack-driven TSPP version bump.

## Timing

| Target | Outcome |
|---|---|
| 6 Sep | validity/change contract aligned with Stack work |
| 11 Sep | TSPP invalidation capability and pressure tests ready |
| 20–25 Sep | participate in coordinated adversarial suite |
| 26 Sep | candidate tag/version decision frozen |
| 27–28 Sep | coordinated eligibility replay |

## Visible judgment

The implementation history must preserve which changes are treated as material, legitimate counter-cases, uncertainty boundaries, and why the selected classification is safe. Green execution alone is not sufficient evidence of the release judgment.

## Continuing backlog

Existing TSPP roadmap items, including UNTP DIA/IDR guidance, supply-chain integrity, schema-contract guidance, assurance-level coverage, and adoption improvements continue as normal backlog. They are not Stack 2026.2 release blockers unless they materially intersect the governing proposition above.
