from typing import Any
import json
import httpx
from app.models.base import ModelClient


class OpenAICompatibleClient(ModelClient):
    """Adapter for a deployed/open endpoint exposing /v1/chat/completions."""

    def __init__(self, model_name: str, base_url: str, api_key: str | None, timeout: float = 60.0) -> None:
        self.model_name = model_name
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.timeout = timeout

    def _headers(self) -> dict[str, str]:
        headers = {"Content-Type": "application/json"}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        return headers

    async def generate(self, messages: list[dict[str, Any]], **kwargs: Any) -> str:
        payload = {"model": self.model_name, "messages": messages, **kwargs}
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            r = await client.post(f"{self.base_url}/v1/chat/completions", json=payload, headers=self._headers())
            r.raise_for_status()
            return r.json()["choices"][0]["message"].get("content", "")

    async def generate_json(self, messages: list[dict[str, Any]], schema: dict[str, Any], **kwargs: Any) -> dict[str, Any]:
        payload = {
            "model": self.model_name,
            "messages": messages,
            "temperature": 0,
            "response_format": {"type": "json_schema", "json_schema": {"name": "clinical_schema", "schema": schema}},
            **kwargs,
        }
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            r = await client.post(f"{self.base_url}/v1/chat/completions", json=payload, headers=self._headers())
            r.raise_for_status()
            content = r.json()["choices"][0]["message"].get("content", "{}")
            return json.loads(content)
