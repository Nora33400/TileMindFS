# TileMindFS – Public Core Principles

This repository implements a resource-aware orchestration framework.

## Public Theoretical Structure

### Multi-objective decision score

L(a) = ΔP − λΔE − μC − ρR + ηΩ

Where:
- ΔP = performance gain
- ΔE = energy cost
- C = structural complexity
- R = risk estimate
- Ω = bounded coherence score

All coefficients are config-driven.

---

### Coherence metric

Ω(s) = exp(-KL(p_world || p_model))

Ω ∈ (0,1]

---

### Budget-constrained dispatch

TopK(prio_i)
subject to Σ r_hat(job_i) ≤ r_t

---

## Engineering Principles

- Deterministic execution (seeded)
- No hardcoded weights
- Modular components
- CLI first
- Manual-guided mode only
- Structured logging
