---
owner: maintainers
last_reviewed: 2026-03-06
tier: 0
---

# Quickstart — TRQP-TSPP

This guide gets you running the TSPP conformance harness against a TRQP deployment in under 10 minutes.

## Prerequisites

- Python 3.10+
- A running TRQP endpoint (or use the bundled reference SUT)

## 1. Clone and install

```bash
git clone https://github.com/sankarshanmukhopadhyay/TRQP-TSPP
cd TRQP-TSPP/harness
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## 2. Start the reference SUT (optional)

If you don't have a TRQP endpoint, start the bundled reference SUT:

```bash
cd examples/reference_sut
pip install -r requirements.txt
uvicorn app:app --reload
```

The SUT will listen on `http://127.0.0.1:8000`.

## 3. Configure the harness

```bash
export TRQP_BASE_URL="http://127.0.0.1:8000"
export TSPP_EXPECT_AL="AL1"
```

For a full list of configuration variables see `harness/README.md`.

## 4. Run the harness

```bash
cd harness
pytest -q
```

To capture a JSON conformance report:

```bash
export TSPP_REPORT_PATH=./tspp_report.json
pytest -q
```

## 5. Package a posture evidence bundle

```bash
python scripts/create_evidence_bundle.py --report tspp_report.json --out reports/posture-bundle
```

The bundle directory contains `bundle_descriptor.json`, `checksums.json`, `bundle.zip`, and `tspp_posture_report.json`.

## Next steps

- Run at AL2 by setting `TSPP_EXPECT_AL="AL2"` — signed response validation is enabled
- Run at AL3/AL4 for independent assessment and continuous monitoring controls
- Combine with the Conformance Suite for a full combined assurance story (see the TRQP Assurance Hub)

## Related resources

- Full harness docs: `harness/README.md`
- Harness configuration: `harness/CONFIG.md`
- Deployment guidance: `docs/deployment-guidance.md`
- TRQP Assurance Hub (combined workflow): https://github.com/sankarshanmukhopadhyay/trqp-assurance-hub
