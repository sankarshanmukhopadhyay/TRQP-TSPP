from __future__ import annotations
import time
from dataclasses import dataclass
from typing import Any, Dict, Optional, Tuple
import requests

@dataclass
class TRQPClient:
    base_url: str
    token: Optional[str] = None
    dpop: Optional[str] = None
    timeout: float = 10.0

    def _headers(self, accept_signature: str = "none", request_id: Optional[str] = None) -> Dict[str, str]:
        h: Dict[str, str] = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Accept-Signature": accept_signature,
        }
        if request_id:
            h["X-Request-ID"] = request_id
        if self.token:
            h["Authorization"] = f"Bearer {self.token}"
        if self.dpop:
            h["DPoP"] = self.dpop
        return h

    def get_metadata(self) -> requests.Response:
        return requests.get(f"{self.base_url}/.well-known/trqp-metadata", headers=self._headers(), timeout=self.timeout)

    def post_authorization(self, body: Dict[str, Any], accept_signature: str = "none") -> requests.Response:
        return requests.post(f"{self.base_url}/authorization", json=body, headers=self._headers(accept_signature), timeout=self.timeout)

    def post_recognition(self, body: Dict[str, Any], accept_signature: str = "none") -> requests.Response:
        return requests.post(f"{self.base_url}/recognition", json=body, headers=self._headers(accept_signature), timeout=self.timeout)

def parse_ratelimit_headers(resp: requests.Response) -> Dict[str, Any]:
    out = {}
    for k in ["RateLimit-Limit", "RateLimit-Remaining", "RateLimit-Reset", "Retry-After"]:
        if k in resp.headers:
            try:
                out[k] = int(resp.headers[k])
            except Exception:
                out[k] = resp.headers[k]
    return out
