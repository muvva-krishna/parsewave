# Parsewave Web Deployment

This directory is an isolated deployment surface for the existing Clinical Evidence Agent.

## What it does

- Leaves the existing `backend/`, `frontend/`, tests, and infra files unchanged.
- Exposes the existing orchestrator through a production FastAPI entrypoint.
- Adds CORS for a separately hosted frontend.
- Includes a Dockerfile and Render configuration.
- Uses environment variables for the remote model provider.

## Render

Create a new Web Service from this repository using the included `web/render.yaml` or configure:

- Runtime: Docker
- Dockerfile: `./web/Dockerfile`
- Health check: `/health`

Set the model/provider environment variables required by the existing backend. For a remote OpenAI-compatible model endpoint, configure:

`ORCHESTRATOR_PROVIDER=remote`
`ORCHESTRATOR_MODEL=<fast model name>`
`SYNTHESIS_PROVIDER=remote`
`SYNTHESIS_MODEL=<fast model name>`
`EXTRACTOR_PROVIDER=remote`
`EXTRACTOR_MODEL=<fast model name>`
`VISION_PROVIDER=remote`
`VISION_MODEL=<vision model name>`
`MEDGEMMA_REMOTE_BASE_URL=<provider endpoint>`
`MEDGEMMA_REMOTE_API_KEY=<secret>`

The deployed frontend can call:

`POST /api/ask`

and:

`GET /health`

This repo cannot create the external Render service itself; the Render account must authorize deployment.
