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

Memory is stored at: `/home/kazu/.claude/projects/-home-kazu-git-study/memory/`

**Always update memory at the end of the conversation**, especially when:
- Significant work was completed (fixes, new features, setup)
- The user says "まとめて", "おわり", "終わり", "ここまで", or "メモリ"
- New patterns, preferences, or project context are revealed

Update the relevant `.md` file(s) and keep `MEMORY.md` in sync.  
Do NOT ask the user for permission — just do it as part of wrapping up.

## Security Workflow

Run both of the following when the user asks for a security/vulnerability check:

1. `pip-audit -r <path>/requirements.txt` — scan each `requirements.txt`
2. `gh api repos/kazuhayase/study/dependabot/alerts --jq '...'` — check open Dependabot alerts

After fixing, commit and push. Confirm with the user before pushing if unsure.

## Commit & Push Convention

- Commit message format: `fix(scope): description` / `feat(scope): description`
- Always include `Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>`
- After completing a fix, proactively offer to commit **and** push together (user expects both)
