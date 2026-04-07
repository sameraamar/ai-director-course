# Purpose
This page is the public Tool Vault for the AI Director Course.
It exists to centralize change-prone tool recommendations so the core lessons can remain stable even as the AI tooling landscape evolves.
AI agents should update this page instead of hard-coding specific vendor recommendations into lesson content whenever possible.

# Maintenance Instructions
Update this page whenever recommended tools, pricing tiers, categories, or replacement guidance changes.
Humans and AI agents may both maintain it, but updates should stay grounded in current course needs and remain easy to scan.
Keep lesson pages focused on workflow concepts and use this page as the canonical tool reference.

# Tool Vault
Use this page as the canonical source for current recommended tools.

## Selection Rules
- Favor reliable tools with clear free or starter tiers when possible.
- Prefer tools that support export quality suitable for ads, portfolios, or e-commerce use.
- Replace outdated tools here instead of rewriting every lesson.

## Tool Categories
| Workflow Area | Free / Starter-Friendly | Paid / Pro-Oriented | Notes |
| --- | --- | --- | --- |
| Storyboarding / Planning | Gemini (Standard) / ChatGPT (Free) | Gemini Advanced / ChatGPT Plus | Use the Day 1 'Director's Blueprint' prompt to break ideas into 5-shot sequences. |
| Image Generation | Leonardo.ai | Midjourney ($10/mo) | Leonardo offers great daily credits for practicing Style Reference (SREF). Midjourney is strictly for final production and Character Consistency (CREF). |
| Image-to-Video | Kling AI / Minimax | Runway Gen-3 / Luma Dream Machine | Kling has the most usable daily free tier right now. Runway is unmatched for multi-shot final cinematic physics. |
| Voice / Dialogue | ElevenLabs (Free Tier) | ElevenLabs (Creator Tier) | The free tier allows 10,000 characters/month, which is more than enough to voice a 60-second trailer. |
| Lip Sync | Kling AI / HeyGen (Trial) | SyncLabs / HeyGen (Pro) | Prioritize lip-sync only if the character is speaking directly to the camera in the shot. |
| Music | Suno (Basic) | Udio / Suno Pro | Suno gives 50 free credits daily (10 songs), which perfectly fits the daily sprint pacing model. |
| Sound Effects / Foley | Freesound.org / Pixabay | Envato Elements / Artlist | Critical for realism. Always add "whooshes" for camera movements and ambient room tone. |
| Editing / Finishing | CapCut (Desktop) | Premiere Pro / DaVinci Resolve | CapCut's free desktop version does 99% of what a learner needs (timeline, basic LUTs, audio syncing). |
| Upscaling | CapCut (Built-in Enhancer) | Topaz Video AI | Prioritize upscaling only on Day 7 to push the final 720p/1080p clips to crisp 4K. |

## Update Checklist
When changing this page:
1. Verify the workflow category still matches current curriculum needs.
2. Note whether the tool is best for free exploration or paid production work.
3. Avoid making the lessons depend on a single vendor if the concept can stay tool-agnostic.
4. Record major changes in internal planning docs when the update affects course flow.

## Maintenance Workflow
### Ownership
- Humans or AI agents may update this page.
- The updater is responsible for keeping categories, labels, and notes consistent with the curriculum.
- When a tool change would alter how a lesson is taught, update the relevant internal docs in `/docs` as well.

### Update Cadence
Review this page:
- before major curriculum refreshes
- when a recommended tool becomes unavailable or unreliable
- when pricing or access changes materially affect learners
- when a new category becomes necessary for the sprint

### Evaluation Criteria
When considering a tool, assess:
- accessibility for beginners
- output quality
- consistency controls
- export flexibility
- reliability and ease of iteration
- fit for the specific workflow stage

### Change Rules
- Prefer replacing entries in this page instead of rewriting lesson pages.
- Keep lesson language workflow-focused and tool-agnostic where possible.
- If no current recommendation is ready, keep `To Be Discovered` rather than guessing.

### Suggested Change Process
1. Confirm the workflow category.
2. Check whether the tool is best labeled free/starter-friendly or paid/pro-oriented.
3. Write or revise the note so it explains *why* the tool fits.
4. Review lesson pages only if the workflow itself has changed.
5. Record any meaningful curriculum impact in internal planning docs.

## Content Ownership Notes
- Category structure is the canonical public abstraction layer.
- Specific vendors are optional and should be added only when the recommendation is stable enough to help learners.
- Lesson pages should reference categories or capabilities more often than brand names.

## Change Log Template
Use this note format internally when a major Tool Vault update affects the course:

```text
Date:
Category updated:
What changed:
Why it changed:
Lesson impact:
Follow-up docs updated:
```
