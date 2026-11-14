---
name: claude-dashboards
description: Make a business dashboard with Claude (Claude Dashboards / dashboard artifacts) that is not a vibe-coded wall of chart junk - five research-backed pillars (why/goal and dashboard type, where/data sources and connectors, what/metrics that matter and BANs, how/presentation without chart junk and with a reference design system, when/refresh schedule and stored vs live data) plus in-dashboard chat, sharing and data-security trade-offs. Use when someone asks for a dashboard, KPI page, metrics view or wants to connect Snowflake/BigQuery/Databricks or apps to one view.
---

# Dashboards with Claude - five pillars

Claude Dashboards: Artifacts in the sidebar -> Dashboard, or just ask for a dashboard in any chat. On paid plans; on
Enterprise it is off by default while in beta (the account owner switches it on). Dashboards pull from several connected
apps and warehouses at once (Snowflake, BigQuery, Databricks), can refresh on their own and can be shared. Each chart can
be inspected for where its numbers came from. "Make me a dashboard" alone gives chart junk - go through the pillars.

## 1. Why - the goal (first, before any tokens are spent)

Three types (from *Information Dashboard Design*, 2006):

- **Operational** - what is happening right now (open support tickets by waiting time, for the support crew).
- **Strategic** - are we on track to the goal (monthly revenue vs this year's target, for management).
- **Analytical** - what insight gets us there faster (churned vs retained customers compared, to find behaviours).

Let Claude interview you one question at a time until the goal, audience and type are clear:
*"Before building anything, interview me one question at a time about who this dashboard is for, the decision it
supports and which type it is (operational/strategic/analytical). Summarise the brief when we are aligned."*

## 2. Where - data sources (connect broadly, trim later)

- Today it is fine to connect every source the business has and decide relevance with Claude afterwards.
- Connect via Customize -> Connectors, or ask Claude to set it up.
- No official connector? Have Claude build a small CLI for the app (it is the lightest kind of connector).
- Paying for a tool only for its numbers? Ask Claude to reverse-engineer the metric (e.g. outlier score ~ a video's views /
  the channel's average), compare with the paid tool, then decide whether to cancel:
  *"Which tools am I paying for only for their data, and can you compute those numbers yourself from my sources?"*

## 3. What - metrics that matter

- Give Claude the dashboard goal and your business goals: *"From all connected sources, which 3-5 metrics matter most for
  this goal, and why?"* Your business taste decides.
- Put those 3-5 **BANs** (big aggregate numbers) at the top: actual vs target revenue (strategic), urgent tickets waiting
  now (operational). Everything else below, with "more info" expanders.

## 4. How - presentation

- No chart junk: nothing decorative. No 3D gauges, no speedometers, avoid pie charts with many categories. A dashboard
  summarises; if all the data is on the page it is a spreadsheet.
- Use a reference design system if you have none: styles.refero.design (comes with a markdown design file - ideal for
  agents; you can send Claude the site and ask for three that fit your business), Mobbin, Dribbble. Screenshot 2-3, adapt to
  brand colours, ask for mock-up layouts, pick one, then build.
- Refine by clicking a number and leaving a comment, like in a document ("compare gross margin with last quarter").
- **AI-powered artifacts** (Settings -> Capabilities): add a chat box in the dashboard so anyone with the link can ask
  questions about its data without knowing Claude.

## 5. When - freshness and storage

- Just for you: refresh when opened (nothing burns tokens in the background).
- Team dashboard: refresh on a schedule (e.g. every weekday 07:00, pull yesterday's numbers before anyone opens it).
- Live vs stored: a shared live dashboard uses the **viewer's** connectors, so teammates need the same apps connected. A
  dashboard can instead store its data (about 100 MB of data and 1 GB of files per dashboard) so viewers need no connectors.
- Security: storing data there means trusting Anthropic with it, as you already trust your email or drive provider. Decide
  per data sensitivity.

## Rules for Claude

- Do not build before the goal, audience and type are written down.
- Every number shows its source and the time it was refreshed.
- Use the `dataviz` skill for chart design, and the platform's Dashboard type when it is available.
