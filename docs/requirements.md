# TSPP Requirements (Normative)

This document enumerates the **testable, ship-stopping requirements** in the TRQP Security & Privacy Profile (TSPP).

Requirement IDs are stable references for:
- implementations,
- conformance harness tests,
- audit evidence,
- discussions/issues/PRs.

## Metadata & Discovery

### TSPP-META-01 — Metadata publication
A TRQP deployment **MUST** publish profile metadata at `/.well-known/trqp-metadata`.

**Evidence:** HTTP 200 response containing a JSON object.

### TSPP-META-02 — Metadata schema conformance
The metadata document **MUST** conform to `schemas/tspp-trqp-metadata.schema.json`.

**Evidence:** Schema validation success.

## Context Controls

### TSPP-CTX-01 — Explicit context allowlist declared
Metadata **MUST** declare `context_allowlist` as an explicit list of accepted context keys.

**Evidence:** `context_allowlist` present in metadata.

### TSPP-CTX-02 — Unknown context key handling
For query endpoints, unknown context keys **MUST** be either:
- rejected (HTTP 400), or
- stripped and ignored.

Unknown keys **MUST NOT** be reflected back in successful responses.

**Evidence:** Harness test on an unknown context key fixture.

## Freshness & Time Semantics

### TSPP-FRESH-01 — Response freshness fields (authorization)
Successful authorization responses **MUST** include a `meta` object containing:
- `time_evaluated` (RFC3339 date-time string)
- `expires_at` (RFC3339 date-time string)

**Evidence:** Harness parses and validates these fields.

### TSPP-FRESH-02 — RFC3339-like formatting
`meta.time_evaluated` and `meta.expires_at` **MUST** be RFC3339-compatible date-time strings.

**Evidence:** Harness assertion.

### TSPP-FRESH-03 — Response freshness fields (recognition)
Successful recognition responses **MUST** include the same freshness fields as authorization.

**Evidence:** Harness test (when recognition fixtures are provided).

## Error Uniformity & Enumeration Resistance

### TSPP-ERR-01 — Uniform error surface
When returning an error as JSON, the response body **SHOULD** be shape-consistent across repeated identical requests.

**Evidence:** Harness samples repeated requests and checks key-shape consistency.

### TSPP-ENUM-01 — Enumeration side-channel mitigation (operator review)
Implementations **SHOULD** minimize side-channel signals (status code variability, response shape variability, and request timing) that enable entity enumeration.

**Evidence:** Harness records samples; operators review deltas. (This is intentionally a **SHOULD**, as strict timing equalization is environment-dependent.)

## Rate Limiting

### TSPP-RL-01 — Rate limit signals on 429
When responding with HTTP 429, the server **SHOULD** include at least one informative rate limit header, such as:
- `RateLimit-Limit`, `RateLimit-Remaining`, `RateLimit-Reset`, or `Retry-After`.

**Evidence:** Harness checks for presence when 429 is encountered.

## Assurance Level AL2 — Signed Responses

### TSPP-AL2-01 — Signed envelope in AL2
When operating in AL2, servers **MUST** return a signed response envelope when the client requests it (e.g., `Accept-Signature: jws`), using `payload` + `signature`.

**Evidence:** Harness validates envelope shape and schema.

### TSPP-AL2-02 — Verifiable signature via declared JWKS
In AL2, servers **MUST** publish a `signing.jwks_uri` in metadata and signatures **MUST** verify against keys from that JWKS.

**Evidence:** Harness fetches JWKS and verifies JWS.

## Bridge Equivalence

### TSPP-BRIDGE-01 — Semantic equivalence fixtures (optional)
If an operator provides bridge equivalence fixtures, a deployment **SHOULD** satisfy the expected semantic outcomes for those cases.

**Evidence:** Harness runs fixtures provided via `TSPP_BRIDGE_FIXTURES`.

---

## AL3 requirements (governance + audit)

These requirements apply when the deployment declares `assurance_level: "AL3"`.
They are **parameterized by** the canonical definitions in `../al-contract.json`
(the Hub is the upstream source of truth).

- **TSPP-AL3-01**: `metadata.signing.default_signed_responses` MUST be `true`.
- **TSPP-AL3-02**: Signed response envelopes MUST include a `meta` section suitable for audit.
- **TSPP-AL3-03**: `metadata.audit.independent_assessment_uri` MUST be present and resolvable.
- **TSPP-AL3-04**: `metadata.governance.change_control_uri` MUST be present and resolvable.

## AL4 requirements (governance + audit + monitoring)

These requirements apply when the deployment declares `assurance_level: "AL4"`.

- **TSPP-AL4-01**: All AL3 requirements MUST hold.
- **TSPP-AL4-02**: `metadata.key_protection.protection` MUST be declared and `metadata.key_protection.evidence_uri` MUST resolve.
- **TSPP-AL4-03**: `metadata.monitoring` MUST declare `evidence_retention_days`, `incident_contact`, and a resolvable `runbook_uri`.
- **TSPP-AL4-04**: `metadata.governance.policy_uri` and `metadata.governance.rollback_uri` MUST resolve.
- **TSPP-AL4-05**: `metadata.audit` MUST declare `audit_log_uri`, `immutability`, and `retention_days`.


## Software Supply Chain Integrity

These requirements apply to the **implementation and release pipeline** of a TRQP service (or authoritative directory service) where supply chain compromise would undermine trust.

### TSPP-SCI-01 — SBOM availability
Implementations **MUST** produce a Software Bill of Materials (SBOM) for production artifacts (service container image, package, or deployment unit).

**Evidence:** SBOM file (SPDX or CycloneDX) included in the evidence bundle.

### TSPP-SCI-02 — Dependency vulnerability monitoring
Implementations **MUST** continuously monitor dependencies for known vulnerabilities and maintain a documented remediation workflow.

**Evidence:** Monitoring configuration + triage/remediation runbook, and a recent scan output.

### TSPP-SCI-03 — Signed releases for production artifacts
Production artifacts **SHOULD** be cryptographically signed (for example, image signing) and verification steps **MUST** be documented.

**Evidence:** Signature material and verification instructions, plus a sample verification log.

### TSPP-SCI-04 — Provenance for build outputs
For AL3 and above, build outputs **MUST** be accompanied by verifiable provenance (for example, SLSA-style provenance).

**Evidence:** Provenance attestation for a release artifact and a documented verification procedure.

### TSPP-SCI-05 — CI policy enforcement
Repositories **MUST** enforce baseline CI security controls (branch protection, required reviews, and protected release workflows).

**Evidence:** Repository policy snapshot (or equivalent) and CI workflow configuration excerpts.

