---
layout: default
title: "Roadmap"
nav_exclude: true
owner: maintainers
last_reviewed: 2026-08-28
---

# TSPP Roadmap

This roadmap records TSPP's repository-local contribution to the coordinated **TRQP Stack 2026.2** planning target for 30 September 2026. The coordinated roadmap and release decision remain owned by the TRQP Assurance Hub. TSPP retains authority over security/privacy controls, posture computation, and its producer evidence.

## Current baseline

TSPP v0.15.0 participates in TRQP Stack 2026.1 — Coconut and produces posture/control evidence under the machine-readable Stack producer contract.

## September governing question

> Can TSPP determine when previously produced security/privacy posture evidence remains reusable after change, and when that evidence must instead be reassessed or invalidated?

A change in bytes or version alone is not sufficient to declare material impact. Conversely, material target, control, provenance, identity, freshness, or deployment changes must not silently preserve prior posture evidence.

## Target capability: posture evidence invalidation

Candidate lifecycle result:

```text
previous TSPP evidence
        +
current target/posture inputs
        +
change evidence
        ↓
UNCHANGED / REASSESS_REQUIRED / INVALID
```

The exact vocabulary is implementation work; the semantic requirement is that downstream consumers can distinguish reusable evidence from evidence whose validity conditions no longer hold.

## Required work

### 1. Define TSPP materiality inputs

Evaluate at least:

- target implementation or target identity change;
- security/privacy configuration change;
- required control addition/removal/change;
- assurance-level or deployment-profile change;
- supply-chain/provenance change;
- evidence freshness/expiry change;
- producer or authority dependency change; and
- integrity failure.

### 2. Produce machine-readable invalidation evidence

The producer contract should expose enough evidence for the Hub to determine whether prior TSPP evidence is current, stale, invalid, or requires reassessment without reinterpreting TSPP control semantics.

### 3. Preserve legitimate non-material reuse

A documentation-only, volatile metadata, or other proven non-material change must be represented as a counter-case. The implementation must not create a policy that blindly reruns TSPP on every repository or artifact mutation.

### 4. Fail safely on unknown impact

When TSPP cannot establish that prior posture evidence remains applicable, the result must require reassessment rather than silently reuse the evidence.

## Pressure tests

| Change | Expected TSPP disposition |
|---|---|
| weakened security configuration | reassess / invalidate |
| required control removed | invalidate |
| target identity changes | invalidate prior target-bound evidence |
| supply-chain provenance changes materially | reassess |
| required evidence expires | stale / reassess |
| assurance/deployment profile changes | reassess |
| proven documentation-only change | reusable |
| impact cannot be determined | reassess |

Tests must validate these claims and boundaries, not merely exercise code paths.

## Candidate release

`v0.16.0` is a planning hypothesis for this capability. It should be cut only if TSPP gains a material adopter-facing invalidation/reassessment contract with tests, documentation, and producer evidence. Otherwise TSPP remains on its current release and the coordinated Stack plan must adapt.

## Target dates

- **1–6 Sep:** agree change/invalidation contract with Hub/TIS/CTS boundaries.
- **4–11 Sep:** implement TSPP invalidation evidence and pressure tests.
- **by 20 Sep:** resolve authority/schema compatibility dependencies.
- **20–25 Sep:** participate in coordinated adversarial tests.
- **26 Sep:** candidate freeze if eligible.

## Release acceptance evidence

TSPP is ready for the coordinated candidate only when:

- material changes cannot silently reuse prior posture evidence;
- a legitimate non-material counter-case is executable;
- unknown impact fails toward reassessment;
- invalidation evidence is machine-readable and bound to target/run/provenance identity;
- existing AL1–AL4 behavior has no unexplained regression; and
- repository-local validation and coordinated Stack producer checks are green.

## Visible judgment

The implementation issue/PR should preserve the proposition tested, the materiality assumptions adopted, pressure cases, the non-material counter-case, rejected approaches if any, and residual uncertainty. The release record should make clear why maintainers accepted the TSPP evidence as sufficient for the Stack 2026.2 candidate.
