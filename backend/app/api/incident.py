from app.schemas.incident import IncidentRequest, IncidentResponse
from app.services.ai_service import AIService
from fastapi import APIRouter

router = APIRouter()


@router.post("/generate-plan", response_model=IncidentResponse)
async def generate_plan(request: IncidentRequest):
    plan = await AIService.generate_incident_plan(
        description=request.description,
        logs=request.logs,
        context=request.context,
        role=request.role,
    )
    return IncidentResponse(steps=plan["steps"], warnings=plan["warnings"])
