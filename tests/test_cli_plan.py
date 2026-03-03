import json
import subprocess
import sys
from pathlib import Path


def test_plan_requires_dry_run(tmp_path: Path):
    jobs = {
        "jobs": [
            {
                "job_id": "job-a",
                "delta_p": 2.0,
                "delta_e": 0.4,
                "complexity": 0.2,
                "risk": 0.1,
                "p_world": [0.5, 0.5],
                "p_model": [0.5, 0.5],
                "resource_estimate": 1.0,
            }
        ]
    }
    jobs_file = tmp_path / "jobs.json"
    jobs_file.write_text(json.dumps(jobs), encoding="utf-8")

    result = subprocess.run(
        [sys.executable, "main.py", "plan", "--jobs", str(jobs_file)],
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode != 0
    assert "Manual-guided mode only" in result.stderr
