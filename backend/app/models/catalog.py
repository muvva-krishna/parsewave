from dataclasses import dataclass


@dataclass(frozen=True)
class ModelSpec:
    name: str
    provider: str
    purpose: str
    modalities: tuple[str, ...]


MODEL_CATALOG = {
    "orchestrator": ModelSpec("qwen3:8b", "ollama", "planning and tool calling", ("text",)),
    "clinical_text": ModelSpec("medgemma:27b", "ollama", "medical text synthesis", ("text",)),
    "clinical_extractor": ModelSpec("medgemma1.5:4b", "ollama", "clinical context extraction", ("text", "image")),
    "clinical_vision": ModelSpec("medgemma:27b", "ollama", "medical image/document interpretation", ("text", "image")),
}
