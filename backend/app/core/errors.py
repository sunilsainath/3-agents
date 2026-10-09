"""Consistent error envelope: {"error": {"code", "message", "request_id"}}."""

import uuid
from typing import Any

from fastapi import Request
from fastapi.responses import JSONResponse


def new_request_id(provided: str | None = None) -> str:
    return provided or uuid.uuid4().hex[:12]


def error_body(code: str, message: str, request_id: str) -> dict[str, Any]:
    return {"error": {"code": code, "message": message, "request_id": request_id}}


class AppError(Exception):
    def __init__(self, code: str, message: str, status_code: int = 400):
        super().__init__(message)
        self.code = code
        self.message = message
        self.status_code = status_code


async def app_error_handler(request: Request, exc: AppError) -> JSONResponse:
    request_id = getattr(request.state, "request_id", new_request_id())
    return JSONResponse(
        status_code=exc.status_code,
        content=error_body(exc.code, exc.message, request_id),
    )
