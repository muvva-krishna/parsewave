from abc import ABC, abstractmethod
from typing import Any


class ModelClient(ABC):
    model_name: str

    @abstractmethod
    async def generate(self, messages: list[dict[str, Any]], **kwargs: Any) -> str:
        raise NotImplementedError

    @abstractmethod
    async def generate_json(self, messages: list[dict[str, Any]], schema: dict[str, Any], **kwargs: Any) -> dict[str, Any]:
        raise NotImplementedError
