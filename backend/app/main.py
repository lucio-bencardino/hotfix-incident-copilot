from app.api.routes import router
from app.core.settings import settings
from fastapi import FastAPI

app = FastAPI(title=settings.PROJECT_NAME)

app.include_router(router, prefix=settings.API_VERSION)
