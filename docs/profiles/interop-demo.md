# Interop demo profile

The interop demo profile is a deliberately lightweight AL1-oriented posture path for workshops, onboarding, and Operational Stack demonstrations.

## Purpose

Use this mode when you need a repeatable posture artifact without pulling operators into a full production hardening exercise.

## Expected invocation

```bash
tspp-harness   --base-url http://127.0.0.1:8001   --expect-al AL1   --report-path reports/interop_demo/tspp-report.json   --run-id opstack-demo-001   --target-id demo-directory
```
