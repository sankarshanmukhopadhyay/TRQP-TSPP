# CIS Kubernetes Benchmark

> **Status:** informative (non-normative)

## Why this matters
If you run TRQP endpoints on Kubernetes, the CIS Kubernetes Benchmark is the de-facto baseline for secure configuration. It is not TRQP-specific—but it is the fastest way to avoid preventable misconfigurations in multi-tenant clusters.

## TSPP touchpoints
- **Related control IDs:** `TSPP-AL4-02`, `TSPP-AL4-03`, `TSPP-AL4-05`
- **Where to implement:** cluster hardening, workload policies, RBAC, admission control, and audit log retention.

## Suggested evidence (operator-ready)
- CIS benchmark scan output (or equivalent managed-service posture report)
- RBAC review artifacts and least-privilege evidence for operators
- Admission control policies (e.g., disallow privileged pods)
- Kubernetes audit log retention configuration aligned to `metadata.audit`

## Practical implementation notes
- Treat these controls as “platform glue” that makes the TSPP controls easier to operate at scale.
- Where possible, automate evidence generation (CI/CD attestations, config snapshots, telemetry exports) to keep audit cost down.
