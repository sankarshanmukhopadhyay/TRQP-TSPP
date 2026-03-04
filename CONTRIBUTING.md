# Contributing

Thanks for helping improve TRQP-TSPP.

## How to contribute
1. Open an issue describing the change (bug, enhancement, or clarification).
2. Submit a pull request referencing the issue.
3. Keep changes small and reviewable.

## Documentation norms
- Use clear normative language (MUST/SHOULD/MAY) only where intended.
- Keep templates under `docs/templates/` and label them clearly as non-normative.

## Security issues
For security concerns, please follow `SECURITY.md`.

## Documentation quality gates

This project treats documentation as a production interface.

- Tier 0–Tier 1 docs MUST include YAML frontmatter (`owner`, `last_reviewed`, `tier`).
- CI runs link checking, lightweight doc tests (JSON/YAML parsing + internal link sanity), and freshness SLA enforcement.
- If your change affects APIs, schemas, CLIs, or behavior, you MUST update the relevant docs in the same PR.

See: [`docs/governance/README.md`](docs/governance/README.md)

