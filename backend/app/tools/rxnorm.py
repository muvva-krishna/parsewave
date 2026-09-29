import httpx
from app.core.config import get_settings
from app.tools.base import ClinicalTool, ToolResult


class RxNormTool(ClinicalTool):
    name = "rxnorm_lookup"
    description = "Normalize a medication name using the NLM RxNorm API."

    async def run(self, drug: str) -> ToolResult:
        s = get_settings()
        try:
            async with httpx.AsyncClient(timeout=s.request_timeout_seconds) as client:
                r = await client.get(f"{s.rxnorm_base_url}/rxcui.json", params={"name": drug})
                r.raise_for_status()
                payload = r.json()
            ids = payload.get("idGroup", {}).get("rxnormId", [])
            return ToolResult(tool_name=self.name, success=True, data={"rxcuids": ids, "input": drug})
        except Exception as exc:
            return ToolResult(tool_name=self.name, success=False, data={}, error=str(exc))
