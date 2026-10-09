"""Tenant/ownership helpers (deny-by-default scaffold).

Unified-workspace rule: a client `company_id` is requested scope only, never
proof of permission. Every company operation must revalidate membership, role,
resource access and business prerequisites.

Until the DB agent lands membership/role lookups + RLS, company-scoped
authorization explicitly DENIES (fail closed) instead of guessing. Personal
scope is the authenticated user derived from the token.
"""

from app.core.errors import AppError
from app.core.security import AuthPrincipal


def require_exactly_one_owner(owner_user_id: str | None, company_id: str | None) -> str:
    """Resources supporting both personal and company ownership need exactly one."""
    has_user = bool(owner_user_id)
    has_company = bool(company_id)
    if has_user == has_company:  # both or neither
        raise AppError(
            "VALIDATION_ERROR",
            "Provide exactly one of owner_user_id or company_id.",
            422,
        )
    return "user" if has_user else "company"


async def require_company_access(principal: AuthPrincipal, company_id: str) -> None:
    """Deny-by-default stub. Real membership/role/resource check lands with DB schema.

    Raises 403 PERMISSION_DENIED until wired to verified membership lookups.
    """
    _ = (principal, company_id)
    raise AppError(
        "PERMISSION_DENIED",
        "Company access is not yet provisioned; membership check pending.",
        403,
    )
