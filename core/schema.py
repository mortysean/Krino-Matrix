from typing import Any
from pydantic import BaseModel, Field


class State(BaseModel):
    data: dict[str, Any]


class Problem(BaseModel):
    state: State
    objective: str
    constraints: list[str]


class Action(BaseModel):
    id: str = Field(
        pattern=r"^[a-z][a-z0-9]*(_[a-z0-9]+)*$",
        description=(
            "Short English snake_case verb phrase that names what the action does, "
            "e.g. take_public_transit; never a generic index like action_1"
        ),
    )
    description: str


class ActionSpace(BaseModel):
    actions: list[Action]


class Decision(BaseModel):
    action: Action
    score: float