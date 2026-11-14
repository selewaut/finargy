---
id: EPIC-9001
type: epic
title: Yield calculation
status: ready
priority: high
owner: unassigned
created: 2026-11-14
updated: 2026-11-14
spec: SPEC-9001
features: [FEAT-9001]
tasks: [TASK-9001, TASK-9002]
tags: [example]
---

# EPIC-9001 — Yield calculation

## Summary

Compute portfolio yield from reconstructed holdings and expose it as a summary
table. This is the smallest slice of SPEC-9001 that gives a usable answer.

## Why now

It unblocks any reporting or alerting work built on top of yield.

## Scope

In scope:

- A pure yield function with tests.
- A summary table built from the function.

Out of scope:

- Charts, exports, scheduling.

## Acceptance criteria

- [ ] Yield can be computed for a date range.
- [ ] A summary table is available for a portfolio.

## Tasks

| Task      | Title                    | Status | Owner |
| --------- | ------------------------ | ------ | ----- |
| TASK-9001 | Add yield formula        | ready  | —     |
| TASK-9002 | Add yield summary table  | draft  | —     |

## Risks and open questions

- Day-count convention undecided; recorded as an open question on the spec.
