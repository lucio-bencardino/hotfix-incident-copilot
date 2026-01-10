from app.core.settings import settings
from app.schemas.health import HealthResponse
from fastapi import APIRouter

router = APIRouter()


@router.get("/health", response_model=HealthResponse)
async def health_check():
    return HealthResponse(
        status="ok", version=settings.VERSION, api_version=settings.API_VERSION
    )
