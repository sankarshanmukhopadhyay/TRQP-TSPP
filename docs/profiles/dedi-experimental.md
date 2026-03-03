# DeDi Experimental Profile (Operator Requirements)

**Status:** Experimental (non-normative)

This profile adapts TRQP-TSPP posture expectations to operators of Decentralized Directory Protocol (DeDi) directories.

## Scope

- Directory operators publishing DeDi artifacts (public keys, membership, revocation/negative lists, and ecosystem-specific records such as Beckn subscriber metadata).
- Assessors validating that a DeDi implementation meets baseline integrity and operational requirements aligned with TRQP Assurance Hub.

## Required artifacts (inputs)

- DeDi schemas and conventions (upstream): https://github.com/LF-Decentralized-Trust-labs/decentralized-directory-protocol
- Published artifacts (operator): `public_key`, `membership`, `revoke` (and any ecosystem record types)

## Posture expectations (high level)

### AL1–AL2 baseline

- **Key management:** operator MUST publish current signing keys and rotation metadata; SHOULD publish a documented rotation procedure.
- **Publication integrity:** operator MUST publish artifacts deterministically (stable formatting + checksums) and SHOULD provide a publication manifest.
- **Revocation:** operator MUST publish a negative list / revocation feed with timestamps and reason codes.
- **Availability:** operator SHOULD document uptime targets and incident response contact points.

### AL3–AL4 uplift

- **Independent assessment evidence:** operator SHOULD provide third-party assessment artifacts and remediation closure records.
- **Operational telemetry:** operator SHOULD provide monitoring summaries and forensic-grade logs for publication events.
- **Rotation proof:** operator MUST provide evidence of key rotation drills and compromise response readiness.

## Relationship to Hub & CTS

- The TRQP Assurance Hub defines the DeDi experimental **assurance profile mapping**.
- The TRQP Conformance Suite provides experimental **schema validation** for DeDi artifacts.

This TSPP profile defines how DeDi operators can satisfy posture expectations using the same evidence bundle patterns.

## Mapping matrix

See `docs/reference/dedi-mapping-matrix.md`
- Machine-readable matrix: `docs/reference/dedi-mapping-matrix.yaml` for the shared DeDi spine linking artifacts to Hub controls, CTS checks, and expected evidence.

