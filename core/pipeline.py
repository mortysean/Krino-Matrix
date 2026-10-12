from concurrent.futures import ThreadPoolExecutor

from pydantic import BaseModel

from .schema import Problem, Decision
from .formulator.formulator import Formulator
from .observer.observer import Observer
from .generator.generator import Generator
from .evaluator.evaluator import Evaluator


class PipelineResult(BaseModel):
    problem: Problem
    decisions: list[Decision]   # every candidate action with its score, best first

    @property
    def decision(self) -> Decision:
        return self.decisions[0]


class Pipeline:
    """Natural-language request → Formulator → Observer → Generator → Evaluator → Decision.

    The observer is optional: without one, the state is only what the formulator read from the request.
    """

    def __init__(
        self,
        formulator: Formulator,
        generator: Generator,
        evaluator: Evaluator,
        observer: Observer | None = None,
        max_workers: int = 8
    ):
        self.formulator = formulator
        self.observer = observer
        self.generator = generator
        self.evaluator = evaluator
        self.max_workers = max_workers     # actions are evaluated concurrently

    def run(
        self,
        request: str
    ) -> PipelineResult:
        problem = self.formulator.formulate(request)
        if self.observer:
            problem = problem.model_copy(update={"state": self.observer.observe(problem)})
        space = self.generator.generate(problem.state, problem.objective, problem.constraints)
        if not space.actions:
            raise ValueError("Generator returned no actions")

        with ThreadPoolExecutor(self.max_workers) as pool:
            scores = list(pool.map(
                lambda action: self.evaluator.evaluate(problem.state, problem.objective, action),
                space.actions,
            ))
        decisions = [Decision(action=action, score=score) for action, score in zip(space.actions, scores)]
        decisions.sort(key=lambda d: d.score, reverse=True)
        return PipelineResult(problem=problem, decisions=decisions)
