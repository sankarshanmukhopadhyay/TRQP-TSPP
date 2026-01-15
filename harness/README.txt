TSPP TRQP Conformance Harness (v0.1)
===================================

This harness runs HTTP-level and semantic conformance checks for a TRQP deployment against
the TRQP Security & Privacy Profile (TSPP) v0.1.

It is intentionally "profile-first":
- validates required freshness semantics (time_evaluated, expires_at)
- checks metadata publication and declared constraints
- exercises rate limiting
- probes anti-enumeration behavior (uniform not_found surface)
- validates context allowlisting behavior
- validates tri-state client outcomes
- (AL2) validates signed response envelope shape and verifies JWS with JWKS

Quick start
-----------
1) Create a virtualenv and install deps:
   pip install -r requirements.txt

2) Set environment variables:
   export TRQP_BASE_URL="https://your-registry.example"
   export TRQP_BEARER_TOKEN="..."   # optional depending on your deployment
   export TSPP_EXPECT_AL="AL1"      # or AL2

3) Run:
   pytest -q

Fixtures
--------
- fixtures/queries.json: sample queries used for tests.
  Replace IDs with ones valid in your test environment.

Schemas
-------
This harness expects the TSPP schemas in ./schemas (metadata + signed response).
You can drop in your local copies, or keep the provided ones.

Notes
-----
- Some controls (mTLS, true timing equalization) cannot be perfectly proven from client-side tests.
  The harness treats them as "evidence required" controls, with optional operator-provided attestations.
