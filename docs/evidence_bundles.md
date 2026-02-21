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

## AL-aware evidence artifact expectations

To operationalize audits (and avoid “interpretive dance”), AL3/AL4 are defined as **auditable properties** with a deterministic evidence surface.

### Canonical artifact kinds

Implementations and tools SHOULD use these `kind` values consistently:

- `signed_response_sample`
- `jwks_snapshot`
- `binding_meta_log`
- `replay_window_test_log`
- `change_log_snapshot`
- `key_rotation_evidence`
- `error_response_sample`
- `key_custody_evidence`
- `monitoring_runbook`
- `retention_policy`

### Evidence artifact matrix (normative)

| Artifact kind | What it proves | AL2 | AL3 | AL4 |
|---|---|---:|---:|---:|
| `signed_response_sample` | Successful responses are signed and verifiable | REQUIRED | REQUIRED | REQUIRED |
| `jwks_snapshot` | Signing keys used during the run are discoverable/consistent | REQUIRED | REQUIRED | REQUIRED |
| `binding_meta_log` | Signed envelope includes binding meta (`query_hash`, `iat`, `exp`) and it is enforced | OPTIONAL | REQUIRED | REQUIRED |
| `replay_window_test_log` | Replay window / TTL controls are enforced (`max_ttl_seconds`) | OPTIONAL | REQUIRED | REQUIRED |
| `change_log_snapshot` | Change transparency signals exist and are consumable | OPTIONAL | REQUIRED | REQUIRED |
| `key_rotation_evidence` | Rotation/overlap posture exists and is evidenced | OPTIONAL | REQUIRED | REQUIRED |
| `error_response_sample` | Structured errors are signed and deterministic | OPTIONAL | OPTIONAL | REQUIRED |
| `key_custody_evidence` | Key protection/custody claims are backed by evidence (HSM/KMS/policy attestation) | OPTIONAL | OPTIONAL | REQUIRED |
| `monitoring_runbook` | Monitoring + incident response posture is documented | OPTIONAL | OPTIONAL | REQUIRED |
| `retention_policy` | Evidence/log retention is declared for auditability | OPTIONAL | OPTIONAL | REQUIRED |

**REQUIRED** means a run claiming that AL MUST include the artifact in its evidence bundle (or a clearly referenced equivalent).  
**OPTIONAL** means it MAY be included and, when present, SHOULD be machine-checkable.


## Redaction policy
- Authorization headers and API keys MUST be redacted.
- Signed responses MAY be stored; private key material MUST NEVER be stored.

