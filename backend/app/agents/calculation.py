import re
from app.agents.base import Agent, AgentContext
from app.tools.calculator_tool import CalculatorTool


class CalculationAgent(Agent):
    name = "calculation_agent"

    async def run(self, ctx: AgentContext) -> None:
        q = ctx.state["query"].lower()
        if "cha2ds2" in q or "cha₂ds₂" in q:
            calc = "CHA2DS2-VASc"
        elif "curb-65" in q:
            calc = "CURB-65"
        elif "wells" in q:
            calc = "Wells PE"
        else:
            ctx.state["calculation_result"] = {"error": "No supported calculator detected."}
            return
        ctx.state["calculator"] = calc
        patient = ctx.state.get("patient_context") or {}
        tool = CalculatorTool()
        inputs = {k: v for k, v in patient.items() if k in {
            "congestive_heart_failure", "hypertension", "age", "diabetes", "stroke_tia_thromboembolism", "vascular_disease", "sex_female",
            "confusion", "bun_gt_19", "respiratory_rate_gte_30", "systolic_bp_lt_90", "age_gte_65",
            "clinical_signs_dvt", "pe_most_likely", "hr_gt_100", "immobilization_or_surgery", "prior_dvt_pe", "hemoptysis", "malignancy"
        }}
        if calc == "CURB-65" and "age_gte_65" not in inputs and "age" in patient:
            inputs["age_gte_65"] = patient["age"] >= 65
        result = await tool.run(calculator=calc, inputs=inputs)
        ctx.add_activity("tool", f"Computed {calc} deterministically", f"success={result.success}")
        ctx.state["calculation_result"] = result.data if result.success else {"error": result.error}
