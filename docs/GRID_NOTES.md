# TSPP notes for GRID-style directories

TSPP implementers may consume a GRID-style directory to discover registrar services and decide whether to treat a registrar as authoritative.

## Minimum posture

- Treat the directory as **claims**, not truth.
- Require the registrar to be `active` in a **signed status feed** before treating it as authoritative.
- Apply the Assurance Hub mapping:
  - AL2: informational only
  - AL3: authoritative allowed
  - AL4: critical/high-assurance allowed

See the Assurance Hub for the canonical workflow:
- `docs/how-to-verify-grid.md`
