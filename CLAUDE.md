# CLAUDE.md

This file provides guidance to Claude Code when working in this repository.

## Repository Overview

Personal study repository by Kazuyoshi Hayase (kazuhayase).  
Contains multiple independent sub-projects for LLM/AI experiments, ML seminars, and data engineering.

| Directory | Purpose |
|---|---|
| `LLM/FDUA2025` | RAG app for FDUA 2025 competition. Uses Hitachi Llama/Qwen APIs via `read_conf.py` |
| `LLM/DA-Elyza2024` | DA Elyza 2024 project. Python (LangChain + FastAPI) + JavaScript |
| `LLM/act-MLS2024` | MLS 2024 LLM app. Same stack as DA-Elyza2024 |
| `LLM/model-compare` | Scripts for comparing open LLMs via Ollama on Mac |
| `mls-seminar` | Jupyter-based ML/statistics environment. Pin-versioned `requirements.txt` |
| `talent-mgmt-db` | HR data consolidation DB using DuckDB (local) + Snowflake (prod) |
| `prompts/` | Prompt library with templates |

## Language

- Respond to the user in **Japanese**
- Code, commit messages, and inline comments in **English**

## Memory — Automatic Update Rules

Memory path varies by machine:
- **Debian**: `/home/kazu/.claude/projects/-home-kazu-git-study/memory/`
- **Mac**: `/Users/kazu/.claude/projects/-Users-kazu-github-study/memory/`

**Always update memory at the end of the conversation**, especially when:
- Significant work was completed (fixes, new features, setup)
- The user says "まとめて", "おわり", "終わり", "ここまで", or "メモリ"
- New patterns, preferences, or project context are revealed

Update the relevant `.md` file(s) and keep `MEMORY.md` in sync.  
Do NOT ask the user for permission — just do it as part of wrapping up.

## Security Workflow

**Run without asking for user confirmation. Commit and push automatically after fixing.**

### Scope
Scan the **entire repository** — all subdirectories recursively. Find dependency files and source code regardless of directory name casing.

### Step 1 — Python dependency scan (OSV API)

**Do NOT use `pip-audit`** — it fails on this Mac (Python 3.14 cannot build fugashi/scikit-learn from source).  
Instead, query the OSV API directly for every pinned package in each `requirements.txt`:

```python
import urllib.request, json

packages = [("pkg-name", "x.y.z"), ...]  # parse from requirements.txt

for pkg, ver in packages:
    data = json.dumps({"version": ver, "package": {"name": pkg, "ecosystem": "PyPI"}}).encode()
    req = urllib.request.Request("https://api.osv.dev/v1/query", data=data,
                                  headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=10) as r:
        result = json.loads(r.read())
    if result.get("vulns"):
        print(f"VULN: {pkg}=={ver}")
```

### Step 2 — JavaScript dependency scan (OSV API)

`gh` CLI is NOT installed on this Mac. Use the same OSV API with `"ecosystem": "npm"` for each package in `package.json` files (strip `^~` from version strings).

### Step 3 — Static code analysis

Search all Python files for:
```bash
grep -rn "os\.system(\|subprocess.*shell=True\|eval(\|exec(" --include="*.py" <dir>
grep -rn "api_key\s*=\s*['\"][^'\"]\|secret\s*=\s*['\"][^'\"]" --include="*.py" <dir>
```

Search R files for hardcoded absolute paths:
```bash
grep -rn "setwd\|/home/\|/Users/" --include="*.R" <dir>
```

### Step 4 — Fix

| Issue | Fix |
|---|---|
| Vulnerable Python package (fix available) | Update version in `requirements.txt` |
| Vulnerable Python package (no fix yet) | Add `# SECURITY: CVE-XXXX (SEVERITY) - <summary>. No fix as of <date>.` comment above the line |
| Vulnerable npm package | Update version in `package.json` |
| `os.system(f"...{var}...")` | Replace with `subprocess.run([sys.executable, ...], stdout=f, check=True)` |
| Hardcoded absolute path with username | Comment out the line |
| Hardcoded secret | Move to environment variable |

### Step 5 — Verify & push

Re-run the OSV checks on updated packages to confirm clean.  
Then commit with `fix(security): ...` and push — **no user confirmation needed**.

### Known limitations (as of 2026-05-30)
- `chromadb==1.5.9`: CVE-2026-45829 (CRITICAL) has no fix on PyPI yet. Keep the comment; re-check on each scan run.
- `pip-audit` fails on this Mac → always use OSV API instead.
- `gh` CLI not installed → always use OSV API or `curl` for GitHub API.

## Commit & Push Convention

- Commit message format: `fix(scope): description` / `feat(scope): description`
- Always include `Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>`
- After completing a fix, commit **and** push immediately — **no need to ask the user**
