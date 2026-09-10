# WP8 independent evidence validation

Status: **experimental TSPP-side assurance evidence**

Trackers:
- https://github.com/sankarshanmukhopadhyay/TRQP-TSPP/issues/79
- https://github.com/sankarshanmukhopadhyay/TRQP-TSPP/issues/80
- https://github.com/sankarshanmukhopadhyay/tswg-trust-registry-protocol/issues/1
- https://github.com/sankarshanmukhopadhyay/tswg-trust-registry-protocol/issues/2

Independent Lab evidence:
- https://github.com/sankarshanmukhopadhyay/trust-protocol-interop-lab/pull/207

External motivating input:
- https://github.com/ayraforum/ayra-trust-registry-resources/issues/43

## Purpose

TSPP independently validates whether an invalidation consumer can preserve material lifecycle and evidence-state distinctions without importing the downstream TRQP reference evaluator as its oracle.

The local vocabulary is deliberately TSPP-oriented rather than a proposed normative TRQP wire vocabulary:

- positive;
- negative;
- unknown;
- stale.

Reasons preserve the evidence distinction required for assurance, including complete versus incomplete absence, non-authoritative source, stale source, incomplete history, revocation, expiry/supersession, purpose/resource non-applicability and unsupported critical conditions.

## Safety invariants

1. A principal's recognition does not imply that every verification material bound to that principal is current or applicable.
2. Absence is a definitive negative only when the source is authoritative and complete for the evaluated scope.
3. Stale, incomplete, non-authoritative or historically insufficient evidence cannot become a positive result.
4. A decision-critical verification-material qualifier cannot be silently discarded into an unqualified positive result.
5. TSPP test evidence must preserve the reason that caused invalidation/uncertainty so the assurance path can distinguish policy rejection from evidence insufficiency.

## Evidence matrix

The executable tests cover current material, revocation, complete/incomplete absence, non-authoritative evidence, stale evidence, historical prior material, incomplete history, wrong purpose, wrong resource, unknown material under complete/incomplete evidence, unsupported critical conditions, expiry/supersession, pre-validity and the legacy qualifier-drop false-positive detector.

## Authority boundary

This document does not define normative TRQP response vocabulary or claim upstream authority. It records independent TSPP assurance behaviour. Relevant upstream TRQP issues must be reconciled before any downstream experimental semantic is promoted as stable.
