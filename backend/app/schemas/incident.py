from app.schemas.base import CamelModel


class IncidentRequest(CamelModel):
    description: str
    logs: str | None = None
    context: str | None = None


class IncidentResponse(CamelModel):
    steps: list[str]
    warnings: list[str] | None = None
