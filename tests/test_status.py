from fastapi.testclient import TestClient

from backend.main import app


def test_status():
    response = TestClient(app).get("/api/status")
    assert response.status_code == 200
    assert response.json() == {"service": "ALICE AI", "status": "ready"}
