import re
from app.agents.base import Agent, AgentContext


class DrugReferenceAgent(Agent):
    name = "drug_reference"

    async def run(self, ctx: AgentContext) -> None:
        q = ctx.state["query"]
        drug = self._drug(q)
        ctx.state["drug"] = drug
        tools = ctx.state["tools"]
        rx = await tools["rxnorm_lookup"].run(drug=drug)
        fda = await tools["openfda_drug_label"].run(drug=drug)
        ctx.add_activity("tool", "Normalized medication with RxNorm", f"drug={drug}")
        ctx.add_activity("tool", "Fetched FDA labeling", f"success={fda.success}")
        ctx.state["drug_data"] = {"rxnorm": rx.data, "fda": fda.data}

    @staticmethod
    def _drug(q: str) -> str:
        common = ["methotrexate", "warfarin", "apixaban", "metformin", "semaglutide", "pembrolizumab"]
        low = q.lower()
        for d in common:
            if d in low:
                return d
        return q.split()[0]
