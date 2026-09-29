import xml.etree.ElementTree as ET
from typing import Any
import httpx
from app.core.config import get_settings
from app.tools.base import ClinicalTool, ToolResult


class PubMedTool(ClinicalTool):
    name = "pubmed_search"
    description = "Search PubMed via NCBI E-utilities and return article metadata/snippets."

    async def run(self, query: str, top_k: int | None = None) -> ToolResult:
        s = get_settings()
        top_k = top_k or s.pubmed_top_k
        params: dict[str, Any] = {"db": "pubmed", "term": query, "retmax": top_k, "retmode": "json"}
        if s.ncbi_email:
            params["email"] = s.ncbi_email
        if s.ncbi_api_key:
            params["api_key"] = s.ncbi_api_key
        try:
            async with httpx.AsyncClient(timeout=s.request_timeout_seconds) as client:
                sr = await client.get("https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi", params=params)
                sr.raise_for_status()
                ids = sr.json().get("esearchresult", {}).get("idlist", [])
                if not ids:
                    return ToolResult(tool_name=self.name, success=True, data=[])
                fp = {"db": "pubmed", "id": ",".join(ids), "retmode": "xml"}
                if s.ncbi_email:
                    fp["email"] = s.ncbi_email
                if s.ncbi_api_key:
                    fp["api_key"] = s.ncbi_api_key
                fr = await client.get("https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi", params=fp)
                fr.raise_for_status()
            root = ET.fromstring(fr.text)
            items = []
            for article in root.findall(".//PubmedArticle"):
                pmid = article.findtext(".//PMID") or ""
                title = " ".join((article.findtext(".//ArticleTitle") or "").split())
                abstract = " ".join(t.text.strip() for t in article.findall(".//AbstractText") if t.text)
                journal = article.findtext(".//Journal/Title") or ""
                year = article.findtext(".//PubDate/Year") or article.findtext(".//PubDate/MedlineDate") or ""
                items.append({"id": pmid, "title": title, "abstract": abstract[:4000], "journal": journal, "year": year, "url": f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/"})
            return ToolResult(tool_name=self.name, success=True, data=items)
        except Exception as exc:
            return ToolResult(tool_name=self.name, success=False, data=[], error=str(exc))
