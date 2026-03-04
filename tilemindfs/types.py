from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class JobInput:
    """Input metrics for one candidate action."""

    job_id: str
    delta_p: float
    delta_e: float
    complexity: float
    risk: float
    p_world: list[float]
    p_model: list[float]
    resource_estimate: float


@dataclass(frozen=True)
class ScoredJob:
    """Score enriched job used by dispatcher."""

    job: JobInput
    score: float


@dataclass(frozen=True)
class PlanResult:
    """Dry-run plan result."""

    selected: list[ScoredJob]
    skipped: list[ScoredJob]
    total_resource: float
    resource_limit: float
    min_score: float | None = None
    eligible_count: int = 0
    budget_slack: float = 0.0
    budget_utilization: float = 0.0
