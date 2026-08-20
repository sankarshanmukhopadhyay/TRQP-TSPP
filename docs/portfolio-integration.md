---
layout: default
title: "Portfolio Integration"
nav_exclude: true
permalink: /docs/portfolio-integration/
---

# Portfolio Integration

TRQP-TSPP participates in the coordinated TRQP repository set through `portfolio/integration-contract.json`.

## Repository responsibilities

TRQP-TSPP owns its protocol requirements and validation artifacts. Shared semantic definitions are referenced from `trust-systems-meta-model` v0.24.0, while shared portfolio and repository schemas are referenced from `trust-infrastructure-schemas` v0.14.1.

The conformance suite tests TSPP requirements, and the assurance hub consumes resulting evidence.

## Automated validation

`tools/validate_portfolio_contract.py` checks the release version, upstream version pins, required local evidence, repository relationships, and invalidation conditions. `.github/workflows/portfolio-contract.yml` runs these checks on pull requests and pushes to `main` and uploads a JSON validation result.

A missing required artifact or incompatible upstream version makes the integration contract invalid, making cross-repository drift detectable in CI.
