# Purpose
This document tracks planned, active, completed, and discovered work for the AI Director Course repository.
It exists to give humans and AI agents a durable task ledger that survives fresh sessions and keeps implementation tied to explicit acceptance criteria.
AI agents should read this file before starting work and update only the relevant task entries after completing changes.

# Maintenance Instructions
Update this file whenever work starts, changes scope, completes, or reveals follow-up tasks.
Humans and AI agents both maintain it, but changes should stay tightly scoped to the task being executed.
Keep it aligned with [docs/design/design.md](design/design.md) and [docs/START_HERE.md](START_HERE.md).

# Phase Overview
- [x] Phase 1 — Repository bootstrap
- [ ] Phase 2 — Public course skeleton refinement
- [ ] Phase 3 — Curriculum authoring
- [ ] Phase 4 — Backend assistant design and implementation
- [ ] Phase 5 — Website chat integration
- [ ] Phase 6 — Community operations and deployment

## Phase 1 — Repository bootstrap

### 1.1 Documentation-first initialization
- Status: [x]
- Started:
- Completed:
- Included in version:
- Acceptance criteria:
    - Internal source-of-truth docs exist under `/docs`.
    - Repository-wide AI instructions exist under `/.github`.
    - Initial design, research, and task templates are available.
    - Starter validation path for tests is documented.
- Validation:
    - Bootstrap files created.
    - Starter scaffold test added under `/tests`.
- Notes:
    - Completed as the first repository scaffold.
- Dependencies: None

#### 1.1.1 Create governance docs
- Status: [x]
- Started:
- Completed:
- Included in version:
- Acceptance criteria:
    - `docs/START_HERE.md`, `docs/tasks.md`, `docs/design/design.md`, and research/template docs exist.
- Validation:
    - Files created with purpose and maintenance instructions.
- Notes:
- Dependencies: None

#### 1.1.2 Create repository AI instructions
- Status: [x]
- Started:
- Completed:
- Included in version:
- Acceptance criteria:
    - `/.github/copilot-instructions.md` defines before/after implementation rules and minimal-diff behavior.
- Validation:
    - File created.
- Notes:
- Dependencies: 1.1.1

#### 1.1.3 Create starter validation test
- Status: [x]
- Started:
- Completed:
- Included in version:
- Acceptance criteria:
    - `/tests` exists and includes a lightweight scaffold check.
- Validation:
    - `tests/test_project_scaffold.py` created.
- Notes:
- Dependencies: 1.1.1

## Phase 2 — Public course skeleton refinement

### 2.1 Create MkDocs site skeleton
- Status: [x]
- Started:
- Completed:
- Included in version:
- Acceptance criteria:
    - `mkdocs.yml` exists.
    - Public site docs live outside internal governance docs.
    - Navigation includes the welcome page, tool vault, and all seven sprint days.
- Validation:
    - `mkdocs.yml` created.
    - `/course` content skeleton created.
- Notes:
    - Chosen approach separates public content (`/course`) from internal docs (`/docs`).
- Dependencies: 1.1.1

#### 2.1.1 Create public course placeholders
- Status: [x]
- Started:
- Completed:
- Included in version:
- Acceptance criteria:
    - Welcome, Tool Vault, and Day 1–Day 7 Markdown files exist.
    - Each page reflects the two-speed pacing concept.
- Validation:
    - Placeholder files created under `/course`.
- Notes:
- Dependencies: 2.1

#### 2.1.2 Add local MkDocs task runner
- Status: [x]
- Started:
- Completed:
- Included in version:
- Acceptance criteria:
    - `.vscode/tasks.json` includes a task to serve the docs locally.
- Validation:
    - Task file created.
- Notes:
- Dependencies: 2.1

## Phase 3 — Curriculum authoring

### 3.1 Write Day 1 complete lesson
- Status: [x]
- Started:
- Completed:
- Included in version:
- Acceptance criteria:
    - Day 1 includes a full Fast Track workflow.
    - Day 1 includes Deep Dive guidance, troubleshooting, and example prompt structures.
- Validation:
    - Expanded `course/day-1-storyboard.md` with a full Fast Track workflow, structured prompts, troubleshooting, and a stronger end-of-day deliverable.
- Notes:
    - Day 1 now establishes the lesson pattern for future curriculum expansion.
- Dependencies: 2.1.1

### 3.2 Write Day 2 complete lesson
- Status: [x]
- Started:
- Completed:
- Included in version:
- Acceptance criteria:
    - Day 2 teaches the cinematic prompt formula, `CREF`, and `SREF` usage.
- Validation:
    - Expanded `course/day-2-images.md` with a full prompt-building workflow, `CREF` and `SREF` guidance, troubleshooting, and frame-selection criteria.
- Notes:
    - Day 2 now defines the consistency discipline that Day 3 motion work will depend on.
- Dependencies: 3.1

### 3.3 Write Day 3 complete lesson
- Status: [x]
- Started:
- Completed:
- Included in version:
- Acceptance criteria:
    - Day 3 teaches image-to-video motion prompts, camera movement, and warping mitigation.
- Validation:
    - Expanded `course/day-3-video.md` with motion prompt templates, camera movement guidance, artifact troubleshooting, and clip-selection rules.
- Notes:
    - Day 3 now defines the motion discipline that protects Day 2 visual consistency during video generation.
- Dependencies: 3.2

### 3.4 Write Days 4 through 7 complete lessons
- Status: [x]
- Started:
- Completed:
- Included in version:
- Acceptance criteria:
    - Remaining lesson files contain actionable instruction, troubleshooting, and project checkpoints.
- Validation:
    - Expanded `course/day-4-audio.md`, `course/day-5-music.md`, `course/day-6-editing.md`, and `course/day-7-final.md` with full workflows, troubleshooting, checkpoints, and end-of-day deliverables.
- Notes:
    - The full seven-day sprint now follows a richer lesson structure with execution steps and deeper guidance.
- Dependencies: 3.3

### 3.5 Formalize Tool Vault maintenance workflow
- Status: [x]
- Started:
- Completed:
- Included in version:
- Acceptance criteria:
    - Tool categories, update cadence, and content ownership are documented.
- Validation:
    - Expanded `course/tool-vault.md` with ownership, update cadence, evaluation criteria, and a suggested change process.
- Notes:
    - The Tool Vault is now the explicit public abstraction layer for change-prone vendor guidance.
- Dependencies: 2.1.1

### D.6 Add course placeholder audit
- Status: [x]
- Started:
- Completed:
- Included in version:
- Acceptance criteria:
    - A lightweight test reports unresolved screenshot or content placeholders under `/course`.
- Validation:
    - Added `tests/test_placeholder_audit.py` to scan course Markdown for placeholder markers such as `YOUR TASK:` and `📷`.
- Notes:
    - This test is intended as a content-completion checklist and will fail until all learner-facing placeholders are replaced.
    - A first pass of mock screenshots is now embedded across Day 1 through Day 7 with alt text and captions, using generated assets under `/course/assets/images`.
- Dependencies: 3.4

## Phase 4 — Backend assistant design and implementation

### 4.1 Design ingestion and retrieval architecture
- Status: [x]
- Started:
- Completed:
- Included in version:
- Acceptance criteria:
    - Design docs describe chunking, embeddings, vector storage, and answer-grounding rules.
- Validation:
    - Added `docs/design/backend/retrieval-architecture.md` covering chunking, embeddings, vector storage, retrieval flow, and grounded-answer behavior.
    - Extended tests to assert the presence of the backend retrieval design document and key sections.
- Notes:
    - ChromaDB is the current MVP vector-store recommendation for local-first developer ergonomics.
    - Learner-facing grounding should prefer course content while preserving room for maintainer-oriented retrieval later.
- Dependencies: 3.1

### 4.2 Implement backend API skeleton
- Status: [x]
- Started:
- Completed:
- Included in version:
- Acceptance criteria:
    - Python backend exposes a health endpoint and a chat endpoint contract.
    - Async architecture is documented and implemented minimally.
- Validation:
    - Added `/backend/ai_director_backend` with FastAPI app, route definitions, request/response models, and a placeholder chat service.
    - Added `tests/test_backend_api.py` covering the health endpoint and chat contract shape.
- Notes:
    - The chat endpoint currently returns a contract-only placeholder response until retrieval is implemented.
- Dependencies: 4.1, D.1

### 4.3 Implement document ingestion pipeline
- Status: [x]
- Started:
- Completed:
- Included in version:
- Acceptance criteria:
    - Repository Markdown content can be chunked and indexed for retrieval.
- Validation:
    - Added `backend/ai_director_backend/ingestion/pipeline.py` and related models for Markdown loading, heading-aware chunking, and local index generation.
    - Added `tests/test_ingestion.py` covering chunking behavior and index file creation.
- Notes:
    - The current implementation writes a structured local index artifact and term index to support the next grounded retrieval step.
- Dependencies: 4.1

### 4.4 Implement grounded answer workflow
- Status: [x]
- Started:
- Completed:
- Included in version:
- Acceptance criteria:
    - Assistant uses retrieved course context and declines out-of-scope questions.
- Validation:
    - Added `backend/ai_director_backend/retrieval/engine.py` for local index loading, chunk retrieval, and grounded answer assembly.
    - Updated `backend/ai_director_backend/services/chat_service.py` so `/api/chat` returns grounded responses or scoped refusals.
    - Added `tests/test_retrieval.py` and expanded `tests/test_backend_api.py` for grounded and out-of-scope behavior.
- Notes:
    - The current retrieval implementation is lightweight and lexical, designed to validate end-to-end grounding before embedding and vector-store integration.
- Dependencies: 4.2, 4.3

## Phase 5 — Website chat integration

### 5.1 Select or build website chat widget approach
- Status: [x]
- Started:
- Completed:
- Included in version:
- Acceptance criteria:
    - Design captures widget UX, API contract, and site integration path.
- Validation:
    - Added `docs/design/chat-widget/website-chat-widget.md` covering widget UX, backend contract expectations, MkDocs integration path, and fallback behavior.
    - Extended scaffold tests to assert the presence of the widget design document.
- Notes:
    - The current recommendation is a small launcher-plus-panel widget implemented through MkDocs theme overrides with lightweight JavaScript and CSS.
- Dependencies: 4.2

### 5.2 Integrate widget with backend assistant
- Status: [x]
- Started:
- Completed:
- Included in version:
- Acceptance criteria:
    - Students can ask grounded questions from the course site.
- Validation:
    - Added MkDocs widget assets and theme override files for the learner-facing chat launcher and panel.
    - Updated `mkdocs.yml` and `.vscode/tasks.json` for local widget and backend testing.
    - Enabled backend CORS for local MkDocs-to-API requests.
    - Verified the site builds successfully and the Python test suite passes.
- Notes:
    - The current widget uses a lightweight non-streaming JavaScript integration and learner-facing mode against `/api/chat`.
- Dependencies: 5.1, 4.4

## Phase 6 — Community operations and deployment

### 6.1 Design Discord support workflow
- Status: [ ]
- Started:
- Completed:
- Included in version:
- Acceptance criteria:
    - Bot responsibilities, moderation boundaries, and role automation handoffs are documented.
- Validation:
- Notes:
- Dependencies: 4.4

### 6.2 Deploy static site and backend services
- Status: [ ]
- Started:
- Completed:
- Included in version:
- Acceptance criteria:
    - Chosen hosts, environment variables, and release workflow are documented.
- Validation:
- Notes:
- Dependencies: 5.2, 6.1

### D.7 Add GitHub Pages deployment workflow
- Status: [x]
- Started:
- Completed:
- Included in version:
- Acceptance criteria:
    - A GitHub Actions workflow can build the MkDocs site and deploy it to GitHub Pages from source without committing `/site` to the main branch.
- Validation:
    - Added `/.github/workflows/deploy-mkdocs.yml`.
    - Updated `README.md` with GitHub Pages setup instructions.
    - Extended scaffold validation to assert the workflow file exists.
- Notes:
    - This deploys only the static site. The FastAPI backend still requires separate hosting and public widget configuration.
- Dependencies: 2.1, D.3

### D.8 Add site author credit
- Status: [x]
- Started:
- Completed:
- Included in version:
- Acceptance criteria:
    - The public MkDocs site shows author credit and repository attribution site-wide.
- Validation:
    - Updated `mkdocs.yml` with `site_author` and footer copyright metadata pointing to the GitHub repository.
- Notes:
    - The credit is rendered by the MkDocs theme footer on every page.
- Dependencies: 2.1

### D.9 Remove local path leakage
- Status: [x]
- Started:
- Completed:
- Included in version:
- Acceptance criteria:
    - Repository docs and generated metadata do not embed workstation-specific absolute paths.
- Validation:
    - Updated `/.github/copilot-instructions.md` to reference the virtual environment using a repository-relative path.
    - Updated ingestion metadata generation so the index stores only the repository name rather than an absolute local filesystem path.
- Notes:
    - Regenerate the ingestion index after this change so `backend/.artifacts/ingestion/index.json` reflects the portable metadata format.
- Dependencies: 4.3

# Discovered Tasks

### D.1 Decide backend package layout
- Status: [x]
- Started:
- Completed:
- Included in version:
- Acceptance criteria:
    - Backend code location and test conventions are explicitly documented before code generation begins.
- Validation:
    - Added `docs/design/backend/package-layout.md` documenting backend root, package structure, and test conventions.
- Notes:
    - `/backend` is the chosen code root and `/tests` remains the current backend test location.
- Dependencies: 4.1

### D.2 Decide publishing boundary between internal docs and public course pages
- Status: [ ]
- Started:
- Completed:
- Included in version:
- Acceptance criteria:
    - Public build excludes internal governance docs unless intentionally exposed.
- Validation:
- Notes:
- Dependencies: 2.1

### D.3 Add repository README
- Status: [x]
- Started:
- Completed:
- Included in version:
- Acceptance criteria:
    - Root README explains how to run the site, backend, tests, and current chat workflow.
- Validation:
    - Added `README.md` with local setup, run, test, and usage instructions.
- Notes:
    - README is a quick-start guide; detailed implementation truth remains under `/docs`.
- Dependencies: 5.2

### D.4 Add optional Gemini synthesis
- Status: [x]
- Started:
- Completed:
- Included in version:
- Acceptance criteria:
    - Backend can optionally pass retrieved repository snippets to Gemini for final answer synthesis without breaking the local fallback path.
- Validation:
    - Added `backend/ai_director_backend/services/gemini_service.py`.
    - Updated chat orchestration to use Gemini only when explicitly enabled.
    - Added `tests/test_gemini_service.py` for prompt and response parsing helpers.
- Notes:
    - Local synthesis remains the default path when Gemini is not configured or fails.
    - The default Gemini model is now `gemini-2.5-flash`, while `.env` can still override it locally.
    - Gemini calls now use the `google-genai` Python client rather than hand-built REST requests.
    - Transient Gemini API failures now use a small retry loop before the backend falls back to local synthesis.
    - Personal identity questions that are outside repository scope are now declined before retrieval so the assistant does not attach irrelevant citations.
    - Personal identity questions with simple punctuation typos, such as `na,e`, are now also caught before retrieval.
    - When retrieval finds no chunks, Gemini can now answer broader in-scope filmmaking questions without citations, while still refusing out-of-scope topics.
    - Backend package logging for `ai_director_backend` is now forced to `INFO` so Gemini-path decisions are visible in local runtime logs.
    - An `AI_DIRECTOR_VERBOSE_LOGGING` option now logs full Gemini prompt and response text in the backend terminal for debugging.
    - Backend application logs are now attached to Uvicorn's error logger and emit a startup configuration line so local runtime logging is visibly active.
    - The retrieval layer now rebuilds the ingestion index automatically when repository Markdown files change, so updated course pages are reflected without a manual reindex step.
- Dependencies: 4.4

### D.5 Add `.env` template workflow
- Status: [x]
- Started:
- Completed:
- Included in version:
- Acceptance criteria:
    - Local Gemini configuration can be read from a repository `.env` file while keeping a commit-safe `.env.template` in version control.
- Validation:
    - Added `.env.template`.
    - Updated Gemini service loading to read `.env` when present.
    - Updated `README.md` to instruct users to copy `.env.template` to `.env`.
- Notes:
    - `.env` remains ignored by git and is intended for local secrets only.
    - The backend now treats repository `.env` values as authoritative for local Gemini configuration so stale shell variables do not silently override the chosen model.
- Dependencies: D.4
