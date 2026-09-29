from app.agents.base import Agent, AgentContext


class PatientHandoutWorkflow(Agent):
    """Workflow boundary for the patient_handout mode; adds workflow-specific instructions/state."""
    name = "patient_handout"

    async def run(self, ctx: AgentContext) -> None:
        ctx.state.setdefault("workflow", {})["patient_handout"] = True
        ctx.add_activity("workflow", "Activated patient_handout workflow")
