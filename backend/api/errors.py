from fastapi import Request
from fastapi.responses import JSONResponse


def register_exception_handlers(app) -> None:
    @app.exception_handler(ValueError)
    async def value_error_handler(request: Request, exc: ValueError) -> JSONResponse:
        return JSONResponse(status_code=400, content={"detail": str(exc)})
