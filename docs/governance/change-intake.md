---
owner: maintainers
last_reviewed: 2026-07-03
tier: 0
---

# Change Intake

TSPP changes should be evaluated by their effect on executable posture checks and downstream assurance evidence.

## Intake checklist

| Question | Required answer |
|---|---|
| Which control changes? | Identify control IDs, test modules, profile names, or schema fields. |
| Which evidence changes? | Name the posture report, control satisfaction object, lifecycle publication, relying-party publication, or bundle descriptor field. |
| What can be tested? | Provide the harness, schema, documentation, or reference SUT command. |
| Who benefits? | Identify operator, implementer, assessor, relying party, or Hub consumer. |
| Is a release justified? | Explain why the change is patch, minor, maturity, or no-release. |

## Batching rule

Batch small wording updates, non-normative notes, and internal cross-link cleanup into the next milestone. Cut a release only when posture computation, control evidence, schema semantics, or adopter workflow materially changes.
