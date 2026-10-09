"""v1 router. Business resources land here as vertical slices (Phases 1+)."""

from fastapi import APIRouter

from app.api.v1 import health, me

router = APIRouter()
router.include_router(health.router, tags=["health"])
router.include_router(me.router, tags=["identity"])
