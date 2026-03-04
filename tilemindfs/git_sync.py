from __future__ import annotations


def dual_remote_plan(errorcat_repo: str, nora_repo: str, branch: str = "work") -> dict[str, list[str]]:
    """Return safe command plans to configure and push to two GitHub remotes."""
    return {
        "bash": [
            f"git remote remove origin 2>/dev/null || true",
            f"git remote add origin {errorcat_repo}",
            f"git remote remove nora 2>/dev/null || true",
            f"git remote add nora {nora_repo}",
            "git fetch origin",
            f"git push -u origin {branch}",
            f"git push -u nora {branch}",
        ],
        "powershell": [
            "git remote remove origin 2>$null",
            f"git remote add origin {errorcat_repo}",
            "git remote remove nora 2>$null",
            f"git remote add nora {nora_repo}",
            "git fetch origin",
            f"git push -u origin {branch}",
            f"git push -u nora {branch}",
        ],
    }


def render_plan(plan: dict[str, list[str]]) -> str:
    lines = ["Dual-remote sync plan", "", "[bash]"]
    lines.extend(plan["bash"])
    lines.append("")
    lines.append("[powershell]")
    lines.extend(plan["powershell"])
    return "\n".join(lines)
