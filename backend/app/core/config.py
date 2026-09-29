from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_env: str = "development"
    log_level: str = "INFO"
    api_v1_prefix: str = "/api/v1"
    orchestrator_provider: str = "ollama"
    orchestrator_model: str = "qwen3:8b"
    synthesis_provider: str = "ollama"
    synthesis_model: str = "medgemma:27b"
    extractor_provider: str = "ollama"
    extractor_model: str = "medgemma1.5:4b"
    vision_provider: str = "ollama"
    vision_model: str = "medgemma:27b"
    ollama_base_url: str = "http://localhost:11434"
    medgemma_remote_base_url: str | None = None
    medgemma_remote_api_key: str | None = None
    medgemma_remote_text_model: str = "google/medgemma-27b-text-it"
    medgemma_remote_vision_model: str = "google/medgemma-27b-it"
    ncbi_email: str | None = None
    ncbi_api_key: str | None = None
    clinicaltrials_base_url: str = "https://clinicaltrials.gov/api/v2"
    openfda_base_url: str = "https://api.fda.gov"
    rxnorm_base_url: str = "https://rxnav.nlm.nih.gov/REST"
    dailymed_base_url: str = "https://dailymed.nlm.nih.gov/dailymed/services/v2"
    pubmed_top_k: int = 8
    trial_top_k: int = 8
    max_agent_steps: int = 10
    request_timeout_seconds: float = 20.0

    model_config = SettingsConfigDict(env_file=".env", extra="ignore", case_sensitive=False)


@lru_cache
def get_settings() -> Settings:
    return Settings()
