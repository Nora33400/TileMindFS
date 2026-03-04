from __future__ import annotations

from typing import Protocol, Sequence

from .types import JobInput, ScoredJob


class ScoringModel(Protocol):
    """Computes a deterministic score for one job."""

    def score(self, job: JobInput) -> float:
        ...


class CoherenceScorer(Protocol):
    """Computes bounded coherence Ω in (0, 1]."""

    def coherence(self, p_world: Sequence[float], p_model: Sequence[float]) -> float:
        ...


class BudgetEvaluator(Protocol):
    """Checks if a job can be accepted with current budget usage."""

    def admissible(self, current_usage: float, required: float, limit: float) -> bool:
        ...


class DispatchStrategy(Protocol):
    """Selects top admissible jobs for a fixed budget."""

    def select(self, scored_jobs: Sequence[ScoredJob], limit: float, top_k: int) -> list[ScoredJob]:
        ...
