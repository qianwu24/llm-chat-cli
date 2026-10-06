from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException

from llm_chat.config import Settings, get_settings
from llm_chat.models import ChatRequest, ChatResponse, ProviderInfo
from llm_chat.service import ChatService

app = FastAPI(title="LLM Chat API", version="0.1.0")


SettingsDependency = Annotated[Settings, Depends(get_settings)]


def get_chat_service(settings: SettingsDependency) -> ChatService:
    return ChatService(settings)


ChatServiceDependency = Annotated[ChatService, Depends(get_chat_service)]


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/providers", response_model=list[ProviderInfo])
async def providers(settings: SettingsDependency) -> list[ProviderInfo]:
    return [
        ProviderInfo(
            name="openai",
            models=settings.models_for("openai"),
            configured=settings.openai_api_key is not None,
        ),
        ProviderInfo(
            name="deepseek",
            models=settings.models_for("deepseek"),
            configured=settings.deepseek_api_key is not None,
        ),
    ]


@app.post("/chat", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    service: ChatServiceDependency,
) -> ChatResponse:
    try:
        return await service.chat(request)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error
    except Exception as error:
        raise HTTPException(status_code=502, detail=f"Provider request failed: {error}") from error
