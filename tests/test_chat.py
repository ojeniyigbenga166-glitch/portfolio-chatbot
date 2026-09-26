from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_chat_empty_message():
    response = client.post("/chat", json={"message": "   "})
    assert response.status_code == 400
    assert response.json()["detail"] == "Message cannot be empty."


def test_chat_portfolio_question():
    response = client.post(
        "/chat",
        json={"message": "What services does Olugbenga Ojeniyi offer?"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "reply" in data
    reply = data["reply"].lower()
    assert any(term in reply for term in ["web design", "frontend", "full-stack", "arltech", "olugbenga"])


def test_lead_capture_success():
    response = client.post(
        "/lead",
        json={
            "name": "Alex Smith",
            "email": "alex@example.com",
            "message": "Looking for web development services",
            "service": "Web Development"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert "Thank you" in data["message"]


def test_lead_capture_validation():
    response = client.post(
        "/lead",
        json={"name": "", "email": "invalid-email"}
    )
    assert response.status_code == 400
    assert "required" in response.json()["detail"]


def test_chat_auto_lead_extraction():
    response = client.post(
        "/chat",
        json={"message": "Hi, my email is client@domain.com and I want to hire Olugbenga for a web project"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "reply" in data


