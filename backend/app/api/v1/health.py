"""Public health check (unauthenticated)."""

from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok", "service": "mytrakin-api", "version": "0.1.0"}
