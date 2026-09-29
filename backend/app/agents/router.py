import re
from app.agents.base import Agent, AgentContext
from app.core.types import WorkflowMode


class IntentRouter(Agent):
    name = "intent_router"

    async def run(self, ctx: AgentContext) -> None:
        q = ctx.state["query"].lower()
        mode = ctx.state.get("requested_mode")
        if mode:
            ctx.state["mode"] = mode
            return
        if any(x in q for x in ["clinical trial", "trial match", "qualify for", "eligibility"]):
            mode = WorkflowMode.CLINICAL_TRIAL_MATCH
        elif any(x in q for x in ["maximum dose", "dose", "dosing", "contraindication", "interaction"]):
            mode = WorkflowMode.DRUG_REFERENCE
        elif any(x in q for x in ["differential", "ddx", "differential diagnosis"]):
            mode = WorkflowMode.DDx
        elif any(x in q for x in ["treatment plan", "treat", "management plan"]):
            mode = WorkflowMode.TX_PLAN
        elif any(x in q for x in ["calculate", "score", "cha2ds2", "wells", "curb-65"]):
            mode = WorkflowMode.CLINICAL_CALCULATION
        elif any(x in q for x in ["patient handout", "home instructions", "patient instructions"]):
            mode = WorkflowMode.PATIENT_HANDOUT
        elif "soap note" in q:
            mode = WorkflowMode.SOAP_NOTE
        elif any(x in q for x in ["guideline", "recommendation"]):
            mode = WorkflowMode.GUIDELINE
        else:
            mode = WorkflowMode.CLINICAL_ANSWER
        ctx.state["mode"] = mode
        ctx.add_activity("router", f"Selected workflow: {mode.value}")
