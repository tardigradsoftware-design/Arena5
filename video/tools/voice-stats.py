#!/usr/bin/env python3
"""Rough voice stats so we can *prove* two takes differ (not just claim it).

    python3 tools/voice-stats.py file.mp3 [file2.mp3 ...]

Reports median fundamental frequency (f0), f0 range, spectral centroid and
speech rate proxy. Decoding is done with the ffmpeg binary from npm.
"""
import json
import subprocess
import sys
import wave

import numpy as np

FFMPEG = json.loads(
    subprocess.check_output(
        ["node", "-e", "import('@ffmpeg-installer/ffmpeg').then(m=>console.log(JSON.stringify({p:m.default.path})))"],
        text=True,
    )
)["p"]


def decode(path, sr=16000):
    tmp = f"/tmp/_vs_{abs(hash(path))}.wav"
    subprocess.run(
        [FFMPEG, "-hide_banner", "-loglevel", "error", "-y", "-i", path,
         "-ac", "1", "-ar", str(sr), tmp],
        check=True,
    )
    with wave.open(tmp) as w:
        data = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16)
    return data.astype(np.float32) / 32768.0, sr


def frame_f0(x, sr, win=0.04, hop=0.02, fmin=70, fmax=500):
    n = int(win * sr)
    h = int(hop * sr)
    lo, hi = int(sr / fmax), int(sr / fmin)
    out = []
    for start in range(0, len(x) - n, h):
        seg = x[start:start + n]
        if np.sqrt(np.mean(seg ** 2)) < 0.01:
            continue
        seg = seg - seg.mean()
        ac = np.correlate(seg, seg, mode="full")[n - 1:]
        ac /= ac[0] + 1e-9
        peak = np.argmax(ac[lo:hi]) + lo
        if ac[peak] > 0.3:
            out.append(sr / peak)
    return np.array(out)


def stats(path):
    x, sr = decode(path)
    f0 = frame_f0(x, sr)
    spec = np.abs(np.fft.rfft(x * np.hanning(len(x))))
    freqs = np.fft.rfftfreq(len(x), 1 / sr)
    centroid = float((freqs * spec).sum() / (spec.sum() + 1e-9))
    dur = len(x) / sr
    return {
        "dosya": path,
        "süre_s": round(dur, 2),
        "f0_medyan_Hz": round(float(np.median(f0)), 1) if len(f0) else None,
        "f0_p10_p90_Hz": [round(float(np.percentile(f0, 10)), 1), round(float(np.percentile(f0, 90)), 1)] if len(f0) else None,
        "tını_merkezi_Hz": round(centroid, 1),
    }


if __name__ == "__main__":
    for p in sys.argv[1:]:
        print(json.dumps(stats(p), ensure_ascii=False))
