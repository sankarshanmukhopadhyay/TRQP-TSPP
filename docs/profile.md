# TRQP Security & Privacy Profile (TSPP) v0.2.1

This document defines a practical security and privacy deployment profile for the Trust Over IP
Trust Registry Query Protocol (TRQP).

**Goal:** convert “security considerations” into **ship-stopping requirements** and make them testable.

## Threat posture

TRQP is a high-leverage primitive: it can become a trust-decision input bus for ecosystems.
The dominant risks are not “crypto breaks,” but:

- endpoint/discovery redirection (authority identifier and endpoint discovery as the control plane)
- replay/staleness windows (caching, revocation propagation, time semantics)
- enumeration and coercion (TRQP as a directory of power)
- correlation privacy harms (identifiers + traffic analysis + optional context)
- semantic drift and ambiguity (action/resource collisions and bridge mapping errors)
- authority laundering through recognition semantics

## Assurance levels

This repository **consumes** Assurance Level (AL1–AL4) semantics from the TRQP Assurance Hub.

- Canonical definitions (normative): `trqp-assurance-hub/docs/guides/assurance-levels.md`
- This profile binds requirements and test expectations to ALs, but **does not redefine** AL meaning.


## Normative requirements (summary)

### Transport and endpoint integrity
- HTTPS only; minimum TLS posture; no silent downgrade.
- AL2: endpoint pinning for high-impact authorities and change transparency expectations.

### Authentication and authorization
- Short-lived, audience-restricted tokens; scope-limited.
- AL2: sender-constrained tokens (mTLS/DPoP) for bulk clients.
- Least privilege quotas and separation between query and admin capabilities.

### Anti-enumeration and abuse resistance
- Rate limits (per-client and per-IP), with evidence headers recommended.
- Prefer uniform not_found surface to avoid oracle leakage.
- Enumeration detection and operator alerting (mandatory for AL2).

### Freshness and replay controls
- Responses MUST include **time_evaluated** and **expires_at**.
- Clients MUST enforce expiry and staleness limits.
- AL2: signed response envelope binding response to query via query_hash.

### Semantic safety
- Namespaced, versioned action/resource tokens (AL2 MUST; AL1 SHOULD).
- Clients MUST implement tri-state outcomes: true/false/indeterminate.

### Context privacy
- Context keys allowlisted; unknown keys rejected or stripped.
- Logs must avoid raw identifiers by default; AL2 requires redaction and break-glass logging.

### Recognition constraints
- Recognition SHOULD/MUST be scoped + expiring.
- Clients must not assume transitivity by default; chain depth must be capped when enabled.

## How to use this repo

- The **OpenAPI contract** in `openapi/` defines required headers/fields and expected HTTP behavior.
- The **schemas** in `schemas/` define:
  - `.well-known/trqp-metadata` declarations, and
  - the AL2 signed response envelope.
- The **conformance harness** in `harness/` runs tests against a live TRQP deployment.

See `docs/threat-model.md` for deeper adversarial framing and `docs/deployment-guidance.md` for practical rollout.
