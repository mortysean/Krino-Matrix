"""Try the API generator:

    python examples/api_generator_demo.py
"""
import sys
from pathlib import Path

# Make the project root importable when this file is run as a script
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from core.schema import State
from core.generator.api_generator import APIGenerator
from services.llm import LLM

# Edit these to try your own scenario
MODEL = None            # None: LLM_DEFAULT in .env; or e.g. "anthropic/claude-opus-5.5"
NUM_ACTIONS = None      # None: 3 to 5 actions
STATE = State(data={
    "weather": "heavy rain",
    "distance_to_office_km": 5,
    "time": "08:10",
    "work_starts": "20:00",
    "has_car": False,
    "has_ebike": True,
})
OBJECTIVE = "14:00 前到达公司"
CONSTRAINTS = [
    "尽量不淋湿",
    "通勤花费不超过 50 元",
]


if __name__ == "__main__":
    llm = LLM(MODEL)
    generator = APIGenerator(llm, num_actions=NUM_ACTIONS)
    print(f"Model: {llm.model} (via {llm.provider.name})\n")

    space = generator.generate(STATE, OBJECTIVE, CONSTRAINTS)
    for i, action in enumerate(space.actions, 1):
        print(f"{i}. {action.id}\n   {action.description}\n")
