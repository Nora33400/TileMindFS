# TileMindFS – Comment l'utiliser, pour qui, pourquoi (4 styles)

## Style doux

TileMindFS t'aide à garder tes fichiers organisés et économes en espace. Il évite les doublons et peut te proposer un plan d'actions sans rien exécuter automatiquement.

**Pour qui ?**
- Débutants
- Curieux
- Personnes qui veulent un outil sûr (dry-run)

**Pourquoi ?**
- Comprendre avant d'agir
- Réduire les risques
- Travailler calmement et progressivement

---

## Style intermédiaire

TileMindFS combine stockage dédupliqué (hash + compression) et planification sous contraintes. Tu peux lancer `plan --dry-run` pour obtenir une priorisation de jobs sans exécution.

**Pour qui ?**
- Développeurs Python
- Maintainers
- Équipes qui veulent des décisions traçables

**Pourquoi ?**
- Avoir une logique de score explicite
- Utiliser des poids configurables (`config.yaml`)
- Respecter un budget ressource

---

## Style fort

TileMindFS impose une discipline d'orchestration: pas d'exécution non guidée, pas de coefficients hardcodés, et décisions reproductibles. Le pipeline score les actions, filtre par budget, puis produit un plan audit-able.

**Pour qui ?**
- Tech leads
- Architectes
- Projets orientés fiabilité/qualité

**Pourquoi ?**
- Standardiser la prise de décision
- Garder un cadre de sécurité (manual-guided)
- Préparer l'industrialisation du processus

---

## Style complexe

TileMindFS opère comme une couche d'orchestration locale orientée compromis multi-objectif, où la sélection d'actions est contrainte par la cohérence probabiliste et le budget ressource. Le système matérialise une politique explicable, modulaire et substituable via protocoles (modèles de score, cohérence, budget, dispatch).

**Pour qui ?**
- Ingénieurs plateforme
- Chercheurs appliqués
- Concepteurs de systèmes décisionnels contraints

**Pourquoi ?**
- Formaliser le compromis utilité/coût/risque/cohérence
- Conserver traçabilité et testabilité
- Permettre l'évolution des modèles sans casser l'interface CLI
