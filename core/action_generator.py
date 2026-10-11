from abc import ABC, abstractmethod
from .schema import State, ActionSpace


class Generator(ABC):

    @abstractmethod
    def generate(
        self,
        state: State,
        objective: str
    ) -> ActionSpace:
        pass