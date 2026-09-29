from app.agents.base import Agent, AgentContext
from app.core.types import EvidenceItem


class EvidenceAgent(Agent):
    name = "evidence_agent"

    async def run(self, ctx: AgentContext) -> None:
        tools = ctx.state["tools"]
        query = ctx.state["query"]
        results: list[EvidenceItem] = []
        pubmed = await tools["pubmed_search"].run(query=query)
        ctx.add_activity("tool", "Searched PubMed", f"success={pubmed.success}")
        for x in pubmed.data:
            results.append(EvidenceItem(id=f"pmid:{x['id']}", source_type="PubMed", title=x["title"], url=x["url"], snippet=x.get("abstract", "")[:1000], metadata=x))
        ctx.state["evidence"] = results
