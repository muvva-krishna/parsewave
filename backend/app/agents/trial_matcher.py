import re
from app.agents.base import Agent, AgentContext
from app.schemas.cards import TrialCriterion


class TrialMatchAgent(Agent):
    name = "trial_matcher"

    async def run(self, ctx: AgentContext) -> None:
        tools = ctx.state["tools"]
        condition = self._condition(ctx.state["query"], ctx.state.get("patient_context") or {})
        result = await tools["clinical_trials_search"].run(condition=condition)
        ctx.add_activity("tool", "Searched ClinicalTrials.gov", f"condition={condition}")
        ctx.state["trials"] = result.data if result.success else []
        if not ctx.state["trials"]:
            ctx.state["trial_criteria"] = []
            return
        study = ctx.state["trials"][0]
        criteria_text = study.get("eligibility_text") or ""
        items = self._extract_criteria(criteria_text)
        patient = ctx.state.get("patient_context") or {}
        criteria: list[TrialCriterion] = []
        for text in items[:12]:
            status, reason = self._match(text, patient)
            criteria.append(TrialCriterion(text=text, status=status, reason=reason, source="ClinicalTrials.gov"))
        ctx.state["trial_criteria"] = criteria

    @staticmethod
    def _condition(query: str, patient: dict) -> str:
        m = re.search(r"(?:with|for) ([A-Za-z][A-Za-z -]{3,60}?)(?:,|?|$)", query, re.I)
        return m.group(1).strip() if m else str(patient.get("diagnosis") or "Alzheimer Disease")

    @staticmethod
    def _extract_criteria(text: str) -> list[str]:
        if not text:
            return []
        chunks = re.split(r"
+|(?:. )", text)
        return [re.sub(r"^[-•*]s*", "", x).strip() for x in chunks if len(x.strip()) > 20]

    @staticmethod
    def _match(text: str, patient: dict) -> tuple[str, str]:
        low = text.lower()
        if "age" in low:
            age = patient.get("age")
            if age is None:
                return "UNKNOWN", "Patient age not provided in structured context."
        if "male" in low and patient.get("sex") == "female":
            return "NO", "Sex criterion conflicts with patient context."
        if "female" in low and patient.get("sex") == "male":
            return "NO", "Sex criterion conflicts with patient context."
        return "UNKNOWN", "Criterion requires patient-level evidence not present in the current context."
