---
layout: default
title: "TRQP Stack producer contract"
nav_exclude: true
---

# TRQP Stack producer contract

TRQP-TSPP is a producer in the coordinated TRQP Operational Trust Stack. Its stack-facing contract is machine-readable at `portfolio/stack-producer-contract.json`.

The stack contract requires TSPP posture and control evidence to carry the same `run_id` and `target_id` used by the conformance execution that will later be aggregated by the TRQP Assurance Hub. A coordinated stack release must additionally preserve component version or commit provenance and artifact integrity hashes.

This repository remains authoritative for TSPP control definitions, posture evaluation semantics, and TSPP evidence generation. It does not acquire authority over CTS conformance semantics, combined assurance decisions, or coordinated stack-release declarations.

A consumer must fail closed when required evidence is absent, schema-invalid, correlated to a different run or target, or produced under an unsupported semantic/schema authority tuple.
