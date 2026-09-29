from app.tools.base import ClinicalTool, ToolResult
from app.calculators.clinical import CALCULATORS


class CalculatorTool(ClinicalTool):
    name = "clinical_calculator"
    description = "Run deterministic clinical calculators from validated Python functions."

    async def run(self, calculator: str, inputs: dict) -> ToolResult:
        fn = CALCULATORS.get(calculator)
        if fn is None:
            return ToolResult(tool_name=self.name, success=False, data={}, error=f"Unknown calculator: {calculator}")
        try:
            return ToolResult(tool_name=self.name, success=True, data=fn(**inputs))
        except Exception as exc:
            return ToolResult(tool_name=self.name, success=False, data={}, error=str(exc))
