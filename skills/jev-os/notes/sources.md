# Sources - what each video taught

Watched in full from their transcripts (fetched through Shorty, since YouTube is not reachable from the build machine).
Names below are as spoken; a few may be transcription spellings. Facts about products and prices are as stated in the
videos - verify before relying on them.

| # | Video | Skill(s) it fed |
|---|---|---|
| 1 | [Anthropic Just Launched Claude DASHBOARDS (Master it in 14 mins)](https://www.youtube.com/watch?v=9RPUZLJ4v7Q) | `claude-dashboards` |
| 2 | [A NEW Agentic OS Standard for Claude 5.5 is here (Claude Mods, Jev, 5.5 Models)](https://www.youtube.com/watch?v=s_1GPN-NXA0) (linked twice in the request) | `jev-os`, `os-skills-routines`, `os-memory`, `jev-router` |
| 3 | [Opus 5.5 Video Editing is Unbelievably Good (master it in 12 mins)](https://www.youtube.com/watch?v=YKFpSe28mlg) | `claude-video-direction` |
| 4 | [Jev will 10x your Claude Code (Here's How)](https://www.youtube.com/watch?v=tTnUcSj-QPA) | `jev-router` |
| 5 | [This NEW Jev + Claude OS Just Changed Every AI Workflow](https://www.youtube.com/watch?v=EOdXR6lU5ZA) | `jev-os`, `jev-router`, `os-memory`, `os-skills-routines` |
| 6 | [I Put My Claude Code AI OS on My Phone](https://www.youtube.com/watch?v=SuI1cRv0YVo) | `jev-os` (phone access) |
| 7 | [Claude Code OS Setup: The $20 AI Coding OS](https://www.youtube.com/watch?v=xOiPjXvj49Y) | `claude-code-setup` |
| 8 | [Anthropic's Ten NEW Rules for Prompting Fable 5.2 (Full Guide)](https://www.youtube.com/watch?v=c_McosB62a4) | `fable-5-2-prompting` |

## Key points per video

**1 - Claude Dashboards.** Five pillars: why (operational / strategic / analytical; let Claude interview you), where
(connect everything incl. Snowflake/BigQuery/Databricks, build CLIs for apps without connectors, reverse-engineer data you
pay for), what (3-5 metrics that matter as BANs at the top), how (no chart junk, reference design systems such as
styles.refero.design, comments on numbers, AI-powered artifacts add a chat box), when (refresh on open for personal, on a
schedule for teams; stored data ~100 MB + 1 GB files vs live data via the viewer's connectors; security = trust decision).

**2 - Agentic OS standard (ARMS).** Apps, Routines, Memory, Skills, three levels each. Skills: database / artifact /
self-triggered (`claude -p`), wildcards against over-fitting, model routing (Haiku for simple skills, Jev as router:
4,451 calls, 0.6 s each, $0.18 total, ~40 % to Haiku), self-improving skills via review-app toggle. Routines: active vs
passive, capped by token cost, a Friday routine that suggests routines. Memory: MEMORY.md -> CLAUDE.md/AGENTS.md map ->
department routers -> database skills, plain text over embeddings; context rot, `/compact` with a purpose, prompt cache
cold after ~1 h; `/note` backlog, `/calibrate`. Apps: connector search order official -> CLI -> API -> MCP (MCPs load into
every session), Claude Code mods (usage bar with cache state), Chrome extensions as browser mods, micro-apps for big jobs,
reusable UI component library.

**3 - Video editing with code.** No generative video model: HTML/CSS/JS, Three.js, ffmpeg; SVG for editable, animatable
graphics. Level 1 one-shot (model tests, showreels), level 2 storyboard (stills + motion descriptions, comments pinned on
frames with timestamp and position), level 3 direct the render (comments on frames and audio, copy all back to Claude).
Taste and the feedback system are the differentiators.

**4 - Jev explained.** System-1 model, answers only binary / menu selection / scale; output tokens free, ~$0.04 per million
input; available from the maker and via OpenRouter. Level 1: model routing (12-prompt test, ~70 % saving, `/jev on`), skill
finding (145 skills, ~5 s vs ~30 s). Level 2: high-volume classification (100 emails into lead classes in < 1 s; fraud,
spam, moderation, refunds, churn). Level 3: new apps - meaning search over a media library, a page de-clutter extension.

**5 - Jev + Claude OS.** Three layers: visual (web app or Obsidian plugin, runs Claude Code or Codex, buttons run headless
skills), memory (Obsidian vault, raw / wiki / outputs, structure written into CLAUDE.md/AGENTS.md; Obsidian is not RAG),
skills (the backbone: mine 30 days of logs + 10-20 min voice brain-dump). Pipeline: voice -> bridge (logs to Obsidian) ->
local Whisper (STT) / Kokoro (TTS) -> Jev picks tier 1 (no AI), tier 2 (small model) or tier 3 (Claude Code / Codex in the
terminal). The dashboard lets teammates and clients run skills without a terminal - the way to package and sell it.

**6 - AI OS on the phone.** Mac (files, local jobs, morning report) + always-on VPS (mobile dashboard, notes and task
records, Telegram morning update, sync back to the Mac) + phone; Tailscale private network; cloud model calls still leave
the boundary. Voice note -> Haiku titles and formats -> confirm -> save. Corrections become rules in the routine's
instructions. Claude Code and Codex read the same markdown files. Start with one project and one routine; draw three boxes
(computer / server / phone) before buying anything.

**7 - $20 coding setup.** Plans and billing catches; Xcode CLT, Homebrew, git + gh, Node LTS, native Claude Code with
subscription login; Zed + external Claude agent via ACP; T3 Code (free, worktrees, supervised mode); Bamboo (paid, task
board, architect + workers); Delta (uploads files, no Claude subscription yet); CLAUDE.md via `/init`, Context7,
frontend-design and Superpowers plugins, Claude in Chrome for browser tests; reading-list app plan-first and verified.

**8 - Fable 5.2 prompting.** High effort by default, avoid max; make it prove its work; make it finish; prune old prompts;
it always thinks; no step-by-step reasoning requests (distillation classifier); say it owns the code; drop sub-agent rules;
ask for progress updates; tone/length only via prompt.
