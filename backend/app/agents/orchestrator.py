from uuid import uuid4
from app.agents.base import AgentContext
from app.agents.router import IntentRouter
from app.agents.premise import PremiseSafetyAgent
from app.agents.planner import ClinicalPlanner
from app.agents.evidence import EvidenceAgent
from app.agents.appraiser import EvidenceAppraiser
from app.agents.verifier import ClaimVerifier
from app.agents.critic import ClinicalCriticAgent
from app.agents.synthesis import ClinicalSynthesisAgent
from app.agents.trial_matcher import TrialMatchAgent
from app.agents.drug_reference import DrugReferenceAgent
from app.agents.calculation import CalculationAgent
from app.core.types import Claim, WorkflowMode
from app.tools.registry import build_registry
from app.tools.calculator_tool import CalculatorTool


class ClinicalOrchestrator:
    async def run(self, query: str, mode=None, patient_context=None, image_urls=None) -> dict:
        state = {
            "request_id": str(uuid4()),
            "query": query,
            "requested_mode": mode,
            "patient_context": patient_context or {},
            "image_urls": image_urls or [],
            "tools": build_registry() | {"clinical_calculator": CalculatorTool()},
        }
        ctx = AgentContext(state)
        await IntentRouter().run(ctx)
        await PremiseSafetyAgent().run(ctx)
        await ClinicalPlanner().run(ctx)
        selected = state["mode"]
        if selected == WorkflowMode.CLINICAL_TRIAL_MATCH:
            await TrialMatchAgent().run(ctx)
        elif selected == WorkflowMode.DRUG_REFERENCE:
            await DrugReferenceAgent().run(ctx)
        elif selected == WorkflowMode.CLINICAL_CALCULATION:
            await CalculationAgent().run(ctx)
        else:
            await EvidenceAgent().run(ctx)
            await EvidenceAppraiser().run(ctx)
        if not state.get("evidence") and selected == WorkflowMode.CLINICAL_TRIAL_MATCH:
            state["evidence"] = []
        await ClinicalSynthesisAgent().run(ctx)
        state["claims"] = [Claim(id="c1", text="See the structured artifact and linked evidence; unverified statements must be reviewed by a clinician.", evidence_ids=[])]
        await ClaimVerifier().run(ctx)
        await ClinicalCriticAgent().run(ctx)
        card = state["card"]
        if hasattr(card, "criteria") and state.get("trial_criteria"):
            card.criteria = state["trial_criteria"]
            card.total = len(card.criteria)
            card.confirmed = sum(c.status == "YES" for c in card.criteria)
            card.match_percent = round((card.confirmed / card.total) * 100) if card.total else 0
        card.warnings.extend(state.get("safety_flags", []))
        return {
            "request_id": state["request_id"],
            "mode": state["mode"],
            "card": card,
            "activities": state.get("activities", []),
            "evidence": state.get("evidence", []),
            "claims": state.get("claims", []),
            "metadata": {"plan": state.get("plan", []), "agentic_steps": len(state.get("activities", []))},
        }
