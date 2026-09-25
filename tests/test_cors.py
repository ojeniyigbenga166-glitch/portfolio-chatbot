"""
CORS verification tests for Phase 1 of chatbot integration.
Tests:
  - ALLOWED_ORIGINS is correctly loaded from environment
  - GET /health returns 200
  - POST /chat works with a valid message
  - OPTIONS preflight from allowed origin returns correct CORS headers
  - OPTIONS preflight from disallowed origin is blocked
  - Actual POST /chat with Origin header gets the CORS header back
"""
import os
from fastapi.testclient import TestClient
from app.main import app, ALLOWED_ORIGINS


client = TestClient(app, raise_server_exceptions=True)


def test_allowed_origins_loaded():
    """ALLOWED_ORIGINS must be a non-empty list."""
    assert isinstance(ALLOWED_ORIGINS, list)
    assert len(ALLOWED_ORIGINS) > 0, "ALLOWED_ORIGINS is empty — check .env"
    print(f"\nALLOWED_ORIGINS: {ALLOWED_ORIGINS}")


def test_health_smoke():
    """GET /health must still return 200 after CORS middleware was added."""
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json() == {"status": "ok"}


def test_chat_smoke():
    """POST /chat must still return a reply for a valid message."""
    r = client.post("/chat", json={"message": "What services does Olugbenga offer?"})
    assert r.status_code == 200
    data = r.json()
    assert "reply" in data
    assert len(data["reply"]) > 0


def test_cors_preflight_allowed_origin():
    """OPTIONS preflight from http://localhost:5173 must be approved."""
    r = client.options(
        "/chat",
        headers={
            "Origin": "http://localhost:5173",
            "Access-Control-Request-Method": "POST",
            "Access-Control-Request-Headers": "Content-Type",
        },
    )
    assert r.status_code == 200, f"Expected 200, got {r.status_code}"
    acao = r.headers.get("access-control-allow-origin", "MISSING")
    assert acao == "http://localhost:5173", (
        f"Expected 'http://localhost:5173', got '{acao}'"
    )
    acam = r.headers.get("access-control-allow-methods", "")
    assert "POST" in acam.upper(), f"POST not in Access-Control-Allow-Methods: {acam}"


def test_cors_preflight_disallowed_origin():
    """OPTIONS preflight from an unlisted origin must NOT return a wildcard or the origin."""
    r = client.options(
        "/chat",
        headers={
            "Origin": "https://evil.com",
            "Access-Control-Request-Method": "POST",
            "Access-Control-Request-Headers": "Content-Type",
        },
    )
    acao = r.headers.get("access-control-allow-origin", "MISSING")
    assert acao != "https://evil.com", (
        "Security failure: disallowed origin was reflected in Access-Control-Allow-Origin"
    )
    assert acao != "*", (
        "Security failure: wildcard origin returned — should never happen"
    )


def test_cors_actual_post_with_origin_header():
    """Actual POST /chat with a valid Origin must include ACAO header in response."""
    r = client.post(
        "/chat",
        json={"message": "What is ARLTECH?"},
        headers={"Origin": "http://localhost:5173"},
    )
    assert r.status_code == 200
    acao = r.headers.get("access-control-allow-origin", "MISSING")
    assert acao == "http://localhost:5173", (
        f"CORS header missing on actual request, got: '{acao}'"
    )


def test_cors_no_credentials():
    """Access-Control-Allow-Credentials must NOT be 'true'."""
    r = client.options(
        "/chat",
        headers={
            "Origin": "http://localhost:5173",
            "Access-Control-Request-Method": "POST",
            "Access-Control-Request-Headers": "Content-Type",
        },
    )
    acac = r.headers.get("access-control-allow-credentials", "false")
    assert acac.lower() != "true", (
        "allow_credentials must be False — credentials header should not be 'true'"
    )
