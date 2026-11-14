---
layout: default
title: "Roadmap"
nav_exclude: true
owner: maintainers
last_reviewed: 2026-11-14
tier: 1
---

# TRQP-TSPP Roadmap

This roadmap records TSPP-owned security/privacy posture work and its relationship to coordinated TRQP Stack releases. TSPP remains authoritative for controls, assurance-level requirements, posture evaluation and producer evidence. The Assurance Hub independently owns coordinated Stack eligibility and publication; neither component changes the upstream TRQP protocol.

## Published baseline

**TRQP Stack 2026.4, Lotus**, is the current published coordinated release. Its immutable tuple is TSPP `v0.18.1`, CTS `v1.11.1`, and Assurance Hub `v1.14.0`, with TSMM `0.24.0` and TIS `0.15.0` as reference authorities. The canonical tuple and release evidence are maintained in the [Hub Lotus release](https://github.com/sankarshanmukhopadhyay/trqp-assurance-hub/releases/tag/trqp-stack-2026.4); local integration details are in [Portfolio Integration](portfolio-integration.md).

The current independent TSPP component release is `v0.18.1`. Changes subsequently merged to `main`, including the November adversarial posture-evidence checks, are not part of that immutable component tag or the Lotus release.

## Delivered capabilities and historical milestones

### September 2026: assurance validity under change

The Stack 2026.2 work introduced machine-verifiable posture evidence reuse, invalidation and reassessment after material changes. The governing [TSPP issue #69](https://github.com/sankarshanmukhopadhyay/TRQP-TSPP/issues/69) is closed; the associated coordination belonged to [Hub issue #39](https://github.com/sankarshanmukhopadhyay/trqp-assurance-hub/issues/39). Material change or unknown impact cannot silently preserve an earlier positive posture conclusion. Proven non-material changes may permit continued reuse under the producer's evidence and rationale contract.

This is **historical delivered work**, not a pending `v0.16.0` candidate or an outstanding September release schedule. The specific evidence and validity semantics are defined by the TSPP producer contract and implementation, not by this roadmap.

### October 2026: state-bound posture evidence

TSPP `v0.18.0` introduced SHA-256 identity binding for the supplied target-state snapshot. The corrected independent `v0.18.1` component is included in Lotus. Unverifiable or changed supplied state requires appropriate reassessment; a matching snapshot digest does **not** independently prove correspondence to a running deployment, continuing verification-material authority or current authorization. See [Evidence Bundles](evidence_bundles.md) for this boundary.

### November 2026: assurance-integrity hardening on maintained `main`

The TSPP [adversarial posture correction](https://github.com/sankarshanmukhopadhyay/TRQP-TSPP/pull/124) rejects contradictory detailed control results and summary counts, missing control observations and unsupported outcome categories. The [component publication reconciliation](https://github.com/sankarshanmukhopadhyay/TRQP-TSPP/pull/125) records the already published `v0.18.1` tag as terminal. These are maintained-code changes and must not be retroactively attributed to the October component tag.

## Next release and work intake

The next coordinated Stack release is **not scheduled or authorized by this roadmap**. [Hub issue #128](https://github.com/sankarshanmukhopadhyay/trqp-assurance-hub/issues/128) records the successor's explicit publication and consumer-verification obligations. TSPP must independently determine whether its post-tag evidence-acceptance changes require a new component version and compatibility guidance before inclusion in a newly pinned tuple.

Further security/privacy controls, supply-chain evidence, profile-specific coverage, adoption and schema-contract improvements should be undertaken only against a concrete TSPP-owned requirement or demonstrated deficiency. A dependency update, roadmap revision or passing CI run alone does not establish a material release event.

## Release judgment

Any new TSPP release requires evidence of changed behavior or a meaningful fix, relevant AL1–AL4 validation, documented evidence/schema compatibility and maintainer approval under [Release Policy](governance/release-policy.md). Where changed controls or evidence affect prior conclusions, reassessment and supersession boundaries must remain explicit. An internally generated test report is not independent certification.
