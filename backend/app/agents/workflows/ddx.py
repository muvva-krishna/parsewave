from app.agents.base import Agent, AgentContext


class DdxWorkflow(Agent):
    """Workflow boundary for the ddx mode; adds workflow-specific instructions/state."""
    name = "ddx"

    async def run(self, ctx: AgentContext) -> None:
        ctx.state.setdefault("workflow", {})["ddx"] = True
        ctx.add_activity("workflow", "Activated ddx workflow")
