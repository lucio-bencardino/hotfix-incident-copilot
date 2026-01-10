from app.core.settings import settings


def test_health_check(client):
    url = f"{settings.API_VERSION}/health"

    response = client.get(url)

    assert response.status_code == 200

    data = response.json()
    assert data["status"] == "ok"
    assert data["version"] == settings.VERSION
    assert data["api_version"] == settings.API_VERSION
