from typing import Any
from app.agents.base import Agent, AgentContext
from app.models.factory import get_model


class BoundedToolLoop(Agent):
    """Bounded ReAct-style loop: model proposes tools, tools return observations, model replans.

    It stores operational events only; raw chain-of-thought is intentionally not persisted.
    """
    name = "bounded_tool_loop"

    def __init__(self, role: str = "orchestrator", max_steps: int = 6) -> None:
        self.role = role
        self.max_steps = max_steps

    async def run(self, ctx: AgentContext) -> None:
        model = get_model(self.role)
        registry = ctx.state["tools"]
        history: list[dict[str, Any]] = [{"role": "user", "content": ctx.state["query"]}]
        tool_schemas = []
        for tool in registry.values():
            tool_schemas.append({
                "type": "function",
                "function": {
                    "name": tool.name,
                    "description": tool.description,
                    "parameters": {"type": "object", "properties": {"query": {"type": "string"}}},
                },
            })
        for step in range(self.max_steps):
            response = await model.client.chat(model=model.model_name, messages=history, tools=tool_schemas) if hasattr(model, "client") else None
            if response is None:
                return
            calls = response.message.tool_calls or []
            if not calls:
                ctx.state["agent_answer"] = response.message.content or ""
                ctx.add_activity("agent", "Agent loop reached a final answer", f"step={step + 1}")
                return
            history.append({"role": "assistant", "content": response.message.content or "", "tool_calls": []})
            for call in calls:
                tool = registry.get(call.function.name)
                if tool is None:
                    continue
                args = call.function.arguments or {}
                result = await tool.run(**args)
                observation = result.model_dump_json()
                history.append({"role": "tool", "content": observation})
                ctx.add_activity("tool", f"Agent called {call.function.name}", f"step={step + 1}, success={result.success}")
        ctx.state["agent_answer"] = "Agent stopped after the bounded tool-call budget."
        ctx.add_activity("agent", "Agent loop stopped at safety/latency budget", f"max_steps={self.max_steps}")
