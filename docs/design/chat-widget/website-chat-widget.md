# Purpose
This document defines the planned website chat widget approach for the AI Director Course public site.
It exists to guide humans and AI agents when integrating the grounded backend assistant into the MkDocs-based learner experience.
AI agents must read this document before implementing frontend chat UI, backend-to-frontend contracts, or site theme overrides related to chat.

# Maintenance Instructions
Update this document when the widget UX, backend contract, embedding strategy, site integration path, or deployment constraints change.
Humans and AI agents may both maintain it, but changes should remain aligned with [docs/tasks.md](../../tasks.md), [docs/design/design.md](../design.md), and the backend assistant design documents.
Keep it synchronized with future widget implementation files and any theme override assets added to the public site.

## Purpose of this Document
This document is part of the modular project design documentation.
It captures the current understanding of this domain area.
Content may be incomplete early in the project.
Keep this document up-to-date as implementation evolves.
AI agents must read this before implementing related tasks and update it after completing them.

# Scope
This document covers:
- learner-facing chat widget UX on the public course site
- frontend-to-backend request and response expectations
- MkDocs integration approach
- progressive enhancement and fallback behavior
- basic security and operational boundaries for the widget

This document does not yet define:
- production authentication
- payment or account-gated access
- analytics implementation details
- Discord UI behavior

# Design Goals
- Keep the learner support experience lightweight and unobtrusive.
- Make the chat widget usable without turning the docs site into a heavy application.
- Preserve the documentation-first character of the site.
- Keep the frontend integration simple enough to maintain in a theme override.
- Support grounded answers with visible citations back to repository-backed content.

# Current Implementation Status
- The first implementation uses `overrides/main.html` to inject runtime widget configuration.
- Widget behavior lives in `course/assets/javascripts/chat-widget.js`.
- Widget styling lives in `course/assets/stylesheets/chat-widget.css`.
- Local development currently assumes MkDocs on `http://127.0.0.1:8000` and the backend API on `http://127.0.0.1:8001`.
- The widget currently sends non-streaming learner-mode requests to `/api/chat`.

# UX Model
## Widget style
Use a small launcher button and expandable panel pattern.

## Why this pattern
- does not interrupt reading by default
- works well on documentation sites
- supports progressive enhancement
- can remain lightweight without a full SPA framework

## Expected learner flow
1. learner reads course content
2. learner opens the chat launcher from any course page
3. learner asks a question about the current sprint or workflow
4. frontend sends the question to the backend assistant
5. widget renders the response and any citations
6. learner can jump back to cited content if needed

# Initial UX Requirements
## Launcher behavior
- visible but not dominant
- anchored near the lower corner of the page
- labeled clearly, such as "Ask the course assistant"

## Panel behavior
- opens without navigating away from the lesson
- keeps a short local conversation history during the current page session
- supports scrolling within the panel
- allows the learner to dismiss or reopen the widget easily

## Message rendering
- render assistant replies as Markdown-safe rich text where practical
- render citations as clickable links when possible
- make out-of-scope replies clear and non-defensive

## Input behavior
- single text input plus send action
- basic disabled/loading state during requests
- optional enter-to-send behavior
- prevent empty submissions

# Backend Contract Expectations
## Initial request shape
Frontend should POST JSON to the backend chat endpoint using the existing contract:

```json
{
  "question": "How do I create a 5-shot storyboard?",
  "user_mode": "learner"
}
```

## Initial response shape
Frontend should expect:

```json
{
  "question": "How do I create a 5-shot storyboard?",
  "answer": "...",
  "grounded": true,
  "status": "grounded",
  "citations": ["course/day-1-storyboard.md#Day 1 — The Director's Blueprint"]
}
```

## Response handling rules
- if `status` is `grounded`, render the answer and citations
- if `status` is `out_of_scope`, render the answer clearly and avoid fake citations
- future streaming support should be additive, not required for the first integration

# MkDocs Integration Path
## Preferred implementation approach
Use a MkDocs Material theme override with a small custom JavaScript file and matching CSS.

## Why this approach
- keeps the public site mostly static
- avoids introducing a heavyweight frontend build system too early
- stays aligned with docs-as-code maintenance
- makes the widget easy to inspect and update

## Expected file areas when implementation begins
Potential implementation files may include:
- `/overrides/main.html`
- `/overrides/partials/`
- `/docs-assets/` or equivalent static asset location for widget JavaScript and CSS

The exact asset path should follow MkDocs Material conventions when task `5.2` begins.

# Frontend State Model
## Minimal state
The first implementation only needs:
- `isOpen`
- `messages`
- `isLoading`
- `errorMessage`

## Message shape
Each rendered message should track:
- role: learner or assistant
- text content
- citations if present
- status if needed for styling

# Citation UX
## Citation behavior
- display citations below the assistant response
- prefer human-readable labels when possible
- allow link navigation back to site content when the citation maps to a public course page

## Internal-doc handling
If a future answer cites internal docs not published publicly, the frontend should either:
- suppress direct links and show a plain source label
- or filter such citations out for learner-facing mode

The learner-facing website should prioritize public course citations.

# Error and Fallback Behavior
## Request failures
If the backend request fails:
- show a short retry-friendly message
- keep the learner's typed question visible if possible
- do not silently clear the panel

## Backend unavailable
Fallback copy should explain that the assistant is temporarily unavailable and the learner can continue with the lesson content.

## No-JavaScript fallback
The site must remain fully usable without the chat widget.
The widget is an enhancement, not a requirement for reading the course.

# Security and Operational Boundaries
## Frontend safety
- do not expose secrets in frontend code
- treat backend URL configuration as environment-driven or build-configured
- sanitize or constrain rendered Markdown as needed

## Abuse considerations
The first version may rely on backend-side rate limiting later, but the widget should still:
- disable repeated rapid submissions while a request is in flight
- avoid rendering raw untrusted HTML

# Accessibility Guidance
- launcher must be keyboard reachable
- panel controls must have visible labels
- sufficient color contrast is required
- loading and error states should be understandable to screen readers where practical

# Testing Strategy
Initial validation for the design phase should remain lightweight.

Minimum expectations:
- this design doc exists and is linked from the top-level design index
- tasks reference the widget design decision
- future implementation task `5.2` should add frontend integration tests or smoke checks where practical

# Recommended Implementation Sequence
1. finalize this widget design
2. confirm public asset location for MkDocs theme overrides
3. implement launcher, panel markup, and styling
4. connect POST requests to the backend chat endpoint
5. render grounded answers and citations
6. add graceful error handling and lightweight smoke checks

# Open Questions
- Should the widget be available on every page or only course lesson pages?
- Should conversation history persist across page navigation or stay per-page-session only?
- How should internal-only citations be represented in learner-facing mode if they appear?
- Is response streaming needed early, or can it wait until after the first non-streaming widget release?
