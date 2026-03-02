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


## Assurance Level AL3 — Independently Assessable

### TSPP-AL3-01 — Default signing declared
In AL3, metadata **MUST** declare `signing.default_signed_responses=true`.

**Evidence:** Metadata field present and set to true.

### TSPP-AL3-02 — Signed envelope includes verifiable meta
In AL3, successful machine-consumed responses **MUST** be signed by default and the signed envelope **MUST** include a `meta` object with:
- `query_hash`
- `iat`
- `exp`

**Evidence:** Harness validates signed envelope shape and schema.

### TSPP-AL3-03 — Independent assessment reference
In AL3, metadata **MUST** declare `audit.independent_assessment_uri` that resolves to evidence suitable for third-party review.

**Evidence:** Harness fetches the URI and expects HTTP 200.

### TSPP-AL3-04 — Transparency change log
In AL3, metadata **MUST** declare:
- `transparency.change_log_uri`
- `transparency.published_at`

**Evidence:** Harness fetches `change_log_uri` and expects HTTP 200.

### TSPP-AL3-05 — Change control documentation
In AL3, metadata **MUST** declare `governance.change_control_uri` describing how policy/config changes are reviewed and activated.

**Evidence:** Harness fetches the URI and expects HTTP 200.

## Assurance Level AL4 — Governance + Audit Ready

### TSPP-AL4-01 — Governance policy + rollback declared
In AL4, metadata **MUST** declare:
- `governance.policy_uri`
- `governance.rollback_uri`

**Evidence:** Harness fetches both URIs and expects HTTP 200.

### TSPP-AL4-02 — Key protection declared
In AL4, metadata **MUST** declare `key_protection.protection` and `key_protection.evidence_uri`.

**Evidence:** Harness fetches `evidence_uri` and expects HTTP 200.

### TSPP-AL4-03 — Monitoring + retention declared
In AL4, metadata **MUST** declare monitoring evidence retention and operational response references:
- `monitoring.evidence_retention_days`
- `monitoring.incident_contact`
- `monitoring.runbook_uri`

**Evidence:** Harness fetches `runbook_uri` and expects HTTP 200.

### TSPP-AL4-04 — Audit log immutability + retention
In AL4, metadata **MUST** declare audit log posture:
- `audit.audit_log_uri`
- `audit.immutability` in {`append-only`, `immutable`}
- `audit.retention_days`

**Evidence:** Harness fetches `audit_log_uri` and expects HTTP 200.

## Bridge Equivalence

### TSPP-BRIDGE-01 — Semantic equivalence fixtures (optional)
If an operator provides bridge equivalence fixtures, a deployment **SHOULD** satisfy the expected semantic outcomes for those cases.

**Evidence:** Harness runs fixtures provided via `TSPP_BRIDGE_FIXTURES`.
