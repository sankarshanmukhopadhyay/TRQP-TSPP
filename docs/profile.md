# TRQP Security & Privacy Profile (TSPP) v0.2

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

TSPP defines assurance levels as **auditable properties**, not vibes. Each level is a bundle of
requirements with clear evidence expectations.

- **AL1 (Baseline / Internet-safe):** minimum posture for public internet exposure.
- **AL2 (High Assurance / Critical infrastructure):** signed responses on demand (when requested) and tightened controls for high-impact authorities.
- **AL3 (Operational non-repudiation + change transparency):** signed responses are the *default* for machine-consumed outputs, with explicit request/response binding, bounded replay windows, and published change transparency signals.
- **AL4 (High-risk / regulated operations):** AL3 plus auditable key custody/protection claims and operational monitoring/retention posture suitable for regulated or nationally strategic reliance.

### What becomes stronger at AL3 / AL4

| Area | AL3 (Auditable operations) | AL4 (Regulated-grade posture) |
|---|---|---|
| Signing default | MUST sign successful machine-consumed responses by default | MUST sign; plus MUST sign structured errors |
| Binding | MUST include request binding (`query_hash`) and time semantics (`iat/exp`) | Same as AL3 (non-negotiable) |
| Replay window | MUST be bounded and declared (`max_ttl_seconds`) | Same as AL3, with stronger evidence retention |
| Change transparency | MUST publish a change log / published-at semantics | MUST publish + treat drift as an incident class |
| Key lifecycle | MUST declare rotation/overlap/revocation posture | MUST declare + provide auditable key protection evidence |
| Monitoring | SHOULD have operational runbooks | MUST declare monitoring + incident contact + retention |

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
