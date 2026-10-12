from pydantic import BaseModel, Field

from services.llm import LLM
from ...schema import State, Problem
from ..formulator import Formulator


# Kept in the user turn rather than the system prompt: some gateways replace the system prompt
PROMPT = """You are the problem formulator of a decision system. Turn the user's request below into \
a decision problem: the current state, the objective and the constraints.

Requirements:
- state: facts about the current situation that matter for the decision, one per entry.
  - Only facts stated or directly implied by the request; never invent missing ones.
  - Only what is true now: targets, deadlines, budgets and preferences belong in the objective \
or constraints, not in the state.
  - key: English snake_case, with the unit in the key when there is one, e.g. distance_to_office_km.
  - value: a number or boolean when the fact is numeric or yes/no, otherwise a short string \
in the same language as the request.
- objective: the single end result the user wants, as specific as the request allows \
(include deadlines or targets the user gave), in the same language as the request.
- constraints: limits or preferences on how the objective may be reached, one per entry, \
in the same language as the request. Do not repeat the objective. Empty if there are none.
- Do not propose or recommend actions; they are generated separately.

Request:
{request}"""


class Fact(BaseModel):
    key: str = Field(pattern=r"^[a-z][a-z0-9]*(_[a-z0-9]+)*$")
    value: bool | int | float | str


# What the LLM returns: facts as a list, since free-form objects are rejected by some structured output APIs
class Formulation(BaseModel):
    state: list[Fact]
    objective: str
    constraints: list[str]


class APIFormulator(Formulator):
    """Formulates problems by calling a hosted LLM through services.llm."""

    def __init__(
        self,
        llm: LLM | None = None
    ):
        self.llm = llm or LLM()

    def formulate(
        self,
        request: str
    ) -> Problem:
        formulation = self.llm.structured(PROMPT.format(request=request), Formulation)
        return Problem(
            state=State(data={fact.key: fact.value for fact in formulation.state}),
            objective=formulation.objective,
            constraints=formulation.constraints,
        )
