import os
import sys

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Keep the existing backend untouched; import it from this isolated web entrypoint.
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BACKEND = os.path.join(ROOT, "backend")
if BACKEND not in sys.path:
    sys.path.insert(0, BACKEND)

from app.agents.orchestrator import ClinicalOrchestrator  # noqa: E402
from app.schemas.requests import AskRequest  # noqa: E402
from app.schemas.response import AgentResponse  # noqa: E402

app = FastAPI(title="Clinical Evidence Agent Web API", version="0.1.0")

allowed_origins = [
    origin.strip()
    for origin in os.getenv("ALLOWED_ORIGINS", "*").split(",")
    if origin.strip()
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"] if "*" in allowed_origins else allowed_origins,
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/api/ask", response_model=AgentResponse)
async def ask(request: AskRequest) -> AgentResponse:
    result = await ClinicalOrchestrator().run(
        query=request.query,
        mode=request.mode,
        patient_context=request.patient_context,
        image_urls=request.image_urls,
    )
    return AgentResponse(**result)
