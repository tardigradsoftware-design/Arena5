import json, os, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PIL import Image
from common import ROOT, FF, BG as BGREF, chunks
from design import canvas
from scenes_v import W, H, SCENES, footer, header, ZONE
import ass

OUT = os.path.join(ROOT, "out")
TMP = os.path.join(ROOT, "out/.tmp")
os.makedirs(TMP, exist_ok=True)
FPS = 30


def bbox(img):
    from PIL import ImageChops
    bg, _ = canvas(*img.size)          # nokta ızgarası dahil boş tuval
    diff = ImageChops.difference(img, bg).convert("L").point(lambda v: 255 if v > 10 else 0)
    return diff.getbbox()


def shot(fn, label):
    """Gövdeyi tam tuvalde çiz, kırp, ZONE içine sığdırarak ortala."""
    img, d = canvas(W, H)
    fn(img, d)
    zone_h = ZONE[1] - ZONE[0]
    b = bbox(img)
    lb, _ = canvas(W, zone_h)
    if b:
        body = img.crop((0, max(0, b[1] - 10), W, min(H, b[3] + 10)))
        if body.height > zone_h:
            k = zone_h / body.height
            body = body.resize((int(W * k), zone_h), Image.LANCZOS)
        y = max(0, (zone_h - body.height) // 2)
        lb.paste(body, ((W - body.width) // 2, y))
    main, dm = canvas(W, H)
    main.paste(lb, (0, ZONE[0]))
    header(main, dm, label)
    footer(dm)
    return main


def main():
    from common import find
    t = json.load(open(os.path.join(ROOT, "content/timing.json")))
    vb, vt = t["v"], t["vt"]
    words = [w for b in vb for w in b["words"]]
    starts = []
    for phrase, _, _ in SCENES:
        starts.append(0.0 if phrase is None else max(0.0, words[find(words, phrase)]["s"] - 0.14))
    starts.sort()
    words2 = words
    chs = [{"t0": c[0]["s"], "t1": c[-1]["e"], "words": c} for c in chunks(words, 3, 26)]

    # 3) ses birleştir (blok aralarına pad)
    lst = os.path.join(TMP, "v_audio.txt")
    with open(lst, "w") as f:
        for b in vb:
            f.write(f"file '{os.path.join(ROOT, b['f'])}'\n")
    voice = os.path.join(TMP, "v_voice.m4a")
    subprocess.run([FF, "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", lst,
                    "-af", "apad=pad_dur=0.30", "-c:a", "aac", "-b:a", "192k",
                    "-ar", "44100", "-ac", "1", voice], check=True)

    # 1) sahne PNG'leri
    for i, (_, fn, lab) in enumerate(SCENES):
        shot(fn, lab).save(os.path.join(TMP, f"v{i:02d}.png"))

    # 2) altyazı
    ass.build(chs, os.path.join(TMP, "v.ass"), W, H, fs=64, sp=0.3, bo=8, sh=3, ml=90, mr=90, mv=430)

    # 3) ses birleştir
    lst = os.path.join(TMP, "v_audio.txt")
    with open(lst, "w") as f:
        for b in vb:
            f.write(f"file '{os.path.join(ROOT, b['f'])}'\n")
    voice = os.path.join(TMP, "v_voice.m4a")
    subprocess.run([FF, "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", lst,
                    "-c:a", "aac", "-b:a", "192k", voice], check=True)

    # 4a) sahne sahne klip (düşük bellek)
    clips = []
    n = len(SCENES)
    for i in range(n):
        d = (starts[i + 1] if i + 1 < n else vt) - starts[i]
        out = os.path.join(TMP, f"c{i:02d}.mp4")
        subprocess.run([FF, "-y", "-v", "error", "-loop", "1", "-t", f"{d+0.15}",
                        "-framerate", str(FPS), "-i", os.path.join(TMP, f"v{i:02d}.png"),
                        "-vf", f"scale={int(W*1.05)}:-1,crop={W}:{H},"
                               f"zoompan=z='min(1.05,1+0.0010*on)':x='iw/2-(iw/zoom/2)':"
                               f"y='ih/2-(ih/zoom/2)':d=1:s={W}x{H}:fps={FPS},"
                               f"trim=duration={d:.3f},setpts=PTS-STARTPTS,setsar=1",
                        "-c:v", "libx264", "-preset", "veryfast", "-crf", "17",
                        "-pix_fmt", "yuv420p", out], check=True)
        clips.append(out)

    # 4b) birleştir + altyazı + ses
    cl = os.path.join(TMP, "clips.txt")
    with open(cl, "w") as f:
        for c in clips:
            f.write(f"file '{c}'\n")
    cmd = [FF, "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", cl, "-i", voice,
           "-filter_complex",
           f"[0:v]fade=t=in:st=0:d=0.18,fade=t=out:st={vt-0.55:.2f}:d=0.5,"
           f"ass={os.path.join(TMP,'v.ass')},format=yuv420p[vout]",
           "-map", "[vout]", "-map", "1:a",
           "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-r", str(FPS),
           "-c:a", "aac", "-b:a", "192k", "-ar", "44100", "-ac", "1",
           "-movflags", "+faststart", "-shortest",
           os.path.join(OUT, "01_dikey_istifa-kidem.mp4")]
    print("render...")
    subprocess.run(cmd, check=True)
    print("ok:", os.path.join(OUT, "01_dikey_istifa-kidem.mp4"), vt)


if __name__ == "__main__":
    main()
