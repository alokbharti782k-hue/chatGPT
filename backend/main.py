from pathlib import Path
from time import monotonic
from uuid import uuid4

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

from backend.api.chat import router as chat_router
from backend.api.chat_stream import router as chat_stream_router
from backend.api.errors import register_exception_handlers
from backend.api.files import router as files_router
from backend.api.health import router as health_router
from backend.api.observability import router as observability_router
from backend.api.rag import router as rag_router
from backend.api.status import router as status_router
from backend.config.settings import get_settings
from backend.observability.metrics import metrics
from backend.security.audit import SecurityAuditLog
from backend.security.auth import authenticate_request
from backend.security.rate_limit import RateLimiter

settings = get_settings()
app = FastAPI(title=settings.app_name, version="1.0.0", debug=settings.debug)
rate_limiter = RateLimiter(limit=settings.rate_limit_per_minute, window_seconds=60.0)
audit_log = SecurityAuditLog()

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type"],
)


@app.middleware("http")
async def security_middleware(request: Request, call_next):
    started = monotonic()
    request_id = uuid4().hex
    path = request.url.path
    if path.startswith("/api/"):
        client = request.client.host if request.client else "unknown"
        if not rate_limiter.allow(client):
            audit_log.record("rate_limit_blocked", client=client, path=path, request_id=request_id)
            metrics.observe_request(started, error=True)
            metrics.observe_security_block()
            return JSONResponse(
                status_code=429,
                content={"detail": "Rate limit exceeded", "request_id": request_id},
                headers={"X-Request-ID": request_id, "Retry-After": "60"},
            )
        if not authenticate_request(request.headers.get("Authorization"), settings.api_key):
            audit_log.record("authentication_failure", client=client, path=path, request_id=request_id)
            metrics.observe_request(started, error=True)
            metrics.observe_security_block()
            return JSONResponse(
                status_code=401,
                content={"detail": "Authentication required", "request_id": request_id},
                headers={"X-Request-ID": request_id, "WWW-Authenticate": "Bearer"},
            )

    response = await call_next(request)
    metrics.observe_request(started, error=response.status_code >= 400)
    response.headers["X-Request-ID"] = request_id
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Referrer-Policy"] = "no-referrer"
    response.headers["Cache-Control"] = "no-store" if path.startswith("/api/") else response.headers.get("Cache-Control", "")
    return response


register_exception_handlers(app)
app.include_router(health_router)
app.include_router(status_router)
app.include_router(chat_router)
app.include_router(chat_stream_router)
app.include_router(files_router)
app.include_router(rag_router)
app.include_router(observability_router)

FRONTEND_DIR = Path(__file__).resolve().parents[1] / "frontend"
if FRONTEND_DIR.exists():
    app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")

    @app.get("/", include_in_schema=False)
    async def index() -> FileResponse:
        return FileResponse(FRONTEND_DIR / "index.html")
else:
    @app.get("/")
    def root() -> dict[str, str]:
        return {"service": settings.app_name, "status": "online"}
