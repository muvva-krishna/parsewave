from enum import Enum
from typing import Any
from pydantic import BaseModel, Field


class WorkflowMode(str, Enum):
    CLINICAL_ANSWER = "clinical_answer"
    DDx = "ddx"
    TX_PLAN = "tx_plan"
    DRUG_REFERENCE = "drug_reference"
    CLINICAL_CALCULATION = "clinical_calculation"
    CLINICAL_TRIAL_MATCH = "clinical_trial_match"
    GUIDELINE = "guideline"
    PATIENT_HANDOUT = "patient_handout"
    SOAP_NOTE = "soap_note"
    QUICK_CURBSIDE = "quick_curbside"
    DEEP_RESEARCH = "deep_research"


class VerificationStatus(str, Enum):
    PASS = "pass"
    FLAG = "flag"
    UNKNOWN = "unknown"


class PatientFact(BaseModel):
    key: str
    value: Any
    source: str = "user"
    confidence: float = Field(default=1.0, ge=0.0, le=1.0)


class EvidenceItem(BaseModel):
    id: str
    source_type: str
    title: str
    url: str | None = None
    snippet: str
    metadata: dict[str, Any] = Field(default_factory=dict)
    retrieval_score: float | None = None
    appraisal: dict[str, Any] = Field(default_factory=dict)


class Claim(BaseModel):
    id: str
    text: str
    evidence_ids: list[str] = Field(default_factory=list)
    verification: VerificationStatus = VerificationStatus.UNKNOWN
    notes: list[str] = Field(default_factory=list)


class ActivityEvent(BaseModel):
    type: str
    label: str
    detail: str | None = None
