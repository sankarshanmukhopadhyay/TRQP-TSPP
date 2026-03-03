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
