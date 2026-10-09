"""Scaffold tests: envelopes, auth guard, ownership invariant, deny-by-default."""

import jwt
from fastapi.testclient import TestClient

from app.core.errors import AppError
from app.core.security import AuthPrincipal
from app.core.tenant import require_company_access, require_exactly_one_owner
from app.main import app

client = TestClient(app, raise_server_exceptions=False)


def _token(sub: str = "user-123") -> str:
    return jwt.encode({"sub": sub}, "test-only", algorithm="HS256")


def test_health_ok() -> None:
    r = client.get("/api/v1/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"


def test_openapi_served() -> None:
    r = client.get("/api/v1/openapi.json")
    assert r.status_code == 200
    assert r.json()["info"]["title"] == "MyTrakin API"


def test_me_requires_auth() -> None:
    r = client.get("/api/v1/me")
    assert r.status_code == 401
    body = r.json()
    assert body["error"]["code"] == "AUTHENTICATION_REQUIRED"
    assert "request_id" in body["error"]


def test_me_with_stub_token() -> None:
    r = client.get("/api/v1/me", headers={"Authorization": f"Bearer {_token()}"})
    assert r.status_code == 200
    assert r.json() == {"user_id": "user-123", "role": "authenticated"}


def test_me_rejects_garbage_token() -> None:
    r = client.get("/api/v1/me", headers={"Authorization": "Bearer not-a-jwt"})
    assert r.status_code == 401
    assert r.json()["error"]["code"] == "AUTHENTICATION_REQUIRED"


def test_request_id_echoed() -> None:
    r = client.get("/api/v1/health", headers={"X-Request-ID": "abc123"})
    assert r.headers["X-Request-ID"] == "abc123"


def test_ownership_requires_exactly_one() -> None:
    for bad in [(None, None), ("u1", "co1")]:
        try:
            require_exactly_one_owner(*bad)
        except AppError as e:
            assert e.code == "VALIDATION_ERROR"
        else:
            raise AssertionError(f"expected VALIDATION_ERROR for {bad}")
    assert require_exactly_one_owner("u1", None) == "user"
    assert require_exactly_one_owner(None, "co1") == "company"


def test_company_access_denies_by_default() -> None:
    import asyncio

    async def run() -> None:
        try:
            await require_company_access(AuthPrincipal(user_id="u1"), "co1")
        except AppError as e:
            assert e.status_code == 403
            assert e.code == "PERMISSION_DENIED"
        else:
            raise AssertionError("expected PERMISSION_DENIED")

    asyncio.run(run())
