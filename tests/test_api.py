from fastapi.testclient import TestClient

from nexus_cloud.app import app

client = TestClient(app)


def test_liveness() -> None:
    response = client.get("/health/live")
    assert response.status_code == 200
    assert response.json()["status"] == "alive"


def test_readiness() -> None:
    response = client.get("/health/ready")
    assert response.status_code == 200
    assert response.json()["status"] == "ready"


def test_gpu_endpoint_has_stable_shape() -> None:
    response = client.get("/v1/compute/gpu")
    assert response.status_code == 200
    payload = response.json()
    assert isinstance(payload["available"], bool)
    assert isinstance(payload["devices"], list)
