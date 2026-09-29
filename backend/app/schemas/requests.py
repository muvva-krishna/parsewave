from typing import Any
from pydantic import BaseModel, Field
from app.core.types import WorkflowMode


class AskRequest(BaseModel):
    query: str = Field(min_length=3)
    mode: WorkflowMode | None = None
    patient_context: dict[str, Any] | None = None
    image_urls: list[str] = Field(default_factory=list)
    session_id: str | None = None
