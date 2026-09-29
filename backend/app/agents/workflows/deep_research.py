from app.agents.base import Agent, AgentContext


class DeepResearchWorkflow(Agent):
    """Workflow boundary for the deep_research mode; adds workflow-specific instructions/state."""
    name = "deep_research"

    async def run(self, ctx: AgentContext) -> None:
        ctx.state.setdefault("workflow", {})["deep_research"] = True
        ctx.add_activity("workflow", "Activated deep_research workflow")
