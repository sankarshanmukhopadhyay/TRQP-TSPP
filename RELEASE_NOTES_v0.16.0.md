# TRQP-TSPP v0.16.0 — Lifecycle Materiality Evidence

This release adds executable security/privacy posture change-impact evidence for TRQP Stack 2026.2.

## Added

- portable lifecycle event fixtures for material, unknown, and demonstrably non-material changes;
- deterministic validation preventing material or unknown change from silently preserving current assurance;
- explicit affected-control and reassessment-scope evidence while retaining TSPP authority over security/privacy posture materiality.

## Authority boundary

TSPP owns posture materiality and affected-control judgments. TIS owns the portable lifecycle serialization contract. CTS owns conformance/replay reassessment consequences. The Assurance Hub owns combined current-assurance recomposition. This release transfers none of those authorities.

## Validation

The lifecycle fixtures and negative pressure tests are included in normal TSPP CI and portfolio integration validation.

## Stack relationship

v0.16.0 is the TSPP component candidate for TRQP Stack 2026.2. A component release does not by itself authorize the coordinated Stack release; the exact tuple remains subject to Hub release eligibility and human release judgment.
