from app.schemas.base import CamelModel


class HealthResponse(CamelModel):
    status: str
    version: str
    api_version: str
