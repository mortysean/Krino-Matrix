from abc import ABC, abstractmethod
from .schema import State, Action, Decision


class Evaluator(ABC):

    @abstractmethod
    def evaluate(
        self,
        state: State,
        objective: str,
        action: Action
    ) -> float:
        pass