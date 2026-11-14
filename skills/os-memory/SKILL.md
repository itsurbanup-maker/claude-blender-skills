---
name: os-memory
description: Set up the memory of an agentic OS so Claude finds things fast and cheap even with hundreds of thousands of files - plain-text maps (MEMORY.md, CLAUDE.md/AGENTS.md as a router, per-department routers, database skills), an Obsidian vault with a raw/wiki/outputs structure, the context window (context rot, purposeful /compact) and the prompt cache (cold after ~1 h idle, re-reading a big chat costs real money). Use when someone builds a second brain, an Obsidian vault for Claude, asks why Claude cannot find their files, why usage drains in long chats, or how to make memory improve over time.
---

# Memory for an agentic OS

A second brain is just the files in your workspace. Its value is **speed of retrieval and cost of retrieval**:
can Claude find your stuff quickly without burning your limits. Obsidian gives Claude no magic memory - it only makes the
same folder easy for a human to browse. A knowledge-graph view looks nice; it is not RAG. **Organisation is everything.**

## Level 1 - long-term memory: give Claude a map

Plain text works. Anthropic reportedly found plain-text maps beat vector embeddings / RAG in their own large workspace, and
one creator runs ~420,000 files this way without embeddings. Add embeddings only when retrieval actually hurts.

Three layers, each a router to the next:

1. **`MEMORY.md`** - Claude Code loads it at the start of every session (one short line per remembered fact). Because it is
   preloaded, link it to every department so it doubles as a card catalogue.
2. **`CLAUDE.md` (or `AGENTS.md`, which Claude Code also reads - keep one file, not two in sync)** - write it as a **map of the
   whole workspace**: "content work -> these folders; personal -> these; clients -> these". Each department has its own
   router file (`business.md` -> its sub-folders and files).
3. **Database skills** - `/<business>-data` style skills whose `SKILL.md` says where the up-to-date data, dashboards and
   references for that business or client live.

Add metadata to visual assets (captions, tags) so they are searchable as text.

### Vault structure (Obsidian or any folder)

A simple structure that works (from Karpathy's Obsidian + Claude Code idea):

```
vault/
  raw/       everything collected as-is (research dumps, transcripts, exports)
  wiki/      organised, Wikipedia-style notes built from raw/ (one topic per folder)
  outputs/   deliverables made from the wiki (decks, reports, explainers)
  CLAUDE.md  the structure above + the filing rules for new content
```

Example: "research AI agents" -> sources land in `raw/ai-agents/`; Claude writes `wiki/ai-agents/` (autonomous coding,
tool-use patterns...); "make a deck about it" -> `outputs/ai-agents-deck/`. Any structure is fine if it makes sense to both
you and Claude. To start: *"This folder is my vault. Propose an organisation, then move the files."* Then write the
filing rules into the vault's `CLAUDE.md`/`AGENTS.md` so it does not drift. The OS logs every request and deliverable here.

## Level 2 - short-term memory: the context window

- Context windows are large (1M tokens on current models) but **context rot** is real: the fuller the chat, the worse the
  recall. And every turn re-reads the whole chat, so a bloated chat also costs more.
- **Compact with a purpose**: `/compact keep the business decisions and the templates we created`. Otherwise Claude decides
  what matters and may drop the one detail you needed. Put your standing "always keep" list into CLAUDE.md.
- **Watch the prompt cache.** Re-reading a cached chat costs a fraction of the price. After about an hour idle the cache goes
  cold and the next message pays to load everything again (one example: a 600k-token chat idle 11 h would re-cache for
  ~$5 at API prices). Keep the cache state visible (a usage-bar mod showing 5-h and 7-day limits plus warm/cold and idle
  minutes). Start a fresh, short session instead of reviving a huge cold one. Some people schedule a light keep-alive ping
  for the few hours they will come back to a big session; first have Claude analyse your last 30 days of sessions to see
  whether that would really save money for you.

## Level 3 - memory that improves itself

If you correct Claude on the same thing twice, the memory system missed something.

- `/note` - backlog of fixes per skill, applied in batches (template in `os-skills-routines`).
- `/calibrate` - lessons that must stick: saved, linked, and the skill fixed now (template in `os-skills-routines`).
- A weekly routine proposes memory fixes alongside routine and skill suggestions; you approve the good ones.

## Rules for Claude

- Before searching the disk, read the map (MEMORY.md -> CLAUDE.md -> department router) and follow it.
- When you file something new, follow the vault's filing rules; if none fit, propose a rule instead of inventing a folder.
- Keep MEMORY.md lines short and current; merge duplicates; delete facts that are no longer true.
