from app.agents.base import Agent, AgentContext
from app.core.types import WorkflowMode


class ClinicalPlanner(Agent):
    name = "clinical_planner"

    async def run(self, ctx: AgentContext) -> None:
        mode: WorkflowMode = ctx.state["mode"]
        if mode == WorkflowMode.CLINICAL_TRIAL_MATCH:
            plan = ["extract_patient_facts", "search_trials", "parse_eligibility", "match_criteria", "verify"]
        elif mode == WorkflowMode.DRUG_REFERENCE:
            plan = ["normalize_drug", "fetch_fda_label", "check_guidance", "verify_dose_frequency", "synthesize"]
        elif mode == WorkflowMode.DDx:
            plan = ["extract_context", "retrieve_evidence", "generate_hypotheses", "look_for_discriminators", "verify"]
        elif mode == WorkflowMode.TX_PLAN:
            plan = ["extract_context", "retrieve_guidelines", "retrieve_drug_evidence", "compare_options", "verify"]
        elif mode == WorkflowMode.CLINICAL_CALCULATION:
            plan = ["identify_calculator", "extract_inputs", "compute_deterministically", "interpret", "verify"]
        elif mode in {WorkflowMode.PATIENT_HANDOUT, WorkflowMode.SOAP_NOTE}:
            plan = ["extract_context", "retrieve_supporting_evidence", "draft_structured_artifact", "verify"]
        elif mode == WorkflowMode.DEEP_RESEARCH:
            plan = ["decompose_question", "multi_hop_search", "appraise", "synthesize", "verify"]
        else:
            plan = ["decompose_question", "search_evidence", "appraise", "synthesize", "verify"]
        ctx.state["plan"] = plan
        ctx.add_activity("planning", "Created adaptive clinical plan", " → ".join(plan))
