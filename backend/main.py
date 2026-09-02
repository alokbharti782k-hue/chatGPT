from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from backend.api.chat import router as chat_router
from backend.api.errors import register_exception_handlers
from backend.api.files import router as files_router
from backend.api.health import router as health_router
from backend.api.rag import router as rag_router
from backend.api.status import router as status_router
from backend.config.settings import get_settings

settings = get_settings()
app = FastAPI(title=settings.app_name, version="0.2.0", debug=settings.debug)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

register_exception_handlers(app)
app.include_router(health_router)
app.include_router(status_router)
app.include_router(chat_router)
app.include_router(files_router)
app.include_router(rag_router)

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
