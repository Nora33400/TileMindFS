from __future__ import annotations

from .interfaces import BudgetEvaluator, DispatchStrategy
from .types import ScoredJob


class Dispatcher(DispatchStrategy):
    """Top-K selection under budget constraints."""

    def __init__(self, budget_model: BudgetEvaluator):
        self._budget_model = budget_model

    def select(self, scored_jobs: list[ScoredJob], limit: float, top_k: int) -> list[ScoredJob]:
        ordered = sorted(scored_jobs, key=lambda it: (-it.score, it.job.job_id))
        selected: list[ScoredJob] = []
        current_usage = 0.0

        for candidate in ordered:
            if len(selected) >= top_k:
                break
            required = candidate.job.resource_estimate
            if self._budget_model.admissible(current_usage, required, limit):
                selected.append(candidate)
                current_usage += required

        return selected
