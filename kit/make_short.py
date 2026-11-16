# usage: python3 make_short.py <src.mp3> <src.words.json> <outdir> <segments.txt> <frame_dir> <frame ids...>
# segments.txt: one "start phrase || end phrase" per line
import json, re, subprocess, sys
from PIL import Image, ImageFilter, ImageEnhance
src, wj, out, segf, fdir = sys.argv[1:6]; ids = sys.argv[6:]
w = json.load(open(wj)); norm = lambda s: re.sub(r"[^a-z0-9]", "", s.lower()); nw = [norm(x["w"]) for x in w]
def find(p, start=0):
    c = [norm(t) for t in p.split() if norm(t)]
    for i in range(start, len(nw)):
        if nw[i:i+len(c)] == c: return i
    raise SystemExit("missing " + p)
parts, words, t = [], [], 0.0
for line in open(segf):
    if "||" not in line: continue
    a, b = [x.strip() for x in line.split("||")]
    i = find(a); j = find(b, i) + len([x for x in b.split() if norm(x)]) - 1
    s, e = max(0, w[i]["s"] - 0.05), w[j]["e"] + 0.25
    parts.append((s, e))
    for k in range(i, j + 1):
        words.append({"w": w[k]["w"], "s": round(w[k]["s"] - s + t, 3), "e": round(w[k]["e"] - s + t, 3)})
    t += e - s
json.dump(words, open(f"{out}/words.json", "w"))
flt = "".join(f"[0:a]atrim={s:.3f}:{e:.3f},asetpts=PTS-STARTPTS[a{k}];" for k, (s, e) in enumerate(parts))
flt += "".join(f"[a{k}]" for k in range(len(parts))) + f"concat=n={len(parts)}:v=0:a=1[out]"
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", src, "-filter_complex", flt, "-map", "[out]", "-c:a", "libmp3lame", "-b:a", "192k", f"{out}/audio.mp3"], check=True)
for n in ids:
    c = Image.open(f"{fdir}/{n}.jpg").convert("RGB").resize((1920, 1080), Image.LANCZOS)
    bw = int(1920 * 16 / 9)
    bg = c.resize((bw, 1920), Image.LANCZOS).crop(((bw - 1080) // 2, 0, (bw - 1080) // 2 + 1080, 1920))
    bg = ImageEnhance.Brightness(bg.filter(ImageFilter.GaussianBlur(40))).enhance(0.45)
    bg.paste(c.resize((1080, 608), Image.LANCZOS), (0, 560))
    bg.save(f"{out}/v/{n}.jpg", quality=92)
print(round(t, 1), "s")
