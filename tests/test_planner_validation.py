import json
from pathlib import Path

import pytest

from tilemindfs.config import Weights
from tilemindfs.dispatcher import Dispatcher
from tilemindfs.models import BudgetModel, CoherenceModel, ScoreEngine
from tilemindfs.planner import Planner, load_jobs
from tilemindfs.types import JobInput


def _planner() -> Planner:
    return Planner(
        scoring_model=ScoreEngine(
            weights=Weights(lambda_=0.4, mu=0.2, rho=0.1, eta=0.3),
            coherence_model=CoherenceModel(),
        ),
        dispatcher=Dispatcher(BudgetModel()),
    )


def test_plan_rejects_non_positive_limits():
    planner = _planner()
    job = JobInput("j", 1.0, 0.1, 0.1, 0.1, [0.5, 0.5], [0.5, 0.5], 1.0)

    with pytest.raises(ValueError):
        planner.plan([job], resource_limit=0.0, top_k=1)
    with pytest.raises(ValueError):
        planner.plan([job], resource_limit=1.0, top_k=0)


def test_plan_respects_min_score_filter():
    planner = _planner()
    low = JobInput("low", 0.1, 1.0, 1.0, 1.0, [0.5, 0.5], [0.5, 0.5], 1.0)
    high = JobInput("high", 5.0, 0.1, 0.1, 0.1, [0.5, 0.5], [0.5, 0.5], 1.0)

    result = planner.plan([low, high], resource_limit=5.0, top_k=5, min_score=1.0)

    selected_ids = {item.job.job_id for item in result.selected}
    assert selected_ids == {"high"}
    assert result.min_score == 1.0
    assert result.eligible_count == 1
    assert result.budget_slack == 4.0
    assert result.budget_utilization == 0.2


def test_load_jobs_rejects_negative_resource(tmp_path: Path):
    payload = {
        "jobs": [
            {
                "job_id": "bad",
                "delta_p": 1,
                "delta_e": 1,
                "complexity": 1,
                "risk": 1,
                "p_world": [0.5, 0.5],
                "p_model": [0.5, 0.5],
                "resource_estimate": -1,
            }
        ]
    }
    fp = tmp_path / "jobs.json"
    fp.write_text(json.dumps(payload), encoding="utf-8")

    with pytest.raises(ValueError):
        load_jobs(fp)


def test_load_jobs_rejects_duplicate_job_ids(tmp_path: Path):
    payload = {
        "jobs": [
            {
                "job_id": "dup",
                "delta_p": 1,
                "delta_e": 1,
                "complexity": 1,
                "risk": 1,
                "p_world": [0.5, 0.5],
                "p_model": [0.5, 0.5],
                "resource_estimate": 1,
            },
            {
                "job_id": "dup",
                "delta_p": 2,
                "delta_e": 1,
                "complexity": 1,
                "risk": 1,
                "p_world": [0.5, 0.5],
                "p_model": [0.5, 0.5],
                "resource_estimate": 1,
            },
        ]
    }
    fp = tmp_path / "jobs_dup.json"
    fp.write_text(json.dumps(payload), encoding="utf-8")

    with pytest.raises(ValueError):
        load_jobs(fp)


def test_load_jobs_rejects_non_list_jobs_payload(tmp_path: Path):
    fp = tmp_path / "jobs_badshape.json"
    fp.write_text(json.dumps({"jobs": {"oops": 1}}), encoding="utf-8")

    with pytest.raises(ValueError):
        load_jobs(fp)
