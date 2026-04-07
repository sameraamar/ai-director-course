# Purpose
This README is the quick-start guide for the AI Director Course repository.
It exists to help humans quickly understand what the project is, how to run it locally, how to test it, and how to use the current course site and assistant.
AI agents may use it as a high-level orientation document, but the detailed source of truth remains under `/docs`.

# Maintenance Instructions
Update this file when the local run workflow, test commands, repository layout, or user-facing usage flow changes.
Humans and AI agents may both maintain it, but it should stay concise and practical.
Keep it aligned with [docs/START_HERE.md](docs/START_HERE.md), [docs/tasks.md](docs/tasks.md), and the current implementation.

# AI Director Course
AI Director Course is a docs-as-code learning platform for a 7-day cinematic AI sprint.
It currently includes:
- a public MkDocs course site
- a grounded Python backend assistant
- a learner-facing website chat widget
- internal design and planning docs for future expansion

# Repository Structure
- [course](course) — public lesson content
- [backend](backend) — Python backend code
- [overrides](overrides) — MkDocs theme overrides
- [docs](docs) — internal planning and design docs
- [tests](tests) — automated validation tests
- [mkdocs.yml](mkdocs.yml) — MkDocs configuration
- [.vscode/tasks.json](.vscode/tasks.json) — local VS Code tasks

# Requirements
- Windows PowerShell
- Python virtual environment already available at [.venv/Scripts/python.exe](.venv/Scripts/python.exe)

This repository is configured to use only:
- [.venv/Scripts/python.exe](.venv/Scripts/python.exe)

# Install or Refresh Dependencies
If you need to refresh the environment, use the project virtual environment.

## Backend and test dependencies
Run:

```powershell
.venv\Scripts\python.exe -m pip install -r backend\requirements.txt
```

## MkDocs site dependencies
Run:

```powershell
.venv\Scripts\python.exe -m pip install mkdocs-material
```

## Why `mkdocs-material` is not currently in `backend/requirements.txt`
The current split is intentional:
- [backend/requirements.txt](backend/requirements.txt) is being used for backend runtime and backend-test dependencies
- `mkdocs-material` belongs to the public docs site toolchain, not the backend API runtime

This keeps backend service dependencies separate from site-building dependencies.

That said, this is a repository convention, not a technical limitation.
If the project later wants a single install command, a root-level dependency file such as `requirements.txt` or `requirements-dev.txt` would be a cleaner place to combine backend and docs tooling.

## Optional Gemini synthesis
The backend can optionally pass retrieved repository snippets to Gemini for final answer synthesis.

This is off by default.

The current default model is `gemini-2.5-flash`.
The current implementation uses the `google-genai` Python client instead of calling the REST endpoint directly.

To enable it for local development:
1. copy `.env.template` to `.env`
2. fill in the Gemini values in `.env`

For this repository's local workflow, values in `.env` are treated as the source of truth for Gemini settings.

Example `.env.template` fields:

```text
AI_DIRECTOR_USE_GEMINI=
GEMINI_API_KEY=
AI_DIRECTOR_GEMINI_MODEL=
AI_DIRECTOR_VERBOSE_LOGGING=
```

Set `AI_DIRECTOR_VERBOSE_LOGGING=true` if you want the backend terminal to print the full Gemini prompt and Gemini text response for both grounded and scoped AI calls.

If Gemini is not enabled, not configured, or fails at runtime, the backend falls back to the local synthesis path.

When retrieval finds no repository chunks, the backend can still use Gemini for broader in-scope filmmaking questions such as lens basics or camera concepts. Those answers return without citations because they are scoped AI explanations rather than repository-grounded quotes.

The real `.env` file is ignored by git.
Only `.env.template` should be committed.

# How to Run the Project
You need two local processes:
1. the backend API
2. the MkDocs site

## Option 1 — Use VS Code tasks
Run these tasks:
- `Run Backend API`
- `Serve MkDocs`

## Option 2 — Run manually in terminals

### Terminal 1: start the backend API
```powershell
.venv\Scripts\python.exe -m uvicorn ai_director_backend.app:app --host 127.0.0.1 --port 8001 --reload --app-dir backend
```

### Terminal 2: start the MkDocs site
```powershell
.venv\Scripts\python.exe -m mkdocs serve
```

## Local URLs
- Course site: <http://127.0.0.1:8000>
- Backend health endpoint: <http://127.0.0.1:8001/api/health>
- Backend chat endpoint: <http://127.0.0.1:8001/api/chat>

# How to Use the Site
1. Open <http://127.0.0.1:8000>
2. Read the course pages from the top navigation
3. Open the chat launcher in the lower corner
4. Ask a sprint-related question such as:
   - `How do I create a 5-shot storyboard?`
   - `How do I turn storyboard shots into image prompts?`
   - `How should I use motion prompts on Day 3?`
5. Review the answer and citations

## Expected chat behavior
### Grounded question example
Ask:

```text
How do I create a 5-shot storyboard?
```

Expected behavior:
- the assistant returns a repository-grounded answer
- citations should reference course files such as Day 1

### Out-of-scope question example
Ask:

```text
What is the capital of France?
```

Expected behavior:
- the assistant declines the question as out of scope
- no fake citations are returned

# How to Run Tests
Run the full automated suite with:

```powershell
.venv\Scripts\python.exe -m unittest -v tests.test_project_scaffold tests.test_backend_api tests.test_ingestion tests.test_retrieval
```

# How to Validate the Site Build
Run:

```powershell
.venv\Scripts\python.exe -m mkdocs build --strict
```

This checks that the public site, theme overrides, and widget assets build cleanly.

# How to Deploy the MkDocs Site to GitHub Pages
This repository now includes a GitHub Actions workflow at [.github/workflows/deploy-mkdocs.yml](.github/workflows/deploy-mkdocs.yml).

To use it:
1. Push the repository to GitHub.
2. In the GitHub repository settings, enable GitHub Pages and set the source to `GitHub Actions`.
3. Push to the `main` branch or run the workflow manually from the Actions tab.

The workflow builds the MkDocs site with `mkdocs build --strict` and deploys the generated [site](site) output to GitHub Pages.

Important:
- You do not need to commit [site](site) to the main branch.
- GitHub Pages deploys only the static frontend.
- The chat widget still needs a separately hosted backend API before public chat can work outside localhost.

# How to Regenerate the Ingestion Index
Run:

```powershell
.venv\Scripts\python.exe -c "import sys; from pathlib import Path; repo = Path.cwd(); sys.path.insert(0, str((repo / 'backend').resolve())); from ai_director_backend.ingestion.pipeline import ingest_repository; print(ingest_repository(repo))"
```

Expected output:
- an index file path under [backend/.artifacts/ingestion/index.json](backend/.artifacts/ingestion/index.json)

# Current Implementation Notes
- retrieval is currently lightweight and lexical, not embedding-based yet
- Gemini can optionally synthesize the final answer from retrieved snippets, but it is disabled unless environment variables enable it
- the chat widget currently uses a non-streaming frontend integration
- learner-facing chat requests currently use `user_mode = learner`
- Discord support and deployment workflows are still planned

# Where to Look Next
- project entrypoint: [docs/START_HERE.md](docs/START_HERE.md)
- task tracker: [docs/tasks.md](docs/tasks.md)
- top-level design: [docs/design/design.md](docs/design/design.md)
- backend retrieval design: [docs/design/backend/retrieval-architecture.md](docs/design/backend/retrieval-architecture.md)
- widget design: [docs/design/chat-widget/website-chat-widget.md](docs/design/chat-widget/website-chat-widget.md)
