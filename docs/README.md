# Documentation

`docs/` holds durable documentation: product specs and architecture decision
records (ADRs). Execution planning lives separately in [`planning/`](../planning/README.md)
so that real documentation is not cluttered by task implementations.

## Layout

```
docs/
  README.md            # this file
  TEMPLATES/
    product-spec.md
    adr.md
  product-specs/       # SPEC-0001-*.md
  adr/                 # ADR-0001-*.md
```

## Product specs

Product specs describe the problem, goals, non-goals, requirements, and success
metrics. They are stable reference documents, not work logs. Use
[`TEMPLATES/product-spec.md`](TEMPLATES/product-spec.md).

- Naming: `product-specs/SPEC-<NNNN>-<kebab-case-title>.md`
- Shared frontmatter: `id`, `type: product-spec`, `title`, `status`, `priority`,
  `owner`, `created`, `updated`, `epics`, `tags`.
- `status` is a document lifecycle, independent of task status:
  `draft → ready → done` (or `cancelled`).
- `epics` links to the planning epics that implement the spec.

## ADRs

Architecture decision records capture a decision, its context, and its
consequences. They are immutable once accepted: to change a decision, write a new
ADR and mark the old one `superseded`. Use [`TEMPLATES/adr.md`](TEMPLATES/adr.md).

- Naming: `adr/ADR-<NNNN>-<kebab-case-title>.md`
- Frontmatter: `id`, `type: adr`, `title`, `status`, `date`, `deciders`,
  `supersedes`, `superseded_by`, `tags`.
- `status`: `proposed | accepted | rejected | superseded`.

## IDs

IDs are never reused. Allocate the next number as max + 1 for that type. `9xxx`
is reserved for examples in `planning/examples/`.

| Type         | Prefix | Directory              |
| ------------ | ------ | ---------------------- |
| Product spec | `SPEC` | `docs/product-specs/`  |
| ADR          | `ADR`  | `docs/adr/`            |
| Epic         | `EPIC` | `planning/epics/`      |
| Feature      | `FEAT` | `planning/features/`   |
| Task         | `TASK` | `planning/tasks/`      |

Dates are ISO `YYYY-MM-DD`. Always bump `updated` when you edit.

## Planning

Epics, features, and tasks live in [`planning/`](../planning/README.md). The
planning model is `product-spec → epic → task`, with features as optional
cross-links. See [`../AGENTS.md`](../AGENTS.md) for the agent workflow.
