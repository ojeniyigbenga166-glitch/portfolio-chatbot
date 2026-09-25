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
