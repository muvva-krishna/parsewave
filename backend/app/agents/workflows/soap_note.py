from app.agents.base import Agent, AgentContext


class SoapNoteWorkflow(Agent):
    """Workflow boundary for the soap_note mode; adds workflow-specific instructions/state."""
    name = "soap_note"

    async def run(self, ctx: AgentContext) -> None:
        ctx.state.setdefault("workflow", {})["soap_note"] = True
        ctx.add_activity("workflow", "Activated soap_note workflow")
