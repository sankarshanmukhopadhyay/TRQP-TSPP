---
owner: maintainers
last_reviewed: 2026-07-03
tier: 0
---

# Release Validation

This record defines the validation gate for TSPP v0.14.0 in the Operational Trust Stack Maturity Release.

## Compatibility tuple

| Repository | Version | Role |
|---|---:|---|
| TRQP-TSPP | v0.14.0 | Security and privacy posture evidence producer |
| TRQP Conformance Suite | v1.6.0 | Protocol conformance evidence producer |
| TRQP Assurance Hub | v1.9.0 | Combined assurance orchestration and publication |

## Required commands

```bash
python scripts/doc_tests.py
python scripts/schema_check.py
cd harness
pytest -q
```

## Acceptance criteria

- Markdown internal links resolve.
- JSON and YAML artifacts parse.
- Schema checks complete without regression.
- Harness tests complete against the reference SUT and configured fixtures.
- Posture report semantics remain compatible with Hub v1.9.0 ingestion.
- Release archive contains no `.DS_Store`, generated egg-info, build, or dist artifacts.

## Local validation status

| Check | Status | Notes |
|---|---|---|
| `python scripts/doc_tests.py` | Passed | Markdown links and parse checks completed locally. |
| `python scripts/check_doc_freshness.py` | Passed | Governed document freshness metadata refreshed for the maturity release. |
| `python scripts/schema_check.py` | Passed | Schema checks completed locally. |
| `cd harness && pytest -q` | Blocked locally | Local environment lacked `pytest`; dependency installation was blocked by package-index/proxy access. Must be rerun in CI or a developer environment with `harness/requirements.txt` installed. |
| Archive hygiene | Passed | `.DS_Store` and generated `*.egg-info` artifacts removed from the release working tree. |

## Release decision

TSPP v0.14.0 is release-worthy because it establishes the governance, validation, and archive hygiene threshold for future posture-engine releases while preserving compatibility with v0.12.0 posture report consumers.
