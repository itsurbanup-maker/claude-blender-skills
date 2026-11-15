---
name: claude-agent-rules
description: The 7 working rules from Anthropic's prompting guide for Fable 5.2 (also good for Opus 5.5) - pick the effort level, finish the job, clean out old instructions, own the project, don't push sub-agents, report progress, write a final report a person can read. Use when writing or cleaning up a CLAUDE.md / AGENTS.md / project instructions / a skill, when setting up a long agent run in Blender, Adobe Premiere Pro or Adobe After Effects (or a website, a game), when Claude stops halfway, works silently, writes dense reports, or costs too much, or when someone asks "how do I prompt Fable 5.2".
---

# Working rules for Claude agents (Fable 5.2 / Opus 5.5)

Fable 5.2 reads instructions more literally than older models. Anthropic published a prompting guide for it. These are its 7 rules,
as explained in the video "Fable 5.2: new prompting rules" (https://youtu.be/M-SCs4D2uZg).

Rules 1-3 matter in a normal chat. Rules 4-7 matter when Claude works alone as an agent, for example in Claude Code.
"Instructions" means the text Claude reads before every conversation: `CLAUDE.md` or `AGENTS.md` in Claude Code, the project
instructions in the Claude app. A ready-made block with all the rules is in `templates/CLAUDE.md`.

The paste-in texts below are short versions of the guide's texts, rebuilt from the video. They are not Anthropic's exact wording.

## Which model

- Opus 5.5 for everyday work. Fable 5.2 only for really hard jobs.
- Fable 5.2 is faster (up to 30%) and cheaper than Fable 5.1: $8 / $40 per million input / output tokens (was $10 / $50).

## Rule 1. Choose how much it thinks (effort)

- 5 levels: low, medium, high, xhigh, max. Higher = more thinking, more time, more tokens.
- **medium** (the default in the Claude app and Claude Code): chat and everyday tasks.
- **high**: the sweet spot for a hard job Claude does on its own. Anthropic: most of the gain, best price for quality.
- **max**: only for rare cases where time and cost don't matter. It is often a little worse, not better.
- From medium up, "answer directly, don't think" no longer skips the thinking. Want it faster? Lower the effort.
  Want it short? Ask for a short answer in plain words.

## Rule 2. Tell it to finish the job

On long jobs (more often on low and medium) it can stop early, list what is left and ask if it should go on. Put this in the
instructions:

```
Don't stop while work I asked for is still left. If you hit a normal error, find out what happened and keep going.
If something is blocked on purpose, leave it blocked and tell me.
```

- Anthropic's test: about half as many sessions stopped with unfinished work. Cost: about 30% more output tokens.
- When you approve a next step, say what you approve. Not "yes", but "yes, send the offer to the client".

## Rule 3. Delete old instructions (the most important rule)

Old notes, old skills and rules written for weaker models now do harm, because the model follows them literally.

- Anthropic's test: 12 notes from old sessions, one of them said "never retry". Without that note, the model retried a busy tool
  almost every time. With it, only about 4 times in 10.
- Delete notes, memory and rules you no longer need. Look for contradictions.
- Avoid rules with "never" / "always". If you keep one, put the exception in the same sentence:
  "Never render the film in the live Blender window, except small preview stills."
- Remove rigid style limits like "max 20 words per sentence". The text comes out choppy.
- Remove requests like "write out all your reasoning in the answer". It refuses them now (protection against distillation).
- This rule also makes Opus 5.5 better.

## Rule 4. Tell it whose project it is

Without this, it acts like a guest: it adds what you asked, and if it sees a problem it only tells you and leaves it.
With it, it cleans up like it's its own house.

```
This project is yours. You decide what it is for and how it is built, and you will keep building on it.
```

- Anthropic's test: less duplicate code in about half the attempts (without the phrase: less than 1 in 10).
- Cost: about 1.5x, and it changes things you didn't ask for. Read its summary: it lists only the biggest changes.
- For one small, targeted job, leave this phrase out.

## Rule 5. Don't push it to use sub-agents

Fable 5.2 starts sub-agents (helper AIs) easily, and each one costs. In one session they can be most of the bill.

- Look again at lines like "always use sub-agents". Delete them if it starts more than needed.
- On xhigh and max it starts its own checker sub-agents.
- Say which model a sub-agent runs on. Sub-agents on Fable 5.2 can eat your credits fast. A tight brief to a cheaper model
  (Sonnet) is usually enough (see the render-check loop in `blender-forest`).

## Rule 6. Ask it to keep you updated

On long jobs it can go quiet: tool call after tool call, nothing new on screen.

```
Every few actions, tell me in one line where you are.
```

- Longer version: say at the start what you are going to do, and end with a summary.
- Cost: about 20% more output tokens. If you leave it alone and only come back for the result, skip this rule.

## Rule 7. Ask for a report you can understand

After a long job the report is dense, full of abbreviations it invented along the way. You didn't see what it saw.

```
Write the final report for a smart person who did not see your work. Put the main points in the first sentences.
Use simple words and short sentences, one idea per sentence. Don't use abbreviations you made up while working.
```

## The rules in Blender, Premiere Pro and After Effects

The 7 rules are the same in every app. What changes is how Claude reaches the app, and where a long job hides.

| | Blender | Premiere Pro | After Effects |
|---|---|---|---|
| How Claude controls it | Python, live through `tools/bridge.py`, or `blender -b` in the background | Writes files Premiere opens: an XML timeline, ProRes clips (`premiere-edit`) | ExtendScript `.jsx` sent to the open app, `aerender` for renders (`after-effects-comp`) |
| Long job (rules 2, 6) | the overnight Cycles render | encoding every shot | the `aerender` render |
| "Blocked on purpose" (rule 2) | a render the user hasn't approved yet | the creative cut: timing, sound, grade, export | a full render that blocks the GPU |
| Whose project (rule 4) | the scene and scripts are Claude's to clean up | `shots.json` and the XML are Claude's; the edit in Premiere is the user's | the comps the script built are Claude's; hand-made comps are the user's |
| Report (rule 7) | frames rendered, time per frame, broken frames | shots, length, fps, size of the sequence | frames rendered and checked, effects skipped |

Add one line for the app to the template, for example: "Premiere: build the timeline as XML; I do the creative edit."

## How to use this skill

1. **New project:** copy `templates/CLAUDE.md` into the project folder. Drop rule 4 for small targeted jobs, rule 6 for unattended runs.
2. **Existing instructions:** apply rule 3. Read the CLAUDE.md / AGENTS.md / skills line by line. For each rule ask: still true?
   Contradicts another? "Never" without an exception? A rigid style limit? "Always use sub-agents"? Show the user a list of
   proposed deletions and changes before editing.
3. **Long run** (a Blender render, a Premiere or After Effects job, a website, a game): effort high, rules 2 + 4 in the instructions, plus "check your own result
   when you are done". That is all the video's demo used: an empty folder, a one-line prompt, no colours or examples.
4. **Approving steps:** write what you approve (rule 2).
