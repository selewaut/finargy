# Worked example

A complete, deliberately tiny chain: one spec, one epic, one feature, two tasks.
IDs use the reserved `9xxx` range so they can never collide with real work. The
spec is shown here only to keep the example together; a real spec would live in
`docs/product-specs/`, while the epic, feature, and tasks live in `planning/`.

Start with the spec and follow the links:

1. [`SPEC-9001-portfolio-yield-report.md`](SPEC-9001-portfolio-yield-report.md)
2. [`EPIC-9001-yield-calculation.md`](EPIC-9001-yield-calculation.md)
3. [`FEAT-9001-yield-summary-table.md`](FEAT-9001-yield-summary-table.md)
4. [`TASK-9001-add-yield-formula.md`](TASK-9001-add-yield-formula.md)
5. [`TASK-9002-add-yield-summary-table.md`](TASK-9002-add-yield-summary-table.md)

Note how:

- The spec names goals and success metrics, not implementation.
- The epic slices the spec and lists acceptance criteria plus a task table.
- Each task has one objective, checkboxes, and a `verify` command.
- `TASK-9002` declares `depends_on: [TASK-9001]`, so it can't be picked first.
- The feature links the spec and the epic that deliver it.
