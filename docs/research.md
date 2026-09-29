# Medical-agent research map

The goal is to map research to engineering decisions.

| Paper/system | Engineering idea |
|---|---|
| MIRA | FHIR sandbox, large action/tool space, governed clinical workflow |
| DeepRare | central host, specialized agents, heterogeneous sources, self-reflection |
| DeepER-Med | planning, agentic retrieval/appraisal, synthesis |
| DeepMed | multi-hop search and controlled tool-call growth |
| ClinicalAgents | dynamic orchestration, memory and backtracking |
| CAREAgent | verifiable tool-use trajectories and structured outputs |
| MIRA medical image reflection | reflective multimodal tool use |
| Mind the Tool Failures | tool reliability and disagreement-aware selection |
| TrialGPT / TrialGPT 2.0 | criterion-level trial matching |
| MedRAX | specialist medical vision/tool composition |
| MedAgentBench | interactive FHIR-agent evaluation |
| MedBrowseComp | multi-hop medical research evaluation |

## Key conclusions

1. Multi-agent structure is useful only where components have distinct interfaces.
2. The environment/action loop is the major difference from static RAG.
3. Evidence appraisal is separate from retrieval.
4. Tool reliability must be observable.
5. Trial matching should treat UNKNOWN separately from NO.
6. Calculators should be deterministic.

## References

- DeepER-Med: https://arxiv.org/abs/2604.15456
- DeepMed: https://aclanthology.org/2026.findings-acl.904/
- ClinicalAgents: https://arxiv.org/abs/2603.26182
- CAREAgent: https://arxiv.org/abs/2606.01094
- MIRA medical image reflection: https://arxiv.org/abs/2608.10827
- Mind the Tool Failures: https://arxiv.org/abs/2605.26691
- TrialGPT 2.0: https://arxiv.org/abs/2609.01202
- MIRA: https://www.nature.com/articles/s41586-026-10675-5
- DeepRare: https://www.nature.com/articles/s41586-025-10097-9
