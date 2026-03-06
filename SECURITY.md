# Security Policy

## Reporting a vulnerability
If you discover a security issue in this repository or its reference implementation artifacts, do not open a public issue with exploit details. Report privately to the maintainers with:

- affected files or components
- potential impact
- safe reproduction steps
- suggested remediation, if available

Maintainers will acknowledge receipt and coordinate remediation and disclosure timing.

## Scope
This repository is in scope for reports that affect:

- the TSPP harness and its ability to produce trustworthy posture verdicts
- the reference SUT under `examples/reference_sut/`
- schemas, examples, and evidence-bundle tooling that could mislead adopters or auditors
- CI workflows and supply-chain integrity controls

## Related guidance
Security reports should be interpreted alongside the threat framing in `docs/threat-model.md` and the deployment guidance in `docs/deployment-guidance.md`.
