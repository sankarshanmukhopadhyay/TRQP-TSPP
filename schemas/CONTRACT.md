# Schema contract

This document declares the stability guarantees and migration policy for all
JSON Schema definitions in `schemas/`. Read this before upgrading AL contract
pins or integrating TSPP schema outputs into downstream tooling.

## Stability tiers

| Tier | Meaning |
|---|---|
| **Stable** | Field names, types, and enum values are frozen across minor versions. |
| **Extensible** | New optional fields may be added in minor versions. Existing fields are stable. |
| **Experimental** | May change in any minor version. Annotated `"x-stability": "experimental"`. |

## Schema-by-schema contract

### `schemas/core/tspp-trqp-metadata.schema.json`

Describes the `/.well-known/trqp-metadata` response.

| Field | Tier | Notes |
|---|---|---|
| `profile`, `assurance_level` | Stable | Required; enum values frozen per AL contract. |
| `operator`, `auth`, `rate_limits`, `freshness`, `context_allowlist` | Stable | Required structure; inner fields extensible. |
| `signing.*` | Extensible | Optional sub-fields may be added as signing requirements evolve. |
| `audit`, `governance`, `key_protection`, `monitoring` | Extensible | AL3/AL4 extension blocks. New fields within these blocks may appear in minor versions. |
| `transparency`, `namespacing`, `recognition_policy` | Extensible | Optional informational blocks. |

### `schemas/core/tspp-trqp-signed-response.schema.json`

Describes the AL2+ signed response envelope.

| Field | Tier | Notes |
|---|---|---|
| `payload`, `signature`, `meta` | Stable | Required fields. |
| `signature.alg`, `signature.kid`, `signature.jws` | Stable | Required within `signature`. |
| `signature.query_hash`, `signature.hash_alg`, `signature.canonicalization` | Extensible | Optional; may be enriched. |
| `meta.query_hash`, `meta.iat`, `meta.exp` | Stable | Required within `meta` at AL3+. |

### `harness/schemas/tspp-conformance-report.schema.json`

Describes the TSPP conformance report emitted by `pytest_sessionfinish`.

| Field | Tier | Notes |
|---|---|---|
| `profile`, `generated_at`, `run_id`, `target_id`, `assurance_level`, `tool_version`, `tool`, `target`, `summary`, `results` | Stable | All required. |
| `summary.exit_status`, `summary.PASS`, `summary.FAIL`, `summary.SKIP`, `summary.NOT_APPLICABLE`, `summary.ERROR`, `summary.XFAIL` | Stable | Required summary counts. |
| `summary.posture_score`, `summary.coverage_index`, `summary.control_satisfaction` | Extensible | Optional metrics added in v0.9.0; stable going forward. |
| `results[*].nodeid`, `results[*].name`, `results[*].outcome`, `results[*].duration_seconds`, `results[*].requirement_ids` | Stable | Required per-result fields. |
| `results[*].notes` | Extensible | Optional. |

### `harness/schemas/tspp-bridge-fixtures.schema.json`

Describes the bridge golden fixtures file.

| Field | Tier | Notes |
|---|---|---|
| `cases[*].id`, `cases[*].query`, `cases[*].expected` | Stable | Canonical fixture shape added in v0.9.0. |
| `cases[*].trqp_query`, `cases[*].expected_trqp_outcome` | Stable (legacy) | Deprecated aliases retained for backwards compatibility. Will not be removed before v1.0.0. |
| `cases[*].system_of_record_truth` | Extensible | Informational; optional. |

### `schemas/evidence/tspp_posture_bundle_descriptor.schema.json`

| Field | Tier | Notes |
|---|---|---|
| All required fields | Stable | Required fields frozen. |
| Optional extension fields | Extensible | New optional fields may appear in minor versions. |

---

## Canonical vs alias layout

`schemas/core/` is the **canonical** location for all normative definitions.
Root-level `schemas/*.schema.json` files and `harness/schemas/*.schema.json`
files are thin `$ref` wrappers pointing to `schemas/core/`. Always read the
canonical file for normative content.

See `schemas/README.md` for the full layout and the `$ref` wrapper pattern.

## Migration policy

### Minor version bump

- New optional fields may be added.
- Enum values for **Extensible** fields may be extended.
- No field removals or type changes on **Stable** fields.
- Downstream pins: update `al-contract.json` SHA-256 and version string.
- Conformance reports from prior minor versions remain structurally valid.

### Major version bump

- Any **Stable** field may change with explicit migration notes in `CHANGELOG.md`.
- A migration guide will be published in `docs/` before the release.
- The `profile` field value in conformance reports will be bumped (e.g., `TSPP-TRQP-0.2`).

### AL contract pin upgrade checklist

1. Update `al-contract.json` → `canonical_source.canonical_doc_sha256` and version pin.
2. Run `scripts/verify_al_contract.py` to confirm the new hash matches.
3. Run `python -m compileall harness/ scripts/ examples/ schemas/` for syntax check.
4. Re-run the full CI matrix to confirm no regressions.

_Last updated: 2026-03-19_
