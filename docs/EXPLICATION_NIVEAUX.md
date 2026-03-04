# TileMindFS – Explication par niveaux

## Niveau simple

TileMindFS est un système qui stocke des fichiers de manière plus intelligente:
- il découpe les données,
- évite de stocker deux fois la même chose,
- compresse pour économiser de l'espace.

Ensuite, il peut proposer un plan d'actions (dry-run) sans exécuter automatiquement.

---

## Niveau intermédiaire

TileMindFS combine deux parties:
1. **Stockage local-first** (hash, déduplication, compression, reconstruction).
2. **Planification orchestrée** basée sur un score multi-objectif:

`L(a) = ΔP − λΔE − μC − ρR + ηΩ`

Les coefficients (`λ, μ, ρ, η`) viennent du fichier de configuration.

La cohérence est bornée avec:

`Ω(s) = exp(-KL(p_world || p_model))`, donc `Ω ∈ (0,1]`.

Le système choisit ensuite des tâches admissibles sans dépasser un budget ressource.

---

## Niveau complet

### Pipeline

1. Charger `config.yaml`.
2. Charger les jobs candidats (JSON).
3. Calculer `Ω` avec le modèle de cohérence.
4. Calculer le score `L(a)` pour chaque job.
5. Trier les jobs par score.
6. Sélectionner les jobs admissibles sous budget (TopK + contrainte ressource).
7. Produire un plan texte ou JSON.

### Garanties d'ingénierie

- Pas de coefficients hardcodés dans la logique de scoring.
- Mode manuel guidé: `--dry-run` obligatoire.
- Validations: budget > 0, top-k > 0, resource_estimate >= 0.
- Architecture modulaire via interfaces/protocoles.

---

## Niveau complexe

TileMindFS met en place une **politique de décision contrainte** où la valeur d'une action n'est pas seulement son gain brut (`ΔP`) mais un compromis explicite entre gain, coût énergétique, complexité, risque et cohérence probabiliste.

Le terme de cohérence `Ω` agit comme une régularisation bornée et stabilisée numériquement, favorisant les décisions alignées avec la distribution observée du monde.

La sélection finale se comporte comme un knapsack glouton sous contraintes:
- maximiser la priorité par score,
- respecter `Σ r_hat(job_i) ≤ r_t`,
- limiter au `TopK`.

Cette approche rend la décision:
- **audit-able** (on sait pourquoi un job est sélectionné),
- **extensible** (on remplace des modèles via interfaces),
- **sûre** (dry-run et validations),
- **reproductible** (config centralisée).
