from app.core.settings import settings


def test_generate_plan(client):
    url = f"{settings.API_VERSION}/generate-plan"

    payload = {
        "description": "Production Database Latency",
        "logs": "Connection timeout on port 5432 (Postgres)",
        "role": "devops",
    }

    response = client.post(url, json=payload)

    assert response.status_code == 200

    data = response.json()

    assert "steps" in data
    assert isinstance(data["steps"], list)
    assert len(data["steps"]) > 0

    if "warnings" in data and data["warnings"] is not None:
        assert isinstance(data["warnings"], list)
