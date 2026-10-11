import json

from services.llm import LLM
from ...schema import State, ActionSpace
from ..generator import Generator


# Kept in the user turn rather than the system prompt: some gateways replace the system prompt
PROMPT = """You are the action generator of a decision system. Given the current state, the objective and \
the constraints, propose {count} feasible actions that could move the state toward the objective.

Requirements:
- Each action must be concrete and executable from the current state.
- Each action must respect all constraints.
- Actions must be clearly distinct, covering different strategies rather than variations of one.
- Do not rank or score the actions; they are evaluated separately.
- id: a short English snake_case verb phrase naming the action, unique within the set.
- description: one or two sentences, in the same language as the objective.

State:
{state}

Objective:
{objective}

Constraints:
{constraints}"""


class APIGenerator(Generator):
    """Generates actions by calling a hosted LLM through services.llm."""

    def __init__(
        self,
        llm: LLM | None = None,
        num_actions: int | None = None
    ):
        self.llm = llm or LLM()
        self.num_actions = num_actions

    def generate(
        self,
        state: State,
        objective: str,
        constraints: list[str]
    ) -> ActionSpace:
        prompt = PROMPT.format(
            count=self.num_actions or "3 to 5",
            state=json.dumps(state.data, ensure_ascii=False, indent=2),
            objective=objective,
            constraints="\n".join(f"- {c}" for c in constraints) or "None",
        )
        return self.llm.structured(prompt, ActionSpace)
