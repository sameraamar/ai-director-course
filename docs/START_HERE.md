# Purpose
This is the project entrypoint for the AI Director Course repository.
It exists to help humans and AI agents recover project intent quickly without relying on chat history.
AI agents should read this file first at the start of every new session or task.

# Maintenance Instructions
Update this file when the project summary, phase, source-of-truth files, or onboarding flow changes.
Humans and AI agents both maintain it as the top-level handoff document.
Keep it synchronized with [docs/tasks.md](tasks.md) and [docs/design/design.md](design/design.md).

# Project Summary
- **Project name:** AI Director Course
- **Description:** A docs-as-code learning platform for a 7-day cinematic AI sprint that teaches students how to produce a polished 30-to-60-second video using AI-assisted storyboarding, image generation, motion, audio, editing, and review workflows.
- **Target users / personas:** Creators, marketers, e-commerce founders, social media advertisers, and portfolio builders who want a guided cinematic AI workflow.
- **Primary business goal:** Ship a maintainable course platform with a searchable static site, an updatable tool vault, and a future Python-powered teaching assistant for student support.
- **Technology preferences:** MkDocs Material for the course site, Python/FastAPI for the backend agent, RAG for grounded answers, and Discord for community support.
- **Constraints:** The tool landscape changes quickly, course content must remain maintainable, AI help must stay grounded in repository knowledge, and implementation should remain modular for future expansion.
- **Expected deployment type:** Public-facing course site plus hosted backend services.

# Current Phase of Work
**Phase 1 — Backend design transition**

The repository now contains project governance docs, a fuller seven-day course curriculum skeleton, MkDocs configuration, a Tool Vault maintenance workflow, backend design docs, a first FastAPI backend skeleton, and lightweight validation tests.
The repository now also contains a first Markdown ingestion pipeline.
The repository now also contains a first grounded retrieval workflow behind the chat endpoint.
The repository now also supports optional Gemini-based answer synthesis on top of retrieved repository snippets when explicitly enabled.
The current backend default Gemini model is `gemini-2.5-flash`, while local `.env` settings may still override it.
The backend now declines personal identity questions before retrieval so irrelevant repository citations are not returned for non-course queries.
That personal-question guard now also handles simple punctuation typos in name-related queries.
When retrieval finds no chunks, Gemini can now answer broader in-scope filmmaking questions without citations while still refusing out-of-scope topics.
Backend package logs now emit at `INFO` level so local terminals show whether answers came from Gemini, local grounding, scoped Gemini, or out-of-scope handling.
An `AI_DIRECTOR_VERBOSE_LOGGING` environment flag now allows full Gemini prompt and response logging during local debugging.
Backend startup now logs the active Gemini and verbose settings so local observability can be verified immediately after launch.
The retrieval index now refreshes automatically when course or docs Markdown files change.
The repository now also contains a first website chat widget design.
The repository now also contains a first website chat widget integration on the public site.
The active next step is to improve retrieval quality and then extend support into Discord and deployment workflows.

# Files That Define Truth
Read these in order:
1. [docs/tasks.md](tasks.md)
2. [docs/design/design.md](design/design.md)
3. Relevant design subdocuments, if they are added later
4. Research context in [docs/research/research-notes.md](research/research-notes.md) when strategy history is needed

# Restarting AI Sessions
When starting a fresh AI session:
1. Read this file completely.
2. Read [docs/tasks.md](tasks.md) and identify the active task ID.
3. Read [docs/design/design.md](design/design.md) and any linked subdocuments relevant to that task.
4. Inspect the relevant implementation files only after the docs are understood.
5. Summarize the current intent, current phase, and minimal next step before editing anything.

# Starting New Tasks
1. Find or create the target task in [docs/tasks.md](tasks.md).
2. Confirm acceptance criteria, dependencies, and validation approach.
3. Review [docs/design/design.md](design/design.md) for architecture and content constraints.
4. Make the smallest reviewable change set possible.
5. Update documentation after implementation.

# Task Kickoff Script
> Read docs/START_HERE.md, then docs/tasks.md,
> then docs/design/design.md,
> then the relevant design subdocuments if they exist.
>
> Summarize the current project intent and phase.
>
> Ask clarifying questions ONLY if required.
>
> Then propose a minimal, reviewable implementation plan.

# Repository Layout Snapshot
- [docs](.) — internal project source of truth
- [course](../course) — public-facing MkDocs course content
- [backend](../backend) — Python backend package and dependency list
- [overrides](../overrides) — MkDocs theme override files for site customization
- [tests](../tests) — starter validation tests
- [mkdocs.yml](../mkdocs.yml) — static site configuration
- [.vscode/tasks.json](../.vscode/tasks.json) — local task runner shortcuts

# Immediate Next Steps
1. Revisit vector-store and embedding integration as retrieval quality needs increase.
2. Improve citation formatting and learner-facing source handling as the widget matures.
3. Reuse the same grounded backend logic later for Discord support.
4. Document deployment workflow for both the static site and backend service.
