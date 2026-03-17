from __future__ import annotations

import asyncio
import hashlib
import json
import os
import time
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, Optional

from fastapi import FastAPI, Header, HTTPException, Request
from fastapi.responses import JSONResponse
from jwcrypto import jwk, jws

APP_VERSION = "0.2.0"

ASSURANCE_LEVEL = os.environ.get("TSPP_REF_AL", os.environ.get("TSPP_EXPECT_AL", "AL1"))
BEARER_TOKEN = os.environ.get("TSPP_REF_BEARER_TOKEN", "dev-token")
RATE_LIMIT_BURST = int(os.environ.get("TSPP_REF_RL_BURST", "999999"))
RATE_LIMIT_WINDOW_SECONDS = int(os.environ.get("TSPP_REF_RL_WINDOW", "60"))

JWKS_PATH = "/.well-known/jwks.json"
KID = "ref-kid-1"

app = FastAPI(title="TSPP TRQP Reference SUT", version=APP_VERSION)

WINDOW_START = time.time()
WINDOW_COUNT = 0
_RL_LOCK = asyncio.Lock()

_SIGNING_KEY = jwk.JWK.generate(kty="RSA", size=2048)
_SIGNING_KEY.kid = KID


PUBLIC_DOCS = {
    "/.well-known/assessment/al3-independent-assessment": {
        "assessment_id": "assess-al3-001",
        "assessor": "Example Independent Assessor Ltd.",
        "scope": ["authorization", "recognition", "metadata"],
        "result": "pass",
        "issued_at": "2026-03-06T00:00:00Z",
    },
    "/.well-known/governance/change-control": {
        "document_id": "chg-ctl-001",
        "owner": "Example Registry Operator",
        "summary": "Change control procedure for TRQP posture changes.",
    },
    "/.well-known/governance/policy": {
        "policy_id": "gov-pol-001",
        "summary": "Governance policy for high-assurance TRQP operation.",
    },
    "/.well-known/governance/rollback": {
        "procedure_id": "rollback-001",
        "summary": "Rollback and release reversal procedure for production incidents.",
    },
    "/.well-known/audit/log": {
        "log_id": "audit-log-001",
        "storage": "append-only",
        "coverage": ["authorization", "recognition", "metadata"],
    },
    "/.well-known/ops/runbook": {
        "runbook_id": "ops-rb-001",
        "summary": "Incident response and monitoring runbook.",
    },
    "/.well-known/keys/protection": {
        "control_id": "key-protection-001",
        "protection": "KMS",
        "evidence": "Example control evidence for key protection posture.",
    },
    "/.well-known/service-docs": {
        "service": "TRQP Reference SUT",
        "version": APP_VERSION,
        "assurance_level": ASSURANCE_LEVEL,
    },
}


def _now() -> datetime:
    return datetime.now(timezone.utc)


def _iso(dt: datetime) -> str:
    return dt.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


def _public_uri(base: str, path: str) -> str:
    return f"{base}{path}"


async def _rate_limit_tick() -> Dict[str, str]:
    global WINDOW_START, WINDOW_COUNT
    async with _RL_LOCK:
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
        if WINDOW_COUNT >= RATE_LIMIT_BURST:
            headers["Retry-After"] = "1"
        return headers


def _require_auth(authorization: Optional[str]) -> None:
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
    ctx = body.get("context") if isinstance(body, dict) else None
    ctx = ctx if isinstance(ctx, dict) else {}
    bound = {k: ctx.get(k) for k in allow_keys if k in ctx}
    for k in ("entity_id", "subject_authority_id"):
        if k in body:
            bound[k] = body.get(k)
    raw = json.dumps(bound, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def _sign_envelope(payload: Dict[str, Any], qh: str, ctx_keys: list[str]) -> Dict[str, Any]:
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
        "meta": {
            "query_hash": qh,
            "iat": _iso(_now()),
            "exp": _iso(_now() + timedelta(seconds=300)),
        },
    }


def _should_sign_success(accept_signature: Optional[str]) -> bool:
    if ASSURANCE_LEVEL in {"AL3", "AL4"}:
        return True
    return ASSURANCE_LEVEL == "AL2" and (accept_signature or "").lower() == "jws"


@app.get("/.well-known/trqp-metadata")
def get_metadata(request: Request):
    base = str(request.base_url).rstrip("/")
    allowlist = ["purpose", "audience", "locale"]
    metadata = {
        "profile": "TSPP-TRQP-0.1",
        "assurance_level": ASSURANCE_LEVEL,
        "operator": {
            "name": "Example Registry Operator",
            "security_contact": {
                "email": "security@example.org",
                "url": _public_uri(base, "/.well-known/service-docs"),
            },
        },
        "auth": {
            "required": True,
            "methods": ["bearer"],
            "max_token_ttl_seconds": 900,
            "required_scopes": ["trqp.authorization.query", "trqp.recognition.query"],
            "audience": "urn:example:trqp-reference-sut",
        },
        "rate_limits": {
            "per_client_rps": 100,
            "per_ip_rps": 100,
            "burst": min(RATE_LIMIT_BURST, 100000),
        },
        "freshness": {
            "max_staleness_seconds": 120,
            "default_expires_seconds": 300,
        },
        "context_allowlist": allowlist,
        "namespacing": {
            "action_required": True,
            "resource_required": False,
            "versioning_required": False,
            "recommended_formats": ["uri", "urn"],
        },
        "signing": {
            "supported": True,
            "required_for_al2": ASSURANCE_LEVEL == "AL2",
            "default_signed_responses": ASSURANCE_LEVEL in {"AL3", "AL4"},
            "algorithms": ["RS256"],
            "jwks_uri": f"{base}{JWKS_PATH}",
            "canonicalization": {
                "json_canonicalization": "operator-defined",
                "unicode_normalization": "none",
                "context_keys_included_in_hash": allowlist,
            },
        },
        "recognition_policy": {
            "scoped_required": True,
            "expiry_required": True,
            "transitive_default": False,
            "max_chain_depth": 1,
        },
        "transparency": {
            "service_docs_uri": _public_uri(base, "/.well-known/service-docs"),
            "change_log_uri": _public_uri(base, "/.well-known/governance/change-control"),
            "security_txt_uri": _public_uri(base, "/.well-known/service-docs"),
        },
    }
    if ASSURANCE_LEVEL in {"AL3", "AL4"}:
        metadata["audit"] = {
            "independent_assessment_uri": _public_uri(base, "/.well-known/assessment/al3-independent-assessment"),
            "audit_log_uri": _public_uri(base, "/.well-known/audit/log"),
            "immutability": True,
            "retention_days": 365,
        }
        metadata["governance"] = {
            "policy_uri": _public_uri(base, "/.well-known/governance/policy"),
            "change_control_uri": _public_uri(base, "/.well-known/governance/change-control"),
            "rollback_uri": _public_uri(base, "/.well-known/governance/rollback"),
        }
    if ASSURANCE_LEVEL == "AL4":
        metadata["key_protection"] = {
            "protection": "KMS",
            "evidence_uri": _public_uri(base, "/.well-known/keys/protection"),
        }
        metadata["monitoring"] = {
            "evidence_retention_days": 365,
            "incident_contact": {"email": "soc@example.org", "url": _public_uri(base, "/.well-known/ops/runbook")},
            "runbook_uri": _public_uri(base, "/.well-known/ops/runbook"),
            "telemetry_uri": _public_uri(base, "/.well-known/ops/runbook"),
        }
    return metadata


@app.get(JWKS_PATH)
def get_jwks():
    pub = jwk.JWK.from_json(_SIGNING_KEY.export_public())
    pub.kid = KID
    return {"keys": [json.loads(pub.export_public())]}


@app.get("/{doc_path:path}")
def get_public_doc(doc_path: str):
    path = "/" + doc_path
    if path in PUBLIC_DOCS:
        return PUBLIC_DOCS[path]
    raise HTTPException(status_code=404, detail="not_found")


@app.post("/authorization")
async def post_authorization(req: Request, authorization: Optional[str] = Header(default=None), accept_signature: Optional[str] = Header(default="none", alias="Accept-Signature")):
    rl_headers = await _rate_limit_tick()
    if rl_headers and int(rl_headers.get("RateLimit-Remaining", "1")) == 0 and WINDOW_COUNT >= RATE_LIMIT_BURST:
        raise HTTPException(status_code=429, detail="rate_limited", headers=rl_headers)

    _require_auth(authorization)

    body = await req.json()
    allowlist = ["purpose", "audience", "locale"]
    ctx = _strip_unknown_context(body.get("context"), allowlist)
    if isinstance(body, dict):
        body["context"] = ctx

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

    if _should_sign_success(accept_signature):
        qh = _query_hash(body, allowlist)
        return _sign_envelope(payload, qh, [k for k in allowlist if isinstance(ctx, dict) and k in ctx])

    return payload


@app.post("/recognition")
async def post_recognition(req: Request, authorization: Optional[str] = Header(default=None), accept_signature: Optional[str] = Header(default="none", alias="Accept-Signature")):
    _require_auth(authorization)
    body = await req.json()
    allowlist = ["purpose", "audience", "locale"]
    raw_ctx = body.get("context") if isinstance(body, dict) else None
    if isinstance(raw_ctx, dict):
        unknown_keys = [k for k in raw_ctx if k not in allowlist]
        if unknown_keys:
            raise HTTPException(
                status_code=400,
                detail={
                    "error": "invalid_context",
                    "message": "Request context contains keys not declared in the server allowlist.",
                    "unknown_keys": unknown_keys,
                    "allowlist": allowlist,
                },
            )
    ctx = _strip_unknown_context(raw_ctx, allowlist)
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
    if _should_sign_success(accept_signature):
        qh = _query_hash(body, allowlist)
        return _sign_envelope(payload, qh, [k for k in allowlist if isinstance(ctx, dict) and k in ctx])
    return payload
