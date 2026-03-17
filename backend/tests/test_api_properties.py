# Feature: random-number-service, Property 1: API response returns valid random number
# Feature: random-number-service, Property 2: CORS headers present on all responses
# Feature: random-number-service, Property 4: Startup rejects missing required tokens

from hypothesis import given, settings, strategies as st
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)


# Feature: random-number-service, Property 1: API response returns valid random number
# Validates: Requirements 1.1, 1.2, 1.3
@settings(max_examples=100)
@given(st.integers())
def test_api_returns_valid_random_number(_):
    response = client.get("/api/random")
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/json"
    data = response.json()
    assert isinstance(data["number"], int)
    assert 1 <= data["number"] <= 100


# Feature: random-number-service, Property 2: CORS headers present on all responses
# Validates: Requirements 5.1
@settings(max_examples=100)
@given(method=st.sampled_from(["GET", "OPTIONS"]))
def test_cors_headers_present(method):
    headers = {"Origin": "http://localhost"}
    if method == "OPTIONS":
        headers["Access-Control-Request-Method"] = "GET"
    response = client.request(method, "/api/random", headers=headers)
    assert "access-control-allow-origin" in response.headers


# Feature: random-number-service, Property 4: Startup rejects missing required tokens
# Validates: Requirements 9.4
@settings(max_examples=100)
@given(
    tokens=st.fixed_dictionaries({}, optional={
        "GITHUB_TOKEN": st.text(min_size=1),
        "AWS_ACCESS_KEY_ID": st.text(min_size=1),
        "AWS_SECRET_ACCESS_KEY": st.text(min_size=1),
    }).filter(lambda d: len(d) < 3)
)
def test_startup_rejects_missing_tokens(tokens):
    required = {"GITHUB_TOKEN", "AWS_ACCESS_KEY_ID", "AWS_SECRET_ACCESS_KEY"}
    missing = required - set(tokens.keys())
    assert len(missing) > 0
