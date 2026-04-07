# Purpose
This file defines repository-wide working rules for humans and AI agents in the AI Director Course repository.
It exists to keep implementation aligned with project documentation and to preserve consistent behavior across fresh AI sessions.
AI agents should treat this file as always-on guidance before making any code or documentation change.

# Maintenance Instructions
Update this file when repository workflow rules, review expectations, or documentation hierarchy change.
Humans or AI agents may update it, but changes should stay small and deliberate because this file affects all future work.
Keep this file aligned with [docs/START_HERE.md](../docs/START_HERE.md), [docs/tasks.md](../docs/tasks.md), and [docs/design/design.md](../docs/design/design.md).

# Always-On Repository Rules

## Before any implementation work
1. Read [docs/START_HERE.md](../docs/START_HERE.md).
2. Read [docs/tasks.md](../docs/tasks.md).
3. Read [docs/design/design.md](../docs/design/design.md) first, then only the relevant design subdocuments if they exist.
4. Confirm the current phase, target task ID, and acceptance criteria before editing files.

## After any implementation work
1. Update [docs/tasks.md](../docs/tasks.md).
2. Update [docs/design/design.md](../docs/design/design.md) and only the relevant design subdocuments when needed.
3. Do not modify unrelated documentation.
4. Leave clear notes for the next fresh-session AI handoff.

## Documentation-First Rules
- Documentation is the primary source of truth, not code.
- If implementation diverges from design, stop and update design docs first.
- Code should remain regenerable from requirements, design decisions, tasks, tests, and domain knowledge stored in this repository.
- Prefer explicit placeholders such as `TBD` or `To Be Discovered` over guessed details.

## Code Surgeon Rules
- Make the smallest possible diff to satisfy the task.
- Never reformat unrelated code.
- Do not rename files, symbols, or folders unless explicitly required.
- Preserve ordering, imports, whitespace, comments, and backward compatibility.
- Keep changes reviewable and easy to trace back to a task ID.

## Refactoring Rules
- Refactoring must be a separate task.
- Keep refactoring diffs isolated from feature work.
- Document why the refactor is needed before starting it.

## Testing Rules
- The conventional test location for this repository is `/tests` unless a future design split requires domain-local tests.
- If tests are deferred for a task, document that decision in [docs/tasks.md](../docs/tasks.md) and the relevant design notes.
- Prefer the smallest useful validation that proves the task works.

<!-- Python environment rule: if Python is needed for this repository, activate and work with `C:\Users\saaamar\source\repos\ai-director-course\.venv\Scripts\python.exe` only. -->
