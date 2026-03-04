from __future__ import annotations

import math
from typing import Sequence

from .config import Weights
from .interfaces import BudgetEvaluator, CoherenceScorer, ScoringModel
from .types import JobInput


class CoherenceModel(CoherenceScorer):
    """Bounded coherence Ω(s) = exp(-KL(p_world || p_model))."""

    def coherence(self, p_world: Sequence[float], p_model: Sequence[float]) -> float:
        if len(p_world) != len(p_model) or not p_world:
            raise ValueError("p_world and p_model must have same non-zero length")

        epsilon = 1e-12
        if any(p < 0 for p in p_world) or any(p < 0 for p in p_model):
            raise ValueError("Probabilities must be non-negative")

        world_sum = sum(p_world)
        model_sum = sum(p_model)
        if world_sum <= 0 or model_sum <= 0:
            raise ValueError("Probability vectors must have a positive sum")

        kl_div = 0.0
        for p_w, p_m in zip(p_world, p_model):
            p_w_s = max(p_w / world_sum, epsilon)
            p_m_s = max(p_m / model_sum, epsilon)
            kl_div += p_w_s * math.log(p_w_s / p_m_s)

        omega = math.exp(-kl_div)
        if math.isnan(omega):
            return epsilon
        return min(1.0, max(epsilon, omega))


class ScoreEngine(ScoringModel):
    """Computes L(a) = ΔP − λΔE − μC − ρR + ηΩ."""

    def __init__(self, weights: Weights, coherence_model: CoherenceScorer):
        self._weights = weights
        self._coherence = coherence_model

    def score(self, job: JobInput) -> float:
        omega = self._coherence.coherence(job.p_world, job.p_model)
        return (
            job.delta_p
            - self._weights.lambda_ * job.delta_e
            - self._weights.mu * job.complexity
            - self._weights.rho * job.risk
            + self._weights.eta * omega
        )


class BudgetModel(BudgetEvaluator):
    """Resource admissibility checks and slack computation."""

    def admissible(self, current_usage: float, required: float, limit: float) -> bool:
        return current_usage + required <= limit

    def slack(self, current_usage: float, limit: float) -> float:
        return max(0.0, limit - current_usage)
