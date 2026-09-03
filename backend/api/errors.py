from __future__ import annotations

import logging

from fastapi import Request
from fastapi.responses import JSONResponse

logger = logging.getLogger(__name__)


def register_exception_handlers(app) -> None:
    @app.exception_handler(ValueError)
    async def value_error_handler(request: Request, exc: ValueError) -> JSONResponse:
        request_id = request.headers.get("X-Request-ID")
        return JSONResponse(
            status_code=400,
            content={"detail": str(exc), "request_id": request_id},
        )

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
        request_id = request.headers.get("X-Request-ID") or "unknown"
        logger.exception("Unhandled request error request_id=%s", request_id)
        return JSONResponse(
            status_code=500,
            content={
                "detail": "ALICE encountered an internal server error. Check the deployment logs for the underlying provider error.",
                "request_id": request_id,
            },
        )
