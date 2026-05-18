"""Tests for Gateway API Key authentication."""

from fastapi.testclient import TestClient

from xybook_gateway.main import app

client = TestClient(app, raise_server_exceptions=False)


def test_health_no_auth():
    resp = client.get("/health")
    assert resp.status_code == 200


def test_community_post_requires_api_key():
    resp = client.post("/api/community/posts", json={"content": "test"})
    assert resp.status_code == 401


def test_community_post_with_valid_key():
    resp = client.post(
        "/api/community/posts",
        json={"content": "test"},
        headers={"x-api-key": "xybook-dev-key"},
    )
    # Auth passes — upstream may fail, but NOT 401
    assert resp.status_code != 401


def test_agents_get_requires_api_key():
    resp = client.get("/api/agents/")
    assert resp.status_code == 401


def test_agents_get_with_key():
    resp = client.get("/api/agents/", headers={"x-api-key": "xybook-dev-key"})
    assert resp.status_code != 401


def test_pipeline_requires_api_key():
    resp = client.get("/api/pipeline/events")
    assert resp.status_code == 401


def test_invalid_api_key():
    resp = client.get("/api/agents/", headers={"x-api-key": "wrong-key"})
    assert resp.status_code == 401


def test_experiments_requires_api_key():
    resp = client.get("/api/experiments/")
    assert resp.status_code == 401
