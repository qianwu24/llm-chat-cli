from typing import Literal

from pydantic import BaseModel, Field

ProviderName = Literal["openai", "deepseek"]


class ChatRequest(BaseModel):
    provider: ProviderName
    model: str = Field(min_length=1)
    message: str = Field(min_length=1)


class ChatResponse(BaseModel):
    provider: ProviderName
    model: str
    response: str


class ProviderInfo(BaseModel):
    name: ProviderName
    models: list[str]
    configured: bool

