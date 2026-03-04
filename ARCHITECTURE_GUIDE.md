# TileMindFS Architecture Guide

## Core Modules

- ScoreEngine
- CoherenceModel
- BudgetModel
- Dispatcher
- Planner
- CLI

---

## ScoreEngine

Responsible for computing:

score = ΔP - λΔE - μC - ρR + ηΩ

All sub-terms are injected via interfaces.

---

## CoherenceModel

Computes bounded coherence:
Ω(s) ∈ (0,1]

Must never return NaN.

---

## BudgetModel

Computes:
- resource slack
- admissibility

---

## Dispatcher

Selects top admissible tasks under resource constraints.

---

## Planner (Manual-Guided Mode)

Produces:
- Human-readable action plan
- JSON plan output
- No execution
