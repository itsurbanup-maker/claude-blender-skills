---
name: premiere-edit
description: Edit a rendered film in Adobe Premiere Pro with Claude - turn a PNG frame sequence (from Blender, After Effects or anything else) into one ProRes clip per shot, then have Claude build the whole timeline as an XML file that Premiere opens with File > Import - shots in order, sound mix, one marker per shot, trims - so you only do the creative part by hand (cut timing, sound, grade, export). Use when someone wants to edit, cut, assemble or finish a film / short / Blender render in Premiere Pro with Claude, asks to "put the shots on a timeline", "make a Premiere sequence from my renders", or wants any single step (ProRes per shot, XML timeline, export).
---

# Edit the film in Premiere Pro with Claude

Claude cannot click inside Premiere. It can write the files Premiere opens. This skill takes the frames a Blender skill rendered
(`blender-film`, `blender-forest`, `blender-car-film`) and gives you a ready Premiere sequence: every shot cut in, the sound
mix under it, markers named after the storyboard shots. You then do the edit by eye.

## Rules for Claude

- Follow `claude-agent-rules` (finish the job, report progress in one line, a final report a person can read).
- Build the timeline as an XML file. Edit the `.prproj` file only through Premiere itself: it is a compressed project file,
  and a broken one can lose the user's edit.
- Use one shot list (`shots.json`) for everything. It is the storyboard in numbers: shot names, first and last frame.
- Encode with ffmpeg and check every shot's frame count. Tell the user how long an encode will take before a big one.
- The user does the creative edit: cut timing, sound, grade, export. Claude prepares it and checks it.

## 0. Setup

- Premiere Pro (any recent version), Python 3, `ffmpeg` and `ffprobe` on PATH.
- Copy `scripts/shots.example.json` into your project as `shots.json` and fill it in: `fps`, the PNG pattern in `frames`,
  `shots_dir` (where the clips go), `audio` (the mix, optional), and every shot with `first` / `last` frame.
  The example is the real shot list of `blender-car-film` (6 shots, 600 frames, 30 fps).

## 1. One ProRes clip per shot

```
python scripts/encode_shots.py shots.json
```

- ProRes 422 HQ keeps the full quality of the render and scrubs smoothly in Premiere. `--codec h264` makes small proxies.
- A shot with missing frames is skipped and named, so you know what to re-render.
- Resumable: shots that are already encoded with the right frame count are skipped.

## 2. The timeline as XML

```
python scripts/make_xml.py shots.json edit/last_drive_home.xml
```

- Final Cut Pro 7 XML, which Premiere imports: File > Import > the `.xml`. You get a bin with the clips and a sequence.
- V1: the shots one after another. A1/A2: the sound mix from frame 0. A marker at the start of every shot.
- Size and length come from the files themselves (ffprobe), so the sequence matches the render.
- Trims: add `"in"` / `"out"` (frames inside the shot clip, out exclusive) to a shot in `shots.json` and run it again.
  Re-import makes a new sequence, so old edits stay safe.

## 3. Edit, sound, export (by hand, Claude checks)

- Cut timing: hold a shot longer or shorter on its marker. Ask Claude to write the new `in` / `out` back into `shots.json`
  if you want the shot list to stay the source of truth.
- Sound: the mix from the Blender skill is already timed to the frames. Add music or voice on A3+.
- Grade: Lumetri only where a shot needs it. Same rule as the Blender skills: the look comes from the lighting.
- Export: File > Export > Media, H.264, match source, high bitrate. Or queue it in Media Encoder and keep working.
- Then ask Claude to check the export with `ffprobe`: length, frame rate, size, sound present.

## Lessons

- Edit the encoded clips, not the PNG sequences: one file per shot imports faster and plays without dropped frames.
- Keep frame numbers in `shots.json` the same as in Blender. Then any re-render drops back in without a new edit.
- If Premiere asks to locate media after import, the paths in the XML don't match this PC: run `make_xml.py` here again.
