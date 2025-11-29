from fastapi.testclient import TestClient
from unittest.mock import patch
from app.main import app

client = TestClient(app)


def test_ai_status_disabled():
    with patch("app.ai_service.GOOGLE_API_KEY", None):
        response = client.get("/ai/status")
        assert response.status_code == 200
        assert response.json() == {"enabled": False}


def test_chat_disabled():
    with patch("app.ai_service.GOOGLE_API_KEY", None):
        # We need a token to bypass auth or mock the auth dependency,
        # but the check for disabled AI happens inside the route handler.
        # However, the `chat` route has `current_user: str = Depends(get_current_user)`.
        # So we need to authenticate first or override the dependency.

        # Let's override the dependency for simplicity
        app.dependency_overrides = {}  # Clear previous
        from app.security import get_current_user

        app.dependency_overrides[get_current_user] = lambda: "testuser"

        response = client.post(
            "/ai/chat",
            json={
                "character_name": "Yoda",
                "character_context": "Jedi Master",
                "message": "Hello",
            },
        )

        assert response.status_code == 503
        assert response.json()["detail"] == "AI services are currently disabled."

        # Clean up safely
        del app.dependency_overrides[get_current_user]


def test_image_disabled():
    with patch("app.ai_service.GOOGLE_API_KEY", None):
        response = client.get("/ai/image?name=Luke&type=people")
        assert response.status_code == 503
        assert response.json()["detail"] == "AI services are currently disabled."
