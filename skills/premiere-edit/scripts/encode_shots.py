"""Turn a rendered PNG sequence into one ProRes 422 HQ .mov per shot, ready to edit in Premiere Pro.

usage: python encode_shots.py shots.json [--codec prores|h264]

Reads shots.json (see shots.example.json): "frames" is the PNG pattern, every shot has "first" and "last" frame numbers.
Writes <shots_dir>/<shot name>.mov. Resumable: a shot whose .mov already has the right frame count is skipped.
ProRes keeps the full quality of the render and scrubs smoothly. Use --codec h264 only for a quick proxy.
"""
import json, os, subprocess, sys


def frame_count(path):
    try:
        out = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-count_packets",
                              "-show_entries", "stream=nb_read_packets", "-of", "csv=p=0", path],
                             capture_output=True, text=True, check=True).stdout.strip()
        return int(out)
    except (subprocess.CalledProcessError, ValueError):
        return -1


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    cfg = json.load(open(sys.argv[1], encoding="utf-8"))
    codec = sys.argv[sys.argv.index("--codec") + 1] if "--codec" in sys.argv else "prores"
    fps, pattern, out_dir = cfg["fps"], cfg["frames"], cfg["shots_dir"]
    os.makedirs(out_dir, exist_ok=True)
    if codec == "prores":
        vcodec = ["-c:v", "prores_ks", "-profile:v", "3", "-pix_fmt", "yuv422p10le", "-vendor", "apl0"]
    else:
        vcodec = ["-c:v", "libx264", "-preset", "slow", "-crf", "14", "-pix_fmt", "yuv420p"]
    for shot in cfg["shots"]:
        n = shot["last"] - shot["first"] + 1
        out = os.path.join(out_dir, shot["name"] + ".mov")
        missing = [f for f in range(shot["first"], shot["last"] + 1) if not os.path.exists(pattern % f)]
        if missing:
            print(f"{shot['name']}: {len(missing)} frames missing (first: {pattern % missing[0]}), skipped")
            continue
        if os.path.exists(out) and frame_count(out) == n:
            print(f"{shot['name']}: already encoded ({n} frames)")
            continue
        cmd = ["ffmpeg", "-v", "error", "-y", "-framerate", str(fps), "-start_number", str(shot["first"]),
               "-i", pattern, "-frames:v", str(n), *vcodec, "-r", str(fps), out]
        subprocess.run(cmd, check=True)
        got = frame_count(out)
        print(f"{shot['name']}: {out} ({got}/{n} frames){'' if got == n else '  <-- WRONG FRAME COUNT'}")


if __name__ == "__main__":
    main()
