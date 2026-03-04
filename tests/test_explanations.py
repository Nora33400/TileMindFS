import pytest

from tilemindfs.explanations import LEVELS, explain_all, explain_level


def test_explain_all_contains_canonical_levels():
    explanations = explain_all()
    assert set(explanations.keys()) == {"simple", "intermediaire", "complet", "complexe"}


def test_explain_level_aliases_work():
    assert explain_level("doux") == explain_level("simple")
    assert explain_level("fort") == explain_level("complet")
    assert explain_level("complex") == explain_level("complexe")
    assert "doux" in LEVELS


def test_explain_level_rejects_unknown_level():
    with pytest.raises(ValueError):
        explain_level("unknown")
