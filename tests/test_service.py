import pytest

from llm_chat.config import Settings
from llm_chat.models import ChatRequest
from llm_chat.service import ChatService


class FakeProvider:
    async def complete(self, model: str, message: str) -> str:
        return f"{model}: {message}"


@pytest.mark.asyncio
async def test_service_returns_provider_response() -> None:
    settings = Settings(
        openai_api_key="test-key",
        openai_models="test-model",
        _env_file=None,
    )
    service = ChatService(settings, provider_factory=lambda _name, _settings: FakeProvider())

    response = await service.chat(
        ChatRequest(provider="openai", model="test-model", message="Hello")
    )

    assert response.response == "test-model: Hello"


@pytest.mark.asyncio
async def test_service_rejects_unconfigured_model() -> None:
    settings = Settings(
        openai_api_key="test-key",
        openai_models="allowed-model",
        _env_file=None,
    )
    service = ChatService(settings, provider_factory=lambda _name, _settings: FakeProvider())

    with pytest.raises(ValueError, match="not configured"):
        await service.chat(
            ChatRequest(provider="openai", model="other-model", message="Hello")
        )

