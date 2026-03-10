"""Utility for validating did:webvh identifier format.

The Ayra Trust Network Profile mandates did:webvh for all ecosystem, trust registry,
and cluster identifiers. This module provides a lightweight format check that can be
called from test modules and schema validation scripts.

Reference:
  https://ayraforum.github.io/ayra-trust-registry-resources/#identifier-requirements

Note: This is a syntax check only. It does NOT resolve the DID document or verify
that service endpoints are correctly configured. Those checks are manual per the
known-gaps section in docs/profiles/ayra-baseline.md.
"""

import re
from typing import Optional


# did:webvh method syntax per did-webvh spec:
# did:webvh:<domain-and-path>
# Domain component must be a valid hostname (with optional port and path segments).
# The method-specific identifier may include colons as path separators.
_DID_WEBVH_PATTERN = re.compile(
    r"^did:webvh:"          # method prefix
    r"[a-zA-Z0-9._\-]+"    # domain (hostname portion)
    r"(?::\d+)?"            # optional port
    r"(?::[a-zA-Z0-9._\-~%!$&'()*+,;=@]+)*"  # optional path segments as colon-separated
    r"$"
)


def is_did_webvh(value: str) -> bool:
    """Return True if value matches the did:webvh syntax, False otherwise."""
    if not isinstance(value, str):
        return False
    return bool(_DID_WEBVH_PATTERN.match(value))


def assert_did_webvh(value: str, field_name: str = "identifier") -> None:
    """Assert that value is a valid did:webvh DID.

    Raises AssertionError with a descriptive message if the check fails.
    Intended for use in pytest test functions.
    """
    assert is_did_webvh(value), (
        f"Ayra Profile MUST: {field_name!r} must be a did:webvh DID, "
        f"got {value!r}. All Ayra ecosystem, trust registry, and cluster "
        f"identifiers must use did:webvh. "
        f"See: https://ayraforum.github.io/ayra-trust-registry-resources/#identifier-requirements"
    )


def check_did_webvh(value: str) -> Optional[str]:
    """Return an error string if value is not a valid did:webvh DID, None if valid.

    Useful for accumulating validation errors without raising immediately.
    """
    if is_did_webvh(value):
        return None
    return (
        f"Expected did:webvh DID, got {value!r}. "
        f"Ayra Profile MUST: all identifiers use did:webvh."
    )
