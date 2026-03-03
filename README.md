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
```

## Developer Onboarding

- Architecture overview: `ARCHITECTURE_GUIDE.md`
- Public core principles: `docs/CORE_PUBLIC.md`
- Task checklist: `TODO_Codex.md`
- Test suite: `pytest`

## Proof

Reconstruction verified via SHA256.
