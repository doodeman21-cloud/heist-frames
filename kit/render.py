"""Render a long video from cut frames + narration + word timings.
Usage: python3 render.py <project_dir> <audio.mp3> <words.json> <out.mp4>
Reads <project_dir>/shots.txt: one shot per line, "image_file | cue words".
A shot starts when its cue words are spoken; the first shot starts at 0."""
import json, os, re, subprocess, sys

proj, audio, words_f, out = sys.argv[1:5]
W, H, FPS = 1920, 1080, 30
words = json.load(open(words_f))
norm = lambda s: re.sub(r"[^a-z0-9]", "", s.lower())
nw = [norm(w["w"]) for w in words]
dur_audio = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", audio]).decode())

# ---- shots: find each cue in the transcript, in order
shots, pos = [], 0
for line in open(os.path.join(proj, "shots.txt")):
    line = line.strip()
    if not line or line.startswith("#"):
        continue
    img, cue = [x.strip() for x in line.split("|")]
    cw = [norm(c) for c in cue.split() if norm(c)]
    hit = None
    for i in range(pos, len(nw) - len(cw) + 1):
        if nw[i:i + len(cw)] == cw:
            hit = i
            break
    if hit is None:
        sys.exit(f"cue not found after word {pos}: {cue}")
    shots.append([img, 0.0 if not shots else words[hit]["s"]])
    pos = hit + len(cw)
for i, s in enumerate(shots):
    s.append((shots[i + 1][1] if i + 1 < len(shots) else dur_audio + 0.6) - s[1])

# ---- per-shot clips with a slow push-in or pull-out
tmp = os.path.join(proj, "_clips")
os.makedirs(tmp, exist_ok=True)
lst = []
for i, (img, start, d) in enumerate(shots):
    n = max(1, round(d * FPS))
    zin = i % 2 == 0
    z = f"'min(1+0.10*on/{n},1.10)'" if zin else f"'max(1.10-0.10*on/{n},1.0)'"
    src = os.path.join(proj, img)
    vf = (f"scale=3840:2160,zoompan=z={z}:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={n}:s={W}x{H}:fps={FPS},"
          f"format=yuv420p")
    if img == "black":
        cmd = ["ffmpeg", "-y", "-loglevel", "error", "-f", "lavfi", "-i", f"color=c=0x0b0b10:s={W}x{H}:r={FPS}", "-t", f"{n / FPS:.3f}"]
        vf = "format=yuv420p"
    else:
        cmd = ["ffmpeg", "-y", "-loglevel", "error", "-loop", "1", "-i", src, "-frames:v", str(n)]
    clip = os.path.join(tmp, f"c{i:03d}.mp4")
    subprocess.run(cmd + ["-vf", vf, "-r", str(FPS), "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", clip], check=True)
    lst.append(f"file '{clip}'")
    print(f"shot {i + 1:02d} {img:10s} {start:7.2f}s  {d:5.2f}s", flush=True)
open(os.path.join(tmp, "list.txt"), "w").write("\n".join(lst))

# ---- captions: two words at a time, the spoken word in red
def ts(t):
    t = max(0, t)
    return f"{int(t // 3600)}:{int(t % 3600 // 60):02d}:{t % 60:05.2f}"
RED, WHITE = r"{\c&H3C4CE8&}", r"{\c&HFFFFFF&}"
ass = ["[Script Info]", "ScriptType: v4.00+", f"PlayResX: {W}", f"PlayResY: {H}", "",
       "[V4+ Styles]",
       "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding",
       "Style: Cap,Poppins,84,&H00FFFFFF,&H00FFFFFF,&H00101014,&H96000000,-1,0,0,0,100,100,1,0,1,5,0,5,60,60,0,1",
       "", "[Events]", "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text"]
ws = [w for w in words if norm(w["w"])]
for k in range(0, len(ws), 2):
    pair = ws[k:k + 2]
    nxt = ws[k + 2]["s"] if k + 2 < len(ws) else pair[-1]["e"] + 0.4
    end_pair = min(nxt, pair[-1]["e"] + 0.6)
    for j, w in enumerate(pair):
        s = w["s"]
        e = pair[j + 1]["s"] if j + 1 < len(pair) else end_pair
        txt = " ".join((RED if m == j else WHITE) + p["w"].upper().strip(",.;:!?\"") for m, p in enumerate(pair))
        ass.append(f"Dialogue: 0,{ts(s)},{ts(e)},Cap,,0,0,0,,{{\\pos({W // 2},{int(H * 0.60)})\\blur2}}{txt}")
sub = os.path.join(proj, "_captions.ass")
open(sub, "w").write("\n".join(ass))

# ---- join, burn captions, add narration
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", os.path.join(tmp, "list.txt"),
                "-i", audio, "-vf", f"subtitles={sub}:fontsdir=/usr/share/fonts/truetype/google-fonts",
                "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-preset", "veryfast", "-crf", "21",
                "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "160k", "-movflags", "+faststart", "-shortest", out], check=True)
print("done", out)
