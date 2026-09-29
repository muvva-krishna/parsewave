from fastapi import APIRouter, HTTPException
from app.agents.orchestrator import ClinicalOrchestrator
from app.schemas.requests import AskRequest
from app.schemas.response import AgentResponse

router = APIRouter(prefix="/ask", tags=["clinical-agent"])


@router.post("", response_model=AgentResponse)
async def ask(request: AskRequest) -> AgentResponse:
    try:
        result = await ClinicalOrchestrator().run(
            query=request.query,
            mode=request.mode,
            patient_context=request.patient_context,
            image_urls=request.image_urls,
        )
        return AgentResponse(**result)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
