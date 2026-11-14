---
id: TASK-9001
type: task
title: Add yield formula
status: ready
priority: high
owner: unassigned
created: 2026-11-14
updated: 2026-11-14
epic: EPIC-9001
feature: null
depends_on: []
verify: "uv run pytest tests/portfolio"
tags: [example]
---

# TASK-9001 — Add yield formula

## Context

Portfolio reconstruction already produces holdings over time. Yield should be a
pure function over that data so it is easy to test.

## Objective

Add a tested function that returns yield for a portfolio over a date range.

## Scope

In scope:

- The formula and its unit tests.

Out of scope:

- Rendering, CLI, persistence.

## Acceptance criteria

- [ ] Function returns the expected yield for a fixture.
- [ ] Unit tests cover the zero-holdings case.

## Verification

```sh
uv run pytest tests/portfolio
```

## Notes for the agent

- Files likely touched: `src/finargy/portfolio/analysis/`, `tests/portfolio/`.
- Do not change the reconstruction API.

## Log

- `2026-11-14` — created.
