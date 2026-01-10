from app.api.health import router as health_router
from app.api.incident import router as incident_router
from fastapi import APIRouter

router = APIRouter()
router.include_router(health_router)
router.include_router(incident_router)
