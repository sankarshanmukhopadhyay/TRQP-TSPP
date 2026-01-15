from __future__ import annotations
import json
from pathlib import Path
from typing import Any, Dict, Optional, Tuple

import jsonschema

def load_schema(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text())

def validate_json(instance: Any, schema: Dict[str, Any]) -> None:
    jsonschema.validate(instance=instance, schema=schema)

def require_fields(obj: Dict[str, Any], fields: Tuple[str, ...]) -> None:
    missing = [f for f in fields if f not in obj]
    if missing:
        raise AssertionError(f"Missing required fields: {missing}")

def iso8601_like(s: str) -> bool:
    # Simple check; conformance suite can swap in stricter parser if desired.
    return "T" in s and ("Z" in s or "+" in s or "-" in s)

def assert_freshness(meta: Dict[str, Any]) -> None:
    require_fields(meta, ("time_evaluated", "expires_at"))
    if not isinstance(meta["time_evaluated"], str) or not iso8601_like(meta["time_evaluated"]):
        raise AssertionError("meta.time_evaluated must be RFC3339 date-time string")
    if not isinstance(meta["expires_at"], str) or not iso8601_like(meta["expires_at"]):
        raise AssertionError("meta.expires_at must be RFC3339 date-time string")
