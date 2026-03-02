# OpenTelemetry (Service Telemetry)

> **Status:** informative (non-normative)

## Why this matters
Audit and incident response get expensive fast unless telemetry is standardized. OpenTelemetry provides a vendor-neutral path to produce traces/metrics/logs that are good enough for SLO governance and “show me what happened” investigations.

## TSPP touchpoints
- **Related control IDs:** `TSPP-AL4-03`, `TSPP-AL4-05`
- **Where to implement:** tracing at ingress, correlation IDs in logs, and retention policies for auditability.

## Suggested evidence (operator-ready)
- Telemetry pipeline architecture (collector, exporters, destinations)
- Evidence of retention settings matching `metadata.monitoring` and `metadata.audit`
- Example incident timeline reconstructed from traces/logs
- SLO/SLA dashboards (or exported snapshots) tied to runbooks

## Practical implementation notes
- Treat these controls as “platform glue” that makes the TSPP controls easier to operate at scale.
- Where possible, automate evidence generation (CI/CD attestations, config snapshots, telemetry exports) to keep audit cost down.
