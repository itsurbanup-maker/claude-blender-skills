---
name: jev-os
description: Build a personal "Claude OS" (an agentic operating system, Jarvis-style) around Claude Code, with Jev as a near-free, near-instant router in front of it - voice in, Jev picks the tier, Claude does the work, everything is logged to an Obsidian/markdown vault and shown on one dashboard you can also open from your phone. Use when someone wants "a JEV via Claude", a Jarvis / AI OS / agentic OS / second brain / Claude OS, a home dashboard for their skills, routines and artifacts, or asks how to organise apps, routines, memory and skills (the ARMS framework) so agents run faster and cheaper. This is the umbrella skill; it points to jev-router, os-skills-routines, os-memory and the other skills for each part.
---

# JEV OS - an agentic operating system with Claude + Jev

Distilled from seven videos (list and per-video notes in `notes/sources.md`). The OS is not the pretty dashboard.
It is a **workspace organised so agents can find things fast and cheap, a backbone of skills that covers the work you
actually do, routines that run them, and one place where all their output lands.** The dashboard is the last 10 %.

## The architecture (one request, end to end)

```
voice / text / button
      |
      v
  bridge  --- logs request + result to the vault (Obsidian)
      |       local STT (Whisper)  ->  text ;  local TTS (Kokoro) <- answer
      v
  Jev (system-1 classifier, ~0.6 s, fractions of a cent)
      |-- tier 1: no AI at all     -> run a command / open a report / open the terminal   (milliseconds)
      |-- tier 2: small model      -> Haiku answers short questions                         (cheap, fast)
      '-- tier 3: real work        -> headless Claude Code (`claude -p`) or an interactive terminal session
```

- Jev never writes text. It only answers in three shapes: **true/false, pick one from a menu, or a 0-10 scale**
  (often as a probability). That is exactly what routing needs. Details and a working router: skill `jev-router`.
- Tier 1 requests never touch an LLM. "Bring up the morning brief" is a file open, not a prompt.
- Everything that goes in or comes out is written to the vault, so the next session can find it.

## The ARMS framework (organise the workspace)

**A**pps, **R**outines, **M**emory, **S**kills. Build them bottom-up, in this order. Each has three levels.

| Layer | Level 1 | Level 2 | Level 3 |
|---|---|---|---|
| **Skills** | Know your skill types: database, artifact, self-triggered | Route each skill to the cheapest model that does it well (Jev or a fixed `model:`) | Skills improve themselves from your feedback |
| **Routines** | Active (hands you output) vs passive (pings only when something is found) | Capped: see token cost per routine, cap the expensive ones | A weekly routine that suggests new routines from your history |
| **Memory** | Long-term: `MEMORY.md` -> `CLAUDE.md`/`AGENTS.md` map -> department routers -> database skills | Short-term: context window, purposeful `/compact`, keep the prompt cache warm | Self-evolving: `/note` backlog, `/calibrate`, suggested memory fixes |
| **Apps** | Connect apps, even ones with no official connector (CLI > API > MCP) | Mods: change Claude Code itself; Chrome extensions for the browser | Micro-apps for the big recurring jobs (review UIs, inboxes) |

Skills + routines: `os-skills-routines`. Memory: `os-memory`. Apps are covered below.

## Build order (do it in this order, stop when it is useful enough)

1. **Skill backbone first** - it is the part that matters most.
   - Ask Claude: *"Read my Claude Code session logs from the last 30 days. Which things do I keep doing that should be
     skills? Which of those should run on a schedule?"*
   - Then talk for 10-20 minutes (voice dictation, stream of consciousness) about what you do every day and week, and ask:
     *"Based on everything I just told you, which skills and automations would take work off my plate?"*
   - These two prompts get you ~90 % of the skill list without knowing the answer up front.
2. **Vault / memory** - pick one folder as the vault, give it a structure (e.g. `raw/`, `wiki/`, `outputs/`), and write
   the structure plus the filing rules into `CLAUDE.md` / `AGENTS.md` so it does not drift. See `os-memory`.
3. **One routine you trust** - one scheduled job whose result you check yourself (morning brief, inbox scan).
4. **Jev router** - add `jev-router` once there is something to route between. Measure savings, keep it if output did not
   get worse.
5. **Dashboard** - one page that collects every skill's deliverable: calendar, next routines, flagged emails, artifacts
   inbox, buttons that run skills (headless `claude -p`), model + effort pickers. See "Dashboard" below.
6. **Voice** - local Whisper for speech-to-text, Kokoro for text-to-speech. Nothing audio leaves the machine.
7. **Phone** - only when you know exactly what you want to reach remotely. See "Phone access".

## Apps

- **Connect anything.** Search order for a connector, lightest first:
  1. the maker's official connector,
  2. a CLI (one short command, short answer - lightest on tokens),
  3. the app's API (heavier: long JSON answers Claude must read),
  4. a community MCP server (heaviest: every MCP's tool list loads into every new session, used or not).
  Keep the MCP list short. A `/search-connectors` skill that follows this order is worth having.
- **Paying for a tool only for its data?** Ask Claude to reverse-engineer how the number is computed (an "outlier score" is
  roughly views / channel average) and get it yourself, then compare with the paid tool before cancelling.
- **Mods.** Claude Code mods change the app itself and cost no tokens (status bars, panels, toasts). Useful one: a usage
  bar showing the 5-hour and 7-day limits *and the prompt-cache state* (warm/cold, idle minutes, tokens that would be
  re-cached). Use the `plugin-authoring` skill to build one.
- **Chrome extensions are mods for the browser** (`chrome://extensions` -> Developer mode -> Load unpacked). Examples:
  click a page element to capture its HTML/CSS for Claude to rebuild (better than a screenshot); right-click a
  thumbnail/title to file it into a database skill. They run as code, so no tokens.
- **Micro-apps for big recurring jobs.** When a job is routine, the chat window is often the wrong interface. Build a small
  local web app (localhost) for it: a review UI where you pin timestamped comments on frames and copy them all back to
  Claude; an Instagram carousel approval board; an inbox of every artifact Claude made (search it without spending tokens);
  a "recommendations" cart where a weekly routine parks suggested improvements and you check out the ones you want.
- **Reusable UI component library + design system skill.** Keep one HTML brand book (colours, fonts, components) behind
  a design-system skill so every artifact, PDF (HTML first, export to PDF) and micro-app looks the same and Claude does not
  rebuild components from scratch.

## Dashboard (the visual layer)

Fully custom. It can be a localhost web app, an Obsidian plugin, or both - the same buttons and terminal work in each.
What earns a place on it:

- deliverables of your skills and routines (reports, briefs, metrics) in one place
- calendar / next meeting, next scheduled routines, emails worth replying to
- buttons for self-triggered skills, each with a model + effort picker (they call `claude -p --model <alias> ...`)
- artifacts inbox with search; a file/graph view of the vault with a search box; a timeline of what the agent last edited
- routines week view **sorted by token cost**; skills and connected apps by token use (retire unused ones)

The dashboard is what lets a teammate or client use the system: they press a button, a headless Claude Code run does the
work, and they never open a terminal. That is also how you package and sell it.
For a dashboard of business data, use `claude-dashboards`.

## Phone access

Three boxes: **computer** (holds the files, runs local jobs, must stay awake), **small always-on server / VPS** (serves the
mobile dashboard, stores notes and task records captured from the phone, sends a morning Telegram update, a sync job copies
records back to the computer), **phone** (reads summaries, captures notes by voice or chat).

- Private network between the devices with Tailscale. The dashboard is never exposed to the open internet.
- A private network does not make a cloud model local: anything sent to Claude leaves the boundary. Use local models for
  anything that must stay home.
- Voice note flow: phone speech-to-text -> Haiku gives it a title and tidies it -> you confirm -> saved to the inbox.
- Layout: real mobile layout (no zooming), panels resizable/hideable/reorderable, each browser remembers its own layout.
- Plan before buying anything: write which jobs run on the computer, which data goes to the server, and what you want to
  read or change from the phone.
- Remote control of the laptop lets you keep working in Claude Code from the phone while it is awake.

## Rules for Claude when building this

- Ask one question at a time to map the user's work before building ("Help me map this part of my work. Ask one question at
  a time about the decisions I make, the files I use and the updates that matter, then suggest one small routine.").
- Start with one project, one routine and Claude Code. Add the server, phone, voice and Jev only when the base works.
- Every skill and routine writes its output where the dashboard reads it (one inbox folder per kind of output).
- When the user corrects a report, turn the correction into a rule in the routine's instruction file and check the next run.
- Keep Claude Code and Codex (or any other agent) reading the same markdown files (`AGENTS.md` is read by Claude Code too),
  so the agent can be swapped without rebuilding the workspace.
- Never put API keys in the vault or the repo; read them from environment variables.

## Related skills

- `jev-router` - Jev setup, model routing, skill finding, classification automations, meaning search.
- `os-skills-routines` - skill types, model routing per skill, self-improving skills, routines, `/note`, `/calibrate`, `/wildcard`.
- `os-memory` - vault structure, CLAUDE.md as a map, context window, compaction, prompt cache.
- `claude-dashboards` - business dashboards with the five pillars.
- `claude-video-direction` - videos and motion graphics made with code, storyboard and direct.
- `fable-5-2-prompting` - the ten prompting rule changes for Fable 5.2.
- `claude-code-setup` - the $20 beginner coding setup on a Mac.
