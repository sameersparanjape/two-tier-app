from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)


def test_get_random_returns_200():
    response = client.get("/api/random")
    assert response.status_code == 200


def test_get_random_returns_json_with_number():
    response = client.get("/api/random")
    data = response.json()
    assert "number" in data
    assert isinstance(data["number"], int)
    assert 1 <= data["number"] <= 100


def test_options_returns_cors_headers():
    response = client.options("/api/random", headers={
        "Origin": "http://localhost",
        "Access-Control-Request-Method": "GET",
    })
    assert "access-control-allow-origin" in response.headers


def test_endpoint_under_api_prefix():
    response = client.get("/api/random")
    assert response.status_code == 200
    response = client.get("/random")
    assert response.status_code != 200
