#!/usr/bin/env python3
"""Jev router: ask a system-1 classifier to pick from a menu, then (optionally) run the task.

Modes
  route  "<task>"            -> tier 1 / 2 / 3 and the Claude model alias to use
  skill  "<task>"            -> the best matching skill from ~/.claude/skills and ./.claude/skills
  pick   "<text>" a b c ...  -> any menu classification (lead triage, ticket routing, ...)
  run    "<task>"            -> route, then run tiers 2/3 headless with `claude -p --model <alias>`

Backend
  OPENROUTER_API_KEY  key for openrouter.ai (or set JEV_BASE_URL + JEV_API_KEY for the maker's own API)
  JEV_MODEL           the exact model slug as listed by your provider (check the provider's model list)
  Without a key or model the script falls back to a small offline keyword heuristic, so it always answers.

Every call is appended to ~/.jev/log.jsonl (choice, latency, backend) so you can measure savings.
"""
import json
import os
import re
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

TIERS = {
    "tier1": "Instant command, no AI needed: open/show a report, file, dashboard or terminal, start a known routine.",
    "tier2": "Short question or small edit a small fast model can do: lookup, summary, rename, find a file path, grammar.",
    "tier3": "Real multi-step work: build, write code, research, create a report/deck/explainer, debug, plan.",
}
MODEL_FOR_TIER = {"tier1": None, "tier2": "haiku", "tier3": os.environ.get("JEV_BIG_MODEL", "sonnet")}
LOG = Path.home() / ".jev" / "log.jsonl"


def _log(rec):
    try:
        LOG.parent.mkdir(parents=True, exist_ok=True)
        with LOG.open("a", encoding="utf-8") as f:
            f.write(json.dumps(rec) + "\n")
    except OSError:
        pass


def _ask_jev(text, options):
    """Return (choice, raw) from the remote classifier, or (None, reason) if unavailable."""
    key = os.environ.get("JEV_API_KEY") or os.environ.get("OPENROUTER_API_KEY")
    model = os.environ.get("JEV_MODEL")
    base = os.environ.get("JEV_BASE_URL", "https://openrouter.ai/api/v1")
    if not key or not model:
        return None, "no JEV_MODEL / API key set"
    menu = "\n".join(f"- {name}: {desc}" for name, desc in options.items())
    body = {
        "model": model,
        "messages": [{"role": "user", "content":
                      f"Pick exactly one option for the input.\nOptions:\n{menu}\n\nInput:\n{text}\n\n"
                      f"Answer with the option name only."}],
        "max_tokens": 16,
        "temperature": 0,
    }
    req = urllib.request.Request(base.rstrip("/") + "/chat/completions", data=json.dumps(body).encode(),
                                 headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            data = json.loads(r.read())
    except Exception as e:  # network, auth, unknown model
        return None, f"jev call failed: {e}"
    raw = json.dumps(data)[:2000]
    return _parse_choice(data, options), raw


def _parse_choice(data, options):
    """Accept a plain-text label, or a {label: probability} map anywhere in the answer."""
    try:
        content = data["choices"][0]["message"]["content"]
    except (KeyError, IndexError, TypeError):
        content = json.dumps(data)
    if isinstance(content, (dict, list)):
        content = json.dumps(content)
    try:
        probs = json.loads(content)
        if isinstance(probs, dict):
            scored = {k: float(v) for k, v in probs.items() if k in options}
            if scored:
                return max(scored, key=scored.get)
    except (ValueError, TypeError):
        pass
    low = content.lower()
    hits = [(low.find(name.lower()), name) for name in options if name.lower() in low]
    return min(hits)[1] if hits else None


def _heuristic(text, options):
    """Offline fallback: score options by word overlap with their description (+ tier keywords)."""
    t = text.lower()
    if set(options) == set(TIERS):
        if re.search(r"\b(open|show|bring up|pull up|display)\b", t) and len(t.split()) <= 10:
            return "tier1"
        if re.search(r"\b(build|create|write|implement|refactor|debug|research|design|plan|explainer|report|deck)\b", t):
            return "tier3"
        return "tier2" if len(t.split()) <= 25 else "tier3"
    words = set(re.findall(r"[a-z0-9]+", t))
    best, score = None, -1
    for name, desc in options.items():
        s = len(words & set(re.findall(r"[a-z0-9]+", (name + " " + desc).lower())))
        if s > score:
            best, score = name, s
    return best


def classify(text, options):
    t0 = time.time()
    choice, raw = _ask_jev(text, options)
    backend = "jev"
    if choice is None:
        choice, backend = _heuristic(text, options), "heuristic (" + raw + ")"
    rec = {"t": time.strftime("%Y-%m-%dT%H:%M:%S"), "input": text[:300], "choice": choice,
           "backend": backend, "seconds": round(time.time() - t0, 3)}
    _log(rec)
    return choice, rec


def list_skills():
    skills = {}
    for root in (Path.home() / ".claude" / "skills", Path.cwd() / ".claude" / "skills"):
        for md in root.glob("*/SKILL.md"):
            text = md.read_text(encoding="utf-8", errors="ignore")
            m = re.search(r"^description:\s*(.+)$", text, re.M)
            skills[md.parent.name] = (m.group(1) if m else "")[:400]
    return skills


def main(argv):
    if len(argv) < 3 or argv[1] not in {"route", "skill", "pick", "run"}:
        print(__doc__)
        return 2
    mode, text = argv[1], argv[2]
    if mode == "pick":
        options = {o: o for o in argv[3:]}
        if len(options) < 2:
            print("pick needs at least two options")
            return 2
        choice, rec = classify(text, options)
        print(json.dumps({"choice": choice, **rec}, indent=2))
        return 0
    if mode == "skill":
        skills = list_skills()
        if not skills:
            print("no skills found in ~/.claude/skills or ./.claude/skills")
            return 1
        choice, rec = classify(text, skills)
        print(json.dumps({"skill": choice, **rec}, indent=2))
        return 0
    tier, rec = classify(text, TIERS)
    model = MODEL_FOR_TIER[tier]
    print(json.dumps({"tier": tier, "model": model, **rec}, indent=2))
    if mode == "run" and model:
        return subprocess.call(["claude", "-p", "--model", model, text])
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
