from app.agents.base import Agent, AgentContext
from app.core.types import VerificationStatus


class ClaimVerifier(Agent):
    name = "claim_verifier"

    async def run(self, ctx: AgentContext) -> None:
        claims = ctx.state.get("claims", [])
        evidence_ids = {e.id for e in ctx.state.get("evidence", [])}
        for claim in claims:
            if claim.evidence_ids and all(eid in evidence_ids for eid in claim.evidence_ids):
                claim.verification = VerificationStatus.PASS
            else:
                claim.verification = VerificationStatus.FLAG
                claim.notes.append("No complete source linkage found in the current evidence set.")
        ctx.state["claims"] = claims
        ctx.add_activity("verification", "Verified claim-to-source linkage", f"{len(claims)} claims checked")
