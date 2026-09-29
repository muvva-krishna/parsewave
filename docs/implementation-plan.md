# Implementation plan

## Phase 0 — foundation

- typed workflow contracts
- separate model adapters
- external clinical-source tools
- deterministic calculators
- bounded orchestration state
- premise/safety layer
- claim verification hook
- thin frontend

## Phase 1 — adaptive agent loop

Use a bounded loop:

decompose question -> select tool -> observe -> normalize evidence -> update state -> contradiction check -> replan/stop.

Persist action, tool, source, success, latency and observation metadata, not hidden reasoning.

## Phase 2 — evidence graph

Represent:

question -> subquestion -> source -> claim -> contradiction

and patient fact -> eligibility criterion.

This supports claim-level citations, trial matching and conflicting evidence.

## Phase 3 — workflow expansion

Implement DDx, Tx Plan, Guidelines, Patient Handout, SOAP Note, Quick Curbside and Deep Research as policies over shared capabilities.

## Phase 4 — multimodal agent

Add MedGemma multimodal and MedSigLIP-backed tools, with reflective decisions about whether additional visual/tool evidence is useful.

## Phase 5 — FHIR sandbox

Add synthetic FHIR resources and benchmark interactive workflows. Keep all write actions sandboxed and explicitly permissioned.

## Phase 6 — trajectory training

Capture clinician-validated trajectories, filter for tool validity and schema compliance, then experiment with SFT and RL.
