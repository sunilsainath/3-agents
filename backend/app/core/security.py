"""Authentication guard.

Derives identity from the validated Supabase JWT in `Authorization: Bearer ...`.
Never trusts user/tenant IDs from request bodies.

Modes:
- If SUPABASE_JWT_SECRET is set: verifies HS256 signature + audience (dev/local).
- If empty (CI/scaffold): stub-decodes the payload WITHOUT signature verification
  so route wiring and 401/403 behaviour can be tested. Production MUST set the
  secret (or JWKS — TODO with DB/auth hardening) or startup fails closed.
"""

from dataclasses import dataclass

import jwt
from fastapi import Depends, Header
from jwt import PyJWTError

from app.core.config import settings
from app.core.errors import AppError


@dataclass(frozen=True)
class AuthPrincipal:
    user_id: str
    role: str = "authenticated"


def _stub_decode(token: str) -> str:
    try:
        payload = jwt.decode(token, options={"verify_signature": False})
    except PyJWTError:
        raise AppError("AUTHENTICATION_REQUIRED", "Invalid token.", 401) from None
    sub = payload.get("sub")
    if not sub or not isinstance(sub, str):
        raise AppError("AUTHENTICATION_REQUIRED", "Token has no subject.", 401)
    return sub


def _verify_hs256(token: str) -> str:
    try:
        payload = jwt.decode(
            token,
            settings.supabase_jwt_secret,
            algorithms=["HS256"],
            audience=settings.supabase_jwt_audience,
            options={"require": ["sub", "exp"]},
        )
    except PyJWTError:
        raise AppError("AUTHENTICATION_REQUIRED", "Invalid or expired token.", 401) from None
    sub = payload.get("sub")
    if not sub or not isinstance(sub, str):
        raise AppError("AUTHENTICATION_REQUIRED", "Token has no subject.", 401)
    return sub


async def get_current_principal(
    authorization: str | None = Header(default=None),
) -> AuthPrincipal:
    if not authorization or not authorization.startswith("Bearer "):
        raise AppError("AUTHENTICATION_REQUIRED", "Authentication required.", 401)
    token = authorization[len("Bearer ") :].strip()
    if not token:
        raise AppError("AUTHENTICATION_REQUIRED", "Authentication required.", 401)
    if settings.supabase_jwt_secret:
        user_id = _verify_hs256(token)
    else:
        user_id = _stub_decode(token)
    return AuthPrincipal(user_id=user_id)


RequireAuth = Depends(get_current_principal)
