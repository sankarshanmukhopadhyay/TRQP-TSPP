# Deployment guidance (TSPP v0.1)

This is operator-focused guidance for rolling out TRQP with the TSPP profile.

## Start with AL1, but design for AL2
- Implement metadata publication, freshness semantics, context allowlisting, and rate limiting immediately.
- Keep the migration path open to signed responses and sender-constrained tokens.

## Recommended rollout sequence
1) Publish `/.well-known/trqp-metadata` and keep it accurate.
2) Enforce schema validation and strict parsing limits.
3) Enforce token TTL, aud scoping, and scopes.
4) Implement rate limits and scan detection.
5) Implement freshness and cache-control semantics (time_evaluated, expires_at).
6) Move to namespaced/versioned vocab for action/resource.
7) For high-stakes ecosystems, adopt AL2 signed responses and endpoint integrity controls.

## Operational checklists

### Token and access management
- Tokens short-lived; separate scopes for authorization vs recognition
- Sender-constrained tokens for bulk clients
- Rotate and revoke client credentials quickly

### Availability
- Cache stable responses (within expiry window)
- Apply circuit breakers and request budgets per client
- Monitor for burst anomalies and scanning

### Privacy
- Do not log raw identifiers by default
- Reject or strip unknown context keys
- Consider privacy gateways/proxies and batching for high-risk deployments

### Governance and recognition
- Require recognition to be scoped and expiring (data model enforcement)
- Cap recognition chain depth; do not assume transitivity

## Running the conformance harness
See `harness/README.txt` for exact steps.
At a minimum, wire up:
- `TRQP_BASE_URL`
- `TRQP_BEARER_TOKEN` (if needed)
- update `harness/fixtures/queries.json` with IDs valid in your environment
