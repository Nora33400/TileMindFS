import subprocess
import sys


def test_cli_sync_help_prints_dual_plan():
    result = subprocess.run(
        [sys.executable, "main.py", "sync-help", "--branch", "work"],
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0
    assert "Dual-remote sync plan" in result.stdout
    assert "git push -u origin work" in result.stdout
    assert "git push -u nora work" in result.stdout
