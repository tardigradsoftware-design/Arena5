#!/usr/bin/env python3
"""Segmentleri temizler, aralara nefes payı koyup birleştirir ve zaman çizelgesini yazar.

    python3 ses/hukuk3/build_audio.py

Çıktı:
    ses/hukuk3/ses.wav        (final seslendirme, 44.1 kHz)
    video/src/scenes/hukuk3-timing.json  (sahne bu dosyayı okur)
"""
import json
import pathlib
import subprocess

BASE = pathlib.Path(__file__).resolve().parent
ROOT = BASE.parents[1]
CHAIN = (
    "highpass=f=85,"
    "equalizer=f=250:width_type=o:width=1.2:g=-2,"
    "equalizer=f=3500:width_type=o:width=1.4:g=2.5,"
    "acompressor=threshold=-18dB:ratio=3:attack=8:release=180,"
    "loudnorm=I=-16:TP=-1.5:LRA=9"
)
GAP = 0.32          # cümle arası nefes
LEAD = 0.45         # videonun başındaki sessizlik
TAIL = 0.90         # kapanış payı
SEGMENTS = ["s1", "s2", "s3", "s4", "s5", "s6"]


def ffmpeg(*args):
    exe = json.loads(
        subprocess.check_output(
            ["node", "-e",
             "import('@ffmpeg-installer/ffmpeg').then(m=>console.log(JSON.stringify({p:m.default.path})))"],
            cwd=ROOT / "video", text=True,
        )
    )["p"]
    subprocess.run([exe, "-hide_banner", "-loglevel", "error", "-y", *args], check=True)


def duration(path):
    exe = json.loads(
        subprocess.check_output(
            ["node", "-e",
             "import('@ffmpeg-installer/ffmpeg').then(m=>console.log(JSON.stringify({p:m.default.path})))"],
            cwd=ROOT / "video", text=True,
        )
    )["p"]
    out = subprocess.run([exe, "-hide_banner", "-i", str(path)],
                         capture_output=True, text=True).stderr
    for line in out.splitlines():
        if "Duration:" in line:
            h, m, s = line.split("Duration:")[1].split(",")[0].strip().split(":")
            return int(h) * 3600 + int(m) * 60 + float(s)
    raise RuntimeError(f"süre okunamadı: {path}")


def main():
    beats = {}
    t = LEAD
    inputs, filters, idx = [], [], 0

    # baştaki sessizlik
    inputs += ["-f", "lavfi", "-i", "anullsrc=r=44100:cl=mono"]
    filters.append(f"[{idx}:a]atrim=duration={LEAD}[z0]")
    parts = ["[z0]"]
    idx += 1

    for i, name in enumerate(SEGMENTS):
        src = BASE / f"{name}.wav"
        clean = BASE / f"{name}-clean.wav"
        ffmpeg("-i", str(src), "-af", CHAIN, "-ar", "44100", str(clean))
        d = duration(clean)
        beats[f"b{i + 1}"] = {"start": round(t, 3), "end": round(t + d, 3), "dur": round(d, 3)}
        inputs += ["-i", str(clean)]
        parts.append(f"[{idx}:a]")
        idx += 1
        t += d

        # nefes payı (son cümleden sonra koymuyoruz)
        if i < len(SEGMENTS) - 1:
            inputs += ["-f", "lavfi", "-i", "anullsrc=r=44100:cl=mono"]
            filters.append(f"[{idx}:a]atrim=duration={GAP}[z{i + 1}]")
            parts.append(f"[z{i + 1}]")
            idx += 1
            t += GAP

    inputs += ["-f", "lavfi", "-i", "anullsrc=r=44100:cl=mono"]
    filters.append(f"[{idx}:a]atrim=duration={TAIL}[zT]")
    parts.append("[zT]")
    idx += 1
    t += TAIL

    filters.append("".join(parts) + f"concat=n={len(parts)}:v=0:a=1[out]")
    out_wav = BASE / "ses.wav"
    ffmpeg(*inputs, "-filter_complex", ";".join(filters), "-map", "[out]",
           "-ar", "44100", str(out_wav))

    timing = {"fps": 30, "width": 720, "height": 1280,
              "duration": round(t, 3), "beats": beats}
    out_json = ROOT / "video" / "src" / "scenes" / "hukuk3-timing.json"
    out_json.write_text(json.dumps(timing, indent=2, ensure_ascii=False))
    print(json.dumps(timing, indent=2, ensure_ascii=False))
    print(f"✓ {out_wav}")


if __name__ == "__main__":
    main()
