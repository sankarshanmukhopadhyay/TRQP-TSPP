# CTR-ACB Alignment (Certification Baseline Compatibility)

This document explains how **TRQP Security & Privacy Baseline (TSPP)** aligns with the *Candidate Trust Registry Assurance & Certification Baseline (CTR-ACB)* defined in the TRQP Assurance Hub.

## Intended relationship

- **TSPP** defines posture expectations for TRQP endpoints and behaviors.
- **CTR-ACB** defines how posture claims are expressed, evaluated, and (optionally) certified using machine-readable baseline artifacts.

TSPP remains a profile/spec layer. CTR-ACB remains a governance/certification baseline layer.

## How to use TSPP with CTR-ACB

A registry can use TSPP outputs as evidence for CTR-ACB controls, for example:

- Endpoint response signing posture
- Error handling determinism and client safety
- Privacy and data minimization claims
- Operational hardening expectations tied to assurance levels

In a certification baseline flow:

1. Registry publishes an Assurance Profile and relevant baseline artifacts.
2. Registry documents TSPP posture (and/or implements TSPP-recommended behaviors).
3. Evidence (including test results, configuration, and policy docs) is referenced from Control Satisfaction Declarations.
4. Optionally, an assessor issues a Certification Attestation.

## Notes

- This repo does not define assessor accreditation.
- This repo does not issue certificates.
- This repo provides posture expectations that can be referenced by certification baselines.

For the baseline model and certification attestation structure, refer to the TRQP Assurance Hub repository.
