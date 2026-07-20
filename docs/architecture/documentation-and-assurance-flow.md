---
layout: default
title: "TSPP assurance execution architecture"
parent: Architecture
nav_order: 1
---

# TSPP assurance execution architecture

The repository previously documented controls, profiles, harness execution, and evidence publication across separate documents without a single end-to-end view. This diagram makes the authority-to-evidence path explicit and identifies the remediation loop.

```mermaid
flowchart LR
    Operator[Trust-service provider operator] --> Profile[Select TSPP profile and assurance level]
    Profile --> Controls[Apply control requirements]
    Controls --> SUT[Configure system under test]
    SUT --> Harness[Run TSPP conformance harness]
    Harness --> Validate{Evidence valid?}
    Validate -- No --> Remediate[Remediate control or implementation gap]
    Remediate --> SUT
    Validate -- Yes --> Report[Generate signed posture report]
    Report --> Bundle[Create immutable evidence bundle]
    Bundle --> Hub[Publish to TRQP Assurance Hub workflow]
    Hub --> RP[Relying-party decision]
```

## Assurance interpretation

The diagram is normative only where it links to an identified specification, schema, profile, or executable test. Each transition should produce inspectable evidence: selected profile identifiers, test inputs, result artifacts, decision records, and publication manifests. Revocation or supersession must be represented by lifecycle data rather than by silently replacing prior evidence.
