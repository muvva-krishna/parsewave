from typing import Any, Literal
from pydantic import BaseModel, Field
from app.core.types import Claim, EvidenceItem, WorkflowMode


class BaseCard(BaseModel):
    type: WorkflowMode
    title: str
    subtitle: str | None = None
    claims: list[Claim] = Field(default_factory=list)
    sources: list[EvidenceItem] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)


class ClinicalAnswerCard(BaseCard):
    type: Literal[WorkflowMode.CLINICAL_ANSWER, WorkflowMode.QUICK_CURBSIDE, WorkflowMode.GUIDELINE]
    answer: str
    takeaways: list[str] = Field(default_factory=list)


class DrugReferenceCard(BaseCard):
    type: Literal[WorkflowMode.DRUG_REFERENCE]
    drug: str
    indication: str | None = None
    dosing: list[dict[str, Any]] = Field(default_factory=list)
    contraindications: list[str] = Field(default_factory=list)
    interactions: list[str] = Field(default_factory=list)
    monitoring: list[str] = Field(default_factory=list)


class TrialCriterion(BaseModel):
    text: str
    status: Literal["YES", "NO", "UNKNOWN"]
    reason: str
    source: str | None = None


class TrialMatchCard(BaseCard):
    type: Literal[WorkflowMode.CLINICAL_TRIAL_MATCH]
    nct_id: str
    phase: str | None = None
    status: str | None = None
    match_percent: int = Field(ge=0, le=100)
    confirmed: int = 0
    total: int = 0
    criteria: list[TrialCriterion] = Field(default_factory=list)
    nearest_sites: list[str] = Field(default_factory=list)


class DdxCard(BaseCard):
    type: Literal[WorkflowMode.DDx]
    differentials: list[dict[str, Any]] = Field(default_factory=list)
    discriminators: list[str] = Field(default_factory=list)


class TxPlanCard(BaseCard):
    type: Literal[WorkflowMode.TX_PLAN]
    assessment: str
    options: list[dict[str, Any]] = Field(default_factory=list)
    monitoring: list[str] = Field(default_factory=list)
    follow_up: list[str] = Field(default_factory=list)


class PatientHandoutCard(BaseCard):
    type: Literal[WorkflowMode.PATIENT_HANDOUT]
    sections: list[dict[str, Any]] = Field(default_factory=list)
    reading_level: str = "plain language"


class SoapNoteCard(BaseCard):
    type: Literal[WorkflowMode.SOAP_NOTE]
    subjective: str
    objective: str
    assessment: str
    plan: str


class CalculationCard(BaseCard):
    type: Literal[WorkflowMode.CLINICAL_CALCULATION]
    calculator: str
    inputs: dict[str, Any] = Field(default_factory=dict)
    result: Any = None
    interpretation: str = ""
    missing_inputs: list[str] = Field(default_factory=list)
