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


## Assurance Level 3 (AL3) — Operational Non-Repudiation & Transparency

### TSPP-AL3-01 — Default signing for machine-consumed responses
When `assurance_level` is `AL3`, the deployment **MUST** advertise `signing.default_signed_responses=true` in metadata.

**Evidence:** metadata contains `signing.default_signed_responses=true`.

### TSPP-AL3-02 — Request/response binding in signed envelopes
When `assurance_level` is `AL3`, signed response envelopes **MUST** include `meta.query_hash`, `meta.iat`, and `meta.exp`.

**Evidence:** harness requests a signed response and validates `meta` fields.

### TSPP-AL3-03 — Bounded replay window declared
When `assurance_level` is `AL3`, the deployment **MUST** advertise `signing.binding.max_ttl_seconds` and it **MUST** be <= 7 days.

**Evidence:** metadata contains `signing.binding.max_ttl_seconds` within bounds.

### TSPP-AL3-04 — Change transparency signals
When `assurance_level` is `AL3`, the deployment **MUST** publish `transparency.change_log_uri` and `transparency.published_at`.

**Evidence:** metadata contains `transparency` object; `change_log_uri` fetch returns HTTP 200.

### TSPP-AL3-05 — Key lifecycle posture declared
When `assurance_level` is `AL3`, the deployment **MUST** advertise `signing.key_lifecycle` including rotation, overlap, and revocation posture.

**Evidence:** metadata contains `signing.key_lifecycle` with required fields.

## Assurance Level 4 (AL4) — Regulated-grade Key Custody & Operational Readiness

### TSPP-AL4-01 — Mandatory signing of structured errors
When `assurance_level` is `AL4`, the deployment **MUST** advertise `signing.sign_errors="MUST"`.

**Evidence:** metadata contains `signing.sign_errors="MUST"`.

### TSPP-AL4-02 — Auditable key protection posture
When `assurance_level` is `AL4`, the deployment **MUST** advertise a `key_protection` object including `protection` and an `evidence_uri`.

**Evidence:** metadata contains `key_protection`; `evidence_uri` fetch returns HTTP 200.

### TSPP-AL4-03 — Monitoring and evidence retention posture
When `assurance_level` is `AL4`, the deployment **MUST** advertise `monitoring` including retention, incident contact, and runbook URI.

**Evidence:** metadata contains `monitoring`; `runbook_uri` fetch returns HTTP 200.
