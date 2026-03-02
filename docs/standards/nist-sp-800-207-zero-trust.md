# NIST SP 800-207 (Zero Trust Architecture)

> **Status:** informative (non-normative)

## Why this matters
Zero Trust reduces implicit trust between service tiers, limits lateral movement, and forces explicit policy enforcement at each request boundary—exactly where TRQP endpoints tend to get abused (authority laundering, metadata scraping, and replay).

## TSPP touchpoints
- **Related control IDs:** `TSPP-CTX-01`, `TSPP-CTX-02`, `TSPP-RL-01`, `TSPP-AL2-01`, `TSPP-AL2-02`
- **Where to implement:** API gateway, service mesh policy, and token issuance/validation (“never trust, always verify”).

## Suggested evidence (operator-ready)
- Network/service segmentation design (service tiers, ingress/egress policy)
- Token validation policy (audience, issuer allowlist, TTL, sender constraints)
- Access policy change control (who can change recognition policies + how it’s reviewed)
- Rate-limit and anomaly detection evidence (dashboards or export snapshots)

## Practical implementation notes
- Treat these controls as “platform glue” that makes the TSPP controls easier to operate at scale.
- Where possible, automate evidence generation (CI/CD attestations, config snapshots, telemetry exports) to keep audit cost down.
