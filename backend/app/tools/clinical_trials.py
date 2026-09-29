from typing import Any
import httpx
from app.core.config import get_settings
from app.tools.base import ClinicalTool, ToolResult


class ClinicalTrialsTool(ClinicalTool):
    name = "clinical_trials_search"
    description = "Search ClinicalTrials.gov API v2 for recruiting studies and eligibility information."

    async def run(self, condition: str, query: str | None = None, top_k: int | None = None) -> ToolResult:
        s = get_settings()
        params: dict[str, Any] = {
            "query.cond": condition,
            "filter.overallStatus": "RECRUITING|NOT_YET_RECRUITING|ENROLLING_BY_INVITATION|ACTIVE_NOT_RECRUITING",
            "pageSize": top_k or s.trial_top_k,
            "format": "json",
        }
        if query:
            params["query.term"] = query
        try:
            async with httpx.AsyncClient(timeout=s.request_timeout_seconds) as client:
                r = await client.get(f"{s.clinicaltrials_base_url}/studies", params=params)
                r.raise_for_status()
                studies = r.json().get("studies", [])
            data = []
            for study in studies:
                p = study.get("protocolSection", {})
                ident = p.get("identificationModule", {})
                status = p.get("statusModule", {})
                design = p.get("designModule", {})
                elig = p.get("eligibilityModule", {})
                locs = p.get("contactsLocationsModule", {}).get("locations", [])
                data.append({
                    "nct_id": ident.get("nctId"),
                    "title": ident.get("briefTitle") or ident.get("officialTitle"),
                    "phase": (design.get("phases") or [None])[0],
                    "status": status.get("overallStatus"),
                    "eligibility_text": elig.get("eligibilityCriteria"),
                    "minimum_age": elig.get("minimumAge"),
                    "maximum_age": elig.get("maximumAge"),
                    "sex": elig.get("sex"),
                    "locations": [x for x in locs if x.get("city")],
                })
            return ToolResult(tool_name=self.name, success=True, data=data)
        except Exception as exc:
            return ToolResult(tool_name=self.name, success=False, data=[], error=str(exc))
