from fastapi import FastAPI
from app.api.routes.health import router as health_router
from app.api.routes.ask import router as ask_router
from app.core.config import get_settings

settings = get_settings()
app = FastAPI(title="Clinical Evidence Agent", version="0.1.0")
app.include_router(health_router)
app.include_router(ask_router, prefix=settings.api_v1_prefix)
