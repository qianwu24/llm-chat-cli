from collections.abc import Callable

from llm_chat.config import Settings
from llm_chat.models import ChatRequest, ChatResponse
from llm_chat.providers import ChatProvider, create_provider

ProviderFactory = Callable[[str, Settings], ChatProvider]


class ChatService:
    def __init__(
        self,
        settings: Settings,
        provider_factory: ProviderFactory = create_provider,
    ) -> None:
        self._settings = settings
        self._provider_factory = provider_factory

    async def chat(self, request: ChatRequest) -> ChatResponse:
        available_models = self._settings.models_for(request.provider)
        if request.model not in available_models:
            raise ValueError(
                f"Model '{request.model}' is not configured for {request.provider}. "
                f"Choose one of: {', '.join(available_models)}"
            )

        provider = self._provider_factory(request.provider, self._settings)
        text = await provider.complete(request.model, request.message)
        return ChatResponse(
            provider=request.provider,
            model=request.model,
            response=text,
        )

