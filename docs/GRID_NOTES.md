# GRID interop notes (for TSPP implementers)

This note explains how TSPP operators can consume GRID-style directory data as **trust claims** rather than as an unquestioned database.

## Practical guidance

- Treat a directory listing as a *claim* bound to an issuer policy.
- Require a **signed status feed** for operational reliance.
- Apply AL-based eligibility (e.g., AL3/AL4) according to your risk posture.
- Prefer verifier-first workflows: validate schema → verify signature → check freshness → apply policy.

## External references

These references are included to demonstrate that TRQP can support different trust registry implementations:

- UN/CEFACT GTR / GRID: https://un.opensource.unicc.org/unece/uncefact/gtr/
- EBSI Trusted Issuers Registry APIs: https://hub.ebsi.eu/apis/pilot/trusted-issuers-registry
