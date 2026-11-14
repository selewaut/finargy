---
id: SPEC-9001
type: product-spec
title: Portfolio yield report
status: ready
priority: high
owner: unassigned
created: 2026-11-14
updated: 2026-11-14
epics: [EPIC-9001]
tags: [example]
---

# SPEC-9001 — Portfolio yield report

## Problem

Computing realized yield across a portfolio requires manual spreadsheet work,
which is slow and error-prone. Users cannot quickly answer "how did my portfolio
perform this period?".

## Goals

- [x] Compute portfolio yield from transaction history.
- [ ] Surface the result as a readable summary table.

## Non-goals

- Tax reporting.
- Multi-currency normalization beyond MEP where already supported.

## Users and use cases

| User     | Use case                          | Value                       |
| -------- | --------------------------------- | --------------------------- |
| Investor | Check period performance          | Fast, trustworthy answer    |
| Analyst  | Compare yields across portfolios  | Consistent calculation      |

## Requirements

### Must

- Yield is derived from existing portfolio reconstruction data.
- Results are reproducible for a given date range.

### Should

- Summary table is exportable.

### Won't (this time)

- Interactive charts.

## Success metrics

| Metric        | Target        | How measured        |
| ------------- | ------------- | ------------------- |
| Yield matches | 100% of sample | Spot-check fixtures |

## Constraints and design notes

- Reuse `src/finargy/portfolio/analysis/`.

## Open questions

- [ ] Which day-count convention should yield use?

## Epic breakdown

| Epic      | Title             | Status |
| --------- | ----------------- | ------ |
| EPIC-9001 | Yield calculation | ready  |
