# Purpose
This document defines the backend package layout and test conventions for the AI Director Course repository.
It exists to ensure humans and AI agents generate backend code in a consistent location and structure before implementation expands.
AI agents must read this document before adding new backend modules or backend tests.

# Maintenance Instructions
Update this document when backend folders, module responsibilities, test conventions, or packaging decisions change.
Humans and AI agents may both maintain it, but updates should stay aligned with [docs/tasks.md](../../tasks.md), [docs/design/design.md](../design.md), and the actual backend code structure.
Keep changes small and reflect only decisions that are ready to guide implementation.

## Purpose of this Document
This document is part of the modular project design documentation.
It captures the current understanding of this domain area.
Content may be incomplete early in the project.
Keep this document up-to-date as implementation evolves.
AI agents must read this before implementing related tasks and update it after completing them.

# Package Layout Decision
## Chosen backend root
Backend Python code lives under `/backend`.

## Chosen import package
The first backend package is `ai_director_backend`.

## Initial directory structure
```text
/backend/
    requirements.txt
    /ai_director_backend/
        __init__.py
        app.py
        models.py
        /ingestion/
            __init__.py
            models.py
            pipeline.py
            /retrieval/
                __init__.py
                engine.py
        /api/
            __init__.py
            routes.py
        /services/
            __init__.py
            chat_service.py
            gemini_service.py
```

# Module Responsibilities
## `ai_director_backend/app.py`
- creates the FastAPI application
- registers routes
- defines top-level app metadata

## `ai_director_backend/models.py`
- stores request and response models for the backend API skeleton
- keeps API contracts explicit and testable

## `ai_director_backend/api/routes.py`
- contains HTTP route handlers
- keeps endpoint definitions separate from service logic

## `ai_director_backend/services/chat_service.py`
- contains chat orchestration logic
- starts as a contract-only placeholder
- later becomes the entry point to retrieval and grounded answering

## `ai_director_backend/services/gemini_service.py`
- holds optional Gemini-based synthesis logic for retrieved chunks
- builds the grounded synthesis prompt and calls Gemini only when explicitly enabled through environment variables
- falls back cleanly to local synthesis when Gemini is not configured or unavailable

## `ai_director_backend/ingestion/models.py`
- stores ingestion data structures such as source documents, chunks, and index metadata
- keeps ingestion output explicit and testable

## `ai_director_backend/ingestion/pipeline.py`
- loads Markdown files from the repository
- normalizes content and splits it into heading-aware chunks
- builds a persisted index artifact for later retrieval work

## `ai_director_backend/retrieval/engine.py`
- loads the local ingestion index artifact
- performs lightweight grounded retrieval over repository chunks
- builds answer-ready content and citations for the chat service

# Test Conventions
## Chosen test location
Backend tests remain under `/tests` for now.

## Why keep tests under `/tests`
- it matches the repository's documented conventional test location
- it keeps bootstrap-stage testing simple
- it avoids splitting tests before the backend grows large enough to justify it

## Backend test naming
Use clear test files such as:
- `tests/test_backend_api.py`
- `tests/test_ingestion.py`
- `tests/test_retrieval.py`

## Import convention for tests
Tests may add `/backend` to `sys.path` until packaging becomes more formal.
If the repository later adopts a `pyproject.toml`-based package install flow, update this document and the tests together.

# Packaging Guidance
## MVP dependency tracking
Use `/backend/requirements.txt` for the first implementation phase.

## Deferred packaging decisions
The following are intentionally deferred:
- `pyproject.toml`
- publishable package metadata
- editable install workflow
- separate dev dependency groups

Those decisions can be revisited once the backend contains more than the initial skeleton.

# Implementation Rules
- Keep the HTTP layer thin.
- Keep service logic separate from route functions.
- Keep schemas explicit rather than passing raw dictionaries between layers.
- Add new backend modules only when they serve a real design area such as ingestion, retrieval, or orchestration.

# Open Questions
- When should the backend move from `requirements.txt` to `pyproject.toml`?
- Should maintainer-only backend tools live inside the same package or a separate support package?
- When should retrieval-specific modules split into their own subpackages?
