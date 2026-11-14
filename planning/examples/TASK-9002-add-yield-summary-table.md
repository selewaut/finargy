---
id: TASK-9002
type: task
title: Add yield summary table
status: draft
priority: medium
owner: unassigned
created: 2026-11-14
updated: 2026-11-14
epic: EPIC-9001
feature: FEAT-9001
depends_on: [TASK-9001]
verify: "uv run pytest tests/portfolio"
tags: [example]
---

# TASK-9002 — Add yield summary table

## Context

Depends on TASK-9001, which provides the yield function. This task only renders
the result.

## Objective

Produce a summary table (DataFrame or equivalent) from the yield function output.

## Scope

In scope:

- Table builder and tests.

Out of scope:

- Export, charts, CLI integration.

## Acceptance criteria

- [ ] One row per portfolio with start, end, and yield.
- [ ] Empty portfolio returns an empty table.

## Verification

```sh
uv run pytest tests/portfolio
```

## Notes for the agent

- Files likely touched: `src/finargy/portfolio/analysis/`, `tests/portfolio/`.
- Do not reimplement the formula; call TASK-9001's function.

## Log

- `2026-11-14` — created.
