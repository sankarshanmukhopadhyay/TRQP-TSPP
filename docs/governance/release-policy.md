---
owner: maintainers
last_reviewed: 2026-07-03
tier: 0
---

# Release Policy

TRQP-TSPP is the security and privacy posture computation engine for the Operational Trust Stack. Releases should improve executable posture evaluation, control evidence, profile clarity, or adopter confidence.

## Release classes

| Class | Allowed when | Example |
|---|---|---|
| Patch | Security fix, broken CI, broken docs link, schema regression, incorrect release metadata | `v0.13.1` |
| Minor | New executable controls, profile coverage, posture evidence semantics, lifecycle checks, or relying-party evidence | `v0.14.0` |
| Maturity | Coordinated TSPP, CTS, and Hub release train | Operational Trust Stack maturity release |
| No release | Typo, prose polish, non-substantive reference refresh | Batch into next milestone |

## Required release evidence

Every release must provide:

- Control or profile impact summary.
- Posture evidence artifact impact summary.
- Validation commands and outcomes.
- Compatibility tuple for TSPP, CTS, and Hub.
- Upgrade note for operators and downstream assurance consumers.

## Release blockers

A release must not be cut when:

- `VERSION`, README, changelog, release notes, and compatibility references disagree.
- New or changed controls lack documented evidence expectations.
- Schema or example changes are not validated.
- Generated files or OS artifacts are present in the release archive.
- The change is only editorial and does not fix a broken public path or incorrect assurance statement.
