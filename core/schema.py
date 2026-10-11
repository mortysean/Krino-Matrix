from typing import Any
from pydantic import BaseModel


class State(BaseModel):
    data: dict[str, Any]


class Action(BaseModel):
    id: str
    description: str


class ActionSpace(BaseModel):
    actions: list[Action]


class Decision(BaseModel):
    action: Action
    score: float