---
name: cleanup
description: Free the machine when it slows down - remove temp files and stray processes that agent sessions left behind. Self-triggered (button or `claude -p "/cleanup"`); prints a short report.
model: haiku
---

# /cleanup

1. List (do not kill yet) processes started by agent sessions that are idle: dev servers, headless browsers, watchers.
2. List temp and cache folders the agent created (build outputs, screenshot dumps, downloaded test files) with their sizes.
3. Delete only what is clearly temporary and not inside a project's tracked files. Stop only processes with no open work.
   Never touch the vault, projects, git repositories, or anything you are not sure about - list those instead.
4. Report: what was removed, space freed, processes stopped, and anything left for the user to decide.
