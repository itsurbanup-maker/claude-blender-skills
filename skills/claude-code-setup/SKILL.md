---
name: claude-code-setup
description: Set up a new Mac for AI-assisted coding on a $20/month budget - choosing a Claude plan (Pro vs Max vs Team/Enterprise, usage credits), command-line tools, Homebrew, git + GitHub CLI, Node LTS, native Claude Code with subscription login, Zed with the external Claude agent (ACP), optional T3 Code / Bamboo / Delta interfaces with their billing catches, CLAUDE.md, Context7, front-end-design and Superpowers plugins, browser testing with Claude in Chrome, and a first reading-list app built plan-first and verified. Use when a beginner asks how to start coding with Claude, which plan or editor to buy, or how to set up Claude Code.
---

# The $20 Claude Code setup (Mac)

Prices are the ones quoted in the video (US, before tax) - check the current pricing page.

## Pick the plan

- Free plan: no Claude Code. **Pro** ($20/month, or $200/year) includes it - start here.
- **Max 5x** ($100) when Pro limits regularly interrupt useful work; **Max 20x** ($200) only if you use it heavily. "5x/20x"
  is per-session allowance vs Pro, not unlimited. 5-hour and weekly limits; chat and Claude Code share the same allowance;
  more terminals or other apps do not add allowance.
- Team: standard and premium seats, from 2 people. Enterprise: seat price plus usage at API rates.
- Occasional overflow: paid usage credits with a monthly spend limit can beat upgrading. Check school/employer access first.
- If an API key is configured, Claude Code may bill the API instead of your subscription - check with `/status`.

## Install (in order)

1. `xcode-select --install` (command-line tools; full Xcode not needed).
2. Homebrew from its official site; **run the PATH lines it prints**; new terminal; `brew --version`.
3. `brew install git gh`; set `git config --global user.name/user.email` (use GitHub's private no-reply email if you like);
   `gh auth login` (HTTPS, browser) then `gh auth setup-git`; check `gh auth status`.
4. Node LTS from nodejs.org; check `node --version`, `npm --version` (the app needs it; native Claude Code does not).
5. `~/projects/ai-starter` (no spaces) -> README -> `git init` -> first commit.
6. Claude Code: native installer from the official setup page; `claude --version`; `claude auth login` with the subscription
   account; in the project run `claude`, `/status`; `claude doctor` if something is off. The native install self-updates.
   First check: "explain the files in this folder".

## Editor and interfaces

- **Zed** (free): run `claude` in its terminal, or the agent panel: Cmd-Shift-P -> `zed: acp registry` -> install the Claude
  agent -> new Claude agent thread -> `/login` with the subscription. Choose the *external Claude agent*; picking an Anthropic
  model for Zed's own agent is a different (paid) route.
- **T3 Code** (free, open source; `brew install --cask t3-code`): Settings -> Providers -> enable Claude (reuses the CLI login).
  Use **supervised** permissions at first. "New worktree" gives a task its own branch and folder; to inspect its files in Zed,
  open the worktree folder, not the original. Review diff -> commit/push/PR.
- **Bamboo** (paid, alpha): task board, diffs, screenshots, an architect agent with up to three workers on separate files.
- **Delta** (from the Zed team, beta): links each change to its conversation, but uploads tracked files to its servers and,
  at the time of the video, could not use a Claude subscription (API key only). Use T3 Code or Zed's Claude agent today.

## Make Claude useful in the project

- After there is real code: `/init`, then trim CLAUDE.md to what Claude needs every time (what the app does, how to run and
  test it, project rules - e.g. TypeScript, data in browser storage, verify with build + tests). Have it write `.gitignore`.
- **Context7** for current library docs: `npx ctx7 setup --claude`, then "check the docs for the version we use".
- Plugins from the official marketplace (`/plugin`): **frontend-design** (give it your own references and colours too),
  **Superpowers** for bigger features (requirements, planning, tests, review - adds process; keep it if it helps).
- **Browser testing**: Chrome + the Claude in Chrome extension, start `claude --chrome`, `/chrome` to check the connection.

## First project: reading list (plan first, verify after)

1. Plan mode (Shift-Tab until "plan"): *"Build a reading list app with React, TypeScript and Vite. Add, edit, delete and
   filter books, saved in browser storage. Warm background, readable type, compact layout that works on a phone. Explain the
   plan first."* Add checks: empty titles rejected, editing does not duplicate, list survives refresh, no horizontal scroll
   on phone.
2. Approve, let it scaffold, add tests for those checks, run the production build. `npm run dev` (from the worktree if used).
3. Second terminal: `claude --chrome` with the exact local URL: add two books, edit one, mark one finished, refresh, check the
   data and the mobile layout. On a failure give the exact behaviour ("edited book disappears after refresh - reproduce, fix
   the cause, re-run the same sequence").
4. Click through yourself (empty state, long title, delete). Read the diff; ask about anything unclear. Commit, push to a
   private repo. Next feature in a fresh conversation.
- `/model` and `/usage` to see models and allowance. The biggest model is not needed for every small edit.
