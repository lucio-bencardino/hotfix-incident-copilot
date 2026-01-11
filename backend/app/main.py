from app.api.routes import router
from app.core.logging import setup_logging
from app.core.settings import settings
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

setup_logging()

app = FastAPI(title=settings.PROJECT_NAME)

if settings.ALLOWED_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOWED_ORIGINS, 
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(router, prefix=settings.API_VERSION)
