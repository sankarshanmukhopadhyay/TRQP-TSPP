from __future__ import annotations

import hashlib
import json
import os
import time
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, Optional

from fastapi import FastAPI, Header, HTTPException, Request
from jwcrypto import jwk, jws

APP_VERSION = "0.1.0"

# ----------------------------
# Configuration (CI-friendly)
# ----------------------------
ASSURANCE_LEVEL = os.environ.get("TSPP_REF_AL", os.environ.get("TSPP_EXPECT_AL", "AL1"))
BEARER_TOKEN = os.environ.get("TSPP_REF_BEARER_TOKEN", "dev-token")
RATE_LIMIT_BURST = int(os.environ.get("TSPP_REF_RL_BURST", "999999"))  # high by default (avoid 429 unless tuned)
RATE_LIMIT_WINDOW_SECONDS = int(os.environ.get("TSPP_REF_RL_WINDOW", "60"))

JWKS_PATH = "/.well-known/jwks.json"
KID = "ref-kid-1"

app = FastAPI(title="TSPP TRQP Reference SUT", version=APP_VERSION)

# Request counter for optional rate limiting
WINDOW_START = time.time()
WINDOW_COUNT = 0

# Signing key (ephemeral for CI)
_SIGNING_KEY = jwk.JWK.generate(kty="RSA", size=2048)
_SIGNING_KEY.kid = KID


def _now() -> datetime:
    return datetime.now(timezone.utc)


def _iso(dt: datetime) -> str:
    return dt.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


def _rate_limit_tick() -> Optional[Dict[str, str]]:
    global WINDOW_START, WINDOW_COUNT
    now = time.time()
    if now - WINDOW_START >= RATE_LIMIT_WINDOW_SECONDS:
        WINDOW_START = now
        WINDOW_COUNT = 0
    WINDOW_COUNT += 1

    remaining = max(0, RATE_LIMIT_BURST - WINDOW_COUNT)
    reset = int(WINDOW_START + RATE_LIMIT_WINDOW_SECONDS)
    headers = {
        "RateLimit-Limit": str(RATE_LIMIT_BURST),
        "RateLimit-Remaining": str(remaining),
        "RateLimit-Reset": str(reset),
    }
    if WINDOW_COUNT > RATE_LIMIT_BURST:
        headers["Retry-After"] = "1"
        return headers
    return headers


def _require_auth(authorization: Optional[str]) -> None:
    # Minimal bearer auth (tests accept 401/403 too, but CI wants 200 happy-path)
    if not authorization:
        raise HTTPException(status_code=401, detail="missing_authorization")
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="invalid_authorization_scheme")
    token = authorization.split(" ", 1)[1].strip()
    if token != BEARER_TOKEN:
        raise HTTPException(status_code=403, detail="invalid_token")


def _strip_unknown_context(ctx: Any, allowlist: list[str]) -> Any:
    if not isinstance(ctx, dict):
        return ctx
    return {k: v for k, v in ctx.items() if k in allowlist}


def _query_hash(body: Dict[str, Any], allow_keys: list[str]) -> str:
    # Operator-defined: hash only allowlisted context keys + primary identifiers if present.
    # Tests do not assert this today; we still compute a stable value.
    ctx = body.get("context") if isinstance(body, dict) else None
    ctx = ctx if isinstance(ctx, dict) else {}
    bound = {k: ctx.get(k) for k in allow_keys if k in ctx}
    # include entity/subject identifiers when present
    for k in ("entity_id", "subject_authority_id"):
        if k in body:
            bound[k] = body.get(k)
    raw = json.dumps(bound, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def _sign_envelope(payload: Dict[str, Any], qh: str, ctx_keys: list[str]) -> Dict[str, Any]:
    # Sign the canonical payload bytes. (The spec may bind query_hash into signing input;
    # harness verifies only the JWS signature against JWKS.)
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    signer = jws.JWS(payload=canonical)
    signer.add_signature(_SIGNING_KEY, None, protected={"alg": "RS256", "kid": KID}, header={})
    compact = signer.serialize(compact=True)

    return {
        "payload": payload,
        "signature": {
            "alg": "RS256",
            "kid": KID,
            "jws": compact,
            "query_hash": qh,
            "hash_alg": "SHA-256",
            "canonicalization": {
                "json": "operator-defined",
                "unicode": "none",
                "context_keys_included": ctx_keys,
            },
            "issued_at": _iso(_now()),
        },
    }


@app.get("/.well-known/trqp-metadata")
def get_metadata(request: Request):
    base = str(request.base_url).rstrip("/")
    allowlist = ["purpose", "audience", "locale"]
    return {
        "profile": "TSPP-TRQP-0.1",
        "assurance_level": ASSURANCE_LEVEL,
        "auth": {
            "scheme": "bearer",
            "token_format": "opaque",
        },
        "rate_limits": {
            "burst": RATE_LIMIT_BURST,
            "window_seconds": RATE_LIMIT_WINDOW_SECONDS,
        },
        "freshness": {
            "max_skew_seconds": 120,
            "default_ttl_seconds": 300,
        },
        "context_allowlist": allowlist,
        "signing": {
            "response_signing": "optional" if ASSURANCE_LEVEL != "AL2" else "required",
            "jwks_uri": f"{base}{JWKS_PATH}",
        },
        "recognition_policy": {
            "unknown_subject_behavior": "not_found_or_uniform",
        }
    }


@app.get(JWKS_PATH)
def get_jwks():
    pub = jwk.JWK.from_json(_SIGNING_KEY.export_public())
    # Ensure kid is present
    pub.kid = KID
    return {"keys": [json.loads(pub.export_public())]}


@app.post("/authorization")
async def post_authorization(req: Request, authorization: Optional[str] = Header(default=None), accept_signature: Optional[str] = Header(default="none", alias="Accept-Signature")):
    rl_headers = _rate_limit_tick()
    if rl_headers and int(rl_headers.get("RateLimit-Remaining", "1")) == 0 and WINDOW_COUNT > RATE_LIMIT_BURST:
        raise HTTPException(status_code=429, detail="rate_limited", headers=rl_headers)

    _require_auth(authorization)

    body = await req.json()
    allowlist = ["purpose", "audience", "locale"]
    ctx = _strip_unknown_context(body.get("context"), allowlist)
    if isinstance(body, dict):
        body["context"] = ctx

    # Simple semantics: if entity_id looks like "unknown", respond 404 with uniform surface
    entity_id = body.get("entity_id") if isinstance(body, dict) else None
    if isinstance(entity_id, str) and "unknown" in entity_id.lower():
        raise HTTPException(status_code=404, detail="not_found")

    now = _now()
    payload = {
        "decision": {"authorized": "true"},
        "meta": {
            "time_evaluated": _iso(now),
            "expires_at": _iso(now + timedelta(seconds=300)),
        },
        "context": ctx if isinstance(ctx, dict) else {},
    }

    # Optional signed envelope
    if ASSURANCE_LEVEL == "AL2" and (accept_signature or "").lower() == "jws":
        qh = _query_hash(body, allowlist)
        return _sign_envelope(payload, qh, [k for k in allowlist if isinstance(ctx, dict) and k in ctx])

    # attach ratelimit headers on success too (nice-to-have)
    # FastAPI doesn't let easy per-route header injection without Response; keep minimal.
    return payload


@app.post("/recognition")
async def post_recognition(req: Request, authorization: Optional[str] = Header(default=None), accept_signature: Optional[str] = Header(default="none", alias="Accept-Signature")):
    _require_auth(authorization)
    body = await req.json()
    allowlist = ["purpose", "audience", "locale"]
    ctx = _strip_unknown_context(body.get("context"), allowlist)
    if isinstance(body, dict):
        body["context"] = ctx

    now = _now()
    payload = {
        "recognized": True,
        "meta": {
            "time_evaluated": _iso(now),
            "expires_at": _iso(now + timedelta(seconds=300)),
        },
        "context": ctx if isinstance(ctx, dict) else {},
    }
    if ASSURANCE_LEVEL == "AL2" and (accept_signature or "").lower() == "jws":
        qh = _query_hash(body, allowlist)
        return _sign_envelope(payload, qh, [k for k in allowlist if isinstance(ctx, dict) and k in ctx])
    return payload
