# Architecture

## Principle

UI modes are workflow contracts. Agents are reusable capabilities shared across workflows.

## Runtime

User request
-> intent and clinical context
-> premise/safety gate
-> adaptive planner
-> clinical tools and evidence retrieval
-> evidence appraisal
-> clinical synthesis
-> claim verification
-> typed response card
-> frontend renderer

## State

The explicit state contains query, patient context, known/unknown facts, workflow mode, plan, tool observations, evidence, hypotheses, claims, contradictions, verification status and response payload.

Do not persist hidden chain-of-thought. Persist operational traces such as tool calls, sources, outcomes, evidence identifiers and high-level state transitions.

## Model routing

- Orchestrator: a reliable tool-calling model such as Qwen3.
- Clinical synthesis: MedGemma 27B after evidence retrieval.
- Clinical extraction: MedGemma 1.5 4B.
- Vision: MedGemma multimodal where supported.
- Provider adapters allow local Ollama or a hosted OpenAI-compatible endpoint.

## Tool reliability

Every tool should eventually implement:

request -> execute -> validate schema -> validate freshness -> detect disagreement -> retry/fallback -> record outcome.
