# Purpose
This document records source research, planning inputs, and evolving assumptions for the AI Director Course project.
It exists to preserve strategic context that should not be lost between AI sessions or contributor handoffs.
AI agents should consult this file when they need background on why the current direction was chosen.

# Maintenance Instructions
Update this file when new strategic discussions, external references, or major planning assumptions are introduced.
Humans and AI agents may both add notes, but entries should stay concise and traceable.
Keep it consistent with [docs/design/design.md](../design/design.md) and [docs/tasks.md](../tasks.md).

# Source Inputs Captured So Far
## Repository bootstrap instruction
The repository began from a documentation-first bootstrap requirement that mandates:
- `/docs` as the internal source of truth
- task-driven implementation
- strong AI-session restartability
- small, reviewable diffs

## Initial product blueprint
The current product direction was consolidated from an external planning discussion with these main themes:
- Public docs-as-code course site
- Tool Vault abstraction layer
- Python async backend assistant with retrieval grounding
- Discord community and support layer
- Seven-day sprint curriculum focused on producing a cinematic short video

# Consolidated Project Goals
1. Launch a maintainable course platform quickly.
2. Keep curriculum stable while tool recommendations evolve independently.
3. Prepare for a grounded AI teaching assistant without locking into a heavy architecture too early.
4. Preserve enough documentation that future implementation can restart without previous chat history.

# Working Assumptions
- MkDocs Material is the preferred static-site foundation.
- Course pages will be authored in Markdown.
- Public course content should stay separate from internal project-governance docs.
- The backend and Discord bot should eventually share retrieval logic.
- Deep implementation details will be added only when corresponding tasks move to active status.

# Risks to Watch
- Tool recommendations may age quickly.
- Retrieval quality will depend on content structure and chunking quality.
- A public course site and internal docs may need separate publishing rules.
- Overbuilding the backend before solidifying curriculum could create rework.

# Open Research Threads
- Compare local vector-store options for developer ergonomics and hosted deployment.
- Decide how to stream grounded answers into the website.
- Define a Discord moderation and role-automation model.
- Establish lesson-writing conventions for Fast Track and Deep Dive sections.
