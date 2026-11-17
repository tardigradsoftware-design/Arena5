import json, os, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PIL import Image
from common import ROOT, FF, BG as BGREF, MUTED, ACCENT, chunks, find
from design import canvas, font, text, rr
from scenes_h import W, H, SCENES, BRAND
import ass

OUT = os.path.join(ROOT, "out")
TMP = os.path.join(ROOT, "out/.tmp")
FPS = 30
NAME = "02_yatay_istifa-kidem-detayli.mp4"


def upper_bar(d):
    d.line([(110, 58), (W - 110, 58)], fill=(34, 41, 54), width=2)
    text(d, (110, 30), BRAND, font("sb", 26), MUTED, anchor="lm")
    text(d, (W - 110, 30), "hukuknotu.com", font("m", 24), (100, 112, 128), anchor="rm")
    d.line([(110, H - 58), (W - 110, H - 58)], fill=(34, 41, 54), width=2)
    text(d, (W - 110, H - 30), "Bilgilendirme amaçlıdır · hukuki tavsiye değildir",
         font("m", 24), (105, 117, 133), anchor="rm")


def bbox(img):
    from PIL import ImageChops
    bg, _ = canvas(*img.size)
    diff = ImageChops.difference(img, bg).convert("L").point(lambda v: 255 if v > 10 else 0)
    return diff.getbbox()


def shot(fn, step):
    img, d = canvas(W, H)
    fn(img, d)
    upper_bar(d)
    # adım sayacı
    if step:
        step = step.split(" · ")[0].strip() or ""
        f = font("sb", 26)
        tw = f.getlength(step)
        rr(d, (W - 110 - tw - 44, 72, W - 110, 118), 23, fill=(30, 37, 48),
           outline=(56, 66, 84), width=2)
        text(d, (W - 110 - tw - 22, 95), step, f, ACCENT, anchor="mm")
    return img


def main():
    t = json.load(open(os.path.join(ROOT, "content/timing.json")))
    hb, ht = t["h"], t["ht"]
    words = [w for b in hb for w in b["words"]]
    starts = []
    for phrase, _, _ in SCENES:
        starts.append(0.0 if phrase is None else max(0.0, words[find(words, phrase)]["s"] - 0.18))
    starts.sort()
    n = len(SCENES)
    print("sahneler:", [round(s, 1) for s in starts], "toplam", ht)

    for i, (_, fn, lab) in enumerate(SCENES):
        shot(fn, lab).save(os.path.join(TMP, f"h{i:02d}.png"))

    chs = [{"t0": c[0]["s"], "t1": c[-1]["e"], "words": c} for c in chunks(words, 5, 44)]
    ass.build(chs, os.path.join(TMP, "h.ass"), W, H, fs=52, sp=0.2, bo=7, sh=3, ml=200, mr=200, mv=120)

    # ses
    lst = os.path.join(TMP, "h_audio.txt")
    with open(lst, "w") as f:
        for b in hb:
            f.write(f"file '{os.path.join(ROOT, b['f'])}'\n")
    voice = os.path.join(TMP, "h_voice.m4a")
    subprocess.run([FF, "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", lst,
                    "-af", "apad=pad_dur=0.30", "-c:a", "aac", "-b:a", "192k",
                    "-ar", "44100", "-ac", "1", voice], check=True)

    clips = []
    for i in range(n):
        d_ = (starts[i + 1] if i + 1 < n else ht) - starts[i]
        out = os.path.join(TMP, f"hc{i:02d}.mp4")
        subprocess.run([FF, "-y", "-v", "error", "-loop", "1", "-t", f"{d_+0.15}",
                        "-framerate", str(FPS), "-i", os.path.join(TMP, f"h{i:02d}.png"),
                        "-vf", f"scale={W+40}:-2,crop={W}:{H},zoompan=z='min(1.02,1+0.0004*on)':"
                               f"x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s={W}x{H}:fps={FPS},"
                               f"trim=duration={d_:.3f},setpts=PTS-STARTPTS,setsar=1",
                        "-c:v", "libx264", "-preset", "veryfast", "-crf", "17",
                        "-pix_fmt", "yuv420p", out], check=True)
        clips.append(out)

    cl = os.path.join(TMP, "hclips.txt")
    with open(cl, "w") as f:
        for c in clips:
            f.write(f"file '{c}'\n")
    subprocess.run([FF, "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", cl, "-i", voice,
                    "-filter_complex",
                    f"[0:v]fade=t=in:st=0:d=0.2,fade=t=out:st={ht-0.7:.2f}:d=0.6,"
                    f"ass={os.path.join(TMP,'h.ass')},format=yuv420p[vout]",
                    "-map", "[vout]", "-map", "1:a",
                    "-c:v", "libx264", "-preset", "medium", "-crf", "21", "-r", str(FPS),
                    "-c:a", "aac", "-b:a", "160k", "-ar", "44100", "-ac", "1",
                    "-movflags", "+faststart", "-shortest", os.path.join(OUT, NAME)], check=True)
    print("ok:", os.path.join(OUT, NAME), ht)


if __name__ == "__main__":
    main()
