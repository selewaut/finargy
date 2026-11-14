# Planning

Execution planning lives here, separate from durable documentation in
[`../docs/`](../docs/README.md). Tasks, epics, and the notes around them can churn
freely without bloating the real docs.

## Model

```
Product Spec (docs/)  →  Epic  →  Task
                          └── Feature (cross-link)
```

Docs live in `docs/`; epics, features, and tasks live here.

## Layout

```
planning/
  README.md        # this file
  TEMPLATES/       # epic.md, feature.md, task.md
  epics/           # EPIC-0001-*.md
  features/        # FEAT-0001-*.md
  tasks/           # TASK-0001-*.md
  examples/        # worked example, IDs in the 9xxx range
```

## Frontmatter

Shared:

```yaml
id: TASK-0001
type: task                # epic | feature | task
title: Short imperative title
status: ready
priority: medium          # low | medium | high | critical
owner: unassigned
created: 2026-11-14
updated: 2026-11-14
tags: []
```

Type-specific:

| Type    | Extra fields                                             |
| ------- | -------------------------------------------------------- |
| epic    | `spec: SPEC-0001`, `features: []`, `tasks: []`           |
| feature | `spec: SPEC-0001`, `epics: []`                           |
| task    | `epic: EPIC-0001`, `feature: null`, `depends_on: []`, `verify: "cmd"` |

## Status lifecycle

```
draft → ready → in-progress → review → done
                     └──────→ blocked ──────┘
draft/ready/in-progress/review/blocked → cancelled
```

| Status        | Meaning                                              |
| ------------- | ---------------------------------------------------- |
| `draft`       | Still being written; not ready to pick up.           |
| `ready`       | Fully specified; can be started.                     |
| `in-progress` | Actively being worked. Exactly one owner.            |
| `blocked`     | Waiting on something; record it in the task's log.   |
| `review`      | Work complete, awaiting human review.                |
| `done`        | Accepted and merged.                                 |
| `cancelled`   | Won't do; keep the file with a reason in the log.    |

A task's `epic:` field is the source of truth for membership. Epic files keep a
task table for humans; keep it in sync as tasks move.

## IDs

Never reuse IDs; allocate the next number as max + 1 for that type. `9xxx` is
reserved for `examples/`.

## Worked example

See [`examples/README.md`](examples/README.md).
