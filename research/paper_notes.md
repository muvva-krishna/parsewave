# Design notes

## Vera
Vera's product model is evidence-first clinical decision support: retrieve sources, rank evidence, then generate concise typed outputs.

## DeepER-Med
Map the agent stages to question decomposition, search planning, evidence retrieval, evidence appraisal and synthesis.

## DeepRare
Borrow a central orchestrator plus specialized agents/tools over heterogeneous medical resources.

## MIRA
Borrow the environment/action loop, but keep actions read-only in the MVP. A future sandbox can expose synthetic FHIR resources and controlled tool actions.

## DeepMed / ClinicalAgents
Borrow controlled planning rather than unbounded tool loops. Stop when evidence is sufficient, verification passes, or a critical unknown is detected.

## CAREAgent
Treat structured outputs and tool calls as first-class data. Later training data should consist of validated trajectories rather than only question-answer pairs.
