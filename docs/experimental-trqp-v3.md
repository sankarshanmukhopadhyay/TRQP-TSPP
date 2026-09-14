# Experimental TRQP v3 protocol/profile evidence

Status: **experimental downstream evidence; not an adopted Trust Over IP specification or profile**.

Tracking issue: https://github.com/sankarshanmukhopadhyay/TRQP-TSPP/issues/95

Umbrella tranche: https://github.com/sankarshanmukhopadhyay/tswg-trust-registry-protocol/issues/55

## Candidate pin

This branch evaluates the downstream candidate at commit `532a570ed8b7b468b7a317030077577b9859c14f` on `sankarshanmukhopadhyay/tswg-trust-registry-protocol: draft/next-trqp`.

The pin is machine-readable at `experimental/trqp-v3/source-pin.json`. A later candidate commit invalidates affected evidence until it is deliberately reconciled and rerun.

## Evidence strategy

TSPP does not import the candidate reference evaluator or the CTS candidate oracle. It reuses the repository's existing independent WP8 material-lifecycle/evidence-state validator and adds a candidate-specific protocol/profile contract.

Existing WP8 evidence already exercises:

- current, revoked, expired/superseded and unknown verification material;
- historical evaluation and incomplete history;
- authoritative vs non-authoritative sources;
- complete vs incomplete absence;
- stale evidence;
- wrong purpose/resource; and
- unsupported decision-critical verification-material context.

`experimental/trqp-v3/profile-contract.json` maps all 32 release-significant candidate requirement IDs to TSPP capabilities. `scripts/v3_profile_validator.py` verifies the authority pin, complete mapping, the existing independent WP8 outcomes and additional profile-boundary invariants covering negotiation, no silent v3→v2 downgrade, transport/semantic separation, discovery, recognition, profile conflict, privacy and audit reconstruction.

## Claim boundary

A `PASS` in the profile contract means the pinned candidate obligation is representable and independently pressure-tested at the TSPP protocol/profile boundary. It does **not** mean the candidate is an adopted upstream TRQP specification, and it is not a general production deployment certification.

Unknown or stale evidence maps to `indeterminate`; it is never converted to positive or authoritative negative merely to make the profile complete.

## Run locally

```bash
make v3-candidate-check
```

This runs the pre-existing WP8 tests plus the candidate profile validator and its regression tests.

## Promotion rule

This evidence is an input to Assurance Hub reconciliation. Stable `main` remains unchanged unless a later explicit governance decision promotes some or all of this experimental work after cross-repository evidence review.
