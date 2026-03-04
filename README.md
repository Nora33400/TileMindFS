# TileMindFS (V2)

Minimal reproducible user-space tile storage system plus a modular, resource-aware dry-run planner.

## Features

- SHA256 tile hashing
- Deduplication
- Compression (zlib)
- Reconstruction bit-identical
- Report + Optimizer loop
- Interface-based planner architecture
- Config-driven orchestration weights
- Manual-guided dry-run dispatch CLI

## Installation

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Configuration

All planner coefficients are loaded from `config.yaml`.
No theoretical weights are hardcoded in code.

## Quick Start

### Tile storage

```bash
python main.py store README.md
python main.py reconstruct README.md README_restored.md
python main.py report
```

### Dry-run planning (manual-guided mode)

Create a jobs file:

```json
{
  "jobs": [
    {
      "job_id": "job-a",
      "delta_p": 3.4,
      "delta_e": 0.8,
      "complexity": 0.5,
      "risk": 0.3,
      "p_world": [0.6, 0.4],
      "p_model": [0.55, 0.45],
      "resource_estimate": 2.5
    }
  ]
}
```

Then run:

```bash
python main.py plan --jobs jobs.json --dry-run --output text
python main.py plan --jobs jobs.json --dry-run --output json
python main.py plan --jobs jobs.json --dry-run --output text --save plan.txt
python main.py plan --jobs jobs.json --dry-run --output json --min-score 1.0
```

Notes:
- `jobs` must be a JSON array.
- each `job_id` must be unique in the input file.
- plan output now includes `eligible_count` (jobs remaining after `--min-score`).
- plan output includes `budget_slack` and `budget_utilization` diagnostics.



### Explanation levels

You can print a natural-language explanation of TileMindFS at different detail levels:

```bash
python main.py explain --level simple
python main.py explain --level intermediaire
python main.py explain --level complet
python main.py explain --level complexe
python main.py explain --level all
```

See also: `docs/EXPLICATION_NIVEAUX.md` and `docs/USAGE_STYLES.md`.


### Dual GitHub sync helper

If you publish the same branch to both accounts (`ErrorCat04` and `Nora33400`):

```bash
python main.py sync-help --branch work
```

See: `docs/DUAL_GITHUB_SYNC.md`.

## Developer Onboarding

- Architecture overview: `ARCHITECTURE_GUIDE.md`
- Public core principles: `docs/CORE_PUBLIC.md`
- Task checklist: `TODO_Codex.md`
- Test suite: `pytest`

## Proof

Reconstruction verified via SHA256.
