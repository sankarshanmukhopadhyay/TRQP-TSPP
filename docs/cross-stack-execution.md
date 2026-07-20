# Cross-Stack Execution

This repository is an evidence producer in the TRQP Operational Trust Stack. Evidence intended for Hub composition MUST contain a stable `run_id`, `target_id`, producer version, execution timestamp, outcome summary, and artifact checksums. The Assurance Hub rejects evidence when producer reports refer to different targets or runs, use an unsupported release tuple, or fail schema and integrity validation.

Run the repository-level material check with:

```bash
make assurance-check
```

Outputs under `artifacts/` are self-generated validation evidence. They support reproducibility and pilot preparation but do not constitute independent assurance or external certification.
