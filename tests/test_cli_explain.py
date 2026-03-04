import subprocess
import sys


def test_cli_explain_all():
    result = subprocess.run(
        [sys.executable, "main.py", "explain", "--level", "all"],
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0
    assert "[simple]" in result.stdout
    assert "[complexe]" in result.stdout


def test_cli_explain_alias_level():
    result = subprocess.run(
        [sys.executable, "main.py", "explain", "--level", "doux"],
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0
    assert "tiles" in result.stdout
