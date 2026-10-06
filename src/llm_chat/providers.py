from typing import Protocol

from openai import AsyncOpenAI

from llm_chat.config import Settings


class ChatProvider(Protocol):
    async def complete(self, model: str, message: str) -> str: ...


class OpenAIProvider:
    def __init__(self, api_key: str) -> None:
        self._client = AsyncOpenAI(api_key=api_key)

    async def complete(self, model: str, message: str) -> str:
        response = await self._client.responses.create(model=model, input=message)
        return response.output_text


class DeepSeekProvider:
    def __init__(self, api_key: str) -> None:
        self._client = AsyncOpenAI(api_key=api_key, base_url="https://api.deepseek.com")

    async def complete(self, model: str, message: str) -> str:
        response = await self._client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": message}],
        )
        content = response.choices[0].message.content
        if content is None:
            raise RuntimeError("DeepSeek returned no text response")
        return content


def create_provider(name: str, settings: Settings) -> ChatProvider:
    api_key = settings.api_key_for(name)
    if name == "openai":
        return OpenAIProvider(api_key)
    if name == "deepseek":
        return DeepSeekProvider(api_key)
    raise ValueError(f"Unsupported provider: {name}")

