import json
import subprocess
import sys
from pathlib import Path


def test_cli_plan_save_writes_file(tmp_path: Path):
    out_file = tmp_path / "plan.txt"
    result = subprocess.run(
        [
            sys.executable,
            "main.py",
            "plan",
            "--jobs",
            "examples/jobs.sample.json",
            "--dry-run",
            "--output",
            "text",
            "--save",
            str(out_file),
        ],
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0
    assert out_file.exists()
    text = out_file.read_text(encoding="utf-8")
    assert "Dry-run plan (manual-guided mode)" in text
    assert "Budget utilization:" in text


def test_cli_plan_min_score_filter_changes_selection(tmp_path: Path):
    jobs = {
        "jobs": [
            {
                "job_id": "low",
                "delta_p": 0.1,
                "delta_e": 1.0,
                "complexity": 1.0,
                "risk": 1.0,
                "p_world": [0.5, 0.5],
                "p_model": [0.5, 0.5],
                "resource_estimate": 1.0,
            },
            {
                "job_id": "high",
                "delta_p": 5.0,
                "delta_e": 0.1,
                "complexity": 0.1,
                "risk": 0.1,
                "p_world": [0.5, 0.5],
                "p_model": [0.5, 0.5],
                "resource_estimate": 1.0,
            },
        ]
    }
    jobs_path = tmp_path / "jobs.json"
    jobs_path.write_text(json.dumps(jobs), encoding="utf-8")

    result = subprocess.run(
        [
            sys.executable,
            "main.py",
            "plan",
            "--jobs",
            str(jobs_path),
            "--dry-run",
            "--output",
            "json",
            "--min-score",
            "1.0",
        ],
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0
    assert '"min_score": 1.0' in result.stdout
    assert '"eligible_count": 1' in result.stdout
    assert '"budget_slack": 9.0' in result.stdout
    assert '"budget_utilization": 0.1' in result.stdout
    assert '"job_id": "high"' in result.stdout
    assert '"job_id": "low"' in result.stdout  # appears in skipped
