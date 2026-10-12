from abc import ABC, abstractmethod
from ..schema import State, Problem


class Observer(ABC):

    @abstractmethod
    def observe(
        self,
        problem: Problem
    ) -> State:
        pass
