# TSPP Traceability Matrix

This matrix links **Requirements → Harness tests → Evidence** so that conformance is auditable.

| Requirement ID | Summary | Harness test | Evidence artifact |
|---|---|---|---|
| TSPP-META-01 | Metadata published at well-known endpoint | `test_01_metadata.py::test_metadata_published_and_valid` | HTTP 200 + body |
| TSPP-META-02 | Metadata validates against schema | `test_01_metadata.py::test_metadata_published_and_valid` | JSON Schema validation |
| TSPP-CTX-01 | Metadata declares context allowlist | `test_01_metadata.py::test_metadata_declares_context_allowlist` | Metadata `context_allowlist` |
| TSPP-CTX-02 | Unknown context key rejected or stripped | `test_03_context_allowlist.py::test_unknown_context_key_rejected_or_stripped` | HTTP status + no reflection |
| TSPP-FRESH-01 | Authorization response includes freshness fields | `test_02_freshness.py::test_authorization_freshness_fields` | `meta.time_evaluated`, `meta.expires_at` |
| TSPP-FRESH-02 | Freshness fields RFC3339-like | `test_02_freshness.py::test_authorization_freshness_fields` | Formatting assertion |
| TSPP-FRESH-03 | Recognition response includes freshness fields | `test_02_freshness.py::test_recognition_freshness_fields` | `meta.time_evaluated`, `meta.expires_at` |
| TSPP-ERR-01 | Uniform error surface (shape consistency) | `test_04_uniform_errors.py::test_uniform_not_found_surface` | Sampled JSON key-shapes |
| TSPP-ENUM-01 | Enumeration side-channel mitigation | `test_04_uniform_errors.py::test_uniform_not_found_surface` | Sample set + operator review |
| TSPP-RL-01 | Rate limit headers present on 429 | `test_05_ratelimits.py::test_ratelimit_headers_present_on_429` | Rate limit headers snapshot |
| TSPP-AL2-01 | Signed envelope in AL2 | `test_06_al2_signed_responses.py::test_al2_signed_response_envelope_shape` | Schema validation |
| TSPP-AL2-02 | Signature verifies against JWKS | `test_06_al2_signed_responses.py::test_al2_signed_response_verifies_with_jwks` | JWS verification success |
| TSPP-BRIDGE-01 | Bridge semantic equivalence fixtures | `test_07_bridge_equivalence.py::test_bridge_semantic_equivalence_fixtures` | Fixture pass/fail |
