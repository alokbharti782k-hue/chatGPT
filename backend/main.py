from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.api.chat import router as chat_router
from backend.api.errors import register_exception_handlers
from backend.api.files import router as files_router
from backend.api.health import router as health_router
from backend.config.settings import get_settings

settings = get_settings()
app = FastAPI(title=settings.app_name, version="0.1.0", debug=settings.debug)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

register_exception_handlers(app)
app.include_router(health_router)
app.include_router(chat_router)
app.include_router(files_router)

@app.get("/")
def root() -> dict[str, str]:
    return {"service": settings.app_name, "status": "online"}
