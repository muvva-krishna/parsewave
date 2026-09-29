from app.agents.base import Agent, AgentContext


class QuickCurbsideWorkflow(Agent):
    """Workflow boundary for the quick_curbside mode; adds workflow-specific instructions/state."""
    name = "quick_curbside"

    async def run(self, ctx: AgentContext) -> None:
        ctx.state.setdefault("workflow", {})["quick_curbside"] = True
        ctx.add_activity("workflow", "Activated quick_curbside workflow")
