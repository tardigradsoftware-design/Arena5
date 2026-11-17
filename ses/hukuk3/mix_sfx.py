#!/usr/bin/env python3
"""Seslendirmeye geçiş efektleri ekler (whoosh / pop / ding).

    python3 ses/hukuk3/mix_sfx.py      -> ses/hukuk3/ses-sfx.wav

Efektler numpy ile toplanır: eski ffmpeg derlemesinde `amix` normalize
seçeneği olmadığı için ffmpeg karıştırma yerine doğrudan örnek toplama.
"""
import json
import pathlib
import wave

import numpy as np

BASE = pathlib.Path(__file__).resolve().parent
ROOT = BASE.parents[1]
VOICE = BASE / "ses.wav"
OUT = BASE / "ses-sfx.wav"
TIMING = json.loads((ROOT / "video" / "src" / "scenes" / "hukuh3-timing.json").read_text()
                    if (ROOT / "video" / "src" / "scenes" / "hukuh3-timing.json").exists()
                    else (ROOT / "video" / "src" / "scenes" / "hukuk3-timing.json").read_text())
B = TIMING["beats"]

GAIN = {"whoosh.wav": 0.55, "pop.wav": 0.35, "ding.wav": 0.32}


def read(path):
    with wave.open(str(path), "rb") as w:
        sr = w.getframerate()
        data = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32) / 32768
    return sr, data


def main():
    sr, voice = read(VOICE)

    events = []
    for key in ["b2", "b3", "b4", "b5", "b6"]:
        events.append(("whoosh.wav", max(0.0, B[key]["start"] - 0.18)))
    for key in ["b2", "b3", "b4"]:
        events.append(("pop.wav", B[key]["start"] + 0.55))
    events.append(("ding.wav", B["b6"]["start"] + 0.1))

    buf = voice.copy()
    for name, when in events:
        esr, fx = read(BASE / "sfx" / name)
        assert esr == sr, f"örnekleme hızı uyuşmuyor: {name}"
        start = int(when * sr)
        end = min(len(buf), start + len(fx))
        if end <= start:
            continue
        buf[start:end] += fx[: end - start] * GAIN[name]

    peak = np.abs(buf).max()
    if peak > 0.98:                      # kırpma koruması
        buf *= 0.98 / peak

    with wave.open(str(OUT), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(sr)
        w.writeframes((buf * 32767).astype(np.int16).tobytes())
    print(f"✓ {OUT} ({len(events)} efekt, tepe {np.abs(buf).max():.2f})")


if __name__ == "__main__":
    main()
