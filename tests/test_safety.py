import pytest
from app.agents.base import AgentContext
from app.agents.premise import PremiseSafetyAgent


@pytest.mark.asyncio
async def test_methotrexate_daily_flag():
    state = {"query": "maximum daily dose of methotrexate for RA"}
    await PremiseSafetyAgent().run(AgentContext(state))
    assert state["safety_flags"]
