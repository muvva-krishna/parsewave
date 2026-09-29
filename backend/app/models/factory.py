from functools import lru_cache
from app.core.config import get_settings
from app.models.base import ModelClient
from app.models.ollama import OllamaClient
from app.models.openai_compatible import OpenAICompatibleClient


@lru_cache
def get_model(role: str) -> ModelClient:
    s = get_settings()
    provider = getattr(s, f"{role}_provider")
    model_name = getattr(s, f"{role}_model")
    if provider == "ollama":
        return OllamaClient(model_name=model_name, base_url=s.ollama_base_url)
    if provider in {"remote", "openai_compatible"}:
        if not s.medgemma_remote_base_url:
            raise RuntimeError("MEDGEMMA_REMOTE_BASE_URL is required for remote/openai_compatible provider")
        return OpenAICompatibleClient(
            model_name=model_name,
            base_url=s.medgemma_remote_base_url,
            api_key=s.medgemma_remote_api_key,
            timeout=s.request_timeout_seconds,
        )
    raise ValueError(f"Unsupported model provider: {provider}")
