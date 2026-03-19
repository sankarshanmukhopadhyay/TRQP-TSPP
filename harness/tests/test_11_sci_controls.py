"""TSPP harness tests for supply chain integrity (SCI) controls.

What these tests prove:
- The registry's implementation artifacts have declared supply chain integrity
  evidence: an SBOM reference, a release provenance attestation, and a signing
  key freshness declaration.
- These checks are advisory at AL1/AL2 and required at AL3+.

Why it matters:
- A registry that passes protocol tests but ships dependencies with known
  vulnerabilities or unsigned releases has a partial security posture.
- Supply chain integrity evidence is increasingly required by trust frameworks
  and procurement authorities.

Requirement coverage:
- TSPP-SCI-01: SBOM reference declared in metadata
- TSPP-SCI-02: Release provenance attestation declared in metadata
- TSPP-SCI-03: Signing key freshness declared in metadata

Evidence:
- Conformance report section: sci_controls, requirement IDs TSPP-SCI-*.

References:
- docs/reference/openssf-supply-chain.md (TRQP-TSPP)
- docs/guides/evidence-artifacts.md (trqp-assurance-hub)
"""

import os
import pytest
import requests

from tspp_trqp_harness.reporting import requirements


def _skip_if_not_al3_plus(client):
    """Skip SCI tests for AL1/AL2 where these are advisory, not required."""
    al = os.environ.get("TSPP_EXPECT_AL", "AL1")
    # For AL1/AL2 run as informational — skip with a clear label
    if al not in {"AL3", "AL4"}:
        pytest.skip(
            f"TSPP-SCI controls are advisory at {al} (required at AL3+). "
            "Run with TSPP_EXPECT_AL=AL3 or AL4 to enforce."
        )


@requirements("TSPP-SCI-01")
def test_sci_sbom_reference_declared(_client):
    """SBOM reference declared in registry metadata.

    At AL3+, the registry metadata MUST include a `supply_chain.sbom_uri` or
    equivalent field pointing to a machine-readable SBOM (SPDX / CycloneDX).

    Advisory at AL1/AL2.
    """
    _skip_if_not_al3_plus(_client)

    r = _client.get_metadata()
    assert r.status_code == 200, f"metadata status {r.status_code}: {r.text}"
    m = r.json()

    sci = m.get("supply_chain") or m.get("sci") or {}
    sbom_uri = sci.get("sbom_uri")
    assert sbom_uri, (
        "AL3+ requires supply_chain.sbom_uri declared in registry metadata. "
        "Provide a URI pointing to an SPDX or CycloneDX SBOM for the deployed implementation."
    )

    # Verify the SBOM URI is reachable
    try:
        resp = requests.get(sbom_uri, timeout=10)
        assert resp.status_code == 200, (
            f"supply_chain.sbom_uri returned {resp.status_code} — expected 200"
        )
    except requests.RequestException as exc:
        pytest.fail(f"Failed to reach supply_chain.sbom_uri {sbom_uri!r}: {exc}")


@requirements("TSPP-SCI-02")
def test_sci_release_provenance_declared(_client):
    """Release provenance attestation declared in registry metadata.

    At AL3+, the registry metadata MUST include a `supply_chain.provenance_uri`
    pointing to a release provenance attestation (e.g. SLSA provenance, GitHub
    Attestations, or equivalent signed build attestation).

    Advisory at AL1/AL2.
    """
    _skip_if_not_al3_plus(_client)

    r = _client.get_metadata()
    assert r.status_code == 200, f"metadata status {r.status_code}: {r.text}"
    m = r.json()

    sci = m.get("supply_chain") or m.get("sci") or {}
    provenance_uri = sci.get("provenance_uri")
    assert provenance_uri, (
        "AL3+ requires supply_chain.provenance_uri declared in registry metadata. "
        "Provide a URI pointing to a signed release provenance attestation."
    )

    try:
        resp = requests.get(provenance_uri, timeout=10)
        assert resp.status_code == 200, (
            f"supply_chain.provenance_uri returned {resp.status_code} — expected 200"
        )
    except requests.RequestException as exc:
        pytest.fail(f"Failed to reach supply_chain.provenance_uri {provenance_uri!r}: {exc}")


@requirements("TSPP-SCI-03")
def test_sci_signing_key_freshness_declared(_client):
    """Signing key freshness declared in registry metadata.

    At AL3+, the registry metadata MUST include either:
    - `signing.key_rotation_policy` with a `max_age_days` field, OR
    - `signing.jwks_uri` pointing to a JWKS that includes key `exp` or `nbf` fields
      from which freshness can be inferred.

    This test checks for the policy declaration. Actual key age verification
    requires live key material and is performed out-of-band by the assessor.

    Advisory at AL1/AL2.
    """
    _skip_if_not_al3_plus(_client)

    r = _client.get_metadata()
    assert r.status_code == 200, f"metadata status {r.status_code}: {r.text}"
    m = r.json()

    signing = m.get("signing") or {}

    # Accept either a key_rotation_policy or a resolvable JWKS URI
    rotation_policy = signing.get("key_rotation_policy") or {}
    max_age_days = rotation_policy.get("max_age_days")
    jwks_uri = signing.get("jwks_uri")

    has_rotation_policy = isinstance(max_age_days, int) and max_age_days > 0
    has_jwks = bool(jwks_uri)

    assert has_rotation_policy or has_jwks, (
        "AL3+ requires at least one of: "
        "(a) signing.key_rotation_policy.max_age_days (integer, days), or "
        "(b) signing.jwks_uri (URI to a JWKS enabling freshness verification). "
        "Neither was found in registry metadata."
    )

    # If rotation policy declared, validate shape
    if has_rotation_policy:
        assert max_age_days <= 365, (
            f"signing.key_rotation_policy.max_age_days is {max_age_days}; "
            "AL3+ deployments SHOULD rotate signing keys at least annually (≤ 365 days)."
        )

    # If JWKS URI declared, verify it is reachable
    if has_jwks:
        try:
            resp = requests.get(jwks_uri, timeout=10)
            assert resp.status_code == 200, (
                f"signing.jwks_uri returned {resp.status_code} — expected 200"
            )
            jwks = resp.json()
            keys = jwks.get("keys", [])
            assert keys, "JWKS at signing.jwks_uri contains no keys"
        except requests.RequestException as exc:
            pytest.fail(f"Failed to reach signing.jwks_uri {jwks_uri!r}: {exc}")
