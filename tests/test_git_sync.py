from tilemindfs.git_sync import dual_remote_plan, render_plan


def test_dual_remote_plan_contains_both_remotes():
    plan = dual_remote_plan("https://github.com/ErrorCat04/TileMindFS.git", "https://github.com/Nora33400/TileMindFS.git", "work")
    bash = "\n".join(plan["bash"])
    assert "origin" in bash
    assert "nora" in bash
    assert "git push -u origin work" in bash
    assert "git push -u nora work" in bash


def test_render_plan_includes_shell_sections():
    text = render_plan(
        {
            "bash": ["echo bash"],
            "powershell": ["echo ps"],
        }
    )
    assert "[bash]" in text
    assert "[powershell]" in text
