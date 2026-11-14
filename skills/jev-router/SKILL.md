---
name: jev-router
description: Use Jev - the system-1 decision model that only answers true/false, pick-from-a-menu or a 0-10 scale, 20-200x faster and 40-400x cheaper than frontier LLMs - next to Claude. Covers setup (maker's API or OpenRouter), routing each task to the cheapest Claude model that can do it (/jev on|off), finding the right skill out of hundreds in seconds, high-volume classification automations (lead triage, tickets, fraud, moderation, churn) and search by meaning. Ships a working router script with an offline fallback. Use when someone mentions Jev, model routing, "use Haiku when it is enough", cheap classification at volume, or wants their Claude setup faster and cheaper.
---

# Jev router

## What Jev is (as explained in the videos - verify current facts on the provider's page)

- A new kind of model from a team led by a co-inventor of ChatGPT. Called a **system-1 model** (fast, snap decisions, as in
  *Thinking, Fast and Slow*); Claude, GPT and the rest are system-2 models (they write text token by token).
- **It is not an LLM and does not write text.** It answers in exactly three shapes:
  1. **binary** - is this statement true or false,
  2. **selection** - which option from a menu (often returned as a probability per option, e.g. "92 % billing"),
  3. **scale** - a score, e.g. 0-10.
- Speed and price quoted in the videos: ~0.6 s per routing call, about $0.04 per million input tokens, output free; roughly
  24x cheaper than Haiku. One creator's log: 4,451 routing calls in a few weeks cost $0.18 in total, ~40 % went to Haiku.
- It is **not a replacement for Claude Code**. The win is to put the system-1 model in front of the system-2 model.

## Setup

1. Get access: sign up with the maker (it left its wait-list recently) or use it through **OpenRouter**, which lists new
   models as they ship. Look up the exact model slug on the provider's model list - do not guess it.
2. Put the key in the environment, never in a file in the repo:
   `export OPENROUTER_API_KEY=...` and `export JEV_MODEL=<slug from the model list>`
   (for the maker's own endpoint: `JEV_BASE_URL=<its OpenAI-compatible base URL>` and `JEV_API_KEY=...`).
3. Ask Claude to confirm it can reach Jev: `python3 scripts/jev_router.py pick "the sky is green" true false`.

`scripts/jev_router.py` modes:

| Command | What it does |
|---|---|
| `route "<task>"` | tier1 / tier2 / tier3 + model alias (none / `haiku` / `sonnet` - set `JEV_BIG_MODEL=opus` for the top tier) |
| `run "<task>"` | route, then run tier 2/3 headless with `claude -p --model <alias> "<task>"` |
| `skill "<task>"` | picks the best skill from `~/.claude/skills` and `./.claude/skills` by their descriptions |
| `pick "<text>" a b c` | any menu classification |

Every call is logged to `~/.jev/log.jsonl` (choice, latency, backend). Without a key it falls back to a keyword heuristic,
so the OS never blocks on the router - the log says which backend answered. The answer parser accepts a plain label or a
`{label: probability}` map, because the response shape depends on the provider.

## Level 1 - inside your own agent setup (faster, cheaper)

**Model routing.** Deciding the model per task used to be the user's job. Let Jev decide:

- tier 1 - no AI: open a report, run a known command, show the terminal (milliseconds)
- tier 2 - small model (Haiku): short questions, file lookups, grammar, quick summaries
- tier 3 - real work: Claude Code with Sonnet/Opus (or the top model only when the task truly needs it)

In one test of 12 prompts, routing saved ~70 % against running the top model every time, because 9 of 12 never needed it.
Measure on your own work: compare outputs, keep routing only if quality held.

**Make it a switch**, not a default, while testing. Add a `/jev` skill (template in `commands/jev.md`):
`/jev on` - for the rest of the session, before delegating any sub-task, run `jev_router.py route` and spawn the helper
sub-agent with the chosen model (e.g. a Haiku helper to find a file path instead of the session's Opus).
`/jev off` - back to normal.

**Skill finding.** Input = the task, menu = your skills (names + descriptions). With ~145 skills, Jev found the right one in
~5 s over 14 tests versus ~30 s for a frontier model searching on its own. Claude then loads that skill.

## Level 2 - business automations at volume

Pattern: **lots of items + one business question with fixed answers = a Jev job.** Demo: 100 emails classified into
warm lead / cold lead / not a lead in under a second, far faster and cheaper than Haiku or the top model.
Candidates: lead triage, support-ticket routing ("I cancelled last month but you charged me again" -> billing, 92 %),
invoice-fraud flags, spam, community moderation, refund requests, churn risk per subscriber.
Hand only the hard or ambiguous items (low top probability) to Claude.

## Level 3 - apps that were not worth building before

- **Search by meaning** in your own media/artifact library: filename search for "claude" finds a few files; asking Jev
  "does this item match the query?" over the items' captions/metadata finds the images that are *about* it.
- **Page de-clutter extension**: classify every element of a web page (ad, cookie banner, slop, content) and hide the junk.
- Anything that needs a quick yes/no or score on every item, every time, at near-zero cost.

## Rules for Claude

- Use Jev only for decisions with predefined choices. Anything that needs text goes to Claude.
- Always keep the fallback: if the Jev call fails, route with the heuristic or the session's default model - never stall.
- Report savings from the log (`~/.jev/log.jsonl`): calls, average latency, share routed to each tier.
- Keep the key in environment variables or the platform's secret store.
