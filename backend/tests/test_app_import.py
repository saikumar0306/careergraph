from fastapi.testclient import TestClient

from backend.app.main import app


def test_app_imports_and_health_endpoint():
    client = TestClient(app)
    response = client.get('/health/db')
    assert response.status_code in {200, 503}
