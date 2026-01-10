from app.core.settings import settings


def test_generate_plan(client):
    url = f"{settings.API_VERSION}/generate-plan"

    payload = {"description": "server_outage", "logs": "high", "context": "database"}

    response = client.post(url, json=payload)

    assert response.status_code == 200

    data = response.json()
    assert "steps" in data
    assert isinstance(data["steps"], list)
    assert "warnings" in data
    assert isinstance(data["warnings"], list)
