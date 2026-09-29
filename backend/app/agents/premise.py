from app.agents.base import Agent, AgentContext


class PremiseSafetyAgent(Agent):
    name = "premise_safety"

    async def run(self, ctx: AgentContext) -> None:
        q = ctx.state["query"].lower()
        flags = []
        if "methotrexate" in q and "daily" in q:
            flags.append("Methotrexate for rheumatoid arthritis is generally prescribed weekly, not daily; verify indication and regimen before acting on the answer.")
        if any(x in q for x in ["overdose", "suicide", "self harm", "poisoning"]):
            flags.append("High-risk acute scenario: provide emergency/specialist guidance and do not infer a management plan from incomplete context.")
        ctx.state["safety_flags"] = flags
        for flag in flags:
            ctx.add_activity("safety", "Premise/safety flag raised", flag)
