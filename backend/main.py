from fastapi import FastAPI

from backend.api.chat import router as chat_router
from backend.api.health import router as health_router
from backend.config.settings import get_settings

settings = get_settings()
app = FastAPI(title=settings.app_name, version="0.1.0", debug=settings.debug)
app.include_router(health_router)
app.include_router(chat_router)
