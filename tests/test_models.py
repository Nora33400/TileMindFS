import pytest

from tilemindfs.config import Weights
from tilemindfs.dispatcher import Dispatcher
from tilemindfs.models import BudgetModel, CoherenceModel, ScoreEngine
from tilemindfs.types import JobInput, ScoredJob


def test_coherence_is_bounded():
    model = CoherenceModel()
    omega = model.coherence([0.5, 0.5], [0.4, 0.6])
    assert 0.0 < omega <= 1.0


def test_coherence_accepts_unnormalized_inputs():
    model = CoherenceModel()
    omega = model.coherence([2.0, 2.0], [4.0, 1.0])
    assert 0.0 < omega <= 1.0


def test_coherence_raises_on_zero_sum_distribution():
    model = CoherenceModel()
    with pytest.raises(ValueError):
        model.coherence([0.0, 0.0], [0.5, 0.5])


def test_budget_never_exceeded():
    dispatcher = Dispatcher(BudgetModel())
    jobs = [
        ScoredJob(
            job=JobInput("a", 1.0, 0.1, 0.1, 0.1, [0.5, 0.5], [0.5, 0.5], 4.0),
            score=2.0,
        ),
        ScoredJob(
            job=JobInput("b", 1.0, 0.1, 0.1, 0.1, [0.5, 0.5], [0.5, 0.5], 7.0),
            score=1.9,
        ),
        ScoredJob(
            job=JobInput("c", 1.0, 0.1, 0.1, 0.1, [0.5, 0.5], [0.5, 0.5], 5.0),
            score=1.8,
        ),
    ]

    selected = dispatcher.select(jobs, limit=10.0, top_k=3)
    total = sum(item.job.resource_estimate for item in selected)
    assert total <= 10.0


def test_budget_slack_is_non_negative():
    model = BudgetModel()
    assert model.slack(current_usage=4.5, limit=10.0) == 5.5
    assert model.slack(current_usage=14.5, limit=10.0) == 0.0


def test_score_is_deterministic():
    engine = ScoreEngine(
        weights=Weights(lambda_=0.4, mu=0.2, rho=0.1, eta=0.3),
        coherence_model=CoherenceModel(),
    )
    job = JobInput(
        job_id="job-1",
        delta_p=5.0,
        delta_e=2.0,
        complexity=1.2,
        risk=0.4,
        p_world=[0.7, 0.3],
        p_model=[0.68, 0.32],
        resource_estimate=2.0,
    )

    s1 = engine.score(job)
    s2 = engine.score(job)
    assert s1 == s2
