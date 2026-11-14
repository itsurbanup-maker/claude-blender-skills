---
name: os-skills-routines
description: Design the skill backbone and the scheduled routines of an agentic OS - find which skills to create from your Claude Code logs and a voice brain-dump, the three skill types (database, artifact, self-triggered via claude -p), wildcards against over-fitting, routing each skill to the cheapest model, self-improving skills, active vs passive routines, capping expensive routines, and a weekly routine that suggests new routines. Includes ready-to-use /note, /calibrate, /wildcard and /cleanup skill templates. Use when someone asks which skills or automations to build, how to organise their skills, why their usage drains, or how to make skills get better over time.
---

# Skills and routines for an agentic OS

To install a template: `mkdir -p ~/.claude/skills/note && cp templates/note.md ~/.claude/skills/note/SKILL.md` (same for the others).

## Find the skills (no need to know them up front)

1. **Logs.** Claude Code keeps every conversation from the last 30+ days. Prompt:
   *"Look at how I have used you over the last 30 days. Which tasks repeat? Turn them into skills, and tell me which of
   those should run on a schedule."*
2. **Brain-dump.** Open the mic and talk 10-20 minutes about your day and week (stream of consciousness is fine). Then:
   *"Based on everything I just told you, which skills or automations would take work off my plate?"*
3. Group the result by area (productivity, research, content, clients, sales, finance, personal). Most people have all of these.
4. Every skill and automation writes its deliverable where the dashboard reads it.

## Level 1 - know the three skill types

- **Database skills** hold knowledge, not steps: your tone of voice (principles + examples), a thumbnail reference library
  (file paths + why each works), a client's data locations. `SKILL.md` acts as a router: it says where each kind of
  information lives so Claude reads only what the prompt needs. For visual databases, keep an artifact that shows the
  current references.
  - **Over-fitting**: references make the agent copy them and stop inventing. Fix: by default, part of every batch is a
    **wildcard** that ignores the references (e.g. 8 of 10 titles from references, 2 free). Good wildcards get promoted into
    the database. Keep the definition in a tiny `/wildcard` skill that other skills point to (`templates/wildcard.md`).
- **Artifact skills** produce things that do not belong in a chat: infographics, decks, PDFs. Make them in **HTML first**
  (agents are very good at it) and export to PDF. Back it with a **design-system skill** and an HTML brand book (colours,
  fonts, components) so nothing looks vibe-coded. Park every artifact in an artifacts inbox you can search without tokens.
- **Self-triggered skills** run outside the chat, from a button or a schedule, through headless Claude:
  `claude -p --model haiku "/cleanup"` (prints a short report of what it fixed). Example: `/cleanup` for temp files and stray
  processes when the machine slows down (`templates/cleanup.md`). Let the button choose model and effort.

## Level 2 - route skills to the cheapest model that does the job

- Skills with a clear-cut process (spell check, filing, formatting) run fine on Haiku or Sonnet. Set it in the skill
  (`model: haiku` in the front matter where supported) or route with Jev (`jev-router`).
- Keep a view of **most-used skills and their token cost**. The heaviest one (often an animation/video skill) is the first to
  optimise; skills you never use are retired.

## Level 3 - skills that improve themselves

- Whenever you give feedback while using a skill, also update the skill. In a review micro-app, add a toggle
  "teach /cut and /animate": when on, the copied comments carry an extra line asking Claude to fold the lessons into those
  skills. Simple reinforcement learning on your own setup.
- `/note <feedback>` - mid-job ideas for later. Haiku appends them to a per-skill backlog file; apply the whole backlog when
  you have spare usage (e.g. just before the weekly limit resets). Fixing mid-job loses the thread. (`templates/note.md`)
- `/calibrate <feedback>` - for feedback that must stick: save it to memory, link related memories, and fix the skill it
  belongs to right away. (`templates/calibrate.md`)

## Routines (scheduled tasks)

- **Level 1 - active vs passive.** Active routines hand you an output to review (daily inbox digest on Telegram, morning
  brief). Passive routines run quietly and only ping when they find something: brand watch (sites using your brand without
  approval), domain/TLD scout, machine health. With 50 routines, if all were active you would review 50 things a day.
- **Level 2 - capped routines.** Show routines in a week view sorted by tokens per week. For an expensive one, ask Claude to
  optimise it with a cap: *"This routine costs ~$10/week in API credits. Cap it at $4/week and cut what does not add value."*
- **Level 3 - a routine that suggests routines.** Every Friday morning a routine reads the week's sessions, spots jobs you
  keep doing by hand, and parks suggestions (routines, skill fixes, memory fixes) in a review list. You approve the good ones
  and send them back to Claude to apply.
- Start with one routine whose result you can check yourself. When a report misses something, add a rule to the routine's
  instructions ("flag a reply from an active client that changes a deadline; keep unrelated outreach separate") and check
  that the next run follows it.

## Rules for Claude

- A routine that finds nothing says nothing (passive by default) unless the user asked for a daily report.
- Every new skill gets: one-line description that says when to use it, the cheapest model that works, where its output goes.
- Before adding a skill or routine, check that an existing one does not already cover it.
