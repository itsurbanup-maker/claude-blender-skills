"""Render the FILM comp with aerender (After Effects without its window), in chunks, resumable.

usage: python render.py shots.json [--comp FILM] [--chunk 50] [--dry-run]

Renders a PNG sequence to after_effects.frames_out (pattern like C:/film/ae/f_[#####].png).
Frames are split into chunks. A chunk whose frames all exist is skipped, so after a crash or power cut you just run it again.
Then checks that every frame exists and is not empty, and encodes an MP4 with the sound (ffmpeg).
Set AERENDER if After Effects is not the 2025 default install. Ask before starting: a long render blocks the GPU.
"""
import json, os, platform, re, subprocess, sys

DEFAULT = {"Windows": r"C:\Program Files\Adobe\Adobe After Effects 2025\Support Files\aerender.exe",
           "Darwin": "/Applications/Adobe After Effects 2025/aerender"}


def arg(name, default):
    return sys.argv[sys.argv.index(name) + 1] if name in sys.argv else default


def frame_path(pattern, n):  # f_[#####].png -> f_00012.png
    m = re.search(r"\[(#+)\]", pattern)
    return pattern[:m.start()] + str(n).zfill(len(m.group(1))) + pattern[m.end():]


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    cfg = json.load(open(sys.argv[1], encoding="utf-8"))
    ae, fps = cfg["after_effects"], cfg["fps"]
    comp, chunk, dry = arg("--comp", "FILM"), int(arg("--chunk", 50)), "--dry-run" in sys.argv
    total = sum(s["last"] - s["first"] + 1 for s in cfg["shots"])
    pattern = ae["frames_out"]
    exe = os.environ.get("AERENDER", DEFAULT.get(platform.system(), "aerender"))
    os.makedirs(os.path.dirname(pattern), exist_ok=True)

    # AE numbers output frames from the comp's start frame (0 by default)
    for s in range(0, total, chunk):
        e = min(s + chunk, total) - 1
        if all(os.path.exists(frame_path(pattern, f)) for f in range(s, e + 1)):
            continue
        cmd = [exe, "-project", ae["project"], "-comp", comp, "-s", str(s), "-e", str(e),
               "-RStemplate", ae.get("rs_template", "Best Settings"),
               "-OMtemplate", ae.get("om_template", "PNG Sequence"), "-output", pattern]
        print(f"frames {s}-{e} / {total - 1}", flush=True)
        if dry:
            print("  " + " ".join(cmd))
            continue
        subprocess.run(cmd, check=True)

    if dry:
        return
    bad = [f for f in range(total) if not os.path.exists(frame_path(pattern, f))
           or os.path.getsize(frame_path(pattern, f)) < 1024]
    if bad:
        sys.exit(f"{len(bad)} frames missing or empty, first: {frame_path(pattern, bad[0])}. Run again.")
    print(f"all {total} frames OK")

    out = ae.get("video_out")
    if out:
        os.makedirs(os.path.dirname(os.path.abspath(out)), exist_ok=True)
        ff_in = re.sub(r"\[(#+)\]", lambda m: f"%0{len(m.group(1))}d", pattern)
        cmd = ["ffmpeg", "-v", "error", "-y", "-framerate", str(fps), "-start_number", "0", "-i", ff_in]
        if cfg.get("audio"):
            cmd += ["-i", cfg["audio"], "-c:a", "aac", "-b:a", "320k", "-shortest"]
        cmd += ["-frames:v", str(total), "-c:v", "libx264", "-preset", "slow", "-crf", "15", "-pix_fmt", "yuv420p", out]
        subprocess.run(cmd, check=True)
        print("video:", out)


if __name__ == "__main__":
    main()
