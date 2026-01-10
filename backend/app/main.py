from app.api.routes import router
from app.core.logging import setup_logging
from app.core.settings import settings
from fastapi import FastAPI

setup_logging()

app = FastAPI(title=settings.PROJECT_NAME)
app.include_router(router, prefix=settings.API_VERSION)
