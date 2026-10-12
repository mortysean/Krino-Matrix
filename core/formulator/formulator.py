from abc import ABC, abstractmethod
from ..schema import Problem


class Formulator(ABC):

    @abstractmethod
    def formulate(
        self,
        request: str
    ) -> Problem:
        pass
