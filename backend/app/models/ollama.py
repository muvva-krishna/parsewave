from typing import Any
import json
from app.models.base import ModelClient


class OllamaClient(ModelClient):
    def __init__(self, model_name: str, base_url: str) -> None:
        import ollama
        self.model_name = model_name
        self.client = ollama.AsyncClient(host=base_url)

    async def generate(self, messages: list[dict[str, Any]], **kwargs: Any) -> str:
        response = await self.client.chat(model=self.model_name, messages=messages, **kwargs)
        return response.message.content or ""

    async def generate_json(self, messages: list[dict[str, Any]], schema: dict[str, Any], **kwargs: Any) -> dict[str, Any]:
        response = await self.client.chat(
            model=self.model_name,
            messages=messages,
            format=schema,
            options={"temperature": 0},
            **kwargs,
        )
        raw = response.message.content or "{}"
        return json.loads(raw)
