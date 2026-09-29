from abc import ABC, abstractmethod
from typing import Any
from app.core.types import ActivityEvent


class AgentContext:
    def __init__(self, state: dict[str, Any]) -> None:
        self.state = state

    def add_activity(self, event_type: str, label: str, detail: str | None = None) -> None:
        self.state.setdefault("activities", []).append(ActivityEvent(type=event_type, label=label, detail=detail))


class Agent(ABC):
    name: str

    @abstractmethod
    async def run(self, ctx: AgentContext) -> None:
        raise NotImplementedError
