---
name: after-effects-comp
description: Finish a rendered film in Adobe After Effects with Claude - Claude sends an ExtendScript to your open After Effects that imports the PNG frame sequence, makes one comp per shot and a FILM comp with the shots in order, the sound, markers, a subtle lens / glow / grain look layer and an optional title, then renders it with aerender in resumable chunks and encodes the MP4. Use when someone wants to composite, add titles, a lens look or VFX to a Blender render in After Effects with Claude, asks Claude to "control After Effects" or "script After Effects", or wants any single step (import a sequence, build comps, render from the command line).
---

# Finish the film in After Effects with Claude

After Effects can be driven by script. Claude writes ExtendScript (`.jsx`), sends it to your open After Effects, and reads
back a log. You watch the comps appear. For the final render Claude runs `aerender` (After Effects without its window), in
chunks, so a crash costs one chunk at most.

## Rules for Claude

- Follow `claude-agent-rules` (finish the job, report progress in one line, a final report a person can read).
- Read every `.jsx` before you send it. Each script runs inside one undo group, so Ctrl+Z undoes it in one step.
- The look comes from the Blender lighting. The LOOK layer stays subtle: slight lens distortion, a little glow on lights,
  grain only if the user wants it. Grade only a shot that needs it.
- Test small, render big: check single frames in the AE viewer first. Ask the user before a full render: it blocks the GPU.
- After a render, check that every frame exists before you encode. `render.py` does this.

## 0. Setup

- After Effects 2023 or newer (paths below are for 2025), Python 3, `ffmpeg` on PATH. Windows or macOS.
- In After Effects: Edit > Preferences > Scripting & Expressions > tick **Allow Scripts to Write Files and Access Network**.
  Without it the script still runs, but Claude can't read its log.
- Copy `scripts/shots.example.json` into your project as `shots.json`. It is the same shot list as `premiere-edit`
  plus an `after_effects` block: project path, log path, output frames, final video, render templates, look settings, title.
- If After Effects is not the default 2025 install, set `AFTERFX` (Windows, path to `AfterFX.exe`), `AE_APP` (macOS, the app
  name) and `AERENDER` (path to `aerender`).

## 1. Build the comps (live, in your open After Effects)

```
python scripts/run_jsx.py shots.json
```

`run_jsx.py` writes `config.jsxinc` from `shots.json`, sends `build_comp.jsx` to After Effects (`AfterFX.exe -r` on Windows,
`osascript` on macOS) and prints the log. The script:

1. imports the whole PNG sequence once, at the film's frame rate;
2. makes one comp per shot (folder `shots`), with the sequence offset to the shot's first frame;
3. makes the `FILM` comp: shot comps in order, a marker per shot, the sound mix;
4. adds a `LOOK` adjustment layer: Optics Compensation (slight barrel distortion), Glow, Add Grain, each one optional in
   `look`; effects missing in your version are skipped and named in the log;
5. adds an optional title (`title`: text, start, duration);
6. puts `FILM` in the render queue as a PNG sequence and saves the project.

If `FILM` already exists, the script changes nothing and says so. To build again, delete it or start a new project.
Per-shot work (VFX, a sky replacement, a sign) goes inside that shot's comp. The FILM comp picks it up by itself.

Any other change is a small `.jsx` Claude writes and sends the same way: `python scripts/run_jsx.py shots.json my_fix.jsx`.

## 2. Render (aerender, resumable)

```
python scripts/render.py shots.json --dry-run     # shows the aerender commands
python scripts/render.py shots.json               # renders, checks, encodes
```

- Renders `FILM` in chunks of 50 frames (`--chunk`). A chunk whose frames all exist is skipped: after a crash, run it again.
- `rs_template` / `om_template` are template names from your After Effects (Edit > Templates). Check that `PNG Sequence`
  exists there, or make it once: Output Module, format PNG Sequence, RGB.
- Then it checks every frame (exists, not empty) and encodes `video_out` with the sound (H.264, CRF 15).
- For an edit in Premiere, use the AE frames as the `frames` of `premiere-edit` and encode them per shot there.

## Lessons

- One image sequence imported once, shot comps offset into it: a re-render from Blender updates every shot by itself.
- Effect property names depend on the After Effects language. The script uses internal effect names, and tries the English
  property names. Misses are logged, never fatal.
- `aerender` numbers output frames from the comp's start (frame 0). Blender frames start at 1. `render.py` uses the AE numbers.
