from fastapi.testclient import TestClient

from nexus_cloud.app import app


def test_gateway_is_disabled_by_default() -> None:
    with TestClient(app) as client:
        response = client.post("/v1/generate", json={"prompt": "hello"})
    assert response.status_code == 503
