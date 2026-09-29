from app.agents.base import Agent, AgentContext
from app.models.factory import get_model
from app.core.types import Claim, EvidenceItem, WorkflowMode
from app.schemas.cards import ClinicalAnswerCard, DdxCard, DrugReferenceCard, PatientHandoutCard, TrialCriterion, TrialMatchCard, TxPlanCard, CalculationCard, SoapNoteCard


class ClinicalSynthesisAgent(Agent):
    name = "clinical_synthesis"

    async def run(self, ctx: AgentContext) -> None:
        mode: WorkflowMode = ctx.state["mode"]
        evidence: list[EvidenceItem] = ctx.state.get("evidence", [])
        citations = [
            {"id": e.id, "title": e.title, "url": e.url, "snippet": e.snippet[:800], "metadata": e.metadata}
            for e in evidence[:8]
        ]
        model = get_model("synthesis")
        system = (
            "You are the clinical synthesis component of an evidence-first decision-support system. "
            "Use only supplied evidence. Do not invent citations. If evidence is missing, say UNKNOWN. "
            "Return concise clinician-facing content; never expose hidden chain-of-thought."
        )
        prompt = f"Workflow={mode.value}
Question={ctx.state['query']}
Patient={ctx.state.get('patient_context') or {}}
Evidence={citations}"
        answer = await model.generate([{"role": "system", "content": system}, {"role": "user", "content": prompt}], temperature=0)
        if mode in {WorkflowMode.CLINICAL_ANSWER, WorkflowMode.GUIDELINE, WorkflowMode.QUICK_CURBSIDE, WorkflowMode.DEEP_RESEARCH}:
            card = ClinicalAnswerCard(type=mode, title="Evidence-backed clinical answer", answer=answer, claims=[])
        elif mode == WorkflowMode.DDx:
            card = DdxCard(type=mode, title="Differential diagnosis", differentials=[{"summary": answer}])
        elif mode == WorkflowMode.TX_PLAN:
            card = TxPlanCard(type=mode, title="Treatment plan", assessment=answer)
        elif mode == WorkflowMode.DRUG_REFERENCE:
            card = DrugReferenceCard(type=mode, title="Drug reference", drug=ctx.state.get("drug", "Unspecified"), monitoring=[answer])
        elif mode == WorkflowMode.PATIENT_HANDOUT:
            card = PatientHandoutCard(type=mode, title="Patient handout", sections=[{"heading": "What to know", "body": answer}])
        elif mode == WorkflowMode.SOAP_NOTE:
            card = SoapNoteCard(type=mode, title="SOAP note", subjective=answer, objective="", assessment="", plan="")
        elif mode == WorkflowMode.CLINICAL_TRIAL_MATCH:
            card = self._trial_card(ctx, answer)
        else:
            card = ClinicalAnswerCard(type=WorkflowMode.CLINICAL_ANSWER, title="Clinical answer", answer=answer)
        ctx.state["card"] = card
        ctx.add_activity("synthesis", "Generated structured clinical artifact")

    def _trial_card(self, ctx: AgentContext, answer: str) -> TrialMatchCard:
        trial = (ctx.state.get("trials") or [{}])[0]
        criteria = [TrialCriterion(text="Eligibility criteria require patient-level verification", status="UNKNOWN", reason="Not enough structured patient data in this MVP.")]
        return TrialMatchCard(
            type=WorkflowMode.CLINICAL_TRIAL_MATCH,
            title=trial.get("title") or "Clinical trial match",
            nct_id=trial.get("nct_id") or "UNKNOWN",
            phase=trial.get("phase"), status=trial.get("status"),
            match_percent=0, confirmed=0, total=len(criteria), criteria=criteria,
            nearest_sites=[f"{x.get('city')}, {x.get('state')}" for x in trial.get("locations", [])[:3]],
            warnings=[answer] if answer else [],
        )
