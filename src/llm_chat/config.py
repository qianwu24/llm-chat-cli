from functools import lru_cache

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    openai_api_key: SecretStr | None = None
    deepseek_api_key: SecretStr | None = None
    openai_models: str = "gpt-5.5"
    deepseek_models: str = "deepseek-flash,deepseek-v4-pro"

    def models_for(self, provider: str) -> list[str]:
        raw_models = {
            "openai": self.openai_models,
            "deepseek": self.deepseek_models,
        }.get(provider)
        if raw_models is None:
            raise ValueError(f"Unsupported provider: {provider}")
        return [model.strip() for model in raw_models.split(",") if model.strip()]

    def api_key_for(self, provider: str) -> str:
        key = {
            "openai": self.openai_api_key,
            "deepseek": self.deepseek_api_key,
        }.get(provider)
        if key is None:
            env_name = f"{provider.upper()}_API_KEY"
            raise ValueError(f"{env_name} is not configured")
        return key.get_secret_value()


@lru_cache
def get_settings() -> Settings:
    return Settings()

