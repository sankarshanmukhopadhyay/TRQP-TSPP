# GRID security and privacy expectations (TSPP)

This document applies TSPP expectations to the **GRID instance profile**, which implements SAD-1.

GRID is treated as an authoritative directory pattern where:

- entries represent registrars (or equivalent authority actors)
- publication and lifecycle updates must be independently verifiable
- governance artifacts bind listings to admission criteria

## What to validate

1. **Schema conformance** for published artifacts (where machine-readable forms exist).
2. **Integrity**: digests match published artifacts and signatures verify.
3. **Governance binding**: listings reference the admission policy and decision records.
4. **Lifecycle**: suspension and revocation events are timely and consistent.
5. **Operational accountability**: auditability, incident response, redress.

## References

- Hub profile: `https://github.com/sankarshanmukhopadhyay/trqp-assurance-hub/blob/main/profiles/grid-profile.md`
- Hub workflow: `https://github.com/sankarshanmukhopadhyay/trqp-assurance-hub/blob/main/docs/guides/directory-assurance-workflow.md`

## Identity anchoring considerations (UNTP DIA)

GRID implementations are likely to rely on UNTP identity anchoring patterns (DIA) so that listed registrars can prove control of issuer identifiers and bind those identifiers to verifiable credentials.

A GRID assessment SHOULD therefore include the SAD-1 identity anchoring extension requirements (SAD-1-ANCHOR-01..04) and ensure that any published anchors reference the correct JSON-LD context and resolver approach.
