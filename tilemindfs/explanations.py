from __future__ import annotations

_CANONICAL_LEVELS = ("simple", "intermediaire", "complet", "complexe")
_ALIAS_TO_LEVEL = {
    "doux": "simple",
    "intermediaire": "intermediaire",
    "fort": "complet",
    "complex": "complexe",
    "complexe": "complexe",
    "simple": "simple",
    "complet": "complet",
}

_EXPLANATIONS = {
    "simple": (
        "TileMindFS coupe des données en blocs (tiles), évite les doublons, puis compresse. "
        "Pour la planification, il compare des actions candidates avec une formule de score et ne "
        "fait qu'un plan en mode dry-run (pas d'exécution automatique)."
    ),
    "intermediaire": (
        "TileMindFS combine un stockage local (hash SHA256 + déduplication + compression zlib) et un "
        "orchestrateur de planification. Le score multi-objectif suit L(a)=ΔP−λΔE−μC−ρR+ηΩ, avec "
        "des poids lus depuis config.yaml. Ω est borné dans (0,1] via exp(-KL). Le dispatcher sélectionne "
        "les jobs admissibles sous contrainte de budget ressource, puis retourne un plan lisible/JSON."
    ),
    "complet": (
        "Architecture: interfaces (ScoringModel, CoherenceScorer, BudgetEvaluator, DispatchStrategy), "
        "implémentations concrètes (ScoreEngine, CoherenceModel, BudgetModel, Dispatcher), agrégées par "
        "Planner. Le flux est: charger config -> charger jobs -> scorer -> trier -> filtrer par budget -> "
        "sortie text/json. Les garde-fous imposent mode manuel (--dry-run), resource_limit>0, top_k>0 et "
        "resource_estimate>=0. L'objectif est extensible et déterministe, sans coefficient théorique codé en dur."
    ),
    "complexe": (
        "Le système réalise un compromis local-first entre utilité, coût énergétique, complexité structurelle, "
        "risque et cohérence probabiliste. La cohérence Ω(s)=exp(-KL(p_world||p_model)) agit comme terme de "
        "régularisation borné qui favorise l'alignement modèle/monde sans casser la stabilité numérique. "
        "La décision suit un knapsack glouton trié par score (TopK contraint par Σ r_hat(job_i) ≤ r_t), "
        "fournissant une politique explicable et audit-able. Le design orienté protocoles permet substitution "
        "des modèles (cohérence, budget, dispatch) sans modifier la CLI ni le contrat de planification."
    ),
}


LEVELS = tuple(_ALIAS_TO_LEVEL.keys())


def _normalize_level(level: str) -> str:
    key = level.strip().lower()
    if key not in _ALIAS_TO_LEVEL:
        available = ", ".join(sorted(LEVELS))
        raise ValueError(f"Niveau inconnu: {level}. Niveaux disponibles: {available}")
    return _ALIAS_TO_LEVEL[key]


def explain_level(level: str) -> str:
    """Return natural-language explanation for a given level or alias."""
    normalized = _normalize_level(level)
    return _EXPLANATIONS[normalized]


def explain_all() -> dict[str, str]:
    """Return canonical explanation levels."""
    return {level: _EXPLANATIONS[level] for level in _CANONICAL_LEVELS}
