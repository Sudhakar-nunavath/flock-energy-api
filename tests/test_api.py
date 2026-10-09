from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health_check():
    response = client.get("/api/v1/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_openapi_documentation_available():
    response = client.get("/openapi.json")

    assert response.status_code == 200
    assert response.json()["info"]["title"] == "Flock Energy Meter API"


def test_meter_list_requires_valid_page():
    response = client.get("/api/v1/meters?page=0")

    assert response.status_code == 422
