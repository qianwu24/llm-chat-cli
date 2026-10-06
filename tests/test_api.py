from fastapi.testclient import TestClient

from llm_chat.api import app, get_chat_service
from llm_chat.models import ChatRequest, ChatResponse


class FakeChatService:
    async def chat(self, request: ChatRequest) -> ChatResponse:
        return ChatResponse(
            provider=request.provider,
            model=request.model,
            response=f"Echo: {request.message}",
        )


def test_chat_endpoint() -> None:
    app.dependency_overrides[get_chat_service] = lambda: FakeChatService()
    try:
        client = TestClient(app)
        response = client.post(
            "/chat",
            json={"provider": "openai", "model": "test-model", "message": "Hello"},
        )
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 200
    assert response.json() == {
        "provider": "openai",
        "model": "test-model",
        "response": "Echo: Hello",
    }


def test_chat_rejects_unknown_provider() -> None:
    client = TestClient(app)
    response = client.post(
        "/chat",
        json={"provider": "unknown", "model": "model", "message": "Hello"},
    )

    assert response.status_code == 422

