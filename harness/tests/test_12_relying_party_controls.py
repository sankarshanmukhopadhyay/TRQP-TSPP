from datetime import datetime
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
EXAMPLE = ROOT / "examples" / "relying-party-publication" / "relying-party-publication.example.json"

def _load():
    return json.loads(EXAMPLE.read_text())

def test_relying_party_publication_example_exists():
    assert EXAMPLE.exists()

def test_publication_has_discoverable_summary_url():
    data = _load()
    assert data["assurance_summary_url"].startswith("https://")

def test_publication_freshness_window_is_valid():
    data = _load()
    generated = datetime.fromisoformat(data["generated_at"].replace("Z", "+00:00"))
    valid_until = datetime.fromisoformat(data["valid_until"].replace("Z", "+00:00"))
    assert valid_until > generated

def test_publication_discloses_limitations_and_revocation_guidance():
    data = _load()
    assert data["limitations"]
    assert "status" in data["revocation_guidance"].lower()

def test_high_reliance_metadata_is_present():
    data = _load()
    assert data["redress_contact"].startswith("mailto:")
    assert data["consumer_impact_statement"]
