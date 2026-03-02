# OWASP API Security Top 10

> **Status:** informative (non-normative)

## Why this matters
The OWASP API Security Top 10 is a pragmatic catalog of failure modes for internet-exposed APIs. TRQP endpoints are APIs—so this list is a convenient “what could go wrong” checklist for security review and hardening.

## TSPP touchpoints
- **Related control IDs:** `TSPP-META-01`, `TSPP-META-02`, `TSPP-ERR-01`, `TSPP-ENUM-01`, `TSPP-RL-01`, `TSPP-AL2-02`
- **Where to implement:** request validation, error hygiene, enumeration resistance, authZ/authN boundaries, and resource consumption protections.

## Suggested evidence (operator-ready)
- API threat model covering at least: broken authZ, excessive data exposure, resource exhaustion
- Schema validation tests (positive + negative)
- Uniform error handling tests to prevent oracle behavior
- Rate limiting configuration + verification tests

## Practical implementation notes
- Treat these controls as “platform glue” that makes the TSPP controls easier to operate at scale.
- Where possible, automate evidence generation (CI/CD attestations, config snapshots, telemetry exports) to keep audit cost down.
