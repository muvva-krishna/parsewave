from app.agents.base import Agent, AgentContext


class TxPlanWorkflow(Agent):
    """Workflow boundary for the tx_plan mode; adds workflow-specific instructions/state."""
    name = "tx_plan"

    async def run(self, ctx: AgentContext) -> None:
        ctx.state.setdefault("workflow", {})["tx_plan"] = True
        ctx.add_activity("workflow", "Activated tx_plan workflow")
