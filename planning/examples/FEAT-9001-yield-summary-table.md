---
id: FEAT-9001
type: feature
title: Yield summary table
status: draft
priority: medium
owner: unassigned
created: 2026-11-14
updated: 2026-11-14
spec: SPEC-9001
epics: [EPIC-9001]
tags: [example]
---

# FEAT-9001 — Yield summary table

## User story

As an investor, I want a summary table of portfolio yield so that I can read
performance at a glance.

## Behavior

Renders one row per portfolio with period start, period end, and yield percentage.
Defaults to the current month when no range is given.

## Acceptance criteria

- [ ] Table shows yield for the requested range.
- [ ] Defaults to the current month.

## Edge cases

- Empty portfolio → empty table, not an error.

## Notes

Delivered by EPIC-9001. See SPEC-9001 for goals and metrics.
