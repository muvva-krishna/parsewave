from typing import Any
from pydantic import BaseModel, Field
from app.core.types import ActivityEvent, Claim, EvidenceItem, WorkflowMode
from app.schemas.cards import BaseCard


class AgentResponse(BaseModel):
    request_id: str
    mode: WorkflowMode
    card: BaseCard
    activities: list[ActivityEvent] = Field(default_factory=list)
    evidence: list[EvidenceItem] = Field(default_factory=list)
    claims: list[Claim] = Field(default_factory=list)
    metadata: dict[str, Any] = Field(default_factory=dict)
