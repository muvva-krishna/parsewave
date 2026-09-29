import pytest
from app.agents.base import AgentContext
from app.agents.router import IntentRouter
from app.core.types import WorkflowMode


@pytest.mark.asyncio
async def test_trial_mode_routes():
    state = {"query": "Does she qualify for any Alzheimer's clinical trial?"}
    await IntentRouter().run(AgentContext(state))
    assert state["mode"] == WorkflowMode.CLINICAL_TRIAL_MATCH
