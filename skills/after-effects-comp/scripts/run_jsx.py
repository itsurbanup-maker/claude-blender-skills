"""Send an ExtendScript file to the After Effects that is open on this PC, then print the log it writes.

usage: python run_jsx.py shots.json [script.jsx]      (default script: build_comp.jsx next to this file)

1. Writes config.jsxinc next to the script: `var CFG = <shots.json>;` (the .jsx reads it with #include).
2. Windows: runs `AfterFX.exe -r script.jsx` (set AFTERFX to its path if AE is not the 2025 default).
   macOS: asks AE through osascript to DoScriptFile (set AE_APP, default "Adobe After Effects 2025").
3. Waits for the log file (after_effects.log in shots.json) and prints it.
AE must be open. Close any modal dialog in AE first, or the script waits behind it.
"""
import json, os, platform, subprocess, sys, time

AE_WIN = r"C:\Program Files\Adobe\Adobe After Effects 2025\Support Files\AfterFX.exe"


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    cfg = json.load(open(sys.argv[1], encoding="utf-8"))
    here = os.path.dirname(os.path.abspath(__file__))
    script = os.path.abspath(sys.argv[2]) if len(sys.argv) > 2 else os.path.join(here, "build_comp.jsx")
    with open(os.path.join(os.path.dirname(script), "config.jsxinc"), "w", encoding="utf-8") as f:
        f.write("var CFG = " + json.dumps(cfg, indent=1) + ";\n")
    log = cfg.get("after_effects", {}).get("log")
    if log and os.path.exists(log):
        os.remove(log)

    if platform.system() == "Windows":
        exe = os.environ.get("AFTERFX", AE_WIN)
        subprocess.Popen([exe, "-r", script])
    elif platform.system() == "Darwin":
        app = os.environ.get("AE_APP", "Adobe After Effects 2025")
        subprocess.run(["osascript", "-e", f'tell application "{app}" to DoScriptFile "{script}"'], check=True)
    else:
        sys.exit("After Effects runs on Windows and macOS only.")

    if not log:
        print("sent. Add after_effects.log to shots.json to see the result here.")
        return
    for _ in range(300):  # up to 5 minutes: big sequences take a while to import
        if os.path.exists(log):
            time.sleep(0.5)
            print(open(log, encoding="utf-8").read())
            return
        time.sleep(1)
    print("no log after 5 minutes. Check AE for an open dialog, and the scripting preference "
          "'Allow Scripts to Write Files and Access Network'.")


if __name__ == "__main__":
    main()
