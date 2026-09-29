# Parsewave — Clinical Evidence Agent

An open, modular clinical evidence-agent MVP inspired by Vera-style clinical workflows: evidence-first retrieval, bounded agentic tool use, verification, deterministic calculators, clinical trial matching, drug reference, and typed response cards.

> Research/MVP infrastructure only. Do not use this repository to diagnose, prescribe, or treat patients. Use synthetic or de-identified data during development.

## Architecture

User request -> intent router -> premise/safety gate -> adaptive planner -> clinical tools/evidence retrieval -> appraisal -> synthesis -> claim verification -> typed response card.

The system intentionally separates agents, models, tools, schemas, workflows and frontend rendering.

## Model routing

| Role | Default | Purpose |
|---|---|---|
| Orchestrator | Qwen3 via Ollama | planning and tool calling |
| Clinical synthesis | MedGemma 27B | medical text synthesis |
| Clinical extraction | MedGemma 1.5 4B | structured context extraction |
| Vision | MedGemma 27B multimodal | medical image/document interpretation |

Model selection is behind adapters so hosted OpenAI-compatible endpoints can be substituted without changing agent code.

## Repository layout

```text
backend/app/
├── agents/        # planning, safety, retrieval, appraisal, synthesis, verification
├── models/        # model/provider adapters
├── tools/         # PubMed, trials, FDA, RxNorm, calculators
├── calculators/   # deterministic clinical calculations
├── schemas/       # typed workflow and response contracts
├── core/          # configuration and state types
└── api/           # HTTP boundary
frontend/          # thin Next.js shell
docs/              # architecture, safety and API notes
research/          # medical-agent paper mapping
tests/
infra/
```

## Public clinical APIs

- PubMed / NCBI E-utilities
- ClinicalTrials.gov API v2
- openFDA drug labeling
- NLM RxNorm

See `docs/sources.md` for official API/model documentation.

## Run

```bash
docker compose -f infra/docker-compose.yml up -d
```

Install Ollama and pull models appropriate for the available hardware:

```bash
ollama pull qwen3:8b
ollama pull medgemma1.5:4b
ollama pull medgemma:27b
```

Install backend:

```bash
cd backend
python -m venv .venv
# Windows: .venv\\Scripts\\activate
# Linux/macOS: source .venv/bin/activate
pip install -e '.[all]'
uvicorn app.main:app --reload --port 8000
```

Ask the API:

```bash
curl -X POST http://localhost:8000/api/v1/ask \
  -H 'Content-Type: application/json' \
  -d '{"query":"What is the recommended first-line treatment for community-acquired pneumonia in an otherwise healthy outpatient?"}'
```

Run tests:

```bash
python -m pytest -q
```

## Agentic roadmap

The next major layer is an evidence-state loop:

```text
decompose -> select tool -> observe -> normalize evidence
        -> update hypotheses -> detect contradictions
        -> replan or stop
```

Later stages add an evidence graph, tool reliability scoring, reflective multimodal agents, synthetic FHIR actions, and clinician-validated trajectory training.

See `docs/architecture.md`, `docs/implementation-plan.md`, and `docs/research.md`.

## Research basis

The architecture maps ideas from DeepER-Med, DeepMed, ClinicalAgents, CAREAgent, DeepRare, MIRA, MedAgentBench, MedBrowseComp, TrialGPT/TrialGPT 2.0 and related medical-agent work.

The project does not persist hidden chain-of-thought. It records operational traces: tool calls, sources, outcomes, evidence identifiers, verification states and workflow transitions.
