"""Build a Premiere Pro timeline as Final Cut Pro 7 XML (xmeml v4). Premiere opens it with File > Import.

usage: python make_xml.py shots.json [out.xml]

Puts the shot files (<shots_dir>/<name>.mov, from encode_shots.py) on V1 one after another, the sound mix on A1 from 0,
and one sequence marker per shot. Size, length and audio of each file are read with ffprobe, so the XML matches the files.
Optional per shot: "in" / "out" (frames inside the shot file, out exclusive) to trim, "file" to use another file.
This is the safe way for Claude to build an edit: plain text, no Premiere plug-in, the user sees the result on import.
"""
import json, os, subprocess, sys
from pathlib import PureWindowsPath, PurePosixPath
from urllib.parse import quote
from xml.sax.saxutils import escape


def probe(path):
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                          "stream=codec_type,width,height,nb_frames,duration,channels,sample_rate:format=duration",
                          "-of", "json", path], capture_output=True, text=True, check=True).stdout
    return json.loads(out)


def path_url(p):
    if len(p) > 1 and p[1] == ":":  # Windows drive path
        parts = PureWindowsPath(p).as_posix()
        return "file://localhost/" + quote(parts, safe="/:")
    return "file://localhost" + quote(str(PurePosixPath(p)), safe="/")


def rate(fps):
    ntsc = "TRUE" if abs(fps - round(fps)) > 0.001 else "FALSE"
    return f"<rate><timebase>{round(fps)}</timebase><ntsc>{ntsc}</ntsc></rate>"


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    cfg = json.load(open(sys.argv[1], encoding="utf-8"))
    fps, name = cfg["fps"], cfg.get("name", "edit")
    out_xml = sys.argv[2] if len(sys.argv) > 2 else os.path.join(cfg["shots_dir"], name + ".xml")
    R = rate(fps)

    video, markers, t, width, height = [], [], 0, None, None
    for i, shot in enumerate(cfg["shots"], 1):
        path = shot.get("file") or os.path.join(cfg["shots_dir"], shot["name"] + ".mov")
        info = probe(path)
        v = next(s for s in info["streams"] if s["codec_type"] == "video")
        width, height = width or v["width"], height or v["height"]
        dur = int(v.get("nb_frames") or round(float(info["format"]["duration"]) * fps))
        src_in, src_out = shot.get("in", 0), shot.get("out", dur)
        length = src_out - src_in
        fid = f"file-{i}"
        video.append(f"""
          <clipitem id="clip-{i}">
            <name>{escape(shot['name'])}</name><enabled>TRUE</enabled><duration>{dur}</duration>{R}
            <start>{t}</start><end>{t + length}</end><in>{src_in}</in><out>{src_out}</out>
            <file id="{fid}">
              <name>{escape(os.path.basename(path))}</name><pathurl>{escape(path_url(path))}</pathurl>{R}
              <duration>{dur}</duration>
              <media><video><samplecharacteristics>{R}<width>{v['width']}</width><height>{v['height']}</height>
                <pixelaspectratio>square</pixelaspectratio></samplecharacteristics></video></media>
            </file>
          </clipitem>""")
        markers.append(f"<marker><name>{escape(shot['name'])}</name><comment></comment>"
                       f"<in>{t}</in><out>-1</out></marker>")
        t += length

    audio = ""
    if cfg.get("audio"):
        a_info = probe(cfg["audio"])
        a = next(s for s in a_info["streams"] if s["codec_type"] == "audio")
        a_dur = round(float(a_info["format"]["duration"]) * fps)
        a_len = min(a_dur, t)
        ch = int(a.get("channels", 2))
        tracks = []
        for c in range(1, ch + 1):  # Premiere puts one channel per track for xmeml audio
            file_xml = (f"""<file id="file-audio"><name>{escape(os.path.basename(cfg['audio']))}</name>
              <pathurl>{escape(path_url(cfg['audio']))}</pathurl>{R}<duration>{a_dur}</duration>
              <media><audio><samplecharacteristics><depth>16</depth><samplerate>{a.get('sample_rate', 48000)}</samplerate>
              </samplecharacteristics><channelcount>{ch}</channelcount></audio></media></file>"""
                        if c == 1 else '<file id="file-audio"/>')
            tracks.append(f"""
        <track>
          <clipitem id="audio-{c}">
            <name>{escape(os.path.basename(cfg['audio']))}</name><enabled>TRUE</enabled><duration>{a_dur}</duration>{R}
            <start>0</start><end>{a_len}</end><in>0</in><out>{a_len}</out>
            {file_xml}
            <sourcetrack><mediatype>audio</mediatype><trackindex>{c}</trackindex></sourcetrack>
          </clipitem>
        </track>""")
        audio = "".join(tracks)

    xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE xmeml>
<xmeml version="4">
  <sequence id="seq-1">
    <name>{escape(name)}</name><duration>{t}</duration>{R}
    <timecode>{R}<string>00:00:00:00</string><frame>0</frame><displayformat>NDF</displayformat></timecode>
    {''.join(markers)}
    <media>
      <video>
        <format><samplecharacteristics>{R}<width>{width}</width><height>{height}</height>
          <pixelaspectratio>square</pixelaspectratio><fielddominance>none</fielddominance></samplecharacteristics></format>
        <track>{''.join(video)}
        </track>
      </video>
      <audio>{audio}
      </audio>
    </media>
  </sequence>
</xmeml>
"""
    os.makedirs(os.path.dirname(os.path.abspath(out_xml)), exist_ok=True)
    open(out_xml, "w", encoding="utf-8").write(xml)
    print(f"{out_xml}: {len(cfg['shots'])} shots, {t} frames ({t / fps:.2f} s) at {fps} fps, {width}x{height}")


if __name__ == "__main__":
    main()
