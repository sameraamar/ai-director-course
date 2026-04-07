# Purpose
This document is the top-level design overview for the AI Director Course project.
It exists to capture product intent, architecture, constraints, and implementation direction in one stable place before the design is split into smaller subdomains.
AI agents should read this file before working on any feature and update it when project behavior or architectural decisions change.

# Maintenance Instructions
Update this document whenever project scope, architecture, tech stack, constraints, testing strategy, or deployment plans change.
Humans and AI agents both maintain it, and it should remain the design index even if future subdocuments are added.
Keep it aligned with [docs/tasks.md](../tasks.md), [docs/START_HERE.md](../START_HERE.md), and any future design subfolders.

## Purpose of this Document
This document is part of the modular project design documentation.
It captures the current understanding of this domain area.
Content may be incomplete early in the project.
Keep this document up-to-date as implementation evolves.
AI agents must read this before implementing related tasks and update it after completing them.

# Product Vision
AI Director Course is a documentation-first course platform that teaches students how to create a cinematic AI video in seven days.
The product combines public curriculum content, a maintainable catalog of current tools, and a future retrieval-grounded assistant that answers student questions using repository knowledge only.

# Current Design State
- The repository is in a bootstrap state.
- Internal governance and planning docs live under `/docs`.
- Public course content for the static site lives under `/course`.
- Day 1 now has a more complete lesson structure that future curriculum days should mirror where appropriate.
- The seven public lesson pages now form a fuller curriculum skeleton with reusable workflow patterns, troubleshooting, and checkpoints.
- The public Tool Vault now defines an explicit maintenance workflow for change-prone tool recommendations.
- A dedicated backend design document now defines the ingestion and retrieval architecture for the future assistant.
- A backend package layout decision now exists and the first FastAPI API skeleton is implemented.
- A first Markdown ingestion pipeline now exists and writes a structured local index artifact for retrieval development.
- A first grounded retrieval workflow now powers the chat endpoint using the local ingestion index and repository citations.
- The grounded retrieval workflow now also supports an optional Gemini synthesis layer for final answer generation when explicitly enabled.
- The current backend default Gemini model is `gemini-2.5-flash`, with local `.env` overrides still supported.
- Gemini synthesis now uses the `google-genai` Python client for model calls.
- Transient Gemini API failures now use a brief retry path before the service falls back to local synthesis.
- Personal identity questions that fall outside repository scope are declined before retrieval so irrelevant course citations are not returned.
- Personal-question detection now normalizes simple punctuation typos before retrieval decisions are made.
- If retrieval finds no repository chunks, Gemini may still answer broader in-scope filmmaking questions, but those responses are explicitly non-grounded and carry no citations.
- Runtime observability now forces the `ai_director_backend` logger to `INFO` so answer-path decisions are visible in local development logs.
- A local `AI_DIRECTOR_VERBOSE_LOGGING` flag now enables full Gemini prompt and response logging for debugging model behavior.
- Backend runtime logs are now attached to Uvicorn's error logger and include a startup configuration line for quick local verification.
- The retrieval layer now treats the local ingestion index as disposable cache and rebuilds it automatically when Markdown source files become newer than the saved index.
- Generated ingestion metadata is now portable and avoids embedding workstation-specific absolute filesystem paths.
- A dedicated website chat widget design now defines the planned learner-facing UI and integration path for the public site.
- The public site now includes a first chat widget integration path through MkDocs assets, theme override configuration, and backend CORS support for local development.
- Discord integration is still planned but not yet implemented.

# Personas
## Primary learners
- Solo creators building portfolio-ready short films or ads
- E-commerce operators building product videos
- Marketers creating social ads quickly

## Secondary operators
- Course maintainers who update curriculum and tool recommendations
- AI agents that must resume work from repository documentation alone

# Natural Language Specifications
- The course should guide a learner from idea to finished 30-to-60-second cinematic video in seven days.
- Every day should support a two-speed pacing model: a fast execution path and deeper supporting material.
- Core lessons should avoid hard-coding vendor recommendations so the curriculum stays stable while the Tool Vault changes.
- The future assistant must answer only from repository-backed knowledge and should avoid hallucinating external guidance.
- Internal documentation must remain strong enough to restart implementation without chat history.

# High-Level Architecture
## 1. Public course layer
- Static site generated with MkDocs Material.
- Source content stored as Markdown in `/course`.
- Navigation defined in [mkdocs.yml](../../mkdocs.yml).
- Search and theme capabilities handled by the static site generator.
- The current site integration plan loads a lightweight chat widget through MkDocs theme override configuration and static assets.
- Site-wide author credit and repository attribution are configured through MkDocs metadata so the footer identifies the course author on every page.

## 2. Internal project-governance layer
- Planning, design, research, and task state stored in `/docs`.
- This layer is not the public curriculum; it is the implementation source of truth.
- AI agents must read this layer before touching code.

## 3. Planned backend assistant layer
- Python service, likely FastAPI-based.
- Async request handling with `asyncio` to support concurrent learners.
- Retrieval-Augmented Generation over repository Markdown content.
- Initial likely components: ingestion script, embedding store, retriever, grounded answer service, and API endpoints.
- Detailed retrieval design now lives in [docs/design/backend/retrieval-architecture.md](backend/retrieval-architecture.md).
- Backend package layout and test conventions now live in [docs/design/backend/package-layout.md](backend/package-layout.md).
- Current implemented skeleton lives under `/backend/ai_director_backend` and exposes health and chat contract endpoints.
- Current ingestion implementation performs heading-aware Markdown chunking and writes a local structured index artifact that later retrieval tasks can build on.
- Current grounded retrieval implementation uses the local index artifact and a lightweight lexical ranking approach to return repository-backed answers with citations.

## 4. Planned community layer
- Discord server for asynchronous peer support.
- Administrative automation can be delegated to existing moderation tools.
- Custom bot behavior should reuse the same grounded knowledge logic as the website assistant.

# Architectural Patterns
- Docs-as-code for both public curriculum and internal execution memory.
- Content abstraction via a centralized Tool Vault.
- Modular design that starts simple and splits only when a domain grows large enough.
- Small-diff implementation workflow enforced through repository instructions.

# Curriculum Structure Guidance
- Each lesson should include a clear outcome, execution-oriented Fast Track steps, and deeper explanatory material.
- Where useful, lessons should include reusable prompt structures, troubleshooting guidance, a learner checkpoint, and a handoff into the next day.
- Day 1 establishes the target baseline for richer lesson detail while preserving tool-agnostic workflow guidance.
- Day 2 establishes that subject consistency, style consistency, and reference-driven image selection should be locked before motion generation begins.
- Day 3 establishes that motion prompts should favor one dominant motion idea, stable physics, and edit-ready clip selection over ambitious but fragile animation.
- Days 4 through 7 establish that optional voice, selective sound design, disciplined editing, and honest final review are part of the course's default production workflow.
- A lightweight placeholder-audit test can be used to track unresolved screenshot or asset markers across `/course` before public launch.
- The current course pages now include a first pass of embedded mock screenshots with alt text and captions, giving the lessons usable staging visuals before real product captures are collected.

# Tool Vault Governance
- The Tool Vault is the public abstraction layer for fast-changing vendor recommendations.
- Lesson content should remain focused on capabilities and workflow logic rather than depend heavily on specific brands.
- Tool Vault updates should capture category fit, learner accessibility, and whether a change affects curriculum guidance.

# Tech Stack
- **Frontend / docs site:** MkDocs Material
- **Public content format:** Markdown
- **Backend language:** Python
- **Planned backend framework:** FastAPI
- **Planned retrieval layer:** ChromaDB first for the MVP, with FAISS still available as a later alternative
- **Planned model provider:** Gemini API
- **Community platform:** Discord

# Constraints and Edge Cases
- AI tool recommendations change rapidly; Tool Vault updates must be isolated from lesson logic.
- The course must be understandable even if a learner skips the deep-dive sections.
- The assistant should refuse or defer when repository knowledge does not contain the answer.
- Future design subdocuments may be needed for backend ingestion, chat UX, Discord operations, and curriculum standards.
- Compliance, security, privacy, and hosting constraints are currently To Be Discovered.

# Non-Functional Requirements
- Repository docs must support fresh-session AI recovery.
- Site content should remain easy to edit by non-developers using Markdown.
- Backend services should be modular, observable, and cheap to iterate on.
- Validation should begin with lightweight tests and expand with implementation complexity.

# Testing Strategy
- Current conventional test location: `/tests`.
- Bootstrap validation uses a simple scaffold smoke test.
- Backend API validation currently uses lightweight endpoint contract tests under `/tests`.
- Backend ingestion validation currently uses lightweight unit tests for chunking and index generation under `/tests`.
- Site integration validation currently uses lightweight configuration checks plus MkDocs build verification.
- Backend, site build, and retrieval tests will be added as implementation begins.
- If any area intentionally defers testing, that decision must be documented in [docs/tasks.md](../tasks.md).

# Deployment Direction
- Planned static hosting: GitHub Pages, Vercel, or similar static host.
- Planned backend hosting: Render, Railway, or similar Python-friendly platform.
- A first GitHub Actions workflow now exists for deploying the MkDocs site to GitHub Pages from source.
- Final deployment decisions are To Be Discovered.

# Future Split Candidates
This document remains the top-level design index until one of these areas justifies its own subdocument:
- Curriculum standards and lesson-writing rules
- Backend ingestion and retrieval architecture: [docs/design/backend/retrieval-architecture.md](backend/retrieval-architecture.md)
- Backend package layout and module responsibilities: [docs/design/backend/package-layout.md](backend/package-layout.md)
- Chat widget integration: [docs/design/chat-widget/website-chat-widget.md](chat-widget/website-chat-widget.md)
- Discord bot operations
- Deployment and infrastructure

# Open Questions
- Which vector store should be the default for local and hosted environments?
- Should private maintainer docs stay separate from public course content at deploy time?
- Which authentication model, if any, is needed for student-facing support features?
- What analytics are required to measure learner completion and support demand?
