---
name: jev
description: Turn Jev model routing on or off for this session. "/jev on" routes every delegated sub-task to the cheapest model that can do it; "/jev off" stops. Copy this folder to ~/.claude/skills/jev/SKILL.md to use it.
---

# /jev on | off

State lives in `~/.jev/state` (`on` or `off`).

## /jev on

1. Write `on` to `~/.jev/state`.
2. For the rest of this session, before you delegate any sub-task (a search, a file lookup, a summary, a build step):
   - run `python3 <path-to>/jev_router.py route "<the sub-task in one sentence>"`,
   - tier1 -> do it directly with a tool call, no model call,
   - tier2 -> spawn the helper sub-agent with model `haiku`,
   - tier3 -> spawn it with the model the router returned (default `sonnet`; `opus` only if JEV_BIG_MODEL says so).
3. Say in one short line which tier and model each sub-task got.

## /jev off

Write `off` to `~/.jev/state` and stop routing. Work with the session's default model again.

## /jev stats

Read `~/.jev/log.jsonl` and report: number of calls, average seconds, share per tier, how many answers came from the
heuristic fallback instead of Jev.
