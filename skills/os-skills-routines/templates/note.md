---
name: note
description: Park a piece of feedback about a skill, app or routine for later, without interrupting the current job. Use when the user types /note followed by feedback.
model: haiku
---

# /note <feedback>

1. Work out which skill, app or routine the feedback is about (ask only if it is truly unclear).
2. Append one line to `~/.claude/backlog/<name>.md`: date, the feedback in the user's words, and the file or step it concerns.
3. Reply with one line: "Parked for <name>." Do not change anything else and do not continue the discussion.

## Applying the backlog (when the user says "apply the backlog" or before a usage reset)

For each file in `~/.claude/backlog/`: read the items, apply each fix to that skill/app/routine, move applied items to
`~/.claude/backlog/done/<name>.md`, and report one line per fix.
