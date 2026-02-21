# Evidence Bundles

Evidence bundles are generated artifacts that make conformance results **auditable** and **replayable**.

## Design goals
- **Deterministic**: rerunning the same inputs against the same SUT should produce comparable outputs
- **Complete**: include enough request/response material to reproduce the decision
- **Safe**: do not leak secrets (API keys, private keys, access tokens)

## Recommended contents
- `run.json`: run metadata (run_id, timestamp, profile, SUT target)
- `verdicts.json`: per-test outcomes with reasons and assertions
- `requests/`: normalized requests used
- `responses/`: normalized responses captured
- `logs/`: runner logs (optional)

## Redaction policy
- Authorization headers and API keys MUST be redacted.
- Signed responses MAY be stored; private key material MUST NEVER be stored.

