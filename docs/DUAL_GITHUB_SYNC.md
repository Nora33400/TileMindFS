# Dual GitHub Sync (ErrorCat04 + Nora33400)

If you maintain two repos, use:

```bash
python main.py sync-help --branch work
```

It prints safe command sequences for **bash** and **PowerShell**:
- configure `origin` -> ErrorCat04
- configure `nora` -> Nora33400
- push the same branch to both remotes

## Why this exists

- avoid forgetting one account/repo
- keep branch names consistent
- standardize your update routine

## Manual override

You can override URLs:

```bash
python main.py sync-help \
  --branch work \
  --errorcat-repo https://github.com/ErrorCat04/TileMindFS.git \
  --nora-repo https://github.com/Nora33400/TileMindFS.git
```
