from typing import Any
import httpx
from app.core.config import get_settings
from app.tools.base import ClinicalTool, ToolResult


class OpenFDADrugLabelTool(ClinicalTool):
    name = "openfda_drug_label"
    description = "Retrieve publicly available FDA drug label sections such as warnings, contraindications and dosing."

    async def run(self, drug: str) -> ToolResult:
        s = get_settings()
        url = f"{s.openfda_base_url}/drug/label.json"
        params: dict[str, Any] = {"search": f'openfda.generic_name:"{drug}"', "limit": 3}
        try:
            async with httpx.AsyncClient(timeout=s.request_timeout_seconds) as client:
                r = await client.get(url, params=params)
                if r.status_code == 404:
                    params = {"search": f'medicinal_product:"{drug}"', "limit": 3}
                    r = await client.get(url, params=params)
                r.raise_for_status()
                results = r.json().get("results", [])
            data = []
            for item in results:
                data.append({
                    "brand": item.get("openfda", {}).get("brand_name", []),
                    "generic": item.get("openfda", {}).get("generic_name", []),
                    "indications": item.get("indications_and_usage", []),
                    "warnings": item.get("warnings", []),
                    "contraindications": item.get("contraindications", []),
                    "dosage": item.get("dosage_and_administration", []),
                    "interactions": item.get("drug_interactions", []),
                    "updated": item.get("effective_time"),
                })
            return ToolResult(tool_name=self.name, success=True, data=data)
        except Exception as exc:
            return ToolResult(tool_name=self.name, success=False, data=[], error=str(exc))
