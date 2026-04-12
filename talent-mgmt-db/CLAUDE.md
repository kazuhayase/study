# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Talent management database for consolidating HR data scattered across departmental Excel files.

**Data domains:**
- Employee master info
- Skills & certifications
- Performance reviews
- Training history
- Career history (hire, transfer, promotion)
- Goal management (OKR / MBO)

## Stack

| Layer | Technology |
|---|---|
| Local / mock DB | DuckDB |
| Production DB | Snowflake |
| Source data | Excel files (multi-department) |

## Architecture Notes

- DuckDB is used locally to prototype schema and queries before promoting to Snowflake. SQL written for DuckDB should be validated for Snowflake compatibility before promotion.
- Excel ingestion is the primary data source; treat Excel files as immutable raw inputs and load them into a staging layer before transformation.
- Schema changes should be managed via migration scripts (not ad-hoc DDL) so they can be replayed against both DuckDB and Snowflake.

## Skill routing

When the user's request matches an available skill, ALWAYS invoke it using the Skill
tool as your FIRST action. Do NOT answer directly, do NOT use other tools first.
The skill has specialized workflows that produce better results than ad-hoc answers.

Key routing rules:
- Product ideas, "is this worth building", brainstorming → invoke office-hours
- Bugs, errors, "why is this broken", 500 errors → invoke investigate
- Ship, deploy, push, create PR → invoke ship
- QA, test the site, find bugs → invoke qa
- Code review, check my diff → invoke review
- Update docs after shipping → invoke document-release
- Weekly retro → invoke retro
- Design system, brand → invoke design-consultation
- Visual audit, design polish → invoke design-review
- Architecture review → invoke plan-eng-review
- Save progress, checkpoint, resume → invoke checkpoint
- Code quality, health check → invoke health
