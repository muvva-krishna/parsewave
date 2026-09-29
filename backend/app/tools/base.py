from abc import ABC, abstractmethod
from typing import Any
from pydantic import BaseModel


class ToolResult(BaseModel):
    tool_name: str
    success: bool
    data: Any
    source_ids: list[str] = []
    error: str | None = None


class ClinicalTool(ABC):
    name: str
    description: str

    @abstractmethod
    async def run(self, **kwargs: Any) -> ToolResult:
        raise NotImplementedError
