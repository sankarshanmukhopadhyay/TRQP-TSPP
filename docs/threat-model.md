# Threat model (TSPP v0.1)

This threat model is intentionally adversarial: it treats TRQP as critical infrastructure.

## Assets
- Integrity of **authority_id** bindings (who an authority is)
- Integrity of endpoint discovery (where clients send TRQP queries)
- Integrity and freshness of query responses (authorization/recognition outcomes)
- Privacy of relying parties and queried entities (avoid linkability and mapping)
- Availability of the query plane (DoS resistance)

## Adversaries
- Internet attackers: DoS, replay, enumeration, token theft, downgrade attempts
- Supply-chain attackers: compromised clients, misconfigured gateways, poisoned caches
- Grey actors: legitimacy laundering via recognition, coercion targeting via enumeration
- Powerful intermediaries: traffic analysis at CDN/ISP layers

## Primary attack classes
1. Endpoint redirection / discovery manipulation  
2. Token replay and credential stuffing  
3. Enumeration oracles via errors, timing, and metadata  
4. Replay via stale caching and revocation lag  
5. Semantic drift in bridges and ambiguous vocabularies  
6. Recognition chain abuse (manufactured legitimacy)  
7. Privacy harms via correlation (IDs + network metadata + optional context)  

## Security goals mapped to controls
- Prevent redirection: TLS posture, pinning (AL2), discovery change transparency
- Prevent replay: short-lived aud-scoped tokens, sender constraints (AL2), freshness and expiry semantics
- Prevent enumeration: uniform errors, rate limits, scan detection
- Prevent semantic failures: namespaced/versioned action/resource, tri-state outcomes, bridge fixtures
- Reduce correlation: context allowlist, log redaction, batching/proxies at architecture level

## Residual risk (explicit)
- Timing equalization cannot be perfectly proven by black-box tests
- Network-level correlation requires architectural mitigations beyond TRQP itself
- Governance quality (what the registry *means*) remains an ecosystem responsibility
