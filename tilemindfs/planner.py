from __future__ import annotations

import json
from pathlib import Path

from .interfaces import DispatchStrategy, ScoringModel
from .types import JobInput, PlanResult, ScoredJob


class Planner:
    """Manual-guided dry-run planning only; never executes jobs."""

    def __init__(self, scoring_model: ScoringModel, dispatcher: DispatchStrategy):
        self._scoring_model = scoring_model
        self._dispatcher = dispatcher

    def plan(
        self,
        jobs: list[JobInput],
        resource_limit: float,
        top_k: int,
        min_score: float | None = None,
    ) -> PlanResult:
        if resource_limit <= 0:
            raise ValueError("resource_limit must be > 0")
        if top_k <= 0:
            raise ValueError("top_k must be > 0")

        scored = [ScoredJob(job=job, score=self._scoring_model.score(job)) for job in jobs]

        eligible = scored
        if min_score is not None:
            eligible = [item for item in scored if item.score >= min_score]

        eligible_count = len(eligible)
        selected = self._dispatcher.select(eligible, resource_limit, top_k)
        selected_ids = {item.job.job_id for item in selected}
        skipped = [item for item in scored if item.job.job_id not in selected_ids]
        total_resource = sum(item.job.resource_estimate for item in selected)
        budget_slack = max(0.0, resource_limit - total_resource)
        budget_utilization = total_resource / resource_limit
        return PlanResult(
            selected=selected,
            skipped=skipped,
            total_resource=total_resource,
            resource_limit=resource_limit,
            min_score=min_score,
            eligible_count=eligible_count,
            budget_slack=budget_slack,
            budget_utilization=budget_utilization,
        )


def load_jobs(path: str | Path) -> list[JobInput]:
    with Path(path).open("r", encoding="utf-8") as fh:
        payload = json.load(fh)

    jobs_payload = payload.get("jobs", [])
    if not isinstance(jobs_payload, list):
        raise ValueError("jobs must be a list")

    jobs: list[JobInput] = []
    seen_ids: set[str] = set()
    for item in jobs_payload:
        job_id = str(item["job_id"])
        if job_id in seen_ids:
            raise ValueError(f"duplicate job_id found: {job_id}")
        seen_ids.add(job_id)

        resource_estimate = float(item["resource_estimate"])
        if resource_estimate < 0:
            raise ValueError(f"resource_estimate must be >= 0 for job {job_id}")

        jobs.append(
            JobInput(
                job_id=job_id,
                delta_p=float(item["delta_p"]),
                delta_e=float(item["delta_e"]),
                complexity=float(item["complexity"]),
                risk=float(item["risk"]),
                p_world=list(item["p_world"]),
                p_model=list(item["p_model"]),
                resource_estimate=resource_estimate,
            )
        )
    return jobs


def plan_to_json(result: PlanResult) -> str:
    serializable = {
        "resource_limit": result.resource_limit,
        "min_score": result.min_score,
        "eligible_count": result.eligible_count,
        "budget_slack": result.budget_slack,
        "budget_utilization": result.budget_utilization,
        "total_resource": result.total_resource,
        "selected": [
            {
                "job_id": item.job.job_id,
                "score": item.score,
                "resource_estimate": item.job.resource_estimate,
            }
            for item in result.selected
        ],
        "skipped": [
            {
                "job_id": item.job.job_id,
                "score": item.score,
                "resource_estimate": item.job.resource_estimate,
            }
            for item in result.skipped
        ],
    }
    return json.dumps(serializable, indent=2)


def plan_to_text(result: PlanResult) -> str:
    lines = [
        "Dry-run plan (manual-guided mode)",
        f"Resource: {result.total_resource:.3f}/{result.resource_limit:.3f}",
        f"Budget slack: {result.budget_slack:.3f}",
        f"Budget utilization: {result.budget_utilization:.3f}",
    ]
    if result.min_score is not None:
        lines.append(f"Min score filter: {result.min_score:.5f}")
    lines.append(f"Eligible after filter: {result.eligible_count}")

    lines.append("Selected:")
    if not result.selected:
        lines.append("  - none")
    for item in result.selected:
        lines.append(f"  - {item.job.job_id}: score={item.score:.5f}, r={item.job.resource_estimate:.3f}")

    lines.append("Skipped:")
    if not result.skipped:
        lines.append("  - none")
    for item in result.skipped:
        lines.append(f"  - {item.job.job_id}: score={item.score:.5f}, r={item.job.resource_estimate:.3f}")

    return "\n".join(lines)
