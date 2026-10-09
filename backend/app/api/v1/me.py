"""Authenticated identity echo. Proves the guard works; real profile data is Phase 1."""

from typing import Annotated

from fastapi import APIRouter, Depends

from app.core.security import AuthPrincipal, get_current_principal

router = APIRouter()


@router.get("/me")
async def me(
    principal: Annotated[AuthPrincipal, Depends(get_current_principal)],
) -> dict[str, str]:
    return {"user_id": principal.user_id, "role": principal.role}
