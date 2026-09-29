from app.agents.base import Agent, AgentContext


class ClinicalCriticAgent(Agent):
    """High-level verifier hook; never exposes private reasoning text."""
    name = "clinical_critic"

    async def run(self, ctx: AgentContext) -> None:
        card = ctx.state.get("card")
        if card is None:
            return
        if not ctx.state.get("evidence") and card.type.value not in {"clinical_trial_match", "clinical_calculation"}:
            card.warnings.append("No evidence records were retrieved; treat the draft as unverified.")
        ctx.add_activity("verification", "Applied clinical output critique")
