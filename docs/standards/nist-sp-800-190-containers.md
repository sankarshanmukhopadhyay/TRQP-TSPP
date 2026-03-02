# NIST SP 800-190 (Application Container Security Guide)

> **Status:** informative (non-normative)

## Why this matters
Most TRQP deployments will be containerized. NIST SP 800-190 provides a concrete checklist for hardening container images, registries, runtimes, and orchestration, which lowers the blast radius of API compromises and configuration drift.

## TSPP touchpoints
- **Related control IDs:** `TSPP-AL4-02`, `TSPP-AL4-03`, `TSPP-AL4-05`
- **Where to implement:** image build pipeline, registry policy, runtime hardening, and secrets/key protection.

## Suggested evidence (operator-ready)
- Image scanning policy + scan reports
- Runtime security configuration snapshots (seccomp/AppArmor, rootless, read-only FS)
- Key/secrets management evidence aligned to `metadata.key_protection.*`
- Incident response runbook coverage for container compromise scenarios

## Practical implementation notes
- Treat these controls as “platform glue” that makes the TSPP controls easier to operate at scale.
- Where possible, automate evidence generation (CI/CD attestations, config snapshots, telemetry exports) to keep audit cost down.
