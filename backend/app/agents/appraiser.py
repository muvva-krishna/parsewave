from app.agents.base import Agent, AgentContext


class EvidenceAppraiser(Agent):
    name = "evidence_appraiser"

    async def run(self, ctx: AgentContext) -> None:
        evidence = ctx.state.get("evidence", [])
        for item in evidence:
            meta = item.metadata
            title = (item.title or "").lower()
            study_type = "unknown"
            for label, words in {
                "systematic_review": ["systematic review", "meta-analysis"],
                "randomized_trial": ["randomized", "randomised", "controlled trial"],
                "guideline": ["guideline", "practice guideline", "consensus"],
                "cohort": ["cohort", "prospective", "retrospective"],
            }.items():
                if any(w in title for w in words):
                    study_type = label
                    break
            item.appraisal = {
                "study_type": study_type,
                "recency_year": meta.get("year"),
                "machine_appraisal": "heuristic_only",
            }
        ctx.add_activity("appraisal", "Appraised retrieved evidence", f"{len(evidence)} evidence items")
