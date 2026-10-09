"""Server-side pagination helpers. Clients cannot inject raw sort/SQL."""

from typing import Any, Generic, TypeVar

from fastapi import Query
from pydantic import BaseModel, Field

from app.core.config import settings

T = TypeVar("T")


class PageParams(BaseModel):
    page: int = Field(default=1, ge=1)
    page_size: int = Field(default=25, ge=1, le=100)


def page_params(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=25, ge=1, le=100),
) -> PageParams:
    size = min(page_size, settings.max_page_size)
    return PageParams(page=page, page_size=size)


class Pagination(BaseModel):
    page: int
    page_size: int
    total: int


class Page(BaseModel, Generic[T]):
    data: list[T]
    pagination: Pagination


def make_page(items: list[T], params: PageParams, total: int) -> dict[str, Any]:
    return {
        "data": items,
        "pagination": {"page": params.page, "page_size": params.page_size, "total": total},
    }
