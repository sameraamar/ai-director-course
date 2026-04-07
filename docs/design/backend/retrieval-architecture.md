# Purpose
This document defines the planned ingestion and retrieval architecture for the AI Director Course backend assistant.
It exists to give humans and AI agents a grounded design for how repository knowledge will be chunked, embedded, stored, retrieved, and passed into answer generation.
AI agents must read this document before implementing backend ingestion, retrieval, or chat-answering code.

# Maintenance Instructions
Update this document when the backend assistant design changes, especially around chunking, embeddings, vector storage, retrieval ranking, or grounding rules.
Humans and AI agents may both maintain it, but changes should remain tightly tied to the corresponding backend tasks in [docs/tasks.md](../../tasks.md).
Keep it aligned with [docs/design/design.md](../design.md), future backend implementation files, and validation tests.

## Purpose of this Document
This document is part of the modular project design documentation.
It captures the current understanding of this domain area.
Content may be incomplete early in the project.
Keep this document up-to-date as implementation evolves.
AI agents must read this before implementing related tasks and update it after completing them.

# Scope
This document covers the backend assistant's knowledge pipeline for:
- loading repository documentation and public course Markdown
- splitting documents into retrieval-friendly chunks
- generating embeddings
- storing and querying vectors
- grounding answer generation in retrieved repository context

It does not yet define:
- final deployment infrastructure
- authentication
- rate limiting
- front-end widget behavior
- Discord bot runtime details

# Design Goals
- Keep the assistant grounded in repository-owned knowledge.
- Make ingestion simple enough to run locally during development.
- Support incremental document updates without rebuilding everything manually.
- Preserve citations back to source files and headings.
- Keep the first implementation cheap, inspectable, and easy to test.

# Knowledge Sources
## Included sources for MVP
- `/course/**/*.md` public lesson content
- `/docs/**/*.md` internal governance and design content that is safe and useful for maintainer-focused assistant behavior

## Exclusion guidance
The ingestion pipeline should skip or optionally exclude:
- generated caches
- virtual environment folders
- binary assets
- temporary exports
- future build output folders

## Source categories
Each chunk should retain a `source_category` value such as:
- `course`
- `design`
- `tasks`
- `research`
- `templates`

This supports filtering and later policy decisions.

# Document Normalization
Before chunking, normalize documents by:
- reading UTF-8 Markdown content
- preserving heading hierarchy when possible
- stripping repeated boilerplate only if it harms retrieval quality
- preserving relative file path metadata
- preserving section titles for citations

The pipeline should not aggressively rewrite content.
It should keep chunks close to the authored text so citations remain trustworthy.

# Chunking Strategy
## Recommended chunk unit
Use heading-aware Markdown chunking first.

Preferred order:
1. split by major headings
2. keep smaller subheadings grouped with their content when the result remains reasonably sized
3. apply a size cap only when a section is too large

## Target chunk size
Initial target:
- approximately 400 to 900 words per chunk
- with small overlap only when splitting a large section

## Overlap guidance
- No overlap is needed when the chunk is already a coherent heading section.
- Use light overlap only for long sections that must be subdivided.
- Recommended initial overlap: 50 to 100 words.

## Metadata per chunk
Each stored chunk should include at minimum:
- `chunk_id`
- `path`
- `title`
- `section_heading`
- `source_category`
- `content_hash`
- `updated_at` or ingestion timestamp
- `ordinal_within_file`

## Why heading-aware chunking
The repository is documentation-first.
Meaning is strongly tied to headings, task IDs, and section structure.
Heading-aware chunking preserves that structure better than raw fixed-size token windows.

# Embedding Strategy
## Model direction
Use a Gemini-compatible embedding workflow if available in the chosen API path.
If Gemini embedding support is not practical for the first implementation, use a well-supported Python embedding fallback that can be swapped later.

## Embedding design requirements
- deterministic enough for repeatable local indexing
- affordable for iterative document updates
- compatible with local persistence
- able to embed Markdown-derived natural language well

## Embedding granularity
Embed each chunk individually after normalization and chunking.
Do not embed whole files as one vector for the MVP.

# Vector Store Decision
## MVP recommendation
Use ChromaDB as the default MVP vector store.

## Why ChromaDB first
- simple local developer setup
- persistent storage without custom index management
- metadata filtering support
- inspectable during early debugging
- good fit for a documentation-heavy local-first workflow

## Alternative kept open
FAISS remains a valid later option for:
- custom ranking workflows
- lower-level performance tuning
- more specialized deployment constraints

For the current phase, ChromaDB is the preferred starting point because developer ergonomics matter more than maximum control.

# Retrieval Flow
## Query-time steps
1. receive user question
2. classify or tag the request lightly if needed
3. embed the query
4. retrieve top candidate chunks from the vector store
5. optionally apply metadata filters
6. optionally re-rank for relevance and source diversity
7. build a grounded context packet for answer generation
8. return an answer with citations or a scoped refusal

## Retrieval defaults for MVP
- retrieve top `k` chunks, initially around 4 to 8
- prefer diversity across files when near-duplicate chunks appear
- preserve chunk ordering within a file when adjacent sections are both selected

## Candidate filtering rules
Potential first-pass filters:
- prefer `course` content for learner-facing questions
- include `design` or `tasks` content for maintainer-facing or system questions
- exclude low-value template content unless the question is clearly about workflow templates

# Grounded Answer Rules
The assistant must behave as a repository-grounded teaching assistant.

## Current implementation note
The current backend supports two synthesis modes:
- a default local synthesis path that rewrites retrieved chunks into concise repository-backed answers
- an optional Gemini synthesis path that receives retrieved snippets and produces the final answer when explicitly enabled

The Gemini path must still remain grounded in retrieved repository context and should fall back to local synthesis if the model call fails.

## System behavior requirements
- answer from retrieved repository context first
- avoid presenting unsupported claims as facts
- say when the answer is outside the current repository scope
- preserve the course's workflow orientation and tool-agnostic tone when possible
- cite relevant source paths or sections in the final response format when implemented

## Refusal / deferral behavior
If retrieval does not provide sufficient support, the assistant should respond with a constrained answer such as:
- the question is outside the current 7-day sprint scope
- the repository does not yet document that detail
- a maintainer decision is still To Be Discovered

## Hallucination boundary
The assistant may use natural language to explain retrieved content, but it should not invent:
- undocumented tool endorsements
- hidden lesson steps
- backend behaviors not present in the docs
- policy claims not backed by repository text

# Citation Requirements
Each answer-ready context packet should preserve enough metadata to cite:
- file path
- section heading
- optional task ID or lesson day

The first backend implementation may return simple file-path citations.
Later iterations can improve citation formatting for the website and Discord.

# Ingestion Workflow
## Full ingest mode
Use this when:
- setting up the vector store for the first time
- changing chunking rules
- changing embedding models
- repairing a corrupted or invalid index

## Incremental ingest mode
Use this when:
- only a subset of Markdown files changed
- content hashes indicate which chunks need refreshing

## Recommended ingestion steps
1. enumerate included Markdown files
2. normalize content
3. split into chunks
4. compute chunk hashes
5. skip unchanged chunks when running incrementally
6. generate embeddings for new or changed chunks
7. upsert into the vector store
8. remove stale chunks when source content no longer exists

# Data Model Sketch
## Suggested Python-level entities
- `SourceDocument`
- `DocumentChunk`
- `EmbeddingRecord`
- `RetrievalResult`
- `GroundedContextPacket`

## Minimal fields
### `SourceDocument`
- `path`
- `source_category`
- `raw_text`
- `content_hash`

### `DocumentChunk`
- `chunk_id`
- `path`
- `section_heading`
- `text`
- `ordinal_within_file`
- `content_hash`

### `RetrievalResult`
- `chunk_id`
- `score`
- `path`
- `section_heading`
- `text`

# Async Architecture Notes
The future FastAPI service should keep ingestion and query logic separate.

Recommended separation:
- ingestion module for scanning and indexing
- retrieval module for query-time vector search
- orchestration module for answer assembly
- API layer for HTTP endpoints

At query time, async behavior should primarily help with:
- network calls to model providers
- concurrent request handling
- possible future parallel retrieval or reranking steps

The vector store access itself may remain synchronous if the chosen library makes that simpler for the MVP.

# Constraints and Edge Cases
- Some repository docs are written for maintainers, not learners.
- Repeated boilerplate across docs may create noisy retrieval if not monitored.
- Future lesson growth may require smarter chunk merging or filtering.
- Public and internal docs may eventually require separate retrieval policies.
- The system must degrade gracefully when embeddings or model APIs are temporarily unavailable.

# Validation Strategy
The first backend design validation should remain lightweight.

Minimum validation expectations:
- design doc exists and is linked from the design index
- tests assert the presence of key architecture sections
- later implementation tasks add unit tests for chunking and retrieval behavior

# Implementation Sequence
1. finalize this design
2. create backend package layout decision
3. implement API skeleton with health and chat contracts
4. implement ingestion pipeline against repository Markdown
5. implement grounded retrieval flow
6. connect the website widget and later Discord integration

# Open Decisions
- exact Gemini embedding API choice and SDK shape
- whether learner-facing and maintainer-facing retrieval should be separated at the API level
- whether reranking is needed in the MVP or can wait until retrieval quality is measured
- how citation formatting should appear in the website assistant UI
