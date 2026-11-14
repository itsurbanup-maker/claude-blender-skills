---
name: fable-5-2-prompting
description: The ten prompting rule changes for Claude Fable 5.2 - effort level (high by default, avoid max), make it prove its work, make it finish long tasks, prune old CLAUDE.md rules, it always thinks, do not ask for step-by-step reasoning (distillation classifier), tell it it owns the code, stop scripting sub-agents, ask for progress updates, and tone/length only change by prompt. Use when someone prompts Fable 5.2, migrates prompts or CLAUDE.md files to it, or asks why it hallucinates, stops early, burns usage or answers too long.
---

# Prompting Fable 5.2 - ten rule changes

Numbers below are the ones quoted in the video (from the system card and benchmarks); check the current docs for exact values.

1. **Effort: use high.** Claude Code defaults to medium. The biggest jump in performance per dollar is medium -> high
   (agentic coding benchmark: 45.3 % at $6.72 on high vs 37.6 % at $2.48 on medium; high roughly matches the previous top
   model on max at about half the cost). Not enough? Go extra-high. Mostly avoid max: much more cost, sometimes worse.
   If medium/low would do, the cheaper model probably does it too.
2. **Make it prove its work.** It states inferences as facts more often and runs fewer tests on low/medium; it sometimes
   invents a stand-in for a missing file. Prompt: *"Before you show me the result, run tests / checks that confirm every claim
   about what you completed. If something is missing, say so instead of creating a substitute."*
3. **Make it finish.** On long agentic tasks it stops early more often (less on high). Prompt: *"Keep working until the task is
   fully done and verified. Do not stop to ask unless you are blocked."* (roughly halves early stops).
4. **Prune your old prompts.** It follows rules almost to the letter, so stale CLAUDE.md files, strict style rules and
   over-prescriptive instructions now hurt output. Delete what you do not truly need; give it room.
5. **You cannot prompt it not to think.** "Just answer, don't deliberate" no longer skips thinking. Lower the effort level to
   think (and spend) less.
6. **Do not ask for step-by-step reasoning.** A classifier treats "explain your reasoning step by step / exactly how you
   thought" as a possible distillation attempt and shuts it down. Asking briefly *why* an answer is right is fine.
7. **Tell it who owns the code.** "You own this codebase" -> less duplicated code, leaner design, but more features, tests and
   output tokens. For minimal, surgical changes do not say it, and be precise about the change.
8. **Stop scripting sub-agents.** It spawns sub-agents on its own when needed (more on extra-high/max). Old rules like
   "always use sub-agents to check your work" are followed to the letter and burn usage. Remove them.
9. **Ask for progress updates if you want them.** On long runs it can stay silent for a long time. Ask for brief updates at
   milestones; an update after every tool call can add ~20 % tokens - pick a middle ground.
10. **Tone and length do not follow effort.** Low effort does not mean shorter answers. Set tone/length in the prompt or in
    CLAUDE.md / AGENTS.md / a rule file.

## Audit checklist for an existing setup

- [ ] default effort set to high for hard work, lower model for easy work
- [ ] "prove it" and "finish it" lines in the project instructions
- [ ] no "use sub-agents for X" rules, no "explain your reasoning step by step"
- [ ] strict style rules removed unless essential; tone/length stated once
- [ ] ownership stated explicitly for build tasks, omitted for small fixes
