# Purpose
This template provides a reusable kickoff prompt for new implementation tasks.
It exists to standardize how humans and AI agents start work so the repository documentation remains the first source of truth.
AI agents should use this template before proposing code or documentation changes.

# Maintenance Instructions
Update this template when the preferred kickoff workflow, planning format, or documentation-reading order changes.
Humans and AI agents may adjust it, but keep it concise and easy to paste into a fresh session.
Keep it aligned with [docs/START_HERE.md](../START_HERE.md) and [docs/tasks.md](../tasks.md).

# Task Kickoff Template

## Read First
1. Read [docs/START_HERE.md](../START_HERE.md).
2. Read [docs/tasks.md](../tasks.md).
3. Read [docs/design/design.md](../design/design.md).
4. Read only the relevant design subdocuments if they exist.
5. Read the relevant implementation files after documentation is understood.

## Summarize Before Acting
Produce a short summary that includes:
- Current project phase
- Target task ID and title
- Relevant constraints
- Dependencies or blockers

## Plan Format
Propose a minimal, reviewable plan using this shape:
1. Context summary
2. Files likely to change
3. Smallest implementation steps
4. Validation approach
5. Documentation updates required after completion

## Working Rules
- Minimize diffs.
- Do not reformat unrelated files.
- Do not rename unless required.
- Update documentation after implementation.
- Ask clarifying questions only if required to avoid incorrect work.
