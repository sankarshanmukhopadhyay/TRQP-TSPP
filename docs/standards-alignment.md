# Standards alignment (informative)

This document provides an **informative mapping** from **TSPP Requirement IDs (Control IDs)** to widely-used security standards. It is designed to reduce adoption friction in mature security programs and speed up control reviews.

**Important:** This mapping is **non-normative**. The normative requirements remain in `docs/requirements.md`. A machine-readable export of control IDs is available at `controls/control-registry.json`.

## Mapping table

| TSPP Requirement ID | Summary | OWASP reference | NIST reference | ISO/IEC reference |
|---|---|---|---|---|
| `TSPP-META-01` | Metadata publication | API1: Broken Object Level Authorization (metadata exposure controls) / API10: Unsafe Consumption (metadata hygiene) | CM-8, PM-5 (inventory/discovery); AC-3 (access control as applicable) | A.5.9 (Inventory of information); A.8.9 (Configuration management) |
| `TSPP-META-02` | Metadata schema conformance | API10: Unsafe Consumption of APIs (schema validation) | SI-10 (input validation); SA-11 (developer testing) | A.8.28 (Secure coding) |
| `TSPP-CTX-01` | Explicit context allowlist declared | API4: Unrestricted Resource Consumption (scope); API2: Broken Authentication (context scoping) | AC-4 (information flow); SC-7 (boundary protection) | A.8.12 (Data leakage prevention) |
| `TSPP-CTX-02` | Unknown context key handling | API10: Unsafe Consumption (strict parsing); API9: Improper Inventory Management (unknown fields) | SI-10 (input validation) | A.8.28 (Secure coding) |
| `TSPP-FRESH-01` | Response freshness fields (authorization) | API5: Broken Function Level Authorization / replay resilience | SC-23 (session authenticity); SI-4 (monitoring) | A.8.16 (Monitoring activities) |
| `TSPP-FRESH-02` | RFC3339-like formatting | API10 (robust parsing/formatting) | SI-10 (input validation) | A.8.28 (Secure coding) |
| `TSPP-FRESH-03` | Response freshness fields (recognition) | API5 replay resilience | SC-23; SI-4 | A.8.16 |
| `TSPP-ERR-01` | Uniform error surface | API7: Security Misconfiguration (error leakage) | SI-11 (error handling); SC-7 | A.8.15 (Logging); A.8.28 |
| `TSPP-ENUM-01` | Enumeration side-channel mitigation (operator review) | API3: Broken Object Property Level Authorization / enumeration resistance | AC-7 (unsuccessful logon attempts); AU-6 (audit review) | A.8.15 (Logging); A.5.17 (Authentication information) |
| `TSPP-RL-01` | Rate limit signals on 429 | API4: Unrestricted Resource Consumption (rate limiting) | SC-5 (DoS protection); SI-4 | A.8.20 (Network security) |
| `TSPP-AL2-01` | Signed envelope in AL2 | API2 (auth); API8 (integrity) — signed responses | SC-12/SC-13 (cryptographic protections); SI-7 (integrity) | A.8.24 (Use of cryptography) |
| `TSPP-AL2-02` | Verifiable signature via declared JWKS | API8: Security Misconfiguration? (key management) / integrity verification | SC-12/SC-13; IA-5 (authenticator management) | A.8.24; A.5.17 |
| `TSPP-BRIDGE-01` | Semantic equivalence fixtures (optional) | API10 (consistent consumption); interoperability risk reduction | SA-15 (development process); SA-11 | A.8.28 |

## Included standards

- OWASP API Security Top 10
- NIST SP 800-53 (control families), NIST SP 800-63 (digital identity), NIST SP 800-218 (SSDF)
- ISO/IEC 27001 / 27002 (and 27701 where relevant)

## How to use this

1. Start with `docs/requirements.md` to understand the normative requirement.
2. Use this mapping to align the requirement to your organization’s security control catalog.
3. Use `docs/traceability-matrix.md` to link the requirement to tests and evidence artifacts.

---

## Recommended at-scale standards (secure distributed services)

The references below are **informative**. They help adopters map TSPP requirements to
well-known programs for operating secure, reliable distributed services at scale.

This repo now includes short operator notes for each reference under `docs/standards/`.

### Crosswalk (informative)

| Standard / guidance | Primary themes | Relevant TSPP control IDs | Operator evidence to collect | Notes in this repo |
|---|---|---|---|---|
| NIST SP 800-207 (Zero Trust Architecture) | Zero Trust, policy enforcement at request boundaries | `TSPP-CTX-01`, `TSPP-CTX-02`, `TSPP-RL-01`, `TSPP-AL2-01`, `TSPP-AL2-02` | ZTA policy docs; token validation policies; segmentation / gateway rules; change control artifacts | `docs/standards/nist-sp-800-207-zero-trust.md` |
| OWASP API Security Top 10 | API threat catalog, common failure modes | `TSPP-META-01`, `TSPP-META-02`, `TSPP-ERR-01`, `TSPP-ENUM-01`, `TSPP-RL-01`, `TSPP-AL2-02` | Schema validation tests; uniform error tests; rate-limit config + verification; API threat model | `docs/standards/owasp-api-security-top-10.md` |
| OpenTelemetry | Traces/metrics/logs, audit-grade observability | `TSPP-AL4-03`, `TSPP-AL4-05` | Telemetry pipeline diagram; retention settings; incident reconstruction example; SLO dashboards | `docs/standards/opentelemetry.md` |
| SLSA | Build provenance, dependency integrity, release hygiene | `TSPP-META-01`, `TSPP-META-02`, `TSPP-AL4-04` | Provenance/attestations; pinned dependency manifests; release promotion + rollback procedures | `docs/standards/slsa.md` |
| NIST SP 800-190 (Container security) | Image/registry/runtime hardening | `TSPP-AL4-02`, `TSPP-AL4-03`, `TSPP-AL4-05` | Image scan outputs; runtime hardening snapshots; secrets/key protection evidence; IR runbooks | `docs/standards/nist-sp-800-190-containers.md` |
| CIS Kubernetes Benchmark | Cluster posture hardening | `TSPP-AL4-02`, `TSPP-AL4-03`, `TSPP-AL4-05` | CIS scan outputs; RBAC review; admission policies; K8s audit retention config | `docs/standards/cis-kubernetes-benchmark.md` |

## UNTP DIA alignment

Directory evaluations that rely on UNTP Digital Identity Anchor (DIA) SHOULD apply the SAD-1 identity anchoring extension requirements and capture DIA artifacts as evidence (context reference, resolver approach, and status lifecycle).


## OpenSSF alignment

TSPP's **Software Supply Chain Integrity** control family (TSPP-SCI-xx) aligns with OpenSSF guidance to make software integrity and provenance **auditable** for TRQP deployments.

| TSPP control | OpenSSF guidance (example) | Notes |
|---|---|---|
| TSPP-SCI-01 | SBOM practices (SPDX/CycloneDX) | Evidence-grade SBOM for production artifacts |
| TSPP-SCI-02 | Scorecard dependency/vuln checks | Continuous monitoring + remediation workflow |
| TSPP-SCI-03 | Signed releases | Artifact signing + verification evidence |
| TSPP-SCI-04 | SLSA provenance | Provenance attestation for AL3+ |
| TSPP-SCI-05 | Scorecard / secure CI practices | Branch protections and guarded release workflows |

Reference: `docs/reference/openssf-supply-chain.md`.

