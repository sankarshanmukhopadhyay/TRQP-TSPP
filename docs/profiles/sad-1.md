# SAD-1 security and privacy expectations (TSPP)

SAD-1 (Sovereign Authoritative Directory) is a **registry-agnostic profile** used by the TRQP ecosystem to evaluate
authoritative directories, including sovereign registries.

This document defines the **security and privacy expectations** that TSPP contributes when SAD-1 is used.

## Threat model focus

Authoritative directories are high-leverage attack surfaces:

- poisoning the directory to elevate unqualified actors
- suppressing or delaying revocation updates
- replaying old publications to bypass governance changes
- correlating directory metadata to derive sensitive operational insights

## TSPP control families that apply

### Publication authenticity and replay resistance

Operators MUST provide verifier-first integrity for published directory artifacts:

- deterministic digests (SHA-256) for all published artifacts
- signed publication manifests (keyed to a governance identity)
- explicit publication timestamps and monotonic update semantics

### Administrative action security

Directory updates are administrative actions and MUST be protected:

- strong authentication for publisher/operator identities
- authorization policy separating submitters, approvers, and publishers
- audit logging that is tamper-evident and retention-bound to AL

### Transparency, accountability, and redress

At AL3/AL4, a directory MUST provide:

- incident reporting and change disclosure expectations
- dispute handling and redress procedures
- evidence of revocation propagation

### Privacy constraints

Directory entries SHOULD minimize personal data exposure:

- publish only what is necessary to verify authority claims
- avoid leaking correlation handles unless explicitly required by the directory model
- document a privacy impact assessment for AL3/AL4 targets

## Evidence bundle expectations

When evaluating a directory under SAD-1, an evidence bundle SHOULD include:

- the published directory artifacts (entries, manifest, status feed)
- key material references (public keys, key rotation policy)
- governance policy documents and decision records
- operational logs or attestations appropriate to the target AL

See also: `docs/evidence_bundles.md` and `docs/requirements.md`.

## Identity anchoring extension (DIA / IDR)

Authoritative directories may bind directory subjects (registrars, facilities, products, trademarks, etc.) to an identity anchoring mechanism so that relying parties can independently verify issuer identity and resolve identifiers.

When UNTP Digital Identity Anchor (DIA) and Identity Resolver (IDR) patterns are used, the directory evaluation scope is the **composite trust system**: directory governance + directory publication integrity + identity anchoring.

### Requirements

SAD-1-ANCHOR-01: If the directory publishes identity anchors, it MUST declare the anchor mechanism and version (for example `UNTP_DIA_0.6.1`).

SAD-1-ANCHOR-02: Anchor credentials MUST be referenceable using the correct JSON-LD context URL for the declared anchor mechanism.

SAD-1-ANCHOR-03: If issuer identifiers are DIDs, the directory operator MUST document the DID method(s) supported and the resolution approach (direct DID resolution, registry-based, or hybrid via an Identity Resolver).

SAD-1-ANCHOR-04: If revocation or status is supported, the directory MUST publish status pointers and lifecycle rules, and MUST ensure revocation state propagates to the directory status feed within defined SLAs.

### Evidence

- Anchor credential samples (or references) and context references
- Resolver configuration / endpoint documentation
- Revocation/status publication artifacts (where applicable)
- Assessment notes on resolution and lifecycle behavior

Normative references:
- UNTP DIA: https://untp.unece.org/docs/specification/DigitalIdentityAnchor/
- UNTP IDR: https://untp.unece.org/docs/specification/IdentityResolver/
- DIA JSON-LD context (0.6.1): https://test.uncefact.org/vocabulary/untp/dia/0.6.1/context/
