# Schema layout

This directory contains all JSON Schema definitions for the TRQP Security and Privacy
Profile (TSPP).

## Structure

```
schemas/
  core/                          # Canonical schema definitions (authoritative)
    tspp-trqp-metadata.schema.json     # Registry posture declaration (/.well-known/trqp-metadata)
    tspp-trqp-signed-response.schema.json  # AL2 signed response envelope
    test_outcome.schema.json           # Test verdict enum (PASS/FAIL/SKIP/…)
  evidence/                      # Evidence bundle schemas
    checksums.schema.json
    tspp_posture_bundle_descriptor.schema.json
  contexts/                      # JSON-LD context snapshots (non-normative vendors)
    untp/dia/0.6.1/
  tspp-trqp-metadata.schema.json      # $ref alias → core/tspp-trqp-metadata.schema.json
  tspp-trqp-signed-response.schema.json   # $ref alias → core/tspp-trqp-signed-response.schema.json
```

## Rules

- `schemas/core/` is the **canonical** location. All normative definitions live here.
- Root-level `schemas/*.schema.json` files are thin `$ref` wrappers for backwards compatibility.
  Do not add logic to them; update `schemas/core/` instead.
- `harness/schemas/` contains `$ref` wrappers pointing to `schemas/core/` for use by pytest.
  They follow the same rule: logic belongs in `schemas/core/`.
