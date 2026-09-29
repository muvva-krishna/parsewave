# Safety boundary

This project is an engineering/research MVP, not a medical device.

## Development boundary

- Use synthetic or de-identified data.
- Do not store PHI in local logs.
- Do not allow autonomous prescribing or order placement.
- Do not infer missing patient facts.
- Treat UNKNOWN as a real state for eligibility criteria.
- Run deterministic calculations in code.
- Keep source URLs and retrieval timestamps.
- Require claim-to-source verification before a result is presented as evidence-backed.

## Product boundary for MVP

Allowed:
- literature search
- guideline retrieval from permissible/public sources
- drug label lookup
- clinical trial candidate retrieval
- deterministic calculators
- clinician-facing drafts
- patient-facing drafts reviewed by a clinician

Not included:
- autonomous treatment orders
- medication changes
- final diagnosis
- emergency triage automation
- production EHR write access
