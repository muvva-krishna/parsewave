from app.agents.base import Agent, AgentContext


class GuidelineWorkflow(Agent):
    """Workflow boundary for the guideline mode; adds workflow-specific instructions/state."""
    name = "guideline"

    async def run(self, ctx: AgentContext) -> None:
        ctx.state.setdefault("workflow", {})["guideline"] = True
        ctx.add_activity("workflow", "Activated guideline workflow")
