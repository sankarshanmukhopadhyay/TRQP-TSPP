from __future__ import annotations

from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional


def requirements(*ids: str):
    """Decorator to attach TSPP requirement IDs to a pytest test function."""
    norm = [i.strip() for i in ids if i and i.strip()]
    def _wrap(fn):
        setattr(fn, "TSPP_REQUIREMENTS", norm)
        return fn
    return _wrap


@dataclass
class TestResult:
    nodeid: str
    name: str
    outcome: str  # passed|failed|skipped|error
    duration_seconds: float
    requirement_ids: List[str]
    notes: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
