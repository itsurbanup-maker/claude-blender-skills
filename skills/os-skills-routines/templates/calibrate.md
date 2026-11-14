---
name: calibrate
description: Teach Claude a lesson that must stick. Saves the feedback to memory, links it to related memories and fixes the skill it belongs to right now. Use when the user types /calibrate followed by feedback, or corrects the same thing a second time.
---

# /calibrate <feedback>

1. Restate the lesson as one rule ("Always ...", "Never ...") with the reason.
2. Save it to memory (MEMORY.md or the memory folder) as one short line, next to related memories; merge duplicates.
3. Find the skill, routine or CLAUDE.md section where the mistake came from and change it so the mistake cannot repeat.
4. Report: the rule, the memory line, and the file you changed (with the diff).
