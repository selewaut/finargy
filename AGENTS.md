# AGENTS.md

Guidance for AI agents (and humans) working in this repo.

## Repo map

- `src/finargy/` — the Python package (src layout; `pytest` sets `pythonpath = ["src"]`).
  - `api/` — `client.py` (`InvertirOnlineAPI`) plus thin endpoint wrappers
    (`account_data.py`, `market_data/*`). Wrappers call `client._request(...)`;
    the underscore is intentional, don't "fix" it.
  - `data_processing/` — DataFrame helpers for API payloads.
  - `portfolio/` — portfolio reconstruction and analysis (`analysis/mep.py` for
    the MEP dollar, `analysis/analysis.py`).
- `docs/` — durable docs: product specs (`docs/product-specs/`) and ADRs
  (`docs/adr/`). See `docs/README.md`.
- `planning/` — execution planning: epics, features, tasks. See
  `planning/README.md`. `planning/tasks/` is the primary unit of agent work.
- `extract_ratios.py` and `portfolio_yield.ipynb` at the repo root are ad-hoc
  scratch, not package code; don't import or build on them.

## Planning framework

Work flows `product-spec → epic → task` (features are optional cross-links).
Each is a markdown file with YAML frontmatter. Read `docs/README.md` and
`planning/README.md` before creating or editing docs. Use the templates in
`docs/TEMPLATES/` (spec, ADR) and `planning/TEMPLATES/` (epic, feature, task).

Keep `docs/` lean: don't put task logs, implementation notes, or work-in-progress
in `docs/`. That belongs in `planning/`.

## Task workflow

1. **Pick** a task with `status: ready` whose `depends_on` are all `done` and
   whose `epic` is `ready` or `in-progress`. Prefer `priority: high`/`critical`.
2. **Claim** it: set `status: in-progress`, `owner` to your agent name, bump
   `updated`, and append a log entry.
3. **Read** the task's `epic`, its `spec`, and any linked features. Do not invent
   scope beyond the acceptance criteria. If something is ambiguous, add an entry
   to the task log and set `status: blocked` rather than guessing.
4. **Do the work.** Touch only files within the task's scope.
5. **Verify** using the task's `verify` command and its acceptance criteria.
   Record the result in the log. If verification fails and you can't fix it,
   leave `status: in-progress` and log the failure.
6. **Submit** for review: set `status: review`, tick completed acceptance
   criteria, bump `updated`, log a summary with files changed.
7. **Finish** only when a human accepts. Then set `status: done`, bump
   `updated`, and update the parent epic's task table.

## Rules

- One task per commit/PR. Reference the task ID in the commit message, e.g.
  `TASK-0007: add MEP yield formula`.
- Never reuse IDs. Allocate the next number as max + 1 for that type.
- Dates are ISO `YYYY-MM-DD`. Always bump `updated` on edit.
- Keep frontmatter valid YAML and keep `type` consistent with the directory.
- Keep the epic task table in sync with task statuses.
- Record significant architecture decisions as an ADR in `docs/adr/`; supersede
  rather than edit accepted ADRs.
- Mark a task `done` only after its verification passes and criteria are ticked.
- Don't expand scope, refactor unrelated code, or add docs the task didn't ask for.
- Never commit secrets, credentials, or `.env` contents.

## Definition of done

- Acceptance criteria ticked.
- `verify` command passes (or a human explicitly waived it).
- Task log has a dated summary of changes.
- Parent epic's task table and `updated` date are current.
- No unrelated files changed.

## Commands

```sh
uv sync --extra dev      # install (Python pinned in .python-version, currently 3.14)
uv run pytest            # tests
uv run python -m ...     # run package code without activating .venv
```

## Repo quirks

- **No tests exist yet.** `tests/` does not exist and `uv run pytest` exits with
  "no tests ran" (code 5). The `verify:` examples that call `uv run pytest tests/...`
  are aspirational; for now use a concrete smoke command (e.g.
  `uv run python -c "import finargy..."`) unless the task adds tests.
- **No lint, formatter, or typecheck config** (no ruff/black/mypy sections, no CI
  workflows). Don't claim or invent such commands.
- **Credentials:** `.env` at repo root with `USER` and `PASSWORD`. `InvertirOnlineAPI`
  calls `load_dotenv()` without `override=True`, so an existing shell `USER` wins
  over `.env` — expect auth confusion and check env precedence before debugging code.
- `InvertirOnlineAPI.__init__` authenticates eagerly (network call); constructing
  it needs valid credentials and network access.
- Stale `__pycache__/*.cpython-312.pyc` files exist; the project targets 3.14.
  Ignore them.
- `src/finargy/api/account_data.py` imports a pytest symbol at module top, so
  importing it outside the `dev` extra (installed via `uv sync --extra dev`) fails.
