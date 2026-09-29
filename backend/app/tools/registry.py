from app.tools.base import ClinicalTool
from app.tools.pubmed import PubMedTool
from app.tools.clinical_trials import ClinicalTrialsTool
from app.tools.openfda import OpenFDADrugLabelTool
from app.tools.rxnorm import RxNormTool


def build_registry() -> dict[str, ClinicalTool]:
    tools = [PubMedTool(), ClinicalTrialsTool(), OpenFDADrugLabelTool(), RxNormTool()]
    return {tool.name: tool for tool in tools}
