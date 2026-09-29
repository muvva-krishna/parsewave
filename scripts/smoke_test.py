import asyncio
from app.agents.orchestrator import ClinicalOrchestrator


async def main():
    result = await ClinicalOrchestrator().run(
        "Maximum daily dose of methotrexate for rheumatoid arthritis?",
        patient_context={"age": 54},
    )
    print(result["mode"])
    print(result["card"].model_dump_json(indent=2))
    for event in result["activities"]:
        print("-", event.label, event.detail or "")


if __name__ == "__main__":
    asyncio.run(main())
